---
name: publish-iteration-doc
description: 把迭代 sprint 产出（PRD + HTML 原型）发布到 product-doc Docusaurus 文档站。Use when user says '发布到文档', '按 runbook 新增文档', '把 PRD 发到文档站', 'publish iteration doc', 或在迭代会话中给出 sprint 目录路径要求发布。
---

# 发布迭代文档到 product-doc 文档站

## 概述

将一个产品迭代的产出物（`11-prd-*.md` + `flow-demo.html`）发布到 Docusaurus 文档站 **product-doc**，使其出现在对应系统的迭代目录下，并内嵌 HTML 原型预览。

## 输入

用户会给出一个 sprint 源目录，两种常见形式：

1. IDP-PD 仓库中的 sprint 目录，如 `/Users/jiajchen/Documents/GitHub/IDP-PD/sprint/202610,接入审批通知渠道配置`
2. 已复制到 product-doc 的 `temp/` 下的目录，如 `product-doc/temp/202609,支持PSP填写非标准工作日工时/`

源目录中通常包含：
- `11-prd-*.md` — PRD 正文（文档主体）
- `flow-demo.html`（或 `<feature>-demo.html`）— 单文件交互原型
- 其他阶段文档（`00-context.md` 等）— **不需要发布**

## 关键路径

| 项 | 路径 |
|---|---|
| 文档站仓库 | `/Users/jiajchen/Documents/GitHub/product-doc` |
| 文档目录 | `product-doc/docs/<system>/iteration-YYYY-MM/` |
| 原型目录 | `product-doc/static/img/prototypes/<system>/<proto-id>/` |

`<system>` 通常是 `idp`（IDP 平台需求）或 `worktime`（工时需求）。已注册模块见 `product-doc/src/config/docModules.ts`。

## 发布步骤

### 1. 读取源文件

- 读 `11-prd-*.md` 全文，作为文档正文。
- 检查 HTML 是否引用本地资源：
  ```bash
  grep -n 'src=\|href=' <sprint>/flow-demo.html | grep -v http
  ```
  若有 `<img src="pic/xxx.png">`、`icons_svg/xxx.svg` 等本地引用，对应资源目录必须与 HTML 一起复制（保持同级相对路径，不改 HTML）。内联 `<use href="#i-xxx">` 是文件内部 SVG 引用，不算本地资源。

### 2. 确定迭代目录与编号

- 迭代月份从 sprint 目录名提取（`202610,xxx` → `2026-10`）。
- 查看已有迭代确定 `_category_.json` 的 position（在最近一个迭代的 position 上加 1）：
  ```bash
  for d in docs/<system>/iteration-*/; do echo "$d: $(cat $d/_category_.json)"; done
  ```
- 若迭代目录不存在，创建 `_category_.json`：
  ```json
  {
    "label": "2026-10 需求迭代",
    "position": 9,
    "link": {
      "type": "generated-index",
      "title": "2026-10 需求迭代",
      "description": "这里放 2026-10 迭代的需求文档。"
    }
  }
  ```

### 3. 复制 HTML 原型

原型目录命名规则：**小写 `<system>-0<NN>-<slug>`**，NN 取现有最大编号 + 1。先查看现有编号：

```bash
ls static/img/prototypes/idp/
# 示例输出：... idp-019-ai-agent-nav-restructure
# → 新目录为 idp-020-approval-channel-config
```

```bash
mkdir -p static/img/prototypes/idp/idp-0NN-slug
cp <sprint>/flow-demo.html static/img/prototypes/idp/idp-0NN-slug/
# 如有本地资源目录（pic/、icons_svg/ 等）一并复制到同级
```

注意：早期目录有 `IDP-004` 这种大写命名，**新目录一律用小写 `idp-0NN-slug` 格式**。

### 4. 创建文档文件

文件名：`YYYY-MM-<slug>.mdx`（有 HTML 原型必用 `.mdx`），如 `2026-10-approval-channel-config.mdx`。同一迭代已有文档时，`sidebar_position` 顺延。

结构模板：

```mdx
---
sidebar_position: 1
title: 2026-10 接入审批通知渠道配置
description: 一两句话概括本需求要点（用于 SEO/列表展示）。
---

# 2026-10 接入审批通知渠道配置

## HTML 原型预览

<HtmlPreview
  title="接入审批通知渠道配置原型"
  path="/img/prototypes/idp/idp-0NN-slug/flow-demo.html"
  height={900}
/>

## 1. 文档信息

- 文档版本：v1.1（取自 PRD 头部）
- 更新时间：YYYY-MM-DD

## 2. 项目背景
...（以下为 PRD 正文）
```

要点：
- `<HtmlPreview>` 已全局注册，无需 import。
- `path` 以 `/img/prototypes/` 开头，**不含** `static`。
- PRD 正文原样保留；若在正文前插入了「文档信息」章节，后续章节编号顺延，并同步修正正文内的交叉引用（如「见 2.6」→「见 3.6」）。
- PRD 开头的 `> 版本：...` 引用块信息提取到「文档信息」章节，不重复保留。

### 5. MDX 转义检查

- 正文中的 `{...}` 表达式必须转义为 `{'{...}'}`，除非位于行内代码或代码块中（代码内安全，如 `` `{channelCode}` `` 无需处理）。
- 独立的 `<` 后跟字母会被当作 JSX 标签，需改为 `&lt;`；`< 5 分钟`（后跟空格/数字）通常安全，但保险起见也可转义。
- 表格单元格内的 `|` 需转义为 `\|`。

### 6. 验证构建

在 product-doc 根目录运行：

```bash
yarn build
```

`onBrokenLinks` 为 `throw`，任何 MDX 错误或死链都会使构建失败。失败则修复后重跑。

### 7. 启动本地服务供验收

```bash
lsof -ti :3000 | xargs kill 2>/dev/null   # 先清掉旧服务，避免端口冲突
yarn start --no-open                      # 后台运行
```

启动后用 curl 确认文档页返回 200：

```
http://localhost:3000/product-doc/<system>/iteration-YYYY-MM/YYYY-MM-slug
```

向用户报告验收地址，**等待用户确认验收通过后再提交**。开发服务器跑在后台任务里，超时被自动停止属正常现象，不影响产出。

### 8. 验收通过后拆分提交

```bash
git add docs/<system>/iteration-YYYY-MM/ && git commit -m "新增 YYYY-MM <需求名>需求文档"
git add static/img/prototypes/<system>/<proto-id>/ && git commit -m "新增 YYYY-MM <需求名>原型 flow-demo.html"
```

- 顺序：先 `docs/` 文档正文，再 `static/` 原型。
- **不要 push**。提交完成后提醒用户：`git push origin main`。
- 若用户 push 报认证失败：远程是内部 GHE（`scm.starbucks.com`），终端通常无凭证，引导用户在 GitHub Desktop → Settings → Accounts 重新登录 GitHub Enterprise。

## 快速检查清单

- [ ] 已读取 sprint 源目录的 `11-prd-*.md` 和 HTML
- [ ] 已检查并复制 HTML 引用的本地资源（如有）
- [ ] 迭代目录与 `_category_.json` 就位，position 递增
- [ ] 原型复制到 `static/img/prototypes/<system>/<idp-0NN-slug>/`，编号取现有最大 +1
- [ ] mdx 命名 `YYYY-MM-slug.mdx`，含 frontmatter 与 `<HtmlPreview>`
- [ ] `path` 为 `/img/prototypes/...` 格式（不含 static）
- [ ] MDX 花括号/小于号已处理，章节交叉引用已同步
- [ ] `yarn build` 通过
- [ ] 本地服务已启动，文档页 curl 返回 200，已报告验收地址
- [ ] 用户验收通过后拆分提交（docs 先、static 后），未 push，已提醒 push
