"""Read Baseline's Style Settings block and resolve it into classes + variables."""
import re


def parse_settings_block(css):
    i = css.find("/* @settings")
    assert i != -1
    # the comment actually starts earlier with /*!
    start = css.rfind("/*!", 0, i)
    end = css.find("*/", i)
    block = css[i:end]
    lines = block.split("\n")
    sections = {}
    cur_section = None
    cur = None
    key = None
    in_options = False
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("name:"):
            continue
        if stripped.startswith("id:") and line == line.lstrip():
            cur_section = {"id": stripped.split(":", 1)[1].strip(), "settings": []}
            sections[cur_section["id"]] = cur_section
            continue
        if stripped == "settings:":
            continue
        if not line.startswith("\t"):
            continue
        indent = len(line) - len(line.lstrip("\t"))
        if stripped == "-" and indent == 1:
            cur = {}
            cur_section["settings"].append(cur)
            in_options = False
            continue
        if stripped == "-" and indent == 3:
            cur.setdefault("options", []).append({})
            in_options = True
            continue
        if ":" not in stripped:
            continue
        k, v = stripped.split(":", 1)
        if k.strip() == "options" and not v.strip():
            cur["options"] = []
            in_options = True
            continue
        v = v.strip().strip("'").strip('"') if k.strip() not in ("description", "markdown") else v.strip()
        if indent == 2 or (indent == 1 and not in_options):
            cur[k.strip()] = v
            key = k.strip()
        elif indent >= 3 and in_options:
            cur["options"][-1][k.strip()] = v
    return sample(sections)


def sample(sections):
    return sections


def load(css, data):
    """Return (flag_defs, class_on, variables)."""
    sections = parse_settings_block(css)
    sec = sections["baseline-style"]
    pref = "baseline-style@@"
    on = set()
    flags = {}          # flag class -> ("toggle"|"select", is_on)
    group_values = {}   # select id -> set of all option values
    variables = {}      # css var name -> value string
    saved = {k[len(pref):]: v for k, v in data.items() if k.startswith(pref)}
    for s in sec["settings"]:
        t = s.get("type")
        sid = s.get("id")
        if t == "class-toggle":
            val = saved.get(sid, None)
            is_on = (val is True) or (val is None and s.get("default") == "true")
            flags[sid] = ("toggle", is_on)
            if is_on:
                on.add(sid)
        elif t == "class-select":
            vals = {o["value"] for o in s.get("options", [])}
            group_values[sid] = vals
            choice = saved.get(sid)
            if choice is None:
                choice = s.get("default", "none")
            if choice and choice != "none":
                for v in vals:
                    flags[v] = ("select", v == choice)
                on.add(choice)
        elif t and t.startswith("variable"):
            if sid in saved:
                fmt = s.get("format", "")
                v = saved[sid]
                if t in ("variable-number", "variable-number-slider"):
                    variables[sid] = f"{v}{fmt}"
                else:
                    if s.get("quotes") == "true":
                        v = f"'{v}'" if v != '@@"' else ""
                    variables[sid] = str(v)
    return flags, on, group_values, variables
