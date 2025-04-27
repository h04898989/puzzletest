#!/bin/bash

# 檢查是否提供參數作為 commit 訊息
if [ -z "$1" ]; then
  commit_message="sara update" # 預設 commit 訊息
  else
    commit_message="$1" # 使用提供的參數作為 commit 訊息
    fi

    # 執行 Git 指令
    git add .
    git commit -m "$commit_message"
    git push origin
