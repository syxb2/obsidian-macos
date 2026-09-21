#!/usr/bin/env python3
"""Derive src/ - this theme's source - from a Baseline checkout.

    git clone --depth 1 https://github.com/aaaaalexis/obsidian-baseline.git /tmp/baseline
    python3 tools/derive-src.py --source /tmp/baseline            # report only
    python3 tools/derive-src.py --source /tmp/baseline --write    # write src/

One-off tool. It copies Baseline's SCSS, drops the Style Settings definition
and every file that only serves an option this theme does not use, and settles
the remaining option conditions in the selectors themselves. Everything after
that is edited by hand in src/.
"""

import argparse
import json
import re
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "lib"))

import baseline_config  # noqa: E402
import css_transform  # noqa: E402
import scss_transform  # noqa: E402

TARGET = os.path.join(ROOT, "src")
CONFIG = os.path.join(ROOT, "docs", "baseline-config.json")
CLONE_HINT = ("git clone --depth 1 "
              "https://github.com/aaaaalexis/obsidian-baseline.git /tmp/baseline")

# 这份文件只是 /_* @settings *_/ 定义（3173 行）加设置面板自己的样式，
# 主题不再有设置面板，所以整份丢掉。
SETTINGS_FILE = os.path.join("app", "style-settings.scss")

# 这些文件整份只服务于没有启用的选项，但选项名写成了 Sass 插值
# （`.h#{$i}-l`），改写器认不出来，所以在这里点名丢掉。
UNUSED_FILES = {
    os.path.join("features", "underline-headings.scss"):
        "下划线标题（h1-l…h6-l）没有启用",
}


def scss_files(source):
    out = []
    for base, _dirs, names in os.walk(source):
        for name in sorted(names):
            if name.endswith(".scss"):
                full = os.path.join(base, name)
                out.append(os.path.relpath(full, source))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=os.path.join(ROOT, "upstream", "baseline"),
                    help="a Baseline checkout (the directory holding src/ and "
                         "theme.css). Not part of this repository - clone one "
                         "first, see tools/README.md")
    ap.add_argument("--write", action="store_true", help="write src/")
    args = ap.parse_args()

    source = os.path.join(args.source, "src")
    if not os.path.isfile(os.path.join(source, "theme.scss")):
        raise SystemExit(
            f"no Baseline checkout at {args.source}\n"
            f"get one first:\n  {CLONE_HINT}\n"
            f"then point --source at it.")

    css = open(os.path.join(args.source, "theme.css"), encoding="utf-8").read()
    config = json.load(open(CONFIG, encoding="utf-8"))
    flags, on, _groups, _variables = baseline_config.load(css, config)
    # 与当初固化时一致：Style Settings 插件视为已加载，所以
    # `:is(<值>, :not(.css-settings-manager))` 这类「或插件不存在」的写法
    # 一律按「不存在」处理，整条规则删掉。
    flags["css-settings-manager"] = ("toggle", True)
    on.add("css-settings-manager")
    # 只碰含开关类名的选择器：没有开关的选择器原样保留
    flag_re = re.compile(
        r"\.(?:" + "|".join(re.escape(f) for f in sorted(flags)) + r")(?![\w-])")

    kept, dropped, edits, skipped = [], [], [], []
    for rel in scss_files(source):
        if rel == "theme.scss":
            continue  # 入口单独重建
        if rel == SETTINGS_FILE:
            dropped.append((rel, "设置面板定义与样式，主题不再有设置面板"))
            continue
        if rel in UNUSED_FILES:
            dropped.append((rel, UNUSED_FILES[rel]))
            continue
        text = open(os.path.join(source, rel), encoding="utf-8").read()
        baker = css_transform.Css(flags, on)
        new, file_edits, file_skipped = scss_transform.rewrite(text, baker, flag_re)
        skipped += [(rel, s) for s in file_skipped]
        file_edits = [(o, n) for o, n in file_edits if o != n]
        if not scss_transform.declares_anything(new):
            dropped.append((rel, "所有规则都挂在未启用的选项上"))
            continue
        kept.append((rel, new))
        edits += [(rel, old, new_sel) for old, new_sel in file_edits]

    kept_names = {rel for rel, _ in kept}
    uses = []
    for line in open(os.path.join(source, "theme.scss"), encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.startswith("@use "):
            continue
        rel = line.split('"')[1]
        if rel in kept_names:
            uses.append(line)

    print(f"保留 {len(kept)} 个文件，丢弃 {len(dropped)} 个")
    for rel, why in dropped:
        print(f"  丢弃 {rel:38s} {why}")
    print(f"\n选择器改写 {len(edits)} 处：")
    for rel, old, new_sel in edits[:40]:
        print(f"  {rel}: {old}  ->  {new_sel if new_sel else '(整条删除)'}")
    if len(edits) > 40:
        print(f"  ... 其余 {len(edits) - 40} 处")
    if skipped:
        print(f"\n跳过（含插值，需要人工检查）{len(skipped)} 处：")
        for rel, head in skipped:
            print(f"  {rel}: {head}")

    if not args.write:
        print("\n（未写入，加 --write 才生成 src/）")
        return

    if os.path.exists(TARGET):
        shutil.rmtree(TARGET)
    for rel, text in kept:
        dest = os.path.join(TARGET, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(text)
    open(os.path.join(TARGET, "theme.scss"), "w", encoding="utf-8").write(
        "\n".join(uses) + "\n")
    print(f"\n已写入 {TARGET}")


if __name__ == "__main__":
    main()
