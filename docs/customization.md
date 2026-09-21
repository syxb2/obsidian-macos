# 说明与改造记录

本主题的源码就是 [Baseline](https://github.com/aaaaalexis/obsidian-baseline) 3.2.12 的源码：
`src/` 里是同名的目录和文件，改动直接写在对应位置；根目录的 `theme.css` 由它编译而来
（`npm run build`），已提交，安装不需要构建。

这份源码派生自 Baseline **3.2.12**：上游仓库
<https://github.com/aaaaalexis/obsidian-baseline>，commit `8c56e83`，
当时那份 `theme.css`（627,672 字节）md5 为 `e6f7572455734753fbbdd474891c031e`。
仓库里不留上游副本；需要对照或重新派生时按
[`../tools/README.md`](../tools/README.md) 把它 clone 到临时目录。

## 一、相对 Baseline 的四处源码改动

### 1. 左侧栏不再是浮卡（`src/layouts/macos.scss`）

Baseline 在 macOS 布局里把左侧栏做成一枚悬浮卡片：8px 外边距、圆角、投影。删掉这些声明
之后，左侧栏由通用规则接管，和右侧栏完全一致。

删除的位置（都在 `body:not(.is-mobile)` 块里）：

- `.mod-sidedock.mod-left-split` 规则：`margin: 8px 0 8px 8px`、`box-shadow`、
  `border-radius`、`overflow: hidden`
- 全屏时的额外圆角：`&.is-fullscreen .mod-sidedock.mod-left-split { border-radius … }`
  以及它内层那条只为浮卡服务的 `height: calc(var(--header-height) - 8px)`
- 为浮卡留白做的补偿：头部容器的 `padding-block: 0px`、
  `min/max-height: calc(var(--header-height) - 16px)`、内层元素的 `padding-block: 4px`
- 只服务于那张卡片的变量 `--shadow-sidedock-spread`

### 2. 左右边栏的底色（`src/layouts/macos.scss`）

边栏需要有自己的底色。没有的话，关闭 Translucent window 后工作区就是
`--background-primary`，而边栏本身透明，会跟着工作区一个色、看不出边界。

Baseline 只处理了暗色，而且要的是「比编辑器深一档」：

```scss
&:not(.is-translucent).theme-dark .mod-sidedock {
  background-color: hsl(from var(--background-primary) h s calc(l - 2));
}
```

本主题给两边都加了底色，取值如下：

```scss
&:not(.is-translucent).theme-dark .mod-sidedock {
  background-color: var(--background-primary-alt);
}
&:not(.is-tablet):not(.is-translucent).theme-light .mod-sidedock {
  background-color: var(--background-secondary);
}
```

两个变量在两种主题下正好是两个方向：亮色是编辑器混 5% 黑（`#f2f2f2` 对纯白），
暗色是编辑器混 3% 白（`#252525` 对 `#1e1e1e`）。于是亮色下边栏比编辑器深一点，
暗色下比编辑器浅一点点，与 macOS 上边栏和内容的关系一致。设置窗口左侧那一列
取同一组值，跟主边栏保持同色。

### 3. 去掉右侧栏与编辑器之间的分割线（`src/layouts/macos.scss`）

Baseline 只给右侧栏的拖拽热区上了分隔线色，左侧栏是透明的：

```scss
.mod-sidedock.mod-right-split > .workspace-leaf-resize-handle {
  border-color: var(--divider-color);
}
```

删掉后两侧统一：静止时都没有线，悬停时照旧高亮。

### 4. 设置窗口的侧栏同样贴边（`src/layouts/macos.scss`）

Baseline 的设置窗口左侧那一列也是浮卡（`margin: 8px 0 8px 8px` + 圆角 + 投影 +
半透明底色）。桌面下改成贴边、无阴影、无圆角、无竖线，底色与主边栏一致（亮色
`--background-secondary`，暗色 `--background-primary` 再暗 2%）。

平板与手机上的那一份（`body.is-tablet` 段里）**原样保留**。

## 二、被固化的配置

Baseline 的样式挂在 Style Settings 插件往 `<body>` 上加的 231 个类名上，还有一批值
由插件直接在运行时写入 CSS 变量。本主题没有设置面板，两件事分别这么处理：

**类名条件**：`src/` 里已经不存在这些条件了。派生的规则是——配置里**开启**的类名
（`layout-macos`、`input-cupertino`、`cupertino-light`…）在主题里永远存在，所以挂在
它上面的条件恒真、直接消掉；配置里**关闭**的类名永不存在，挂在它上面的规则恒假、
整条删除。用到的脚本和取值见 [`../tools/README.md`](../tools/README.md) 与
[`baseline-config.json`](baseline-config.json)。

**CSS 变量**：写死在 `src/app/config.scss` 里（13 个），文件在 `@use` 列表最后，
所以能盖过 Baseline 的同名默认值。

| 类别 | 取值 |
| --- | --- |
| 工作区布局 | `layout-macos` |
| 元素风格 / 状态栏 | `input-cupertino` / `status-bar-cupertino` |
| 亮色 / 暗色调色板 | `cupertino-light` / `cupertino-dark` |
| 标签页 | `tab-floating-center`，左上 / 右上图标、左右紧凑样式 |
| 元数据 / 标注 / 代码 | `metadata-cupertino` / `callouts-tactile` / `code-tactile` |
| 界面与正文字体 | `'SF Pro', 'system-ui'`（写在 `config.scss`） |
| 标签栏高度 / 标题字号 / 复选框圆角 | 52px / H1 1.5em…H6 0.875em / 100px（同上） |

## 三、被删掉的文件

`src/` 里没有这些上游文件，因为它们整份只服务于没有启用的选项：

- `app/style-settings.scss`——3173 行的 `/* @settings */` 定义 + 设置面板自己的样式
- `color-schemes/` 里除 `cupertino.scss` 之外的 25 套配色，`layouts/` 里除 `macos.scss`
  和 `cupertino.scss`（macOS 布局与它共用规则）之外的 6 套布局，`elements/` 里的
  `adwaita / fluent / material / tactile`（我们用的是 cupertino + tactile 的标注与代码）
- 挂在未启用开关上的功能文件：`features/colorful-*`、`features/focus-mode.scss`、
  `features/underline-headings.scss`

`theme.scss` 的 `@use` 列表也随之收窄。

## 四、移动端

桌面改动都在 `body:not(.is-mobile)` 段内，并且新增的两条还额外排除了 `.is-tablet`；
`src/app/mobile.scss` 与 `src/layouts/macos.scss` 里的 `body.is-tablet` 段没有改动。
所以移动端与平板的规则仍是 Baseline 的原文，本主题没有新增任何一条。

不过移动端的样子并不是 Baseline 的默认样子：第二节那份固化配置里，配色、字体、
标注、代码块、复选框圆角、标题字号这些取值都写在 `body` / `.theme-light` /
`.theme-dark` 这类全局作用域里，移动端一并生效。换句话说，移动端等于「Baseline 的
移动端样式 + 原来那套 Style Settings 取值」，与以前开着 Style Settings 插件时一致；
区别只在于现在不需要插件，也不可自定义。

## 五、想改的话

直接改 `src/`，然后：

```bash
npm install      # 只需一次（联网），装 dart-sass；之后编译不再需要网络
npm run build    # 重新生成 theme.css
npm run watch    # 或者边改边编译
```

常见改动的位置：

- **边栏底色深浅**：`src/layouts/macos.scss` 里搜 `--background-secondary`。
  换成 `--background-primary-alt` 是与编辑器差 3%，换成 `--background-secondary-alt`
  是差 8%；亮色下这两个值更深，暗色下更浅
- **恢复分隔线**：把上面第 3 条那段加回 `src/layouts/macos.scss`
- **配色 / 字体 / 标签栏**：`src/app/config.scss`（变量）与
  `src/color-schemes/cupertino.scss`、`src/app/tabs.scss`

## 六、换 Baseline 版本

1. 把新版本 clone 到临时目录，例如
   `git clone --depth 1 https://github.com/aaaaalexis/obsidian-baseline.git /tmp/baseline`。
2. 跑 `python3 tools/derive-src.py --source /tmp/baseline`（只报告不写入），
   看有哪些文件会被丢弃、哪些选择器会被改写。
3. 确认后用 `--write` 生成新的 `src/`，再按本文档重做上面四处改动
   （工具会覆盖 `src/`，`app/config.scss` 需要重新加回）。
4. `npm run build`，对比 `theme.css` 的差异。

## 七、已知事项

- **厂商前缀**：上游发布版里有约 10 处 `-webkit-` 前缀是 autoprefixer 加的（其余 107 处
  是源码里手写的）。本主题直接用 dart-sass 编译，不带这一步，所以这 10 处（`user-select`、
  `text-decoration`、`transition`、`box-decoration-break` 等的旧式重复声明）没有了。
  现代 Chromium / WKWebView 都支持不带前缀的写法，功能无差别；要完全对齐可以再加
  autoprefixer。
- **主题名与目录名**统一为 `obsidian-macos`。
- 截图尚未提交：`img/` 和根目录的 `obsidian-macos.png` 需要自己放，约定见
  [`../img/README.md`](../img/README.md)。
- 仓库里不含 Baseline 的任何副本；派生基线（版本 / commit / md5）记在本文档开头，
  需要时按上面的命令取上游源码。
