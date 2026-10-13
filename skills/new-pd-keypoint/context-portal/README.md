# Context Portal Skill

活的上下文系统 - 产品 & 代码双轨上下文管理

---

## 概述

Context Portal 是一个产品上下文与代码规则的双轨管理系统，建立产品规则与代码规则之间的桥梁，确保"应该是什么"与"实际是什么"保持一致。

## 核心能力

| 能力 | 说明 |
|------|------|
| **产品规则建立** | 从 PRD 提取功能、规则、用户故事 |
| **产品规则更新** | 基于新 PRD 增量更新上下文 |
| **代码规则提取** | 从代码提取隐式业务规则 |
| **一致性检查** | 比对代码规则 vs 产品规则 |
| **产品影响分析** | 代码变更影响哪些产品功能 |

## 四大流程

### 1. 产品上下文冷启动
```
/product-context:init --path ./docs/prd/
```
从历史 PRD 文档初始化产品上下文数据库。

### 2. 产品上下文更新
```
/product-context:update --change new-prd.md
```
基于新 PRD/变更文档更新产品上下文。

### 3. 代码规则提取
```
/code-context:init --repo ./my-service
```
从代码仓库提取业务规则并与产品规则建立映射。

### 4. 一致性检查
```
/context:check-consistency --staged
```
检查代码变更是否与产品规则冲突。

## 文件结构

```
context-portal/
├── SKILL.md                      # Skill 主文档
├── README.md                     # 本文件
├── references/
│   ├── data-model.md            # 数据模型详细定义
│   ├── extraction-rules.md      # 提取规则指南
│   ├── output-templates.md      # 输出模板
│   └── workflow-guide.md        # 工作流指南
└── scripts/
    └── db_manager.py            # 数据库管理脚本
```

## 数据模型

核心表结构：
- **entities**: 存储产品实体和代码实体
- **relations**: 存储实体间关系（implements, validates, conflicts, orphan）
- **versions**: 版本历史
- **chunks**: 文本分块（用于检索）

## 输出文档

| 文档 | 说明 |
|------|------|
| product-context-YYYY-MM-DD.md | 产品上下文文档 |
| code-rules-YYYY-MM-DD.md | 代码规则清单 |
| rule-mapping-report.md | 规则映射报告 |
| consistency-check-report.md | 一致性检查报告 |
| impact-analysis-report.md | 产品影响分析报告 |
| orphaned-rules.md | 孤儿规则清单 |

## 使用示例

### 场景 1: 新项目初始化

```bash
# 从历史 PRD 初始化产品上下文
/product-context:init --path ./docs/prd/ --output ./context/

# 从代码仓库提取规则
/code-context:init --repo ./src/ --output ./context/
```

### 场景 2: 迭代更新

```bash
# 基于新 PRD 更新产品上下文
/product-context:update --change prd-v2.0.md --iteration Sprint-25
```

### 场景 3: 提交前检查

```bash
# 检查 staged 变更
/context:check-consistency --staged

# 查看产品影响
/context:analyze-impact --since HEAD~1
```

### 场景 4: 查询上下文

```bash
# 查询产品上下文
/product-context:query "工单有哪些状态"

# 影响分析
/product-context:query --entity "泳道管理" --impact
```

## 数据库脚本

```bash
# 初始化数据库
python scripts/db_manager.py --db context.db --init

# 查看统计
python scripts/db_manager.py --db context.db --stats

# 搜索实体
python scripts/db_manager.py --db context.db --search "审批权限"

# 查看冲突
python scripts/db_manager.py --db context.db --conflicts

# 查看孤儿规则
python scripts/db_manager.py --db context.db --orphans
```

## 参考文档

- [数据模型](references/data-model.md) - 详细的 SQLite Schema
- [提取规则](references/extraction-rules.md) - PRD 和代码提取规则
- [工作流指南](references/workflow-guide.md) - 四大流程详细步骤
- [输出模板](references/output-templates.md) - 标准化输出格式

## 相关 Skill

- `ux-phase1-context` - Phase 1: 上下文收集
- `ux-context-update-after-design-finish` - 产品设计完成后的上下文更新
