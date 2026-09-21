<div align="center">

<!-- 截图放在 img/。放好 img/hero.png 之后，把下面这行的注释去掉：
![](img/hero.png)
-->

# obsidian-macos

### 用 Baseline 的源码做的主题，左右边栏都贴边停靠。

_[Baseline](https://github.com/aaaaalexis/obsidian-baseline) 3.2.12 的源码，
配置固定、可调项全部移除——没有能调错的地方。_

[English](README.md) · **简体中文**

</div>

## 概览

**只有一种样子，没有开关。** Baseline 的 macOS 布局把左侧栏做成一枚悬浮卡片：
8px 外边距、圆角、投影。这里它是一个贴边的普通面板，和右侧栏完全一样；原来摆在
Style Settings 面板里的那些选择，已经写死在样式源码里，没有可以乱调的地方。

**边栏终于像边栏。** 关闭 *Translucent window* 时，Obsidian 会在边栏后面铺一层白色
工作区，边栏本身就化在里面看不出来了。这个主题给边栏自己的底色，设置窗口左侧那一列
也一样。

**移动端保持 Baseline 原样。** 这个主题新增的规则都限定在桌面端，手机和平板沿用
Baseline 原本的样式。

## 改了什么

| | [Baseline](https://github.com/aaaaalexis/obsidian-baseline) | obsidian-macos |
| :-- | :-- | :-- |
| 左侧栏 | 悬浮卡片：8px 外边距、圆角、投影 | 贴边面板，紧贴窗口边缘 |
| 与编辑器之间的分隔线 | 只有右侧栏有 | 两侧都没有 |
| 关闭 Translucent window 时的边栏 | 透明，白色工作区透出来，边栏看不出边界 | 亮色下是浅灰；暗色本来就正常，未改动 |
| 设置窗口的侧栏 | 悬浮的圆角卡片 | 贴边，底色与主边栏一致 |
| Style Settings | 约 200 个选项 | 没有——配置已写死在源码里 |
| 移动端与平板 | Baseline | Baseline |

配色、排版、标签页、标注与代码块的样式都是 Baseline 的，只是把那套 Style Settings
取值固化进了源码。完整清单见 [`docs/customization.md`](docs/customization.md)。

## 安装

**手动**

1. 下载 `theme.css` 和 `manifest.json`。
2. 放进 `<你的库>/.obsidian/themes/obsidian-macos/`。
3. 打开 **设置 → 外观 → 主题**，选择 `obsidian-macos`。

如果列表里没有，用 `Cmd`/`Ctrl` + `R` 重载一下应用。

**从源码**——clone 仓库，跑 `npm install && npm run build`，再按上面两步把两个文件
放过去。主题就是一个 CSS 文件，不依赖任何插件；Style Settings 不需要，也不会识别它。

## 目录结构

```
src/                 主题源码：Baseline 的 SCSS，已按本主题改动
theme.css            Obsidian 加载的样式，由 src/ 编译而来，已提交
manifest.json        主题元数据
versions.json        版本 → 最低 Obsidian 版本
obsidian-macos.png   主题商店缩略图
docs/                说明与更新记录
img/                 本 README 用到的截图
tools/               当初把 Baseline 派生成 src/ 的一次性脚本
```

结构参照 Baseline 的仓库，有两处有意的不同：没有 `snippets/` 目录——本主题的改动
全部落在 `src/` 里，改动的入口就是主题本身；另外，除了 `src/` 派生自的那部分代码，
仓库里不再保留 Baseline 的任何东西。对照关系见 [`docs/README.md`](docs/README.md)。

## 编译

[`src/`](src) 就是 Baseline 的 SCSS——目录和分文件都一样——只是把没启用的选项、
布局、元素风格和配色删掉了，把选定的那套配置落进选择器，再把本主题的改动写在它该在
的位置。`theme.css` 就是这份源码编译出来的：

```bash
npm install          # 只需一次，需要联网：把 dart-sass 装进 node_modules/
npm run build        # sass src/theme.scss theme.css —— 离线，几百毫秒
npm run watch        # 边改边自动重新编译
```

装过这一次之后，`npm run build` 完全不需要网络。不想留 `node_modules/` 的话，用任何
Sass 命令行都可以，例如 `brew install sass/sass/sass`，然后：

```bash
sass --no-source-map --no-charset --style=compressed src/theme.scss theme.css
```

`src/` 是从 Baseline 3.2.12 派生一次得到的：派生用的脚本和那套配置都在
[`tools/`](tools) 里。仓库里不留 Baseline 的任何副本，编译时也不下载任何东西。
编译好的 `theme.css` 已经提交，所以即使从不编译也能直接用；整个流程（编译时和运行时）
都不需要 Style Settings 插件。

相对 Baseline 的每一处改动都列在 [`docs/customization.md`](docs/customization.md)，
写明了文件位置和在 `src/` 里搜什么。

## 致谢

- 主题与工作区设计：[**Baseline**](https://github.com/aaaaalexis/obsidian-baseline)
  by [Alexis C](https://github.com/aaaaalexis)，MIT 许可。本项目是它的衍生作品：
  `src/` 是 Baseline 的源码加上 [`docs/customization.md`](docs/customization.md)
  里的那些改动，并保留了 Baseline 内嵌的字体。没有它就没有这个主题。
- 内嵌标题字体：Instrument Serif。
- Baseline 自身又建立在 [Minimal](https://github.com/kepano/obsidian-minimal)
  等主题之上，完整名单见它的 README。

## 许可

Baseline 与这个主题都是 MIT 许可，见 [`LICENSE.txt`](LICENSE.txt)（里面两行版权声明）。
