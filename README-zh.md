<div align="center">

<!-- 截图放在 img/。放好 img/hero.png 之后，把下面这行的注释去掉：
![](img/hero.png)
-->

# obsidian-macos

### 左右边栏都贴边停靠的 Obsidian 主题。

基于 [Baseline](https://github.com/aaaaalexis/obsidian-baseline) 构建。

[English](README.md) · **简体中文**

</div>

## 概览

**左右边栏都是普通面板。** 两侧边栏紧贴窗口边缘，没有外边距、圆角、投影，与编辑器
之间也没有分隔线，看着就是工作区的一部分。

**边栏有自己的底色。** 关闭 *Translucent window* 时，边栏不会化进白色工作区：亮色下
是浅灰，暗色下沿用原来的表现。设置窗口左侧那一列同样贴边、同色。

**只有一种样子。** 没有设置项，装好即定稿；主题就是一个 CSS 文件，不依赖任何插件，
也不需要 Style Settings。

**移动端不做改动。** 手机和平板维持原有的移动端外观。

## 安装

**手动**

1. 下载 `theme.css` 和 `manifest.json`。
2. 放进 `<你的库>/.obsidian/themes/obsidian-macos/`。
3. 打开 **设置 → 外观 → 主题**，选择 `obsidian-macos`。

如果列表里没有，用 `Cmd`/`Ctrl` + `R` 重载一下应用。

**从源码**——clone 仓库，跑 `npm install && npm run build`，再按上面两步把两个文件
放过去。

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

装主题只需要 `theme.css` 和 `manifest.json` 两个文件，其余目录都只和开发有关。仓库里
不提供 `snippets/`，样式改动全部写在 `src/` 里。

## 编译

`src/` 是主题源码，`theme.css` 由它编译而来：

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

编译好的 `theme.css` 已经提交，不编译也能直接用。样式源码的改动清单见
[`docs/customization.md`](docs/customization.md)。

## 致谢

- 主题基于 [**Baseline**](https://github.com/aaaaalexis/obsidian-baseline) 构建，
  by [Alexis C](https://github.com/aaaaalexis)，MIT 许可。样式源码、工作区布局与内嵌
  字体都来自它。
- 内嵌标题字体：Instrument Serif。
- Baseline 自身又建立在 [Minimal](https://github.com/kepano/obsidian-minimal)
  等主题之上，完整名单见它的 README。

## 许可

本项目采用 MIT 许可，见 [`LICENSE.txt`](LICENSE.txt)。
