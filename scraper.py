import requests
from bs4 import BeautifulSoup
import csv
import time

# ここでエリアURLを指定（例: 新宿・歌舞伎町）
area_url = "https://yoasobi-heaven.com/ja/tokyo/A1304/shop-list/biz6/"

# ヘッダーを付けてアクセス（ブロック対策）
headers = {
    "User-Agent": "Mozilla/5.0"
}

# URL取得用リスト
shop_urls = []

# エリアページから店舗一覧を取得
res = requests.get(area_url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 店舗リンクの要素を抽出（aタグに特定パターンのhref）
for a in soup.find_all("a", href=True):
    href = a["href"]
    link_text = a.get_text(strip=True)

    # 表示テキストが無効（"Not Found", "...", 空文字）のリンクを除外
    if not link_text or "Not Found" in link_text or "..." in link_text:
        continue

    # 東京都の特定パターンの店舗URLのみを抽出（例: /ja/tokyo/A1304/xxx）
    if href.startswith("/ja/tokyo/A1304/") and href.count("/") == 5 and "shop-list" not in href:
        full_url = "https://yoasobi-heaven.com" + href
        if full_url not in shop_urls:
            shop_urls.append(full_url)

# ファイルに保存
with open("urls.txt", "w", encoding="utf-8") as f:
    for url in shop_urls:
        f.write(url + "\n")

print(f"{len(shop_urls)} 件のURLを urls.txt に保存しました ✅")

# 新しいHTMLテンプレートを作成
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tokyo Escort Directory</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
        h1 { color: #333; }
        .lang-select, .filter, .chatbot { margin-bottom: 20px; }
        button { padding: 10px 15px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Tokyo Escort Directory</h1>

    <div class="lang-select">
        <label for="lang">Language:</label>
        <select id="lang">
            <option value="en">English</option>
            <option value="ja">日本語</option>
            <option value="zh">中文</option>
            <option value="ko">한국어</option>
        </select>
    </div>

    <div class="filter">
        <button onclick="filterNow()">Show Girls Available Now</button>
    </div>

    <div class="chatbot">
        <p>🤖 Ask for recommendations:</p>
        <input type="text" id="userQuery" placeholder="e.g. 'Big boobs, under 160cm'" size="40">
        <button onclick="sendQuery()">Ask</button>
        <p id="chatResponse"></p>
    </div>

    <script>
        function filterNow() {
            alert("Feature not implemented yet. Will show girls available now.");
        }
        function sendQuery() {
            const q = document.getElementById("userQuery").value;
            document.getElementById("chatResponse").textContent = `Searching for: "${q}"... (GPT will respond here)`;
        }
    </script>
</body>
</html>
"""

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

results = []

for url in shop_urls:
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        name = soup.title.string.strip() if soup.title else "不明"

        # 電話番号
        phone = next((t.strip() for t in soup.stripped_strings if "03-" in t or "+81" in t), "不明")

        # 営業時間
        hours = next((t.strip() for t in soup.stripped_strings if "～" in t or "時" in t or ":" in t), "不明")

        # 料金（「円」が含まれるテキスト）
        prices = [t.strip() for t in soup.stripped_strings if "円" in t and any(c.isdigit() for c in t)]
        price = prices[0] if prices else "不明"

# 店名が "Not Found" や空欄のものを除外
if name == "Not Found" or name.strip() == "":
    print(f"⛔️ 無効な店舗名のためスキップ: {url}")
    continue
    
        results.append({
            "店舗名": name,
            "URL": url,
            "電話番号": phone,
            "営業時間": hours,
            "料金": price
        })

        print(f"[OK] {name} を収集しました")

        time.sleep(1)  # 過負荷防止
    except Exception as e:
        print(f"[ERROR] {url} の取得で問題が発生しました: {e}")
        continue

# CSVに保存
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["店舗名", "URL", "電話番号", "営業時間", "料金"])
    writer.writeheader()
    writer.writerows(results)

print("✅ データ取得完了！results.csv に保存しました。")

# HTML一覧表示用データを生成（results.csv を元に index.html に反映）
from jinja2 import Template

# テンプレート読み込み
html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Tokyo Escort Directory</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #eee; }
    </style>
</head>
<body>
    <h1>Tokyo Escort Directory</h1>
    <table>
        <tr>
            <th>店舗名</th>
            <th>電話番号</th>
            <th>営業時間</th>
            <th>料金</th>
            <th>URL</th>
        </tr>
        {% for row in results %}
        <tr>
            <td>{{ row["店舗名"] }}</td>
            <td>{{ row["電話番号"] }}</td>
            <td>{{ row["営業時間"] }}</td>
            <td>{{ row["料金"] }}</td>
            <td><a href="{{ row["URL"] }}" target="_blank">リンク</a></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>"""

template = Template(html_template)
rendered_html = template.render(results=results)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(rendered_html)

print("📝 index.html に最新店舗情報を書き出しました！")