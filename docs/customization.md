# 说明与改造记录

本主题的源码就是 [Baseline](https://github.com/aaaaalexis/obsidian-baseline) 3.2.12 的源码：
`src/` 里是同名的目录和文件，改动直接写在对应位置；根目录的 `theme.css` 由它编译而来
（`npm run build`），已提交，安装不需要构建。

这份源码派生自 Baseline **3.2.12**：上游仓库
<https://github.com/aaaaalexis/obsidian-baseline>，commit `8c56e83`，
当时那份 `theme.css`（627,672 字节）md5 为 `e6f7572455734753fbbdd474891c031e`。
仓库里不留上游副本；需要对照或重新派生时按
[`../tools/README.md`](../tools/README.md) 把它 clone 到临时目录。

## 一、相对 Baseline 的八处源码改动

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

左侧的功能区（ribbon）自己不带底色（Baseline 把 `--ribbon-background` 设成
`transparent`），露出来的是它底下的工作区，于是开着 Show ribbon 时那一栏总跟旁边差一个
色阶。所以这几条规则里加上了 `.workspace-ribbon.mod-left`，按「旁边是谁」分两种：

- 左边栏开着（功能区不带 `is-collapsed`）：跟边栏同色——亮色 `--background-secondary`、
  暗色 `--background-primary-alt`、半透明时 50% 的 `--background-primary`、
  窗口失焦时 `--background-modifier-hover`（和边栏那几条一一对应）；
- 左边栏收起（功能区带 `is-collapsed`）：它右边就是编辑器，这一栏取
  `--background-primary`，跟编辑器连成一片，否则编辑器是白的、那一栏是灰的。

顺带把失焦时的 `opacity: 0.5` 从 `.workspace-ribbon` 挪到 `.workspace-ribbon > *`：
边栏失焦时只有内容变淡、底色照旧，功能区也一样，两边才不会又岔开。

还有一处过渡要对齐：`.mod-sidedock` 的 `transition` 里 `background-color` 是 0s
（底色瞬间切、不渐变），而功能区在 `app/sidedock.scss` 里写的是整条 320ms，
于是失焦 / 聚焦切换时边栏底色已经切完、功能区还在渐变，看起来「不同步」。
`src/layouts/macos.scss` 里给功能区补了一条
`transition: var(--anim-duration-moderate), background-color 0s !important`，
只把底色提到 0s，宽度、内边距这些照旧走动画。

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

### 5. 打开 Show ribbon 时的左边栏与功能区（`src/layouts/macos.scss`）

Baseline 在 macOS 布局里还有一段「把左边栏拉到功能区底下」的写法，挂在 `show-ribbon` 上：

```scss
.mod-sidedock.mod-left-split:not(.is-sidedock-collapsed) {
  margin-left: calc(-1 * var(--ribbon-width) + 8px);
  padding-left: var(--ribbon-width);
}
.workspace-ribbon.mod-left:not(.is-collapsed) { padding-left: 16px; }
```

它是为上面第 1 条里那张浮卡准备的：`+ 8px` 正好对齐卡片的 `margin-left: 8px`，
`padding-left` 让卡片内容让开功能区那一栏（图标则跟着 16px 贴过去）。浮卡删掉之后，
这段只剩两个后果——左边栏左边缘到窗口还留着 8px 的缝（看着就像卡片仍悬在那儿，
这条缝的颜色是工作区底色，和边栏自身的底色不一样），文件浏览器又被挤窄一整栏 44px。

所以整段去掉：功能区自己占左边一栏，左边栏从它右边开始，跟「收起左边栏」时完全一样；
图标回到 `--ribbon-padding` 的 4px，在那一栏里居中，开关左边栏时不会再横移。

同一处还删掉了三样给浮卡/浮条留的定位：`margin-block: 8px`（非 macOS 与
macOS 的 frameless 形态，让功能区自己缩在中间）和
`body:not(.is-mobile).mod-macos.is-hidden-frameless .workspace-ribbon.mod-left.is-collapsed`
里的 `margin-top: calc(var(--header-height) - 1px)`、`padding-top: 8px` 与那条
`border-top`。最后一条现在改成对两种形态都生效的

```scss
body:not(.is-mobile).mod-macos.is-hidden-frameless .workspace-ribbon.mod-left {
  margin-top: 0;
  padding-top: calc(var(--header-height) + 8px);
  border-top: none;
}
```

功能区于是铺满整个窗口高度，连窗口左上角那一块（红绿灯所在处）也跟边栏同色；
图标位置和原来一样（原来靠 margin 让开标题栏，现在换成等量的 padding）。

### 6. 去掉边栏打开 / 关闭时的缩放动画（`src/app/sidedock.scss`）

Baseline 给边栏里的叶子加了一段入场动画：每次开关左右边栏，文件浏览器这些内容都会从
95% 放大到 100%，顺带从透明淡入。

```scss
@keyframes workspaceLeafIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
}
.mod-sidedock .workspace-leaf:not([style*="display: none"]) {
  animation: workspaceLeafIn var(--anim-duration-moderate) var(--anim-motion-baseline) forwards;
}
```

Obsidian 原生开关边栏时内容是直接出现的，没有这段动画，所以规则和只服务于它的
`@keyframes` 一起删掉。它本来就写在 `body:not(.is-mobile)` 块里，移动端与平板不受影响。

### 7. 左边栏的内容也「从自己那一侧滑进来」（`src/app/sidedock.scss`）

开关边栏时 Obsidian 只动画边栏容器的宽度（`width: 0 ↔ 设定值`，140ms、
`var(--anim-motion-swing)`），容器里的内容是被钉在容器左边缘上的。于是两边观感不同：

- 右边栏：容器贴着窗口右侧，宽度变化时动的是它的**左**边缘，内容跟着一起滑 ——
  打开时看起来是从右侧进入；
- 左边栏：容器贴着功能区，宽度变化时动的是它的**右**边缘，左边缘不动，内容又钉在左边缘
  上，于是内容原地不动、只是被慢慢露出来，像「长出来」而不是滑进来。

把左侧栏的内容改钉到它那条会动的边缘（右边缘）上，滑动方向就镜像过来了：

```scss
body:not(.is-mobile) .workspace-split.mod-left-split.mod-horizontal {
  align-items: flex-end;
}
```

边栏的 split 是 `mod-horizontal`（`flex-direction: column`），`align-items` 管的正是水平
方向；静止时容器与内容同宽，这两种对齐看不出差别，所以拖拽调宽之类的状态不受影响。
移动端的边栏是抽屉（不是 `workspace-split`），这条规则碰不到它。

### 8. 弹窗打开时不再有缩放动画（`src/app/dialog.scss`、`src/elements/cupertino-dialog.scss`）

Baseline 给弹窗（设置窗口也在内）写了入场动画，而且写了两份，后者生效：

```scss
// app/dialog.scss
@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.975);
  }
}
// elements/cupertino-dialog.scss
@keyframes modalInCupertino {
  from {
    opacity: 1;
    filter: none;
    transform: scale(0.99);
  }
}

.modal {
  animation: … forwards; // 两处各挂了一条，后一条把它从 99% 放大到 100%
}
```

于是打开设置窗口时，它会在 320ms 里从 99% 放大到 100%，而 `--anim-motion-baseline` 这条
缓动还带一点过冲，看起来就是「弹」出来。Obsidian 原生的弹窗没有这段动画，所以把两条
`.modal` 的动画和 `modalInCupertino` 一并删掉，弹窗直接出现，没有任何过渡。

`@keyframes modalIn` 保留：`.prompt`（`src/app/prompt.scss`，快速切换 / 命令面板那一层）
还在用它，本主题没有改那部分。

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
3. 确认后用 `--write` 生成新的 `src/`，再按本文档重做上面八处改动
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
