import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ページの末尾までスクロールする関数
def scroll_to_bottom(driver):
    old_position = 0
    new_position = None

    while new_position != old_position:
        # 新しい位置までスクロール
        old_position = new_position
        new_position = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;"
        )

        # 新しいコンテンツがロードされるのを待つ
        time.sleep(3)


def count_items_in_wishlist(url):
    # Braveの実行ファイルパス
    brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

    # WebDriverの設定
    options = Options()
    options.binary_location = brave_path

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # ページの末尾までスクロール
    scroll_to_bottom(driver)

    # URLからHTMLコンテンツを取得
    html_content = driver.page_source

    driver.quit()

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html_content, "html.parser")

    # 特定の要素を見つけてカウント
    items = soup.find_all("li", {"data-id": True})
    return len(items)


# 例として、ダミーのURLを使用
url = "https://www.amazon.co.jp/"
item_count = count_items_in_wishlist(url)
print(f"ほしいものリストには {item_count} 個の商品があります。")
