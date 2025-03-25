import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

# URLリスト読み込み
with open("urls.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

# 結果を保存するCSV
csv_file = "results.csv"

# ヘッダー
headers = ["timestamp", "url", "store_name", "address", "base_price", "area_price_shinjuku", "area_price_other", "phone", "hours"]

# CSVファイルの初期化（ヘッダー追加）
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

# 各URLにアクセスしてデータ取得
for url in urls:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        store_name = soup.title.text.split("|")[0].split("/")[0].strip() if soup.title else "不明"

        # 住所
        meta_desc = soup.find("meta", {"property": "og:description"})
        address = meta_desc["content"].split("は")[1].split("にある")[0].strip() if meta_desc else "不明"

        # 電話番号
        phone_candidates = [t.strip() for t in soup.find_all(string=True) if any(c.isdigit() for c in t) and "-" in t]
        phone = next((p for p in phone_candidates if "03-" in p or "+81" in p), "不明")

        # 営業時間
        text_all = " ".join([t.strip() for t in soup.find_all(string=True)])
        import re
        hours_match = re.search(r"(\d{1,2}:\d{2}～\d{1,2}:\d{2}|\d{1,2}時～\d{1,2}時)", text_all)
        hours = hours_match.group(0) if hours_match else "不明"

        # 料金
        price_candidates = [t.strip() for t in soup.find_all(string=True) if "円" in t]
        cleaned_prices = [p for p in price_candidates if any(c.isdigit() for c in p)]
        base_price = cleaned_prices[0] if len(cleaned_prices) > 0 else "不明"
        area_price_shinjuku = cleaned_prices[1] if len(cleaned_prices) > 1 else "不明"
        area_price_other = cleaned_prices[2] if len(cleaned_prices) > 2 else "不明"

        # 書き込み
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, url, store_name, address, base_price, area_price_shinjuku, area_price_other, phone, hours])

        print(f"✅ 完了: {store_name}")
    
    except Exception as e:
        print(f"❌ エラー: {url} → {e}")
        import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# ファイルからURLリストを読み込む
with open("urls.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

results = []

for url in urls:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        store_name = soup.title.text.split("|")[0].split("/")[0].strip() if soup.title else "不明"

        meta_desc = soup.find("meta", {"property": "og:description"})
        address = meta_desc["content"].split("は")[1].split("にある")[0].strip() if meta_desc else "不明"

        text_data = [text.strip() for text in soup.find_all(string=True)]

        # 料金情報抽出
        price_candidates = [text for text in text_data if "円" in text and any(char.isdigit() for char in text)]
        prices = [p for p in price_candidates if "分" in p or "円～" in p]

        base_price = prices[0] if prices else "不明"
        area_price_1 = next((p for p in price_candidates if "新宿区：" in p), "")
        area_price_2 = next((p for p in price_candidates if "新宿区外：" in p), "")

        # 電話番号
        phone_number = next((text for text in text_data if "03-" in text or "+81" in text), "不明")

        # 営業時間
        business_hours = next((text for text in text_data if ":" in text and "～" in text), "不明")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        results.append({
            "URL": url,
            "店名": store_name,
            "住所": address,
            "基本料金": base_price,
            "新宿区": area_price_1,
            "新宿区外": area_price_2,
            "電話番号": phone_number,
            "営業時間": business_hours,
            "取得日時": timestamp
        })

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# CSVに保存
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("✅ データ取得完了！results.csv に保存しました。")
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URLリストを読み込む
with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# 出力ファイル名（タイムスタンプ付き）
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"yoasobi_data_{timestamp}.csv"

# CSVファイルのヘッダー
headers = ["取得日時", "URL", "店名", "住所", "電話番号", "営業時間", "基本料金", "新宿区", "新宿区外"]

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")

            # 店名
            store_name = soup.title.text.split("|")[0].split("/")[0].strip() if soup.title else "不明"

            # 住所
            meta_desc = soup.find("meta", {"property": "og:description"})
            address = meta_desc["content"].split("は")[1].split("にある")[0].strip() if meta_desc else "不明"

            # 電話番号
            phone_candidates = [t.strip() for t in soup.find_all(string=True) if any(c.isdigit() for c in t) and "-" in t]
            phone = next((p for p in phone_candidates if "03-" in p or "+81" in p), "不明")

            # 営業時間
            import re
            text_blob = " ".join([t.strip() for t in soup.find_all(string=True)])
            match = re.search(r"(\d{1,2}:\d{2}～\d{1,2}:\d{2}|\d{1,2}時～\d{1,2}時)", text_blob)
            business_hours = match.group(0) if match else "不明"

            # 料金
            price_candidates = [t.strip() for t in soup.find_all(string=True) if "円" in t]
            cleaned_prices = [p for p in price_candidates if any(c.isdigit() for c in p)]
            basic_price = cleaned_prices[0] if len(cleaned_prices) > 0 else "不明"
            price_shinjuku = cleaned_prices[1] if len(cleaned_prices) > 1 else "不明"
            price_outside = cleaned_prices[2] if len(cleaned_prices) > 2 else "不明"

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url,
                store_name,
                address,
                phone,
                business_hours,
                basic_price,
                price_shinjuku,
                price_outside
            ])
            print(f"[OK] {store_name} を収集しました")

        except Exception as e:
            print(f"[ERROR] {url} の取得で問題が発生しました: {e}")
            