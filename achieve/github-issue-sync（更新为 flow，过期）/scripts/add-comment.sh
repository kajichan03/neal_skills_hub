#!/bin/bash
# GitHub Issue 评论脚本 - 为指定 issue 添加评论
# 用法: ./scripts/add-comment.sh <issue-number> "<评论内容>"

ISSUE_NUMBER="$1"
COMMENT="$2"

if [ -z "$ISSUE_NUMBER" ]; then
  echo "错误: 请提供 issue 编号"
  echo "用法: ./scripts/add-comment.sh <issue-number> \"<评论内容>\""
  exit 1
fi

if ! [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "错误: issue 编号必须是数字"
  exit 1
fi

if [ -z "$COMMENT" ]; then
  echo "错误: 请提供评论内容"
  echo "用法: ./scripts/add-comment.sh <issue-number> \"<评论内容>\""
  exit 1
fi

# 添加评论
gh issue comment "$ISSUE_NUMBER" --body "$COMMENT" 2>/dev/null || {
  echo "错误: 无法为 issue #$ISSUE_NUMBER 添加评论"
  echo "可能原因:"
  echo "  - issue 不存在"
  echo "  - 没有评论权限"
  echo "  - 未登录 GitHub CLI (运行 gh auth login)"
  exit 1
}

echo "✅ 评论已添加到 issue #$ISSUE_NUMBER"
