<div align="center">

<!-- Screenshots live in img/. Uncomment once img/hero.png is in place:
![](img/hero.png)
-->

# obsidian-macos

### An Obsidian theme with both sidebars docked.

Built on [Baseline](https://github.com/aaaaalexis/obsidian-baseline).

**English** · [简体中文](README-zh.md)

</div>

## Overview

**Both sidebars are plain panels.** They sit flush against the window edge — no
inset, no rounded corners, no drop shadow, and no divider between them and the
editor, so they read as part of the workspace.

**The sidebars have a surface of their own.** With *Translucent window* off they
no longer disappear into the white workspace: light grey in light mode, left as
it was in dark mode. The settings window's left column is docked and coloured
the same way.

**One look, no knobs.** There is nothing to configure — the theme is a single
CSS file with no plugin dependency, and it does not need Style Settings.

**Mobile is untouched.** Phones and tablets keep their original appearance.

## Installation

**Manual**

1. Download `theme.css` and `manifest.json`.
2. Put them in `<your vault>/.obsidian/themes/obsidian-macos/`.
3. Open **Settings → Appearance → Themes** and pick `obsidian-macos`.

If it does not show up, reload the app with `Cmd`/`Ctrl` + `R`.

**From source** — clone the repository, run `npm install && npm run build`, then
copy the two files the same way.

## Repository layout

```
src/                 the theme's source: the styles live in this SCSS
theme.css            the theme Obsidian loads - built from src/, committed
manifest.json        theme metadata
versions.json        manifest version → minimum Obsidian version
obsidian-macos.png   store thumbnail
docs/                notes and changelog
img/                 screenshots used by this README
tools/               the one-off tool that generated src/, not needed to build
```

Installing the theme needs only `theme.css` and `manifest.json`; the other
directories are for development. There is no `snippets/` directory — every style
change lives in `src/`.

## Building

`src/` is the theme's source and `theme.css` is that source compiled:

```bash
npm install          # once, needs network: fetches dart-sass into node_modules/
npm run build        # sass src/theme.scss theme.css - offline, a few hundred ms
npm run watch        # rebuild on save while editing
```

After that first `npm install`, `npm run build` works with no network at all. Any
Sass CLI works too if you would rather not have `node_modules/` — for example
`brew install sass/sass/sass`, then:

```bash
sass --no-source-map --no-charset --style=compressed src/theme.scss theme.css
```

The compiled `theme.css` is committed, so the repository is usable as-is without
ever running the build. The changes made to the styles are listed in
[`docs/customization.md`](docs/customization.md).

## Credits

- The theme is built on [**Baseline**](https://github.com/aaaaalexis/obsidian-baseline)
  by [Alexis C](https://github.com/aaaaalexis), MIT licensed. Its styles, workspace
  layout and embedded fonts all come from it.
- Embedded heading font: Instrument Serif.
- Baseline itself builds on [Minimal](https://github.com/kepano/obsidian-minimal)
  and others — see its README for the full list.

## License

This project is MIT licensed. See [`LICENSE.txt`](LICENSE.txt).
