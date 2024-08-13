# 匯入所需的套件

# 引入 Selenium 的 webdriver 模組，用於操作瀏覽器 打開網頁、點擊元素、獲取內容等
from selenium import webdriver

# 引入 Service 類，用於設置 ChromeDriver 的服務 需要時啟動和停止
from selenium.webdriver.chrome.service import Service

# 引入 ChromeDriverManager 類，能自動下載和管理適合當前 Chrome 版本的 ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

# 引入異常類型，用於處理網頁元素查找和超時錯誤
# TimeoutException：當等待某個條件超過指定時間但條件未滿足時拋出的異常。
# NoSuchElementException：當嘗試查找不存在的網頁元素時拋出的異常。
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 引入 WebDriverWait 類，用於設置顯示等待 以確保某些條件滿足後再進行後續操作
from selenium.webdriver.support.ui import WebDriverWait

# 引入 expected_conditions 模組，用於設定等待條件
from selenium.webdriver.support import expected_conditions as EC

# 引入 By 類，用於指定元素的查找方式
from selenium.webdriver.common.by import By

# 引入 sleep 函數，用於添加延遲
from time import sleep


# 瀏覽器設定
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")           #最大化視窗
my_options.add_argument("--incognito")                 #開啟無痕模式
my_options.add_argument("--disable-popup-blocking")    #禁用彈出攔截
my_options.add_argument("--disable-notifications")     #取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")                #設定為正體中文


# 開啟自動控制瀏覽器
driver = webdriver.Chrome(options = my_options,)

# 爬蟲流程

# 走訪頁面
def visit():
    driver.get("https://market.591.com.tw/list?regionId=3&postType=2,8")
    
    # 等待一下
    sleep(1)

# 按鈕選擇器
def button():
    try:
        # 等待元素
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.guide-button")))
        
        # 使用 CSS 選擇器查找按鈕
        button = driver.find_element(By.CSS_SELECTOR, "button.guide-button").click()
    except NoSuchElementException:
        print("沒有彈跳式資訊")

    # 等待一下
    sleep(1)

# 篩選 (選項)
def filter():
    try:
        # 等待元素
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".t5-dropdown-select")))
        
        # 選擇區域
        driver.find_element(By.CSS_SELECTOR, ".t5-dropdown-select").click()

        # 選擇永和
        driver.find_element(By.CSS_SELECTOR, "#areaFilterItemEle17").click()

        # 選擇確定
        driver.find_elements(By.CSS_SELECTOR, "section.grid-filter-btn button")[1].click()

    except NoSuchElementException:
        print("篩選出錯")

    # 等待一下
    sleep(1)
    

if __name__ == '__main__':
    visit()
    button()
    filter()
