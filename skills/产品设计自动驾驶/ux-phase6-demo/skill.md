---

name: ux-phase6-flow-demo
description: 以用户为中心设计工作流 流程演示 Demo - 流程演示 Demo 生成。基于用户旅程文档，生成可交互的 HTML 页面，用于验证用户操作流程是否符合预期。
license: MIT
compatibility: Requires 05-user-journey.md from 用户旅程设计
metadata:
  author: ux-workflow
  version: "1.0"
  workflow: user-centric-design
  phase: "6"
  tags:
    - Flow Demo
    - Interactive Prototype
    - User Journey Verification
    - HTML Prototype
  input_files:
    - 05-user-journey.md (必需)
    - 04-mvp-scope.md (可选)
    - page-structure-schema.md (推荐)
  output_files:
    - flow-demo.html (可交互的 HTML 页面)

---

# 流程演示 Demo：流程演示 Demo 生成（Flow Demo Generation）

## 阶段目标

基于用户旅程文档，生成可交互的 HTML 原型页面，用于：
1. **验证流程** - 确认用户操作路径是否符合预期
2. **发现遗漏** - 识别用户旅程中的断点或缺失步骤
3. **快速迭代** - 在投入开发前低成本验证产品方向

## 核心原则

> **流程优先** - 不关注视觉样式，重点验证操作路径和页面跳转逻辑  
> **交互真实** - 点击、跳转、弹窗等交互必须真实可操作  
> **数据驱动** - 用户旅程中的每个步骤必须真实映射到 Demo 中  
> **快速产出** - 最小化 HTML 结构，最大化验证效率  

## 输入与输出

| 类型 | 文件 | 说明 |
|------|------|------|
| **输入 (必需)** | `05-user-journey.md` | 用户旅程设计 产出，包含完整的用户旅程和页面结构图 |
| **输入 (可选)** | `04-mvp-scope.md` | MVP 划定 产出，包含 MVP 功能清单 |
| **输入 (推荐)** | `page-structure-schema.md` | 页面结构 Schema 定义 |
| **输出** | `flow-demo.html` | 可交互的 HTML 原型页面 |

---

## 执行流程

### 步骤 1：读取并解析用户旅程文档

**1.1** 读取 `05-user-journey.md`

如果文件不存在，提示用户先运行 `/ux:phase5-user-journey`。

从文档中提取：
- Persona 列表
- 每个 Persona × 场景的用户旅程表格
- 关键触点信息（核心触点、决策点、等待点、跳出点）
- 功能模块结构图

**1.2** 读取 `04-mvp-scope.md`（如存在）

提取：
- MVP 核心目标
- Must-have 功能列表
- 成功指标（用于理解验证重点）

**1.3** 读取 `05-user-journey.md` 中的 Part 3：页面结构图

提取：
- 每个页面的结构图（当前 vs 目标）
- 页面类型（列表页/表单页/详情页/弹窗等）
- 页面区域划分和组件层级
- 新增/修改/删除的区域标注

> 💡 **重要**：Demo 的页面布局和组件结构应严格遵循页面结构图中的定义。

---

### 步骤 2：规划 Demo 结构

根据用户旅程，规划 HTML 原型的页面结构：

**2.1 确定需要创建的页面**

从用户旅程的"位置"字段提取唯一页面列表。案例如下：

| 来源字段 | 示例 | 提取结果 |
|---------|------|---------|
| 变更管理系统/发布单列表 | 位置 = 发布单列表 | 需要「发布单列表页」 |
| 变更管理系统/发布单详情页 | 位置 = 发布单详情页 | 需要「发布单详情页」 |
| 文件选择弹窗 | 跳转 = 文件选择弹窗 | 需要「文件选择弹窗」 |
| 删除确认弹窗 | 跳转 = 删除确认弹窗 | 需要「删除确认弹窗」 |

**2.2 确定页面间的跳转关系**

从用户旅程的"跳转"字段提取跳转关系，案例如下：

| 跳转类型 | 示例 | 实现方式 |
|---------|------|---------|
| Step X | 跳转 = Step 2 | 跳转到指定步骤对应的页面 |
| 流程结束 | 跳转 = 流程结束 | 显示「流程完成」提示 |
| 弹窗 | 跳转 = 文件选择弹窗 | 显示模态弹窗覆盖当前页 |
| 返回 | 跳转 = 返回列表 | 跳转到列表页 |

---

### 步骤 3：创建 HTML 骨架

创建基础的 HTML 文件，包含以下结构：

**3.1 基础 HTML 模板**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>流程演示 Demo - 附件上传功能</title>
    <!-- 引入 Ant Design -->
    <link rel="stylesheet" href="https://unpkg.com/antd@5.12.8/dist/reset.min.css">
    <style>
        /* 星巴克主题配色 + Ant Design 风格 */
        :root {
            --starbucks-green: #00704A;
            --starbucks-green-light: #1e3932;
            --starbucks-cream: #f1f8f6;
            --ant-primary: #00704A;
            --ant-primary-hover: #005938;
            --ant-border: #d9d9d9;
            --ant-bg: #ffffff;
            --ant-text: rgba(0, 0, 0, 0.88);
            --ant-text-secondary: rgba(0, 0, 0, 0.45);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--starbucks-cream);
            padding: 24px;
            color: var(--ant-text);
            line-height: 1.5;
        }

        .page { display: none; background: var(--ant-bg); border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 2px 8px rgba(0, 0, 0, 0.08); }
        .page.active { display: block; }

        /* 按钮样式 - Ant Design 风格 */
        .btn {
            padding: 8px 16px;
            margin: 4px;
            cursor: pointer;
            border: 1px solid var(--ant-border);
            background: white;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .btn:hover { border-color: var(--ant-primary); color: var(--ant-primary); }
        .btn-primary {
            background: var(--ant-primary);
            color: white;
            border-color: var(--ant-primary);
        }
        .btn-primary:hover { background: var(--ant-primary-hover); border-color: var(--ant-primary-hover); }

        /* 模态弹窗 */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.45); justify-content: center; align-items: center; z-index: 1000; }
        .modal.active { display: flex; }
        .modal-content { background: var(--ant-bg); padding: 24px; border-radius: 8px; max-width: 500px; width: 90%; box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12); }

        /* 面包屑 - Ant Design 风格 */
        .breadcrumb { color: var(--ant-text-secondary); margin-bottom: 16px; font-size: 14px; }
        .breadcrumb a { color: var(--ant-text-secondary); text-decoration: none; }
        .breadcrumb a:hover { color: var(--ant-primary); }

        /* 区块样式 */
        .section { margin: 16px 0; padding: 16px; background: #fafafa; border-radius: 8px; border: 1px solid var(--ant-border); }
        .section h3 { font-size: 16px; font-weight: 500; margin-bottom: 12px; color: var(--ant-text); }

        /* 列表项 - Ant Design 风格 */
        .list-item { padding: 12px 16px; border-bottom: 1px solid #f0f0f0; cursor: pointer; transition: all 0.3s; display: flex; justify-content: space-between; align-items: center; }
        .list-item:hover { background: #f5f5f5; }
        .list-item:first-child { border-top-left-radius: 8px; border-top-right-radius: 8px; }
        .list-item:last-child { border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; border-bottom: none; }

        /* 标签徽章 - Ant Design 风格 */
        .badge { display: inline-block; padding: 2px 8px; font-size: 12px; border-radius: 4px; border: 1px solid transparent; }
        .badge-pending { background: #fffbe6; border-color: #ffe58f; color: #d48806; }
        .badge-fixed { background: #f6ffed; border-color: #b7eb8f; color: #389e0d; }

        /* 文件项 */
        .file-item { display: flex; justify-content: space-between; padding: 12px; border: 1px solid var(--ant-border); margin: 8px 0; border-radius: 6px; background: white; }

        /* Tab 样式 - Ant Design 风格 */
        .tabs { display: flex; border-bottom: 1px solid var(--ant-border); margin-bottom: 16px; }
        .tabs .btn { border: none; border-bottom: 2px solid transparent; border-radius: 0; margin-bottom: -1px; }
        .tabs .btn.active { border-bottom-color: var(--ant-primary); color: var(--ant-primary); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* 输入框 - Ant Design 风格 */
        input[type="text"] { padding: 8px 12px; border: 1px solid var(--ant-border); border-radius: 6px; font-size: 14px; width: 200px; transition: all 0.3s; }
        input[type="text"]:focus { border-color: var(--ant-primary); outline: none; box-shadow: 0 0 0 2px rgba(0, 112, 74, 0.1); }

        /* 标题样式 */
        h2 { font-size: 20px; font-weight: 600; margin-bottom: 16px; color: var(--ant-text); }
    </style>
</head>
<body>
    <!-- 页面内容将由 JavaScript 动态控制 -->

    <script>
        // Demo 逻辑将通过 JavaScript 实现
    </script>
</body>
</html>
```

---

### 步骤 4：实现页面内容

根据用户旅程和**页面结构图**实现页面内容。

**实现原则**：
- 严格按照 `05-user-journey.md` 中 Part 3 的页面结构图进行布局
- 页面区域、组件层级、位置关系必须与结构图一致
- 新增/修改的区域必须体现，无变更的区域保持简化

**示例**：列表页和详情页实现

**4.1 案例：发布单列表页**

创建：

```html
<div id="page-list" class="page active">
    <div class="breadcrumb">变更管理系统 / 发布单列表</div>
    <h2>发布单列表</h2>

    <!-- 搜索区域 -->
    <div class="section">
        <input type="text" id="search-input" placeholder="搜索发布单名称或编号">
        <button class="btn" onclick="filterList()">搜索</button>
    </div>

    <!-- 发布单列表 -->
    <div id="release-list">
        <div class="list-item" onclick="goToDetail('R-2024-001')">
            <span><strong>R-2024-001</strong> - 系统升级发布</span>
            <span class="badge badge-pending">待审核</span>
        </div>
        <div class="list-item" onclick="goToDetail('R-2024-002')">
            <span><strong>R-2024-002</strong> - 漏洞修复发布</span>
            <span class="badge badge-fixed">已修复</span>
        </div>
        <!-- 根据实际数据添加更多 -->
    </div>
</div>
```

**4.2 案例：发布单详情页**

此案例的详情页内容包含：
- Tab 导航（基本信息、变更内容、安全漏洞情况）
- 安全漏洞情况 Tab 内的漏洞列表区域
- 附件上传区域（新增）
- 附件列表区域（新增）

```html
<div id="page-detail" class="page">
    <div class="breadcrumb">
        <a href="#" onclick="showPage('page-list')">发布单列表</a> / <span id="release-id">R-2024-001</span>
    </div>
    <h2>发布单详情</h2>

    <!-- Tab 导航 -->
    <div class="tabs">
        <button class="btn" onclick="switchTab('tab-basic', this)">基本信息</button>
        <button class="btn" onclick="switchTab('tab-change', this)">变更内容</button>
        <button class="btn btn-primary active" onclick="switchTab('tab-security', this)">安全漏洞情况</button>
    </div>

    <!-- 安全漏洞情况 Tab -->
    <div id="tab-security" class="tab-content active">
        <!-- 漏洞列表区域 -->
        <div class="section">
            <h3>漏洞列表</h3>
            <div class="list-item">
                <span>CVE-2024-0001 - SQL注入漏洞</span>
                <span class="badge badge-fixed">已修复</span>
            </div>
        </div>

        <!-- 附件上传区域（新增功能） -->
        <div class="section">
            <h3>附件上传</h3>
            <button class="btn btn-primary" onclick="showModal('modal-upload')">
                上传附件
            </button>
        </div>

        <!-- 附件列表区域（新增功能） -->
        <div class="section">
            <h3>已上传附件</h3>
            <div id="attachment-list">
                <!-- 动态渲染附件列表 -->
            </div>
        </div>
    </div>
</div>
```

---

### 步骤 5：实现交互逻辑

**5.1 页面导航控制**

```javascript
// 当前显示的页面
let currentPage = 'page-list';

// 页面映射表（用于跳转）
const pageMap = {
    'page-list': '发布单列表页',
    'page-detail': '发布单详情页'
};

// 显示指定页面
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
    currentPage = pageId;
}

// 跳转到详情页
function goToDetail(releaseId) {
    document.getElementById('release-id').textContent = releaseId;
    showPage('page-detail');
    // 可选：自动切换到安全漏洞情况 Tab
    switchTab('tab-security');
}
```

**5.2 模态弹窗控制**

```javascript
// 显示模态弹窗
function showModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

// 关闭模态弹窗
function hideModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// 文件上传模拟
function uploadFile() {
    const fileInput = document.getElementById('file-input');
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        addAttachment(file.name);
        hideModal('modal-upload');
        alert('上传成功');
    } else {
        alert('请选择文件');
    }
}

// 添加附件到列表
function addAttachment(fileName) {
    const list = document.getElementById('attachment-list');
    const item = document.createElement('div');
    item.className = 'file-item';
    item.innerHTML = `
        <span>${fileName}</span>
        <div>
            <button class="btn" onclick="downloadAttachment('${fileName}')">下载</button>
            <button class="btn" onclick="confirmDelete('${fileName}')">删除</button>
        </div>
    `;
    list.appendChild(item);
}
```

**5.3 删除确认弹窗逻辑**

```javascript
let pendingDeleteFile = null;

function confirmDelete(fileName) {
    pendingDeleteFile = fileName;
    showModal('modal-delete');
}

function executeDelete() {
    if (pendingDeleteFile) {
        // 从列表中移除
        const list = document.getElementById('attachment-list');
        const items = list.querySelectorAll('.file-item');
        items.forEach(item => {
            if (item.querySelector('span').textContent === pendingDeleteFile) {
                item.remove();
            }
        });
        alert('删除成功');
        pendingDeleteFile = null;
        hideModal('modal-delete');
    }
}
```

---

### 步骤 6：添加 Demo 控制面板

在页面顶部添加控制面板，方便测试不同场景：

```html
<div id="control-panel" style="background: #1e3932; padding: 20px; margin-bottom: 24px; border-radius: 8px; color: white;">
    <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 12px;">场景选择（用于 Demo 测试）</h3>
    <p style="color: rgba(255,255,255,0.8); margin-bottom: 16px;">当前 Persona：安全部门审计人员</p>
    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        <button class="btn" style="background: transparent; color: white; border-color: rgba(255,255,255,0.5);" onclick="resetDemo(); startScenario('upload')">场景1: 上传附件</button>
        <button class="btn" style="background: transparent; color: white; border-color: rgba(255,255,255,0.5);" onclick="resetDemo(); startScenario('download')">场景2: 下载附件</button>
        <button class="btn" style="background: transparent; color: white; border-color: rgba(255,255,255,0.5);" onclick="resetDemo(); startScenario('delete')">场景3: 删除附件</button>
        <button class="btn" style="background: transparent; color: white; border-color: rgba(255,255,255,0.5);" onclick="resetDemo(); startScenario('audit')">场景4: 审计查看</button>
    </div>
    <p style="margin-top: 16px; font-size: 12px; color: rgba(255,255,255,0.6);">
        💡 提示：此面板仅用于 Demo 测试，实际产品中不会显示
    </p>
</div>

<script>
function resetDemo() {
    // 重置 Demo 状态
    document.getElementById('attachment-list').innerHTML = '';
    showPage('page-list');
}

function startScenario(scenario) {
    switch(scenario) {
        case 'upload':
            // 预设一些附件数据
            break;
        case 'download':
            // 预设一些附件数据
            break;
        // ...
    }
}
</script>
```

---

### 步骤 7：验证流程完整性

使用以下清单验证 Demo：

| 验证项 | 检查方法 |
|--------|---------|
| 用户旅程 Step 覆盖 | 对照用户旅程表格，确认每个 Step 都有对应页面/交互 |
| 跳转逻辑正确 | 跟随用户旅程走一遍，确认每步跳转正确 |
| 关键触点存在 | 确认核心触点、决策点、等待点、跳出点都已实现 |
| 弹窗正常 | 测试上传弹窗、删除确认弹窗能正常打开/关闭 |
| 列表操作 | 测试附件能正确添加到列表、正确从列表删除 |
| 流程可闭环 | 从头走到尾，确认流程能完整结束 |

---

## 输出模板：`flow-demo.html`

完整的 HTML 文件应包含：

1. **控制面板** - 场景选择按钮，方便测试不同用户旅程
2. **页面数量正确** - 页面数量与`### 步骤 2：规划 Demo 结构`里确定需要创建的页面数量一致。
3. **页面导航逻辑** - JavaScript 控制页面切换
4. **交互逻辑** - 上传、下载、删除等操作实现
5. **易用性检查**：
    1. **列表页** - 包含搜索功能
    2. **详情页** - 包含 Tab 切换
    3. **二次确认** - 删除等操作是否有二次确认弹窗
---

## 示例代码结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>流程演示 Demo - 发布单附件管理</title>
    <!-- 引入 Ant Design -->
    <link rel="stylesheet" href="https://unpkg.com/antd@5.12.8/dist/reset.min.css">
    <style>
        /* 星巴克主题配色 + Ant Design 风格 */
        :root {
            --starbucks-green: #00704A;
            --starbucks-green-light: #1e3932;
            --starbucks-cream: #f1f8f6;
            --ant-primary: #00704A;
            --ant-primary-hover: #005938;
            --ant-border: #d9d9d9;
            --ant-bg: #ffffff;
            --ant-text: rgba(0, 0, 0, 0.88);
            --ant-text-secondary: rgba(0, 0, 0, 0.45);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--starbucks-cream);
            padding: 24px;
            color: var(--ant-text);
            line-height: 1.5;
        }
        .page { display: none; background: var(--ant-bg); border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03), 0 2px 8px rgba(0, 0, 0, 0.08); }
        .page.active { display: block; }
        .btn {
            padding: 8px 16px;
            margin: 4px;
            cursor: pointer;
            border: 1px solid var(--ant-border);
            background: white;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .btn:hover { border-color: var(--ant-primary); color: var(--ant-primary); }
        .btn-primary { background: var(--ant-primary); color: white; border-color: var(--ant-primary); }
        .btn-primary:hover { background: var(--ant-primary-hover); border-color: var(--ant-primary-hover); }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.45); justify-content: center; align-items: center; z-index: 1000; }
        .modal.active { display: flex; }
        .modal-content { background: var(--ant-bg); padding: 24px; border-radius: 8px; max-width: 500px; width: 90%; box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12); }
        .breadcrumb { color: var(--ant-text-secondary); margin-bottom: 16px; font-size: 14px; }
        .breadcrumb a { color: var(--ant-text-secondary); text-decoration: none; }
        .breadcrumb a:hover { color: var(--ant-primary); }
        .section { margin: 16px 0; padding: 16px; background: #fafafa; border-radius: 8px; border: 1px solid var(--ant-border); }
        .section h3 { font-size: 16px; font-weight: 500; margin-bottom: 12px; color: var(--ant-text); }
        .list-item { padding: 12px 16px; border-bottom: 1px solid #f0f0f0; cursor: pointer; transition: all 0.3s; display: flex; justify-content: space-between; align-items: center; }
        .list-item:hover { background: #f5f5f5; }
        .list-item:first-child { border-top-left-radius: 8px; border-top-right-radius: 8px; }
        .list-item:last-child { border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; border-bottom: none; }
        .badge { display: inline-block; padding: 2px 8px; font-size: 12px; border-radius: 4px; border: 1px solid transparent; }
        .badge-pending { background: #fffbe6; border-color: #ffe58f; color: #d48806; }
        .badge-fixed { background: #f6ffed; border-color: #b7eb8f; color: #389e0d; }
        .file-item { display: flex; justify-content: space-between; padding: 12px; border: 1px solid var(--ant-border); margin: 8px 0; border-radius: 6px; background: white; }
        .tabs { display: flex; border-bottom: 1px solid var(--ant-border); margin-bottom: 16px; }
        .tabs .btn { border: none; border-bottom: 2px solid transparent; border-radius: 0; margin-bottom: -1px; }
        .tabs .btn.active { border-bottom-color: var(--ant-primary); color: var(--ant-primary); }
        input[type="text"] { padding: 8px 12px; border: 1px solid var(--ant-border); border-radius: 6px; font-size: 14px; width: 200px; transition: all 0.3s; }
        input[type="text"]:focus { border-color: var(--ant-primary); outline: none; box-shadow: 0 0 0 2px rgba(0, 112, 74, 0.1); }
        h2 { font-size: 20px; font-weight: 600; margin-bottom: 16px; color: var(--ant-text); }
    </style>
</head>
<body>
    <!-- 控制面板 -->
    <div id="control-panel">...</div>

    <!-- 发布单列表页 -->
    <div id="page-list" class="page active">...</div>

    <!-- 发布单详情页 -->
    <div id="page-detail" class="page">...</div>

    <!-- 上传弹窗 -->
    <div id="modal-upload" class="modal">...</div>

    <!-- 删除确认弹窗 -->
    <div id="modal-delete" class="modal">...</div>

    <script>
        // 页面导航
        // 弹窗控制
        // 业务逻辑（上传统件、下载、删除等）
        // 场景预设
    </script>
</body>
</html>
```

---

## 审查清单

执行完本阶段后，检查以下事项：

| 检查项 | 状态 |
|--------|------|
| 已读取 `05-user-journey.md` | [ ] |
| 已提取 Part 3 页面结构图 | [ ] |
| 已提取所有 Persona × 场景组合 | [ ] |
| Demo 页面布局与页面结构图一致 | [ ] |
| 新增/修改区域在 Demo 中体现 | [ ] |
| 已实现页面间的跳转逻辑 | [ ] |
| 已实现弹窗（上传、删除确认） | [ ] |
| 已实现核心交互（上传、下载、删除） | [ ] |
| 已添加场景选择控制面板 | [ ] |
| 已验证每个用户旅程能完整走通 | [ ] |
| 已生成 `flow-demo.html` | [ ] |

---

## 关联阶段

| 阶段 | 文件 | 关系 |
|------|------|------|
| 用户旅程设计 | [ux-phase5-user-journey](../ux-phase5-user-journey/SKILL.md) | 上一阶段 |
| 流程演示 Demo | [ux-phase6-demo](./skill.md) | 当前阶段 |
| 项目章程 | [ux-phase7-project-goal](../ux-phase7-project-goal/SKILL.md) | 下一阶段 |

---

## 护栏

- **功能优先** - 不关注视觉样式，只验证操作流程
- **流程完整** - 必须覆盖用户旅程中的所有步骤
- **交互真实** - 点击、跳转、弹窗必须真实可操作
- **可闭环** - 每个场景都能从头走到尾，流程可结束
- **便于测试** - 添加场景选择控制面板，方便快速切换测试场景

---

## 下一阶段建议

完成流程演示 Demo 后，可以进入以下方向之一：

1. **用户测试** - 邀请实际用户试用 Demo，收集反馈
2. **流程优化** - 根据测试反馈调整用户旅程
3. **详细设计** - 进入 UI 设计阶段
4. **技术评审** - 与开发团队评审 Demo 的技术可行性

---

## 下一步

完成此阶段后，建议调用 **ux-flow** skill 来确定下一步：

```bash
/ux:flow
```

ux-flow 会根据当前已产出的文件，推荐最合适的下一步阶段。
