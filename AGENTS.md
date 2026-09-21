# AGENTS.md

给在本仓库工作的 agent 的说明。这里只写那些「不看就会做错」的事，项目介绍见
[`README.md`](README.md) 与 [`docs/`](docs/README.md)。

## 这是什么

`obsidian-macos` 是一个 Obsidian 主题，源码派生自 Baseline 3.2.12
（<https://github.com/aaaaalexis/obsidian-baseline>）。没有 JavaScript、没有插件依赖、
也不提供 Style Settings 选项：外观是固定的，`src/` 编译出的 `theme.css` 就是最终样式。

## 常用命令

```bash
npm install    # 只需一次，需要联网，把 dart-sass 装进 node_modules/
npm run build  # sass src/theme.scss theme.css，离线，几百毫秒
npm run watch  # 边改边编译
```

仓库没有测试套件，验证方式是「重新编译后 `theme.css` 无差异」加上下面那几条检查。

## 目录

| 路径 | 说明 |
| --- | --- |
| `src/` | 主题源码，唯一的构建输入；改动都写在这里 |
| `theme.css` | 由 `src/` 编译而来，**已提交**，Obsidian 直接加载它 |
| `manifest.json` / `versions.json` | 主题元数据与版本 → 最低 Obsidian 版本 |
| `docs/` | `customization.md`（相对 Baseline 的改动）、`changelog.md`、`baseline-config.json` |
| `tools/` | 一次性迁移脚本，编译不需要；只在换 Baseline 版本时用 |
| `img/` | README 截图，约定见 `img/README.md` |

## 硬性约束

1. **改了 `src/` 就必须跑 `npm run build` 并提交 `theme.css`。** `theme.css` 是构建产物，
   但它同时是发布物，CI 会重新编译并比对，产物与源码不一致直接失败。
2. **不允许出现 Style Settings。** `src/` 里不能有 `@settings` 块，也不能有
   `src/app/style-settings.scss`；`theme.css` 同理。这个主题的定位就是「装完即定稿」。
3. **不要新增可选项，也不要建 `snippets/`。** 需要固定的取值写进 `src/app/config.scss`
   （它排在 `@use` 列表最后，用来覆盖 Baseline 的同名默认值）。
4. **移动端与平板保持 Baseline 原样。** 桌面改动都写在 `body:not(.is-mobile)` 段内，
   `body.is-tablet` 段和 `src/app/mobile.scss` 不要动；移动端只是共享了固化后的全局取值。
5. **版本号三处同步**：`package.json`、`manifest.json`、`versions.json`。
   `versions.json` 里必须存在 `manifest.version` 这个键、值等于 `manifest.minAppVersion`，
   且它是最新的键。
6. **发布靠 tag**：push `v1.2.0` 这类 tag 会触发 release 工作流，tag 去掉 `v` 必须等于
   `manifest.json` 的 `version`，否则失败。
7. **别把构建残留提交进去**：`node_modules/`、`build/`、`.obsidian/`、`*.css.map` 已在
   `.gitignore` 里；反过来 `theme.css`、`manifest.json`、`versions.json`、`package-lock.json`
   必须提交。

## 重新派生源码时要小心

`python3 tools/derive-src.py --source <baseline checkout> --write` 会**整个覆盖** `src/`。
覆盖后必须手工补回工具不生成的内容，细节见 [`tools/README.md`](tools/README.md) 与
[`docs/customization.md`](docs/customization.md)：

- `src/app/config.scss`（13 个固化变量）
- `src/theme.scss` 的头部注释与最后那行 `@use "app/config.scss"`
- `src/layouts/macos.scss` 里本主题的四处改动

上游 Baseline 的副本不入库，需要时 clone 到临时目录再用 `--source` 指过去。

## 文档

- 改样式就同步 [`docs/customization.md`](docs/customization.md)，发版本就补
  [`docs/changelog.md`](docs/changelog.md)。
- 注释、`docs/`、`.gitignore` 用中文；`README.md` 英文、`README-zh.md` 中文，两边内容要一致。

## 提交前

```bash
npm run build && git diff --exit-code -- theme.css   # 产物与源码一致
! grep -rq "@settings" src/                          # 没有 Style Settings
```

`theme.css` 还应满足：无 BOM、花括号数量平衡、包含 `obsidian-macos` 与
`Baseline 3.2.12` 字样——这几条就是 CI 检查的内容。
