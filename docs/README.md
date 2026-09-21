# docs

Notes that do not belong in the README.

| File | Contents |
| --- | --- |
| [`customization.md`](customization.md) | 这个主题相对 Baseline 都改了什么、怎么改（中文） |
| [`changelog.md`](changelog.md) | 版本记录 |
| [`baseline-config.json`](baseline-config.json) | 当初固化的那套 Style Settings 取值，换基线版本时对照用 |

## 目录结构

本仓库的结构参照 [Baseline](https://github.com/aaaaalexis/obsidian-baseline)：

| Baseline | 本仓库 | 说明 |
| --- | --- | --- |
| `src/` | 同名 | **本主题的源码**：Baseline 的 SCSS 原样搬过来，改动写在里面 |
| `theme.css` | 同名 | 由 `src/` 编译而来（`npm run build`），已提交 |
| `manifest.json` / `versions.json` | 同名 | 主题元数据 |
| `baseline.png` | `obsidian-macos.png` | 主题商店缩略图，放在仓库根目录 |
| `img/` | 同名 | README 用的截图 |
| `docs/` | 同名 | Baseline 的 `docs/` 是 GitHub Pages 站点；这里是 Markdown 笔记 |
| — | `tools/` | 当初把上游源码派生成 `src/` 的一次性脚本 |
| `snippets/` | **无** | 本主题的改动全部固化进 `theme.css`，不提供可选片段 |
| `.github/` | 同名 | 工作流与 issue 模板 |

关于 `snippets/`：Baseline 用它发可选增强（例如中文字体），与本主题的定位不同。
本主题的目标是「装完即定稿」——安装后没有任何需要再打开的开关，所以不提供片段目录。

关于 `tools/`：那里的脚本按 [`baseline-config.json`](baseline-config.json) 把上游源码
变成 `src/`——删除未启用的变体、把开关条件从选择器里消掉。仓库里不放上游副本，
需要重新派生时按 [`../tools/README.md`](../tools/README.md) 把上游 clone 到临时目录，
用 `--source` 指过去。

派生自哪一版：Baseline **3.2.12**，上游仓库
<https://github.com/aaaaalexis/obsidian-baseline>，对应 commit `8c56e83`，
当时那份 `theme.css`（627,672 字节）的 md5 是 `e6f7572455734753fbbdd474891c031e`。
用这四项可以确认派生基线没跑偏。
