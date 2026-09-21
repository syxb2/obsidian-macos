"""Bake a resolved Style Settings configuration into a standalone stylesheet.

The transformer walks the CSS AST and removes every class condition that the
Style Settings plugin would have satisfied (or never satisfied), so the
resulting stylesheet needs no plugin and no body classes.
"""
import re

FLAG_RE = re.compile(r"^[a-zA-Z][\w-]*$")


class Ctx:
    def __init__(self, flags, on):
        self.flags = flags
        self.on = on

    def state(self, name):
        """'on' | 'off' | 'unknown'"""
        if name in self.flags:
            return "on" if self.flags[name][1] else "off"
        return "unknown"


# ---------------------------------------------------------------- CSS parsing
def parse_nodes(text):
    """Parse a stylesheet/block body into a list of (kind, a, b) tuples."""
    nodes = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("/*", i):
            j = text.find("*/", i)
            j = n if j == -1 else j + 2
            nodes.append(("comment", text[i:j], None))
            i = j
            continue
        if text[i] in " \n\t\r":
            i += 1
            continue
        j, depth, in_str, in_paren = i, 0, None, 0
        while j < n:
            c = text[j]
            if in_str:
                if c == "\\":
                    j += 2
                    continue
                if c == in_str:
                    in_str = None
            elif c in "\"'":
                in_str = c
            elif c == "(":
                in_paren += 1
            elif c == ")":
                in_paren -= 1
            elif in_paren == 0 and c in "{;}":
                break
            j += 1
        if j >= n:
            nodes.append(("raw", text[i:], None))
            break
        head = text[i:j]
        if text[j] == ";":
            nodes.append(("at-stmt", head.strip() + ";", None))
            i = j + 1
            continue
        if text[j] == "}":
            nodes.append(("raw", head, None))
            i = j + 1
            continue
        # find matching close brace
        k, depth, in_str, in_paren = j, 0, None, 0
        while k < n:
            c = text[k]
            if in_str:
                if c == "\\":
                    k += 2
                    continue
                if c == in_str:
                    in_str = None
            elif c in "\"'":
                in_str = c
            elif c == "(":
                in_paren += 1
            elif c == ")":
                in_paren -= 1
            elif in_paren == 0:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        break
            k += 1
        inner = text[j + 1:k]
        nodes.append(("block", head.strip(), inner))
        i = k + 1
    return nodes


GROUP_AT = ("@media", "@supports", "@container", "@layer", "@starting-style", "@scope")


# ------------------------------------------------------------- selector logic
def split_top(s, sep=","):
    out, depth, cur, in_str = [], 0, "", None
    for c in s:
        if in_str:
            cur += c
            if c == "\\":
                continue
            if c == in_str:
                in_str = None
            continue
        if c in "\"'":
            in_str = c
            cur += c
            continue
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        if c == sep and depth == 0:
            out.append(cur)
            cur = ""
            continue
        cur += c
    out.append(cur)
    return out


def split_simples(comp):
    """Split a compound selector into simple-selector strings."""
    parts, i, n = [], 0, len(comp)
    cur = ""
    while i < n:
        c = comp[i]
        if c == "\\":
            cur += comp[i:i + 2]
            i += 2
            continue
        if c in ".#:[":
            if cur:
                parts.append(cur)
                cur = ""
            if c == "[":
                j = comp.index("]", i)
                parts.append(comp[i:j + 1])
                i = j + 1
                continue
            j = i + 1
            while j < n and (comp[j].isalnum() or comp[j] in "_-"):
                j += 1
            if j < n and comp[j] == "(":
                depth, k = 0, j
                while k < n:
                    if comp[k] == "(":
                        depth += 1
                    elif comp[k] == ")":
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                parts.append(comp[i:k + 1])
                i = k + 1
            else:
                parts.append(comp[i:j])
                i = j
            continue
        cur += c
        i += 1
    if cur:
        parts.append(cur)
    return parts


def split_selector(sel):
    """-> list of tokens: ('compound', text) | ('comb', text)"""
    toks, cur, i, n, in_str = [], "", 0, len(sel), None
    depth = 0
    while i < n:
        c = sel[i]
        if in_str:
            cur += c
            if c == in_str:
                in_str = None
            i += 1
            continue
        if c in "\"'":
            in_str = c
            cur += c
            i += 1
            continue
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        if depth == 0 and (c in ">+~" or c.isspace()):
            if cur.strip():
                toks.append(("compound", cur.strip()))
                cur = ""
                if c in ">+~":
                    toks.append(("comb", c))
                    i += 1
                    while i < n and sel[i].isspace():
                        i += 1
                    continue
                continue
            else:
                cur += c
                i += 1
                continue
        cur += c
        i += 1
    if cur.strip():
        toks.append(("compound", cur.strip()))
    return toks


class Css:
    def __init__(self, flags, on):
        self.ctx = Ctx(flags, on)
        self.log = []
        self.pairs = []

    def reduce_simple_list(self, simples, kind):
        """Process the simple selectors of one compound.
        Returns (status, new_simples, reasons)."""
        out = []
        reasons = []
        for s in simples:
            if s.startswith("."):
                st = self.ctx.state(s[1:])
                if st == "on":
                    reasons.append(("flag-on", s))
                    continue
                if st == "off":
                    return ("impossible", None, reasons + [("flag-off", s)])
                out.append(s)
                continue
            if s.startswith(":"):
                m = re.match(r"^:([\w-]*)", s)
                name = m.group(1)
                args = None
                if "(" in s:
                    args = s[s.index("(") + 1:s.rindex(")")]
                if name in ("is", "where", "has", "matches", "any") or (name == "" and args):
                    alts = split_top(args)
                    keep = []
                    got_true = False
                    for a in alts:
                        st, news, why = self.reduce_selector(a, nested=True)
                        if st == "impossible":
                            reasons.append(("alt-dropped", a))
                            continue
                        if news.strip() == "" or a.strip() == "body":
                            got_true = True
                            reasons.append(("alt-true", a))
                            continue
                        keep.append(news)
                    if got_true:
                        reasons.append(("func-true", s))
                        continue
                    if not keep:
                        return ("impossible", None, reasons + [("func-empty", s)])
                    out.append(f":{name}(" + ",".join(keep) + ")")
                    continue
                if name == "not":
                    alts = split_top(args)
                    keep = []
                    for a in alts:
                        st, news, why = self.reduce_selector(a, nested=True)
                        if st == "impossible":
                            reasons.append(("not-satisfied", a))
                            continue
                        if news.strip() == "" or a.strip() == "body":
                            return ("impossible", None, reasons + [("not-true", a)])
                        keep.append(news)
                    if not keep:
                        reasons.append(("not-empty", s))
                        continue
                    out.append(":not(" + ",".join(keep) + ")")
                    continue
                out.append(s)
                continue
            out.append(s)
        return ("ok", out, reasons)

    def reduce_selector(self, sel, nested=False):
        """-> (status, new_selector_text)"""
        toks = split_selector(sel)
        new = []
        pending_reasons = []
        for kind, text in toks:
            if kind == "comb":
                new.append(text)
                continue
            simples = split_simples(text)
            st, out, reasons = self.reduce_simple_list(simples, kind)
            pending_reasons += reasons
            if st == "impossible":
                return ("impossible", "", pending_reasons)
            if not out:
                # compound became empty
                if nested:
                    # inside :is()/:not()/:where() an unconstrained compound
                    # means "matches anything"
                    continue
                if new and new[-1] in (">", "+", "~"):
                    # compound after a non-descendant combinator: replace with body
                    new.append("body")
                elif new:
                    # descendant combinator: drop the compound
                    pass
                else:
                    new.append("body")
                continue
            new.append("".join(out))
        return ("ok", self.tidy(new), pending_reasons)

    @staticmethod
    def tidy(toks):
        out = []
        for t in toks:
            if t in (">", "+", "~"):
                while out and out[-1] == " ":
                    out.pop()
                out.append(t)
            else:
                if out and out[-1] not in (">", "+", "~", " "):
                    out.append(" ")
                out.append(t)
        return "".join(out).replace(" > ", ">").replace(" + ", "+").replace(" ~ ", "~").strip()

    def transform_selector_list(self, sel_text):
        kept, dropped = [], 0
        for part in split_top(sel_text):
            st, news, why = self.reduce_selector(part)
            if st == "impossible":
                dropped += 1
                self.log.append(("DROP", part.strip(), why))
                self.pairs.append((part.strip(), None))
                continue
            self.pairs.append((part.strip(), news))
            if news != part.strip():
                self.log.append(("REWRITE", part.strip(), news))
            kept.append(news)
        if not kept:
            return None
        return ",".join(kept)

    def transform_nodes(self, nodes):
        out = []
        for kind, a, b in nodes:
            if kind in ("comment", "raw", "at-stmt"):
                out.append((kind, a, b))
                continue
            if kind == "block":
                if a.startswith("@"):
                    at = a.split()[0].lower() if a.split() else a
                    if at in GROUP_AT:
                        out.append(("block", a, self.transform_nodes(parse_nodes(b))))
                    else:
                        out.append((kind, a, b))
                    continue
                sel = self.transform_selector_list(a)
                if sel is None:
                    continue
                out.append(("block", sel, b))
        return out


def render(nodes):
    out = []
    for kind, a, b in nodes:
        if kind == "comment":
            out.append(a)
        elif kind == "raw":
            out.append(a)
        elif kind == "at-stmt":
            out.append(a)
        else:
            body = b if isinstance(b, str) else render(b)
            out.append(f"{a}{{{body}}}")
    return "".join(out)


# ------------------------------------------------------------ pretty-printing
DECL_RE = re.compile(r"^([-\w]+)\s*:\s*")


def _decl_lines(inner):
    """Split a rule body into one declaration per line."""
    out = []
    for kind, a, _ in parse_nodes(inner):
        text = a.strip()
        if not text:
            continue
        if kind == "comment":
            out.append(text)
            continue
        m = DECL_RE.match(text)
        # Leave url(...) and @-statements alone: "http://" is not a declaration.
        if m:
            text = f"{m.group(1)}: {text[m.end():]}"
        out.append(text)
    return out


def _pretty(nodes, depth, out):
    pad = "\t" * depth
    for kind, a, b in nodes:
        if kind == "block":
            head = a.strip()
            inner_nodes = b if isinstance(b, list) else parse_nodes(b)
            # @media / @supports / @keyframes wrap further rules; everything
            # else (@font-face included) holds declarations.
            if any(k == "block" for k, _, _ in inner_nodes):
                out.append(f"{pad}{head} {{")
                _pretty(inner_nodes, depth + 1, out)
                out.append(f"{pad}}}")
                continue
            # Selector lists read better one per line.
            if not head.startswith("@") and len(split_top(head)) > 1:
                out.append(",\n".join(f"{pad}{s.strip()}" for s in split_top(head) if s.strip()) + " {")
            else:
                out.append(f"{pad}{head} {{")
            if isinstance(b, list):
                _pretty(b, depth + 1, out)
            else:
                for line in _decl_lines(b):
                    out.append(f"{pad}\t{line}")
            out.append(f"{pad}}}")
            continue
        text = a.strip()
        if text:
            out.append(f"{pad}{text}")


def pretty(text):
    """Re-indent a stylesheet: one selector and one declaration per line."""
    out = []
    _pretty(parse_nodes(text), 0, out)
    return "\n".join(out) + "\n"
