import csv
from datetime import datetime

html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>店舗一覧</title>
    <style>
        body {{ font-family: sans-serif; background: #f9f9f9; padding: 2rem; }}
        table {{ width: 100%; border-collapse: collapse; background: #fff; }}
        th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; }}
        th {{ background: #eee; }}
    </style>
</head>
<body>
    <h1>インバウンド風俗店舗データ</h1>
    <p>更新日: {timestamp}</p>
    <table>
        <thead>
            <tr><th>店名</th><th>住所</th><th>料金</th><th>電話番号</th><th>営業時間</th></tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</body>
</html>
"""

def generate_row(row):
    return f"<tr><td>{row['店名']}</td><td>{row['住所']}</td><td>{row['基本料金']}</td><td>{row['電話番号']}</td><td>{row['営業時間']}</td></tr>"

with open("results.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows_html = "\n".join([generate_row(row) for row in reader])

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
html_content = html_template.format(timestamp=timestamp, rows=rows_html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ index.html を作成しました！")
