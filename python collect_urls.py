#!/bin/bash

git init
git branch -M main
git remote add origin https://github.com/kopekin/tokyo-escort-directory.git
git add index.html scraper.py main.py generate_html.py .github/workflows/main.yml urls.txt
git commit -m "🚀 デプロイ設定とスクレイピングスクリプトを追加"
git push -u origin main
