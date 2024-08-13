'''
匯入套件
    用於操作瀏覽器 打開網頁、點擊元素、獲取內容等
    需要時啟動和停止
    管理適合當前 Chrome 版本的 ChromeDriver
    處理網頁元素查找和超時錯誤
    設置顯示等待
    設定等待條件
    指定元素的查找方式
    添加延遲
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json
import csv
import os
import pandas as pd



# 瀏覽器設定
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")           #最大化視窗
my_options.add_argument("--incognito")                 #開啟無痕模式
my_options.add_argument("--disable-popup-blocking")    #禁用彈出攔截
my_options.add_argument("--disable-notifications")     #取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")                #設定為正體中文

# 開啟自動控制瀏覽器
driver = webdriver.Chrome(options = my_options,)



# 建立資料夾
folderPath = '591_data'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 放置爬取的資料
listData = []



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
    

# 滾動頁面
def scroll():
    innerHeight = 0  # 瀏覽器內部的高度
    offset = 0       # 當前捲動的量(高度)
    count = 0        # 累計無效滾動次數
    limit = 3        # 最大無效滾動次數

    # 在捲動到沒有元素動態產生前，持續捲動
    while count <= limit:
        # 每次移動高度
        offset = driver.execute_script('return document.documentElement.scrollHeight;')

        # 捲軸往下滑動
        driver.execute_script(f'''
            window.scrollTo({{
                top:{offset},
                behavior:'smooth'
            }});
        ''')

        # 強制等待，此時若有新元素生成，瀏覽器內部高度會自動增加
        sleep(5)
        
        # 透過執行 js 語法來取得捲動後的當前總高度
        innerHeight = driver.execute_script('return document.documentElement.scrollHeight;')
        
        # 經過計算，如果滾動距離(offset)大於等於視窗內部總高度(innerHeight)，代表已經到底了
        if offset == innerHeight:
            count += 1

        # 測試用，捲動超過一定的距離，就結束程式
        # if offset >= 600:
        #     break

# 爬取資料
def scrape_data():
    # 使用全域變數
    global listData
    
    # 清空存放資料的變數
    listData.clear()

    # 取得主要元素的集合
    elements = driver.find_elements(By.CSS_SELECTOR,'a.community-card')

    for card in elements:
        print("=" * 30)

        name = card.find_element(By.CSS_SELECTOR, 'h3 em[data-v-c7d6a2ce]').get_attribute('innerText')

        try:
            address = card.find_elements(By.CSS_SELECTOR, 'p em[data-v-c7d6a2ce]')[1].get_attribute('innerText')
        except:
            address = card.find_elements(By.CSS_SELECTOR, 'p em[data-v-c7d6a2ce]')[-1].get_attribute('innerText')

        try:
            price = card.find_element(By.CSS_SELECTOR, 'span.price-info').get_attribute('innerText')
        except NoSuchElementException:
            price = "未提供價格"

        link = card.get_attribute('href')
        
        print(name)
        print(address)
        print(price)
        print(link)

        listData.append({
            "名稱": name,
            "地址":address,
            "價格":price,
            "網址":link
        })

# 將 list 存成 json
def saveJSON():
    with open(f"{folderPath}/591_data.json", "w", encoding='utf-8') as file:
        file.write( json.dumps(listData, ensure_ascii=False, indent=4) )


# 將 list 存成 csv
def saveCSV():
    # 讀取 JSON 資料
    with open(f"{folderPath}/591_data.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    # 將 JSON 資料轉換為 DataFrame
    df = pd.DataFrame(data)
    
    # 儲存為 CSV 文件
    df.to_csv(f"{folderPath}/591_data.csv", index=False, encoding='utf-8-sig')



if __name__ == '__main__':
    visit()
    print("==完成載入網頁=="*5)
    button()
    print("==完成彈跳資訊=="*5)
    filter()
    print("==完成篩選地區=="*5)
    scroll()
    print("==完成滾動網頁=="*5)
    scrape_data()
    print("==完成爬取資料=="*5)
    saveJSON()
    print("==完成儲存JSON=="*5)
    saveCSV()
    print("==完成儲存CSV=="*5)


# 關閉瀏覽器
driver.quit()
