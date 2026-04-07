---
name: ux-init
description: 初始化与阶段推进 - 项目初始化，生成流程状态文档
license: MIT
compatibility: Starting phase, no prior files required
metadata:
  author: ux-workflow
  version: "1.0"
  workflow: user-centric-design
  phase: "init"
---

## 什么时候使用

产品设计流程的起始阶段，或需要初始化新项目时使用此 skill。

## 目标

分析用户提供的输入信息，初始化项目并生成流程状态文档。

## 核心功能

### 1. 输入分析

用户可以提供以下类型的信息：

| 类型 | 说明 | 示例 |
|------|------|------|
| 痛点描述 | 用户遇到的问题 | "团队成员经常错过需求评审会议" |
| 背景文档 | 现有项目背景信息 | 产品文档、技术文档 |
| 用户故事 | 已定义的用户需求 | "作为产品经理，我想..." |
| MVP 范围 | 已确定的最小可行产品 | "第一版只做需求收集和提醒" |
| 原型/PRD | 已完成的设计产出 | 设计稿链接、PRD 文档 |

### 2. 文件检测

检查 `input/` 目录下的文件：

```bash
ls -la input/
```

常见输入文件：
- `projectBrief.md` - 项目简要
- `context.md` - 上下文文档
- `page-structure-schema.md` - 页面结构 Schema 定义（推荐，可提升 Demo 质量）
- `user-stories.md` - 用户故事
- `mvp-scope.md` - MVP 范围
- `flow-status.md` - 流程状态文档（如已存在）
- `*.md` - 其他背景文档

> 💡 **提示**：`page-structure-schema.md` 可从 `latest/ux-page-structure/page-structure-schema.md` 复制，提供此文档可显著提升 Demo 和原型生成质量。

### 3. 项目初始化

#### 3.1 检查现有流程状态文档

```bash
ls -la input/flow-status.md
```

#### 3.2 如不存在，创建新的流程状态文档

- 使用 `flow-status-template.md` 作为模板（与 SKILL.md 同目录）
- 填充项目名称（询问用户或从上下文推断）
- 记录创建时间
- 设置当前阶段为"未开始"

#### 3.3 如已存在，读取并确认

- 读取 `input/flow-status.md`
- 确认项目名称和当前状态

### 4. 上下文补充引导

如果没有足够背景信息，引导用户补充：

```
建议提供的信息：
1. 产品文档：信息模块结构、各功能模块的功能规则描述
2. 页面结构文档（page-structure-schema.md）：定义页面类型和结构，可显著提升 Demo 和原型生成质量
3. 相关方文档：各相关方的角色、关心内容、需求、话语权
4. 本次想要调研的问题或原始诉求列表
```

**关于页面结构文档**：
- 如果没有，可从 `latest/ux-page-structure/page-structure-schema.md` 复制标准模板
- 如有已定义的产品页面结构，可放在 `input/[product]-page-structures.md`

### 5. 引导到 ux_flow

初始化完成后，提示用户调用 ux_flow 来确定下一步：

```bash
/ux:flow
```

---

## 输出

- 已创建/更新的 `input/flow-status.md`
- 项目初始化完成提示
- 下一步建议（调用 /ux:flow）

---

## 阶段对照表

| 阶段 | Skill | 说明 |
|------|-------|------|
| 问题锚定 | ux-phase0-anchor | 半天内对齐问题方向 |
| 上下文补充 | ux-phase1-context | 收集组织背景、技术栈 |
| 方案研究 | ux-phase2-research | 用户故事 + 业界方案调研 |
| 对抗式 Synthesis | ux-phase3-synthesis | 多 Agent 对抗 |
| MVP 划定 | ux-phase4-mvp | Must-have 筛选 |
| 用户旅程设计 | ux-phase5-user-journey | 完整用户旅程 |
| 流程演示 Demo | ux-phase6-demo | 可交互原型 |
| 项目章程 | ux-phase7-project-goal | 渐进式规则 |
| 规则详细设计 | ux-phase8-rules | 复杂功能点详细规则 |
| 易用性检查 | ux-phase9-usability-check | 易用性清单 |
| 拆分设计任务 | ux-phase10-design-task-split | 按旅程拆分任务 |
| 执行设计任务 | ux-phase10-design-task-execute | 循环执行设计 |
| PRD 生成 | ux-phase11-prd | 面向研发 |
| 项目收尾 | ux-context-update_after_design_finish | 更新 context |

## 下一步

初始化完成后，引导用户调用 `/ux:flow` 来确定项目的具体阶段和下一步行动。