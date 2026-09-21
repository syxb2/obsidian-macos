# docs

放不进 [README](../README.md) 的笔记：这个主题相对上游改了什么、什么时候改的，
以及将来重新派生源码时要对照的东西。

## 本目录

| 文件 | 用处 |
| --- | --- |
| `README.md` | 本页。docs/ 里有什么，以及整个仓库的目录怎么摆、每个文件做什么 |
| [`customization.md`](customization.md) | 相对 Baseline 3.2.12 的改造记录：四处源码改动、固化的配置取值、删掉的上游文件、移动端说明、常见改动的位置、换基线版本的步骤。改样式之后要同步这里 |
| [`changelog.md`](changelog.md) | 版本记录，一次发版一条。改它时要连带动版本号，清单见下面「改 changelog 时要一起改的」 |
| [`baseline-config.json`](baseline-config.json) | 当初固化的那套 Style Settings 取值（26 项），键名是 Baseline 的设置项 id。它回答「现在这个样子是从哪套配置来的」 |

## 改 changelog 时要一起改的

`changelog.md` 里的条目都对应一个已发布版本，加一条就不能只动它：

1. 在 `changelog.md` 最上面插入 `## <版本> — <日期>`，下面先写一句这次改了什么，
   再列要点；最新的版本在最上面。
2. 四处版本号改成同一个值：`package.json`、`package-lock.json`（顶层与 `packages[""]`
   里各一份）、`manifest.json`、`versions.json`。
3. `versions.json` 加上 `"<版本>": "<manifest.minAppVersion>"`，放在最前面；它必须是最新
   的键，否则 CI 的元数据检查会失败。
4. 这次要是动了 `src/`，先 `npm run build`，把重新编译的 `theme.css` 一起提交。
5. 发布时打 `v<版本>` 的 tag，去掉 `v` 必须等于 `manifest.json` 的 `version`；
   release 工作流会带上 `manifest.json` 与 `theme.css`。

面向使用者的改动写进 changelog，源码层面的事（工具、工作流、目录调整）写进
[`customization.md`](customization.md)。

## 仓库目录

```text
obsidian-macos/
├── src/                        主题源码，唯一的构建输入
│   ├── theme.scss              编译入口：头部说明加 @use 列表，顺序就是层叠顺序
│   ├── app/                    应用外壳与界面
│   │   ├── root.scss           根节点的全局 CSS 变量
│   │   ├── config.scss         固化下来的 13 个变量；人工新增，排在最后用来盖过 Baseline 默认值
│   │   ├── fonts.scss          内嵌的 Instrument Serif 标题字体（base64）
│   │   ├── icons.scss          lucide 图标的微调
│   │   ├── tabs.scss           标签页
│   │   ├── sidedock.scss       左右边栏的导航项与拖拽把手
│   │   ├── dialog.scss         菜单与建议框
│   │   ├── prompt.scss         命令面板、快速切换
│   │   ├── settings.scss       设置窗口
│   │   ├── status-bar.scss     状态栏
│   │   ├── empty-state.scss    空白工作区的空状态
│   │   ├── core-plugins.scss   核心插件，例如反向链接
│   │   ├── community-plugins.scss  社区插件适配，例如 Omnisearch
│   │   └── mobile.scss         移动端
│   ├── editor/                 笔记正文
│   │   ├── editor.scss         编辑器本身与文件边距
│   │   ├── frontmatter.scss    属性（frontmatter）
│   │   ├── blockquote.scss     引用块
│   │   ├── callout.scss        标注
│   │   ├── table.scss          表格
│   │   └── bases.scss          Bases 视图
│   ├── layouts/                工作区布局
│   │   ├── macos.scss          本主题的改动集中在这里：边栏贴边、浅灰底色、去掉分割线、设置侧栏
│   │   └── cupertino.scss      macOS 布局共用的规则
│   ├── elements/               控件与容器风格
│   │   ├── baseline.scss       基础控件
│   │   ├── cupertino.scss      Cupertino 风格主体
│   │   ├── cupertino-dialog.scss    弹窗
│   │   ├── cupertino-settings.scss  设置项
│   │   ├── cupertino-prompt.scss    命令面板
│   │   └── cupertino-mobile.scss    移动端的 Cupertino 控件
│   ├── color-schemes/
│   │   └── cupertino.scss      唯一保留的配色，亮色与暗色都在这里
│   └── features/               逐项功能
│       ├── alternative-checkboxes.scss  复选框外观
│       ├── banners.scss                 笔记顶部的 banner
│       ├── block-width.scss             正文行宽
│       ├── callout-icon.scss            标注图标
│       ├── colorful-headings.scss       空文件，没有规则，见下面的说明
│       ├── dataview-cards.scss          Dataview 卡片
│       ├── file-explorer.scss           文件列表
│       ├── helpers-tables.scss          表格辅助类
│       ├── hover-sidedock.scss          悬停展开边栏
│       ├── image-filters.scss           暗色下的图片滤镜
│       └── image-zoom.scss              图片点击放大
├── theme.css                   由 src/ 编译而来，已提交；Obsidian 加载的就是它
├── manifest.json               主题元数据：名称、版本、最低 Obsidian 版本
├── versions.json               版本到最低 Obsidian 版本的映射
├── package.json                npm 脚本（build / watch）与 dart-sass 依赖
├── package-lock.json           锁住 dart-sass 版本，CI 用 npm ci 复现
├── README.md / README-zh.md    面向使用者的说明，英文与中文两份，内容保持一致
├── LICENSE.txt                 MIT
├── AGENTS.md                   给在本仓库工作的 agent 的约定
├── .gitignore                  忽略 node_modules/、build/、.obsidian/ 等；头部注释说明了哪些产物必须提交
├── docs/                       本目录
├── tools/                      换 Baseline 版本时的派生工具，编译用不到
│   ├── README.md               工具的用法，以及它到底改写了什么
│   ├── derive-src.py           入口：读一份上游 checkout，按 baseline-config.json 生成 src/
│   └── lib/
│       ├── baseline_config.py  解析 Baseline 的 /* @settings */ 块，算出哪些类名开着
│       ├── css_transform.py    CSS 解析与选择器化简：一个条件该消掉还是该整条删掉
│       └── scss_transform.py   SCSS 选择器改写，按位置替换，其余原文一字不动
├── img/                        README 用的截图
│   ├── README.md               截图清单与拍摄建议
│   └── screenshot-1.png        README 顶部那张
└── .github/
    ├── workflows/release.yml         打 tag 时建 release，上传 manifest.json 与 theme.css
    ├── workflows/version-check.yml   CI：元数据一致性、theme.css 完整性、src/ 不含设置面板、产物与源码一致
    └── ISSUE_TEMPLATE/               issue 模板
```

`src/features/colorful-headings.scss` 目前是个空壳：外层 `@media` 里没有任何规则，
`theme.scss` 还引用着它。而 [`customization.md`](customization.md) 把它列在「被删掉的
文件」里。两种处理都行，但文件和文档的说法应该统一。

## 不在仓库里

- `snippets/`：Baseline 用它发可选增强（例如中文字体），本主题的定位是「装完即定稿」，
  安装后没有任何需要再打开的开关，所以不提供片段目录。
- 上游 Baseline 的源码副本：仓库里不放。需要对照或重新派生时，把它 clone 到临时目录，
  按 [`../tools/README.md`](../tools/README.md) 用 `--source` 指过去。
- `obsidian-macos.png`：主题商店缩略图，放在仓库根目录，目前还没提交。命名、尺寸与
  拍摄建议见 [`../img/README.md`](../img/README.md)。
- `node_modules/`、`build/`、`.obsidian/`：本地产物，`.gitignore` 已经挡掉。

## 与 Baseline 的目录对应

本仓库的结构参照 [Baseline](https://github.com/aaaaalexis/obsidian-baseline)：

| Baseline | 本仓库 | 说明 |
| --- | --- | --- |
| `src/` | 同名 | 主题源码，Baseline 的 SCSS 搬过来之后把改动写在里面 |
| `theme.css` | 同名 | 由 `src/` 编译而来（`npm run build`），已提交 |
| `manifest.json` / `versions.json` | 同名 | 主题元数据 |
| `baseline.png` | `obsidian-macos.png` | 主题商店缩略图，位于仓库根目录 |
| `img/` | 同名 | README 用的截图 |
| `docs/` | 同名 | Baseline 的 `docs/` 是 GitHub Pages 站点；这里是 Markdown 笔记 |
| `snippets/` | 无 | 改动全部固化进 `theme.css`，不提供可选片段 |
| `.github/` | 同名 | 工作流与 issue 模板 |
| — | `tools/` | 当初把上游源码派生成 `src/` 的脚本，本仓库新增 |

## 派生基线

Baseline **3.2.12**，上游仓库 <https://github.com/aaaaalexis/obsidian-baseline>，
对应 commit `8c56e83`，当时那份 `theme.css`（627,672 字节）的 md5 是
`e6f7572455734753fbbdd474891c031e`。这四项凑齐就能确认派生基线没跑偏。
