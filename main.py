import os
import sys

# urls.txt がなければ空で作成
if not os.path.exists("urls.txt"):
    with open("urls.txt", "w", encoding="utf-8") as f:
        pass
    print("🆕 urls.txt を新規作成しました")

# collect_urls.py が存在するかチェック
if os.path.exists("collect_urls.py"):
    os.system("python collect_urls.py")
else:
    print("❌ エラー: collect_urls.py が見つかりません。スクリプトを確認してください。")
    sys.exit(1)

# scraper.py が存在するかチェック
if os.path.exists("scraper.py"):
    os.system("python scraper.py")
else:
    print("❌ エラー: scraper.py が見つかりません。スクリプトを確認してください。")
    sys.exit(1)

# Create collect_urls.py file
with open("collect_urls.py", "w", encoding="utf-8") as f:
    f.write("""import requests
from bs4 import BeautifulSoup

BASE_URL = "https://yoasobi-heaven.com/ja/tokyo/shop-list/"
FOREIGNER_KEYWORDS = ["外国人", "英語", "English", "日本語が話せない", "multilingual"]

def get_store_urls():
    print("🔍 東京都内の店舗一覧ページを確認中...")
    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # 店舗リンクを取得（仮に a タグ内で /ja/tokyo/ を含むリンクを対象とする）
    links = soup.find_all("a", href=True)
    store_urls = []

    for link in links:
        href = link["href"]
        if "/ja/tokyo/" in href and "/shop-list/" not in href and "/ja/tokyo/" != href:
            full_url = "https://yoasobi-heaven.com" + href
            if full_url not in store_urls:
                store_urls.append(full_url)

    print(f"✅ 店舗候補URL数: {len(store_urls)}")

    # 各店舗ページにアクセスし、外国人対応ワードが含まれるか確認
    filtered_urls = []
    for url in store_urls:
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if res.status_code == 200:
                html = res.text
                if any(keyword in html for keyword in FOREIGNER_KEYWORDS):
                    filtered_urls.append(url)
                    print(f"🌍 外国人OK: {url}")
        except Exception as e:
            print(f"⚠️ エラー: {url} → {e}")

    # urls.txt に保存
    with open("urls.txt", "w", encoding="utf-8") as f:
        for url in filtered_urls:
            f.write(url + "\\n")

    print(f"✅ 最終的な外国人OK店舗数: {len(filtered_urls)} 件 → urls.txt に保存完了")

if __name__ == "__main__":
    get_store_urls()
""")

# Create generate_html.py file
with open("generate_html.py", "w", encoding="utf-8") as f:
    f.write("""import csv
from datetime import datetime

INPUT_CSV = "results.csv"
OUTPUT_HTML = "index.html"

def generate_html():
    with open(INPUT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f\"\"\"<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo Foreigner-Friendly Escort Shops</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; background: white; }}
        th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
        th {{ background-color: #eee; }}
        tr:hover {{ background-color: #f1f1f1; }}
    </style>
</head>
<body>
    <h1>Foreigner-Friendly Escort Shops in Tokyo</h1>
    <p>Last updated: {now}</p>
    <table>
        <tr>
            <th>店名</th>
            <th>住所</th>
            <th>料金</th>
            <th>電話番号</th>
            <th>営業時間</th>
            <th>URL</th>
        </tr>
\"\"\" 

    for row in rows:
        html += f\"\"\"<tr>
            <td>{{row.get("店名", "")}}</td>
            <td>{{row.get("住所", "")}}</td>
            <td>{{row.get("基本料金", "")}}<br>{{row.get("エリア別料金", "")}}</td>
            <td>{{row.get("電話番号", "")}}</td>
            <td>{{row.get("営業時間", "")}}</td>
            <td><a href="{{row.get("URL", "")}}" target="_blank">リンク</a></td>
        </tr>
\"\"\" 

    html += \"\"\"
    </table>
</body>
</html>
\"\"\"

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTMLファイル {OUTPUT_HTML} を作成しました。")

if __name__ == "__main__":
    generate_html()
""")
