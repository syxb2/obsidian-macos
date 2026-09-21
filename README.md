<div align="center">

<!-- Screenshots live in img/. Uncomment once img/hero.png is in place:
![](img/hero.png)
-->

# obsidian-macos

### Baseline's source, with both sidebars docked.

_[Baseline](https://github.com/aaaaalexis/obsidian-baseline) 3.2.12 with a fixed
configuration and the options removed — nothing to misconfigure._

**English** · [简体中文](README-zh.md)

</div>

## Overview

**One look, no knobs.** Baseline's macOS layout floats the left sidebar as a
rounded card with an 8px inset and a drop shadow. Here it is a plain panel,
flush with the window edge, exactly like the right sidebar — and the choices
that used to live in the Style Settings panel are settled in the stylesheet
itself, so there is nothing to wander into.

**Sidebars that read as sidebars.** With *Translucent window* off, Obsidian
paints a white workspace behind the sidebars and they disappear into it. This
theme gives them a surface of their own, and the settings window's left column
matches.

**Mobile is Baseline, untouched.** Every rule this theme adds is scoped to the
desktop, so phones and tablets keep the original styling.

## What it changes

| | [Baseline](https://github.com/aaaaalexis/obsidian-baseline) | obsidian-macos |
| :-- | :-- | :-- |
| Left sidebar | floating card: 8px inset, rounded corners, drop shadow | docked panel, flush with the window edge |
| Divider against the editor | only on the right sidebar | on neither |
| Sidebars, translucency off | transparent over a white workspace, so they vanish into it | light grey in light mode; dark mode was already fine and is left alone |
| Settings window sidebar | floating rounded card | docked, same surface as the sidebars |
| Style Settings | ~200 options | none — the configuration is baked in |
| Mobile and tablet | Baseline | Baseline |

Colors, typography, tab style, callouts and code blocks are Baseline's, with one
Style Settings configuration frozen into the source. The full list is in
[`docs/customization.md`](docs/customization.md).

## Installation

**Manual**

1. Download `theme.css` and `manifest.json`.
2. Put them in `<your vault>/.obsidian/themes/obsidian-macos/`.
3. Open **Settings → Appearance → Themes** and pick `obsidian-macos`.

If it does not show up, reload the app with `Cmd`/`Ctrl` + `R`.

**From source** — clone the repository, run `npm install && npm run build`, then
copy the two files the same way. The theme is a single CSS file with no plugin
dependency; Style Settings is not needed and will not recognise it.

## Repository layout

```
src/                 the theme's source: Baseline's SCSS, modified
theme.css            the theme Obsidian loads - built from src/, committed
manifest.json        theme metadata
versions.json        manifest version → minimum Obsidian version
obsidian-macos.png   store thumbnail
docs/                notes and changelog
img/                 screenshots used by this README
tools/               the one-off tool that derived src/ from Baseline
```

The layout follows Baseline's repository, with two deliberate differences:
there is no `snippets/` directory — everything this theme changes is settled in
`src/` instead of being handed out as optional add-ons — and nothing of
Baseline's is kept in the repository beyond the code `src/` was derived from.
[`docs/README.md`](docs/README.md) explains the mapping.

## Building

[`src/`](src) is Baseline's SCSS — the same layout, the same partials — with the
unused options, layouts, element styles and colour schemes deleted, the chosen
configuration settled in the selectors, and this theme's changes written in at
the place they belong. `theme.css` is that source compiled:

```bash
npm install          # once, needs network: fetches dart-sass into node_modules/
npm run build        # sass src/theme.scss theme.css - offline, a few hundred ms
npm run watch        # rebuild on save while editing
```

After that first `npm install`, `npm run build` works with no network at all. Any
Sass CLI works too if you would rather not have `node_modules/` — for example
`brew install sass/sass/sass`, then
`sass --no-source-map --no-charset --style=compressed src/theme.scss theme.css`.

`src/` was derived once from Baseline 3.2.12 — the tool that did it, and the
configuration it used, are in [`tools/`](tools). Nothing of Baseline's is kept
in the repository and nothing is downloaded at build time. The compiled
`theme.css` is committed, so the repository is usable as-is without ever running
the build. No step needs the Style Settings plugin, at build time or at runtime.

Every change relative to Baseline is listed in
[`docs/customization.md`](docs/customization.md), with the file and the selector
to look for in `src/`.

## Credits

- Theme and workspace design: [**Baseline**](https://github.com/aaaaalexis/obsidian-baseline)
  by [Alexis C](https://github.com/aaaaalexis), MIT licensed. This project is a
  derived work: `src/` is Baseline's source with the changes in
  [`docs/customization.md`](docs/customization.md) applied, and it keeps
  Baseline's embedded fonts. It would not exist without Baseline.
- Embedded heading font: Instrument Serif.
- Baseline itself builds on [Minimal](https://github.com/kepano/obsidian-minimal)
  and others — see its README for the full list.

## License

Baseline is MIT licensed; so is this. See [`LICENSE.txt`](LICENSE.txt), which
carries both copyright lines.
