#!/bin/bash
# GitHub Issue 评论脚本 - 为指定 issue 添加评论
# 用法: ./scripts/add-comment.sh <issue-number> "<评论内容>"

ISSUE_NUMBER="$1"
COMMENT="$2"

# 验证参数
if [ -z "$ISSUE_NUMBER" ]; then
  echo "❌ 错误: 请提供 issue 编号"
  echo "用法: ./scripts/add-comment.sh <issue-number> \"<评论内容>\""
  echo "示例: ./scripts/add-comment.sh 42 \"已完成初步分析\""
  exit 1
fi

if ! [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "❌ 错误: issue 编号必须是数字"
  exit 1
fi

if [ -z "$COMMENT" ]; then
  echo "❌ 错误: 请提供评论内容"
  echo "用法: ./scripts/add-comment.sh <issue-number> \"<评论内容>\""
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

echo "💬 正在为 Issue #$ISSUE_NUMBER 添加评论..."

# 添加评论
RESULT=$(gh issue comment "$ISSUE_NUMBER" --body "$COMMENT" 2>&1)

if [ $? -eq 0 ]; then
  echo "✅ 评论已添加到 issue #$ISSUE_NUMBER"
else
  echo "❌ 添加评论失败"
  echo ""
  echo "可能原因:"
  echo "  • issue 不存在"
  echo "  • 没有评论权限"
  echo "  • 未登录 GitHub CLI (运行 gh auth login)"
  echo ""
  echo "错误信息: $RESULT"
  exit 1
fi
