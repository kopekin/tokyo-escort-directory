import requests
from bs4 import BeautifulSoup

area_url = "https://yoasobi-heaven.com/ja/tokyo/A1304/shop-list/biz6/"
headers = {"User-Agent": "Mozilla/5.0"}
shop_urls = []

res = requests.get(area_url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

for a in soup.find_all("a", href=True):
    href = a["href"]
    link_text = a.get_text(strip=True)

    # 無効リンク除外
    if "Not Found" in link_text or "..." in link_text or link_text.strip() == "":
        continue

    if href.startswith("/ja/tokyo/A1304/") and href.count("/") == 5 and "shop-list" not in href:
        full_url = "https://yoasobi-heaven.com" + href
        if full_url not in shop_urls:
            shop_urls.append(full_url)

# 保存
with open("urls.txt", "w", encoding="utf-8") as f:
    for url in shop_urls:
        f.write(url + "\n")

print(f"{len(shop_urls)} 件のURLを urls.txt に保存しました ✅")

