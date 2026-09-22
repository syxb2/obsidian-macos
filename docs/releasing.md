# 发版操作说明

改完东西之后怎么把它变成一次 release，照这份清单走。机制是打 tag 触发
[`../.github/workflows/release.yml`](../.github/workflows/release.yml)：那条工作流会重新
编译、校验，然后建 release 并上传产物。另一条
[`../.github/workflows/version-check.yml`](../.github/workflows/version-check.yml) 在推 main
和开 PR 时跑同样的检查，用来提前发现问题。

## 速览

1. 改 `src/` 的话先 `npm run build`
2. 定版本号，四处改同一个值、`versions.json` 加一条
3. 在 `changelog.md` 最上面加一条
4. 本地跑一遍检查
5. 提交、push、等 main 上的 Version check 变绿
6. `git tag v<版本>` 并 push tag
7. 到 Releases 页面验收

## 一次性设置

这些只做一次，之后每次发版都不用管：

- GitHub 仓库 **Settings → Actions → General → Workflow permissions** 选
  **Read and write permissions**。选只读的话，工作流里 `gh release create` 会拿到 403，
  而 workflow 文件里写的 `permissions: contents: write` 管不了仓库这一层设置。
- 本地 `npm install` 一次（需要联网，把 dart-sass 装进 `node_modules/`），之后 `npm run build`
  离线就能跑。
- 不需要配置任何 secret，发布用的是 Actions 内置的 `GITHUB_TOKEN`。

## 一、要不要发版

面向使用者的改动（主题样式、安装方式、README 里写的东西）就发一个版本；只动工具、工作流、
目录结构这类源码层面的事，提交到 main 就行，不必发版。

本仓库的版本号跟着变化的大小走，和语义化版本一致：修样式是补丁位（`1.2.0` → `1.2.1`），
加了能看出来的新样子是中版本位（`1.1.1` → `1.2.0`）。

## 二、动了 `src/` 就先编译

`theme.css` 是构建产物，但同时是发布物，必须和源码一起提交：

```bash
npm run build
```

忘了跑这一步，CI 的 `theme.css 与 src/ 编译结果一致` 会失败，release 也会被拦下来。

## 三、改版本号

四处必须是同一个值：

| 文件 | 要改的位置 |
| --- | --- |
| `package.json` | `version` |
| `package-lock.json` | 顶层的 `version` 与 `packages[""]` 里的 `version`，两处 |
| `manifest.json` | `version` |
| `versions.json` | 加一个 `"<版本>": "<manifest.minAppVersion>"`，放在**最前面** |

`package.json` 和 `package-lock.json` 这两处可以交给 npm 改：

```bash
npm version 1.2.1 --no-git-tag-version
```

`--no-git-tag-version` 是让它别顺手建 tag。剩下的 `manifest.json` 和 `versions.json` 手改，
`versions.json` 里的新键必须在最前面，否则 CI 的元数据检查会失败。

`minAppVersion` 没变的话就照抄上一条的值；这个键说明「这个版本最低要 Obsidian 多少」，
只有真的用到新 API 时才动它。

## 四、补 changelog

在 [`changelog.md`](changelog.md) 最上面插入新的一条，最新的版本永远在最上面：

```markdown
## 1.2.1 — 2026-09-23

一句话说这次改了什么。

- 要点一，面向使用者，说清楚哪里变了
- 要点二
```

题目用当天的日期。这条 entry 会被 release 工作流抓出来当 release 说明，所以写给人看，
别写成 commit message。

## 五、同步文档

- 改了样式，同步 [`customization.md`](customization.md)：改了什么、写在哪个文件、
  取值是多少。这份文档是「现在长这样是从哪来的」的答案。
- 改了安装方式或使用者能看到的说明，`README.md` 与 `README-zh.md` 两份一起改，内容要对得上。
- 改了工具、工作流、目录结构这类，写进 `customization.md`，不进 changelog。

## 六、发布前本地检查

```bash
npm run build && git diff --exit-code -- theme.css   # 产物与源码一致
! grep -rq "@settings" src/                          # 没有 Style Settings
```

顺手看一眼 `git status --short`，确认要提交的文件都对，`build/`、`node_modules/` 没有被带进来
（`.gitignore` 已经挡着）。

## 七、提交并推送

```bash
git add -A
git commit -m "doc: 发版 1.2.1：补 changelog 并同步四处版本号"
git push
```

推上去会触发 main 上的 Version check：编译一遍、比对 `theme.css`、检查 `src/` 里没有设置面板、
检查 `theme.css` 的完整性（无 BOM、花括号平衡、含主题名与 Baseline 版本），再对四处版本号与
`versions.json`。等它绿了再打 tag。

## 八、打 tag 发布

tag 去掉 `v` 必须等于 `manifest.json` 的 `version`，否则 release 工作流第一步就会失败。
先确认这个名字没用过：

```bash
git tag -l                       # 本地
git ls-remote --tags origin      # 远端
```

都没有的话：

```bash
git tag v1.2.1
git push origin v1.2.1
```

推 tag 这一下才真的发布。工作流会依次做这些事：校验 tag 与 `manifest.json` 的版本一致 →
`npm run build` → 确认 `theme.css` 与源码一致 → 打成 `obsidian-macos-<版本>.zip`（里面是
`obsidian-macos/theme.css` 与 `obsidian-macos/manifest.json`）→ 从 changelog 抓这一版的说明 →
建 release，上传 `theme.css`、`manifest.json` 和那个 zip。

## 九、验收

打开 <https://github.com/syxb2/obsidian-macos/releases> 看新那一页：说明应该是 changelog 里
那一段，附件有三个。命令行也行：

```bash
gh release view v1.2.1
```

顺手下一份 zip 解开确认结构是 `obsidian-macos/theme.css` + `obsidian-macos/manifest.json`，
手动安装的用户解压到 `.obsidian/themes/` 就能直接用。

## 出错了怎么办

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `tag v1.2.1 去掉 v 之后是 1.2.1，与 manifest.json 的 1.2.0 不一致` | 版本号没改全 | 补齐四处版本号，提交 push，再重新打 tag |
| `theme.css 与 src/ 的编译结果不一致` | 改了 `src/` 没重新编译 | 本地 `npm run build`，把 `theme.css` 一起提交 |
| `versions.json 最新的键是 …` | 新版本那条没放在最前面 | 提到最前面 |
| `gh release create` 报 403 / Resource not accessible | 仓库的 Workflow permissions 是只读 | 改成 Read and write，再重跑 |
| 工作流本身临时失败（网络、runner） | 与代码无关 | 在 Actions 页面 re-run 同一个 tag 的运行 |

工作流的发布那一步是幂等的：同一个 tag 上已经有 release 时，它会改成更新说明并覆盖上传产物，
不会因为「release 已存在」报错，所以放心重跑。

### 想把已经发出去的版本重做

改动落在 tag 之后的话，得把 tag 挪过去。顺序是先删 release 再删 tag，不然会留下一个指向
不存在 tag 的孤儿 release：

```bash
# 先在 GitHub 上删掉那个 release（Release 页面 → Delete）
git tag -d v1.2.1
git push origin :refs/tags/v1.2.1
# 改完、提交、push 之后重新打
git tag v1.2.1 && git push origin v1.2.1
```

只是想换个说明或者补个文件，就不用动 tag，重跑工作流或者直接编辑 release 都行。
