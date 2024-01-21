import time
from collections import Counter

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def initialize_driver(brave_path):
    """WebDriverの初期化"""
    options = Options()
    options.binary_location = brave_path
    return webdriver.Chrome(options=options)


def get_page_content(driver, url):
    """ページのHTMLコンテンツを取得"""
    driver.get(url)
    scroll_to_bottom(driver)
    html_content = driver.page_source
    return html_content


def scroll_to_bottom(driver):
    """ページの末尾までスクロール"""
    old_position, new_position = 0, None
    while new_position != old_position:
        old_position, new_position = new_position, driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;"
        )
        time.sleep(3)


"""test"""
# def scroll_to_bottom(driver):
#     """ページを3回スクロールする"""
#     for _ in range(3):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(3)


def analyze_items(soup):
    """商品の分析: 数のカウントと重複するタイトルの抽出"""
    items = soup.find_all("li", {"data-id": True})
    titles = [tag["title"] for tag in soup.find_all("a", {"title": True})]
    duplicate_titles = [title for title, count in Counter(titles).items() if count > 2]

    kindle_books = []
    for item in items:
        title = item.find("a", {"title": True}).get("title", "")
        author_tag = item.find("span", {"class": "a-size-base"})
        if author_tag and "Kindle" in author_tag.text:
            kindle_books.append(f"{title} - {author_tag.text.strip()}")

    return len(items), duplicate_titles, kindle_books


# 実行部分
brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
url = "https://www.amazon.co.jp/hz/wishlist/ls/13A6BVSZHVP0A?ref_=list_d_wl_lfu_nav_2"

driver = initialize_driver(brave_path)
html_content = get_page_content(driver, url)
soup = BeautifulSoup(html_content, "html.parser")
item_count, duplicates, kindle_books = analyze_items(soup)
driver.quit()

print(f"ほしいものリストには {item_count} 個の商品があります。\n")
print("重複するタイトルの商品: \n" + "\n".join(duplicates) + "\n")
print("Kindle版の書籍: \n" + "\n".join(kindle_books))
