#!/bin/bash
cd /Users/mckay/vault/hcmp/o315/blog || exit 1
if [ -n "$(git status --porcelain content/)" ]; then
  git add content/
  git commit -m "Auto-commit: update blog content"
  git push
fi
