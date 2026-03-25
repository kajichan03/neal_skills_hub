#!/bin/bash
# GitHub Issue Feature Request 创建脚本
# 用法: ./scripts/create-feature.sh "<标题>" "<现状>" "<问题>" "<预期>" "<优先级>" "<补充信息>"

TITLE="$1"
CURRENT="$2"
PROBLEM="$3"
EXPECTED="$4"
PRIORITY="$5"
EXTRA="$6"

# 验证必需参数
if [ -z "$TITLE" ]; then
  echo "❌ 错误: 需求标题不能为空"
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
BODY="## 现状
${CURRENT:-未提供}

## 问题
${PROBLEM:-未提供}

## 预期
${EXPECTED:-未提供}

## 优先级
${PRIORITY:-未指定}

## 补充信息
${EXTRA:-无}"

# 创建 issue
echo "📝 正在创建 Feature Request Issue..."
ISSUE_URL=$(gh issue create \
  --title "[Feature] $TITLE" \
  --body "$BODY" \
  --label "enhancement" 2>&1)

if [ $? -eq 0 ]; then
  echo "✅ Feature Request Issue 创建成功！"
  echo "🔗 $ISSUE_URL"
else
  echo "❌ 创建失败: $ISSUE_URL"
  exit 1
fi
