# 提取规则指南

> 从 PRD 和代码中提取实体和规则的详细指南

---

## 第一部分：从 PRD 提取产品实体

### 1.1 功能模块提取

**识别特征**:
- PRD 中第 2 章 "功能需求" 下的顶层章节
- 通常以 "## REQ-XXX: 模块名称" 或 "### 模块名称" 形式出现
- 包含多个功能点的集合

**提取内容**:
| 字段 | 来源 | 示例 |
|------|------|------|
| name | 章节标题 | 变更管理系统 |
| type | 固定值 | module |
| domain | 固定值 | product |
| content | 章节内容摘要 | 负责变更申请、审批、执行的系统 |

---

### 1.2 用户场景（Persona）提取

**识别特征**:
- PRD 第 1 章 "目标用户" 或 "用户场景"
- 表格形式，包含角色、职责、诉求

**提取内容**:
| 字段 | 来源 | 示例 |
|------|------|------|
| name | 角色名 | 安全工程师 |
| type | 固定值 | persona |
| content | 完整用户场景 | 描述+职责+诉求 |

---

### 1.3 业务规则提取

**识别特征**:
- 功能点下的 "业务规则" 表格
- 包含规则项、规则内容、备注三列

**提取内容**:
| 字段 | 来源 | 示例 |
|------|------|------|
| name | 规则项 | 审批权限 |
| type | 固定值 | rule |
| content | 完整规则定义 | 规则内容+备注 |

---

### 1.4 状态定义提取

**识别特征**:
- 功能点下的 "状态定义" 表格
- 包含状态、进入条件、离开条件、页面表现

**提取内容**:
| 字段 | 来源 | 示例 |
|------|------|------|
| name | 状态名 | 待审批 |
| type | 固定值 | state |
| content | 完整状态定义 | 进入/离开条件+页面表现 |

---

### 1.5 权限规则提取

**识别特征**:
- 功能点下的 "权限规则" 表格
- 包含角色、可见、可操作三列

**提取内容**:
| 字段 | 来源 | 示例 |
|------|------|------|
| name | 角色名 | 安全工程师 |
| type | 固定值 | permission |
| content | 完整权限定义 | 可见+可操作 |

---

### 1.6 工单类型提取（新增）

**识别特征**:
- 章节标题包含 "工单类型："
- 包含功能描述、是否在自服务目录展示、审批流程、执行信息等

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 工单类型名 | ticket_type:{工单类型名} |
| name | 工单类型名称 | 如：泳道新建、业务系统申请 |
| type | 固定值 | ticket_type |
| content | JSON 格式 | 完整工单类型定义 |

**content JSON 结构**:
```json
{
  "description": "新建泳道，无阻塞并行各个需求的测试",
  "in_catalog": true,
  "icon": "🏊‍♂️ 🆕",
  "card_style": "渐变浅色规范中循环",
  "title_format": "创建泳道环境申请工单:{泳道名称}",
  "execution_type": "自动/人工",
  "sections": ["基础信息", "流程日志", "组件变更信息", "中间件信息"]
}
```

---

### 1.7 审批流程提取（新增）

**识别特征**:
- 工单类型下的 "审批流程" 表格
- 包含顺序、审批节点、描述三列

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 工单类型+flow | approval_flow:{工单类型}:flow |
| name | 审批流程名称 | 如：业务系统申请审批流程 |
| type | 固定值 | approval_flow |
| content | JSON 格式 | 完整审批流程定义 |

**content JSON 结构**:
```json
{
  "ticket_type": "业务系统申请",
  "nodes": [
    {
      "sequence": 1,
      "name": "业务系统owner并签",
      "type": "parallel",
      "approver": "新建表单填写的业务系统owner",
      "condition": ""
    },
    {
      "sequence": 2,
      "name": "arch Review并签",
      "type": "parallel",
      "approver": "新建表单填写的架构师",
      "condition": ""
    }
  ]
}
```

**关系建立**:
- 工单类型 `has_approval_flow` 审批流程
- 审批流程 `contains` 审批节点（单独提取为 approval_node 类型）

---

### 1.8 审批节点提取（新增）

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 工单类型+node+序号 | approval_node:{工单类型}:node{序号} |
| name | 节点名称 | 如：业务系统owner并签 |
| type | 固定值 | approval_node |
| content | JSON 格式 | 节点定义 |

**content JSON 结构**:
```json
{
  "sequence": 1,
  "approval_type": "parallel/serial",
  "approver_role": "业务系统owner",
  "approver_source": "新建表单填写",
  "condition": "仅为digital tech时需要审批",
  "escalation": "离职由Harry.He@starbucks.cn审批"
}
```

---

### 1.9 表单字段提取（新增）

**识别特征**:
- 工单类型下的 "属性字段" 表格
- 包含字段名称、字段类型与范围、备注三列

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 工单类型+字段名 | form_field:{工单类型}:{字段名} |
| name | 字段名称 | 如：工单名称、业务系统名称 |
| type | 固定值 | form_field |
| content | JSON 格式 | 完整字段定义 |

**content JSON 结构**:
```json
{
  "ticket_type": "泳道新建",
  "field_name": "泳道名称",
  "field_type": "单行文本",
  "required": true,
  "validation": "必填，限制为英文",
  "auto_generate": false,
  "default_value": "",
  "order": 1,
  "section": "基础信息"
}
```

---

### 1.10 通知模板提取（新增）

**识别特征**:
- "工单通知规则" 章节下的表格
- 包含触发条件、渠道、目标用户、标题、内容

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 触发状态+notification | notification:{触发状态}:notification |
| name | 通知名称 | 如：待执行通知 |
| type | 固定值 | notification |
| content | JSON 格式 | 完整通知定义 |

**content JSON 结构**:
```json
{
  "trigger": "待执行",
  "channel": "邮件",
  "target_user": "工单执行人（具体用户/用户组/用户组轮流的当前用户）",
  "title_template": "{工单标题} 你有待执行的工单",
  "content_template": "{工单标题} 你有待执行的工单，请及时处理。<br>{工单待我处理的链接}"
}
```

---

### 1.11 派生流程提取（新增）

**识别特征**:
- 工单类型下的 "派生流程" 描述
- 包含多批次派生工单的说明

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 父工单类型+派生类型 | derived_process:{父工单类型}:{派生类型} |
| name | 派生流程名称 | 如：证书申请派生 |
| type | 固定值 | derived_process |
| content | JSON 格式 | 完整派生流程定义 |

**content JSON 结构**:
```json
{
  "parent_ticket_type": "业务系统变更",
  "batch": 2,
  "derived_types": ["内网证书申请", "外网证书申请"],
  "description": "包含多批次派生工单：批次1-业务系统变更；批次2-证书申请；批次3-证书安装及删除工单"
}
```

---

### 1.12 页面结构提取（新增）

**识别特征**:
- 信息架构图中的页面层级
- 各页面类型的详细结构说明

**提取内容**:
| 字段 | 来源 | 存储格式 |
|------|------|----------|
| id | 页面名+structure | page_structure:{页面名}:structure |
| name | 页面结构名称 | 如：工单列表页结构 |
| type | 固定值 | page_structure |
| content | JSON/YAML 格式 | 完整页面结构定义 |

**content JSON 结构（参考 page-structure-schema.md）**:
```json
{
  "page_name": "工单列表页",
  "page_type": "list",
  "header": {
    "title": "工单列表",
    "filters": [
      {"field": "工单类型", "label": "类型"},
      {"field": "创建时间", "label": "时间范围"}
    ],
    "actions": ["新建工单"]
  },
  "list": {
    "columns": ["工单ID", "工单名称", "状态", "创建时间", "申请人", "工单类型"],
    "row_actions": ["查看", "编辑"]
  }
}
```

---

## 第二部分：从代码提取规则

### 2.1 权限规则提取

**代码特征**:
- `@PreAuthorize` 注解
- `if (user.hasRole(...))` 或 `if (!user.hasRole(...))`
- `checkPermission()` 等方法调用

**提取示例**:
```java
@PreAuthorize("hasRole('APPROVER')")
public void approveTicket(Long ticketId) { ... }
```

提取:
- id: code:TicketService:approveTicket:permission
- name: 工单审批权限
- type: permission (code domain)
- content: 只有角色 APPROVER 能执行 approveTicket 操作
- source_file: TicketService.java
- source_type: commit

---

### 2.2 状态规则提取

**代码特征**:
- 状态机定义（StateMachine、StatePattern）
- 状态转换方法
- 状态字段赋值

**提取示例**:
```java
public void approve() {
    if (this.status != Status.PENDING) {
        throw new IllegalStateException("只能审批待处理状态的工单");
    }
    this.status = Status.APPROVED;
}
```

提取:
- id: code:Ticket:approve:state
- name: 工单审批状态流转
- type: state (code domain)
- content: 从 PENDING 到 APPROVED，触发条件：approve 操作
- source_file: Ticket.java

---

### 2.3 前置条件提取

**代码特征**:
- `if (condition) throw new ...Exception()`
- 参数校验（@Valid、@NotNull）
- 业务校验方法

**提取示例**:
```java
public void createOrder(OrderRequest request) {
    if (request.getAmount() <= 0) {
        throw new ValidationException("订单金额必须大于0");
    }
    if (request.getItems().isEmpty()) {
        throw new ValidationException("订单必须包含商品");
    }
    // ...
}
```

提取:
- id: code:OrderService:createOrder:precondition
- name: 创建订单前置条件
- type: rule (code domain)
- content: 1) 订单金额必须大于0；2) 订单必须包含商品
- source_file: OrderService.java

---

### 2.4 数据校验规则提取

**代码特征**:
- `@Valid`、`@Validated` 注解
- Bean Validation 注解（@NotNull、@Size、@Min、@Max）
- 自定义校验器

**提取示例**:
```java
public class TicketRequest {
    @NotNull(message = "工单标题不能为空")
    private String title;
    
    @Size(max = 1000, message = "描述不能超过1000字")
    private String description;
    
    @Min(value = 1, message = "优先级必须大于等于1")
    @Max(value = 5, message = "优先级必须小于等于5")
    private Integer priority;
}
```

提取:
- id: code:TicketRequest:validation
- name: 工单请求校验规则
- type: rule (code domain)
- content: 1) 工单标题不能为空；2) 描述不能超过1000字；3) 优先级范围1-5
- source_file: TicketRequest.java

---

### 2.5 业务约束提取

**代码特征**:
- 计数限制（count、size 检查）
- 频率限制（RateLimiter）
- 时间窗口限制

**提取示例**:
```java
public void submitRequest(User user) {
    // 每人每天最多申请3次
    int todayCount = requestRepo.countByUserAndDate(user, today);
    if (todayCount >= 3) {
        throw new LimitExceededException("每人每天最多申请3次");
    }
    // ...
}
```

提取:
- id: code:RequestService:submitRequest:constraint
- name: 申请频次限制
- type: rule (code domain)
- content: 每人每天最多申请3次
- source_file: RequestService.java

---

### 2.6 API 定义提取

**代码特征**:
- `@RequestMapping`、`@GetMapping`、`@PostMapping` 等
- OpenAPI/Swagger 注解
- 方法签名（参数+返回值）

**提取示例**:
```java
@RestController
@RequestMapping("/api/v1/tickets")
public class TicketController {
    
    @PostMapping
    public ResponseEntity<Ticket> createTicket(@RequestBody TicketRequest request) {
        // ...
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Ticket> getTicket(@PathVariable Long id) {
        // ...
    }
}
```

提取:
- id: api:ticket-service:POST:/api/v1/tickets
- name: POST /api/v1/tickets
- type: api
- content: 创建工单；参数：TicketRequest；返回：Ticket
- source_file: TicketController.java

---

## 第三部分：规则匹配策略

### 3.1 精确匹配

当代码规则和产品规则完全对应时：

```
产品规则: "只有审批人能审批工单"
代码规则: "if (!user.hasRole("APPROVER")) throw..."

关系: validates (代码验证了产品规则)
置信度: 0.95
```

### 3.2 模糊匹配

当代码规则和产品规则语义相近但表述不同时：

```
产品规则: "工单金额必须大于0"
代码规则: "if (request.getAmount() <= 0) throw..."

关系: validates
置信度: 0.85
备注: 需要确认金额单位（元/分）
```

### 3.3 孤儿规则

当代码规则没有对应的产品规则时：

```
代码规则: "每人每天最多申请3次"
产品规则: [无匹配]

关系: orphan
建议: 在产品文档中补充该规则
```

### 3.4 冲突检测

当代码规则与产品规则矛盾时：

```
产品规则: "只有审批人能审批工单"
代码规则: "if (!user.hasRole("ADMIN")) throw..."

关系: conflicts
冲突类型: PERMISSION_MISMATCH
详情: 角色不一致（审批人 vs 管理员）
建议: 请确认正确规则并更新 PRD 或代码
```

---

## 第四部分：冲突类型定义

| 冲突类型 | 说明 | 示例 |
|---------|------|------|
| PERMISSION_MISMATCH | 权限角色不一致 | 审批人 vs 管理员 |
| VALUE_MISMATCH | 数值不一致 | 100条 vs 1000条 |
| STATE_MISMATCH | 状态定义不一致 | 待审批 vs 待处理 |
| RULE_MISSING | 产品规则缺失 | 代码有校验，产品文档未说明 |
| RULE_WEAKENED | 规则被弱化 | 删除了原有校验 |
| RULE_VIOLATED | 规则被违反 | 代码逻辑与产品规则矛盾 |
| FIELD_MISMATCH | 表单字段不一致 | 字段类型/必填状态变化 |
| FLOW_MISMATCH | 审批流程不一致 | 节点顺序/审批人变化 |
