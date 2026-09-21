"""Reduce Style Settings conditions inside SCSS selectors.

The theme is fixed: the options are gone, so a selector gated on one of them
can be settled at source level. A class that the frozen configuration turns on
is always present, so conditions on it are vacuous and disappear; a condition
on a class that is off can never match, so the whole rule goes away.

Unlike the CSS baker this rewriter edits the original text in place: every span
it does not deliberately touch - comments, `//` comments, declarations,
interpolation, indentation - is copied through byte for byte.
"""


def _skip_string(text, i, end):
    quote = text[i]
    i += 1
    while i < end:
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == quote:
            return i + 1
        i += 1
    return end


def _line_comment_at(text, i):
    """True at the start of a `//` comment (not `://`, not inside url())."""
    return (text.startswith("//", i)
            and (i == 0 or text[i - 1] not in ":/"))


def _matching_brace(text, i, end):
    """i points at '{'; return the index just past the matching '}'."""
    depth = 0
    while i < end:
        c = text[i]
        if c in "\"'":
            i = _skip_string(text, i, end)
            continue
        if _line_comment_at(text, i):
            i = text.find("\n", i)
            if i == -1:
                return end
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i)
            i = end if j == -1 else j + 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return end


def _head_end(text, i, end):
    """Return (index, terminator) for the next top-level { ; or } from i."""
    depth = 0
    while i < end:
        c = text[i]
        if c in "\"'":
            i = _skip_string(text, i, end)
            continue
        if _line_comment_at(text, i):
            newline = text.find("\n", i)
            if newline == -1:
                return end, ""
            i = newline
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i)
            i = end if j == -1 else j + 2
            continue
        if text.startswith("#{", i):
            i = _matching_brace(text, i + 1, end)
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and c in "{;}":
            return i, c
        i += 1
    return end, ""


def declares_anything(text):
    """True if the rewritten file can still emit CSS (any block at all)."""
    return "{" in text


def rewrite(text, baker, flag_re=None):
    """Reduce every selector in an SCSS document.

    Returns (new_text, edits, skipped): edits is a list of
    (old_selector, new_selector_or_None) and skipped lists heads that were left
    alone because they are not plain selectors.
    """
    edits, skipped, spans = [], [], []
    n = len(text)

    def walk(start, end):
        i = start
        while i < end:
            c = text[i]
            if c in " \t\r\n":
                i += 1
                continue
            if _line_comment_at(text, i):
                newline = text.find("\n", i)
                i = end if newline == -1 else newline + 1
                continue
            if text.startswith("/*", i):
                j = text.find("*/", i)
                i = end if j == -1 else j + 2
                continue
            j, term = _head_end(text, i, end)
            if term != "{":
                i = j + 1
                continue
            body_end = _matching_brace(text, j, end)
            head = text[i:j]
            bare = head.strip()
            if not bare or bare.startswith("@") or "#{" in bare:
                if bare and not bare.startswith("@") and "#{" in bare:
                    skipped.append(bare)
                if bare.startswith("@"):
                    walk(j + 1, body_end)
                elif "#{" in bare:
                    walk(j + 1, body_end)
                i = body_end
                continue
            if flag_re is not None and not flag_re.search(bare):
                # 这个选择器里没有开关类名，原样保留（避免组合器空格之类的
                # 无意义改写）
                walk(j + 1, body_end)
                i = body_end
                continue
            new = baker.transform_selector_list(bare)
            if new is None:
                spans.append((i, body_end, ""))
                for old, replacement in baker.pairs:
                    edits.append((old, replacement))
                baker.pairs.clear()
            else:
                if new != bare:
                    lead = len(head) - len(head.lstrip())
                    trail = len(head) - len(head.rstrip())
                    spans.append((i + lead, j - trail, new))
                for old, replacement in baker.pairs:
                    edits.append((old, replacement))
                baker.pairs.clear()
                walk(j + 1, body_end)
            i = body_end

    walk(0, n)
    out, last = [], 0
    for start, stop, replacement in spans:
        out.append(text[last:start])
        out.append(replacement)
        last = stop
    out.append(text[last:])
    return "".join(out), edits, skipped
