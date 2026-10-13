# Context Portal 输出模板

> 标准化输出文档格式

---

## 1. Product Context 模板

**文件名**: `product-context-YYYY-MM-DD.md`

```markdown
# 产品上下文

> 版本：{version} | 更新日期：{date}

---

## 目录

- [1. 信息架构图](#1-信息架构图)
- [2. 功能模块](#2-功能模块)
  - [2.1 {模块名}](#21-{模块名})
  - [2.2 {模块名}](#22-{模块名})
- [3. 其他信息](#3-其他信息)
  - [3.1 技术栈](#31-技术栈)
  - [3.2 约束条件](#32-约束条件)

---

## 1. 信息架构图

```
{系统名称}
├── {模块A}
│   ├── {子模块A1}
│   └── {子模块A2}
└── {模块B}
    └── {子模块B1}
```

---

## 2. 功能模块

### 2.1 {模块名称}

#### 用户场景

| 角色 | 描述 | 职责 | 核心诉求 |
|------|------|------|----------|
| {角色} | {描述} | {职责} | {诉求} |

#### 功能点与规则

##### {功能点名称}

**功能描述**
{一句话描述}

**状态定义**
| 状态 | 进入条件 | 离开条件 | 页面表现 |
|------|---------|---------|----------|
| {状态} | {条件} | {条件} | {显示} |

**权限规则**
| 角色 | 可见 | 可操作 |
|------|------|--------|
| {角色} | {是/否} | {操作} |

**业务规则**
| 规则项 | 规则内容 | 备注 |
|-------|---------|------|
| {规则} | {内容} | {备注} |

---

## 3. 其他信息

### 3.1 技术栈

| 维度 | 技术/工具 | 说明 |
|------|----------|------|
| {维度} | {技术} | {说明} |

### 3.2 约束条件

| 类型 | 内容 | 说明 |
|------|------|------|
| {类型} | {内容} | {说明} |
```

---

## 2. Code Rules 模板

**文件名**: `code-rules-YYYY-MM-DD.md`

```markdown
# 代码规则清单

> 生成日期：{date}
> 代码仓库：{repo_path}

---

## 统计概览

| 规则类型 | 数量 |
|---------|------|
| 权限规则 | {count} |
| 状态规则 | {count} |
| 前置条件 | {count} |
| 后置条件 | {count} |
| 数据校验 | {count} |
| 业务约束 | {count} |
| **总计** | **{total}** |

---

## 1. 权限规则

### {规则名称}

| 属性 | 值 |
|------|-----|
| 规则 ID | {id} |
| 代码位置 | {file}:{line} |
| 关联产品规则 | {product_rule_id} |
| 置信度 | {confidence} |

**代码片段**
```{language}
{code_snippet}
```

**提取的规则**
{rule_description}

---

## 2. 状态规则

### {规则名称}

| 属性 | 值 |
|------|-----|
| 规则 ID | {id} |
| 代码位置 | {file}:{line} |
| 关联产品规则 | {product_rule_id} |
| 置信度 | {confidence} |

**状态流转**
```
{from_state} --{action}--> {to_state}
```

**代码片段**
```{language}
{code_snippet}
```

---

## 3. 数据校验规则

...
```

---

## 3. Rule Mapping Report 模板

**文件名**: `rule-mapping-report.md`

```markdown
# 规则映射报告

> 生成日期：{date}

---

## 统计概览

| 映射状态 | 数量 | 占比 |
|---------|------|------|
| ✅ 已匹配 (validates) | {count} | {percentage} |
| ⚠️ 孤儿规则 (orphan) | {count} | {percentage} |
| ❌ 冲突 (conflicts) | {count} | {percentage} |
| **总计** | **{total}** | 100% |

---

## ✅ 已匹配规则

### {产品规则名称} ↔ {代码规则名称}

| 属性 | 产品规则 | 代码规则 |
|------|---------|---------|
| ID | {product_id} | {code_id} |
| 内容 | {product_content} | {code_content} |
| 来源 | {product_source} | {code_source} |

**置信度**: {confidence}
**关系类型**: validates

---

## ⚠️ 孤儿规则（建议补充到产品文档）

### {代码规则名称}

| 属性 | 值 |
|------|-----|
| ID | {code_id} |
| 类型 | {rule_type} |
| 代码位置 | {file}:{line} |
| 描述 | {description} |

**建议操作**: 在 PRD 中补充此规则的定义

---

## ❌ 冲突规则

### {产品规则名称} vs {代码规则名称}

| 属性 | 产品规则 | 代码规则 |
|------|---------|---------|
| ID | {product_id} | {code_id} |
| 内容 | {product_content} | {code_content} |

**冲突类型**: {conflict_type}
**冲突详情**: {conflict_detail}
**建议操作**: {suggestion}
```

---

## 4. Consistency Check Report 模板

**文件名**: `consistency-check-report-YYYY-MM-DD.md`

```markdown
# 一致性检查报告

> 检查日期：{date}
> 检查范围：{commit_range}

---

## 执行摘要

| 检查项 | 结果 | 数量 |
|--------|------|------|
| 规则冲突 | {status} | {count} |
| 规则弱化 | {status} | {count} |
| 孤儿规则 | {status} | {count} |
| **总体状态** | **{overall_status}** | - |

---

## 详细结果

### ❌ 规则冲突

#### 冲突 #{number}

**产品规则**
- ID: {product_rule_id}
- 内容: {product_rule_content}
- 来源: {product_source}

**代码规则（变更后）**
- ID: {code_rule_id}
- 内容: {code_rule_content}
- 位置: {file}:{line}

**冲突分析**
| 维度 | 产品规则 | 代码规则 | 差异 |
|------|---------|---------|------|
| {dimension} | {value1} | {value2} | {diff} |

**建议操作**
- 选项 A: {option_a}
- 选项 B: {option_b}

---

### ⚠️ 规则弱化警告

#### 警告 #{number}

**变更前**
- {old_rule}

**变更后**
- {new_rule}

**风险**: {risk_description}

**建议**: {suggestion}

---

### ℹ️ 孤儿规则

#### 规则 #{number}

- ID: {rule_id}
- 类型: {rule_type}
- 位置: {file}:{line}
- 描述: {description}

**建议**: 确认此规则是否应补充到产品文档

---

## 行动清单

- [ ] {action_item_1}
- [ ] {action_item_2}
- [ ] {action_item_3}
```

---

## 5. Impact Analysis Report 模板

**文件名**: `impact-analysis-report-YYYY-MM-DD.md`

```markdown
# 产品影响分析报告

> 分析日期：{date}
> 变更范围：{commit_range}

---

## 变更摘要

| 属性 | 值 |
|------|-----|
| 变更文件数 | {count} |
| 新增代码规则 | {count} |
| 修改代码规则 | {count} |
| 删除代码规则 | {count} |

---

## 影响分析

### 1. 功能影响

#### 直接影响

| 功能 | 影响程度 | 说明 |
|------|---------|------|
| {feature} | {high/medium/low} | {description} |

#### 间接影响

| 功能 | 依赖关系 | 影响说明 |
|------|---------|----------|
| {feature} | {depends_on} | {description} |

---

### 2. 用户场景影响

#### 受影响角色

| 角色 | 影响场景 | 影响类型 |
|------|---------|----------|
| {persona} | {scenario} | {positive/negative/neutral} |

#### 业务流程变化

```
变更前: {old_flow}
变更后: {new_flow}
```

---

### 3. 依赖功能影响

#### 上游依赖

| 功能 | 依赖方式 | 是否需要同步变更 |
|------|---------|-----------------|
| {feature} | {dependency_type} | {yes/no} |

#### 下游依赖

| 功能 | 被依赖方式 | 是否需要回归测试 |
|------|-----------|-----------------|
| {feature} | {dependency_type} | {yes/no} |

---

### 4. 测试覆盖建议

#### 新增测试场景

- [ ] {test_scenario_1}
- [ ] {test_scenario_2}

#### 回归测试范围

- [ ] {regression_test_1}
- [ ] {regression_test_2}

#### 边界条件测试

- [ ] {boundary_test_1}
- [ ] {boundary_test_2}

---

## 风险评估

| 风险项 | 等级 | 说明 | 缓解措施 |
|--------|------|------|----------|
| {risk} | {high/medium/low} | {description} | {mitigation} |

---

## 建议操作

1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}
```

---

## 6. Orphaned Rules 模板

**文件名**: `orphaned-rules-YYYY-MM-DD.md`

```markdown
# 孤儿规则清单（建议补充到产品文档）

> 生成日期：{date}
> 代码仓库：{repo_path}

---

## 说明

以下规则是从代码中提取的，但在产品文档（PRD）中没有对应的定义。
建议产品经理审查这些规则，决定是否需要在 PRD 中补充。

---

## 规则列表

### 1. {规则名称}

| 属性 | 值 |
|------|-----|
| 规则类型 | {type} |
| 代码位置 | {file}:{line} |
| 所属服务 | {service} |

**代码片段**
```{language}
{code_snippet}
```

**提取的规则描述**
{description}

**建议补充到 PRD 的位置**
- 建议章节: {suggested_section}
- 建议格式: {suggested_format}

**建议内容**
```markdown
### {规则名称}

**业务规则**
| 规则项 | 规则内容 | 备注 |
|-------|---------|------|
| {name} | {content} | 从代码提取 |
```

---

## 快速操作

将这些规则补充到 PRD 后，重新运行：
```bash
/product-context:update --change updated-prd.md
```
```
