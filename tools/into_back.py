import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tools.get_time_now import get_time
from tools.write_log import main as write_log

def close_window_handler(driver: webdriver.Chrome, xpath: str):
    try:
        close_window = driver.find_element(By.XPATH, xpath)
        close_window.click()
    except Exception as e:
        pass

def into_back(driver: webdriver.Chrome,name,params):
    info = f"{name}: 进入后台中"
    print(info)
    write_log(name,get_time()+' '+info,params)
    time.sleep(1)
    driver.get('https://cuttlefish.baidu.com/shopmis?_wkts_=1672510169727#/taskCenter/majorTask')

    time.sleep(1)
    # 将弹出的提示消息关闭 这里可能存在的弹出框有两种 一种是完成新手任务的提示框 一种是未完成签署协议的
    info = '关闭弹窗中'
    print(info)
    write_log(name,get_time()+' '+info,params)
    close_window_handler(driver, '//*[@id="app"]/div[1]/section/main/div[3]/div/div/div[3]/span/button')
    close_window_handler(driver, '//*[@id="app"]/div[1]/section/main/div[3]/div/div/div[1]/button')
    info = '弹窗关闭完成'
    print(info)
    write_log(name,get_time()+' '+info,params)
    time.sleep(1)

    # 模拟点击创作中心
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/aside/ul/li[2]/ul/li/ul/li/span').click()
    #driver.execute_script("document.body.style.zoom='0.8'")  # 缩小浏览器

def main(driver,name,params):
    into_back(driver,name,params)