#!/bin/bash
# GitHub Issue Bug 创建脚本
# 用法: ./scripts/create-bug.sh "<标题>" "<问题描述>" "<复现步骤>" "<期望结果>" "<实际结果>" "<环境信息>" "<错误日志>"

TITLE="$1"
DESCRIPTION="$2"
REPRO_STEPS="$3"
EXPECTED="$4"
ACTUAL="$5"
ENVIRONMENT="$6"
LOGS="$7"

# 验证必需参数
if [ -z "$TITLE" ]; then
  echo "❌ 错误: 问题标题不能为空"
  exit 1
fi

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
  echo "❌ 错误: GitHub CLI (gh) 未安装"
  echo "请访问 https://cli.github.com/ 安装"
  exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
  echo "❌ 错误: GitHub CLI 未登录"
  echo "请运行: gh auth login"
  exit 1
fi

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir &> /dev/null; then
  echo "❌ 错误: 当前目录不是 Git 仓库"
  exit 1
fi

# 构建 body
BODY="## 问题描述
${DESCRIPTION:-未提供}

## 复现步骤
${REPRO_STEPS:-未提供}

## 期望结果
${EXPECTED:-未提供}

## 实际结果
${ACTUAL:-未提供}

## 环境信息
${ENVIRONMENT:-未提供}

## 错误日志
<details>
<summary>展开查看</summary>

\`\`\`
${LOGS:-无}
\`\`\`
</details>"

# 创建 issue
echo "📝 正在创建 Bug Issue..."
ISSUE_URL=$(gh issue create \
  --title "[Bug] $TITLE" \
  --body "$BODY" \
  --label "bug" 2>&1)

if [ $? -eq 0 ]; then
  echo "✅ Bug Issue 创建成功！"
  echo "🔗 $ISSUE_URL"
else
  echo "❌ 创建失败: $ISSUE_URL"
  exit 1
fi
