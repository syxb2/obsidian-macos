# tools/

> **编译主题不需要这个目录。** 编译是 `npm run build`（`sass src/theme.scss theme.css`），
> 只读 `src/`。这里的脚本是当初把上游 Baseline 的 SCSS **变成** `src/` 的一次性迁移工具，
> 只有将来 Baseline 发新版本、你想重新派生一份源码时才用得上。

它做的事：读一份 Baseline checkout，按
[`../docs/baseline-config.json`](../docs/baseline-config.json) 里那套取值，把 231 个
Style Settings 开关在源码层面结掉，并丢掉只服务未启用选项的文件。

```bash
git clone --depth 1 https://github.com/aaaaalexis/obsidian-baseline.git /tmp/baseline

python3 tools/derive-src.py --source /tmp/baseline            # 只报告
python3 tools/derive-src.py --source /tmp/baseline --write    # 真的写 src/
```

输入是一份 Baseline 源码 checkout——`--source` 指到仓库根目录即可，脚本读它的
`src/` 和 `theme.css`；仓库里不放上游副本，需要时按上面命令 clone。另外还读
[`../docs/baseline-config.json`](../docs/baseline-config.json)（当初固化下来的那套
Style Settings 取值），不联网，只用标准库。

## 它做什么

Baseline 的样式挂在 Style Settings 插件往 `<body>` 上加的 231 个类名上。既然本主题
固定用一套取值，这些条件可以在源码层面结掉：

* **开启**的类名（`layout-macos`、`input-cupertino`、`cupertino-light`…）在本主题里永远
  存在，挂在它上面的条件恒真，于是从选择器里去掉；
* **关闭**的类名永不存在，挂在它上面的规则恒假，整条删掉；
* `:is(<值>, :not(.css-settings-manager))` 是 Baseline 表示「或者没装插件」的写法。
  本主题永远没有这个插件，所以整条规则删掉；
* 一个文件改写完不再产出任何规则时，说明它只服务于没启用的选项，整份丢弃
  （配色、布局、元素风格里的那些就是这么没的）；
* 其余的文本——注释、`//` 注释、声明、插值、缩进——一字不动，它只替换选择器那一段。

改写不碰带插值的选择器（例如 `.h#{$i}-l`）。这类文件在 `UNUSED_FILES` 里点名丢弃。

## 文件

| 路径 | 作用 |
| --- | --- |
| `derive-src.py` | 入口（`--source` 指向上游 checkout） |
| `lib/scss_transform.py` | SCSS 选择器改写（按位置替换，保留其余原文） |
| `lib/css_transform.py` | CSS 解析器与选择器化简逻辑（判断条件该消还是该删） |
| `lib/baseline_config.py` | 解析 Baseline 的 `/* @settings */` 块，算出哪些类名开着 |

## 注意

`--write` 会**整个覆盖** `src/`。而 `src/` 里有两处是人工加的、工具不会生成：

- `src/app/config.scss`（固化的 CSS 变量）
- `src/theme.scss` 的头部注释与那行 `@use "app/config.scss"`

以及 `src/layouts/macos.scss` 里本主题的四处改动（见
[`../docs/customization.md`](../docs/customization.md)）。重跑之后要按那份文档重做一遍。
