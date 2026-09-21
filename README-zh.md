<div align="center">

# Obsidian MacOS

### 一个符合 Mac 原生风格的 Obsidian 主题

基于 [Baseline](https://github.com/aaaaalexis/obsidian-baseline) 构建

[English](README.md) · **简体中文**

![](img/screenshot-1.png)

![](img/screenshot-2.png)

</div>

## 概览

这个主题把 macOS 原生应用的设计语言搬到 Obsidian 里：左右边栏不再是浮在窗口上的卡片，而是像访达、备忘录那样一路贴到窗口边缘、铺满标题栏下方，方角、无投影；边栏与内容之间靠一层略深的底色来分区，而不是画分割线——右边栏与编辑器之间那条线已删除，两侧从此一致，关闭 Translucent window 后边栏有自己固定的浅灰底，设置窗口左侧那一列也贴边同色。它刻意保持"默认即定稿"的思路：外观交给系统，拿到手就是本该有的样子，只有一种形态，没有设置项，不需要 Style Settings，不依赖任何插件，一个 CSS 文件就是全部。移动端沿用同一套已固化的配色、字体与标注取值，主题新增的边栏规则只作用于桌面端，移动端不做改动，也不受影响。

## 安装

**手动**

1. 下载 `theme.css` 和 `manifest.json`。
2. 放进 `<你的库>/.obsidian/themes/obsidian-macos/`。
3. 打开 **设置 → 外观 → 主题**，选择 `obsidian-macos`。

如果列表里没有，用 `Cmd`/`Ctrl` + `R` 重载一下应用。

**从源码**

clone 仓库，跑 `npm install && npm run build`，再按上面两步把两个文件放过去。

## 目录结构

```
src/                 主题源码：样式都写在这里的 SCSS 里
theme.css            Obsidian 加载的样式，由 src/ 编译而来，已提交
manifest.json        主题元数据
versions.json        版本 → 最低 Obsidian 版本
obsidian-macos.png   主题商店缩略图
docs/                说明与更新记录
img/                 本 README 用到的截图
tools/               生成 src/ 的一次性脚本，编译主题用不到
```

装主题只需要 `theme.css` 和 `manifest.json` 两个文件，其余目录都只和开发有关。仓库里不提供 `snippets/`，样式改动全部写在 `src/` 里。

## 编译

`src/` 是主题源码，`theme.css` 由它编译而来：

```bash
npm install          # 只需一次，需要联网：把 dart-sass 装进 node_modules/
npm run build        # sass src/theme.scss theme.css —— 离线，几百毫秒
npm run watch        # 边改边自动重新编译
```

装过这一次之后，`npm run build` 完全不需要网络。不想留 `node_modules/` 的话，用任何 Sass 命令行都可以，例如 `brew install sass/sass/sass`，然后：

```bash
sass --no-source-map --no-charset --style=compressed src/theme.scss theme.css
```

编译好的 `theme.css` 已经提交，不编译也能直接用。样式源码的改动清单见
[`docs/customization.md`](docs/customization.md)。

## 致谢

- 主题基于 [**Baseline**](https://github.com/aaaaalexis/obsidian-baseline) 构建，by [Alexis C](https://github.com/aaaaalexis)，MIT 许可。样式源码、工作区布局与内嵌字体都来自它。
- 内嵌标题字体：Instrument Serif。

## 许可

本项目采用 MIT 许可，见 [`LICENSE.txt`](LICENSE.txt)。
