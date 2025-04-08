import csv
from datetime import datetime

# CSVファイルから読み込み
csv_file = "results.csv"
html_file = "index.html"

rows = []
with open(csv_file, encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)
    rows = list(reader)

# HTML生成
with open(html_file, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html lang='ja'>\n<head>\n")
    f.write("<meta charset='UTF-8'>\n<title>YOASOBI Heaven 収集データ</title>\n</head>\n<body>\n")
    f.write("<h1>YOASOBI Heaven 収集データ</h1>\n")
    f.write(f"<p>更新日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
    f.write("<table border='1'>\n<tr>\n")

    for h in headers:
        f.write(f"<th>{h}</th>")
    f.write("</tr>\n")

    for row in rows:
        f.write("<tr>\n")
        for cell in row:
            f.write(f"<td>{cell}</td>")
        f.write("</tr>\n")
    f.write("</table>\n</body>\n</html>\n")

print("✅ index.html を作成しました！")