import csv
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expe_conditon

# 读取账号csv文件写出的文件
csv_account_path = "account.csv"
account_cookies_path = "cookies.txt"
# 需要配置文件路径
accounts = []
# 驱动位置
chrome_driver = 'drivers/chromedriver'
# 访问网址
cuttlefish_url = 'https://cuttlefish.baidu.com/'
# 登陆网站，生成cookie信息
def login_baidu(login_uname, login_pwd):
    driver = webdriver.Chrome()
    driver.get(cuttlefish_url)
    try:
        # 登陆
        login_icon = WebDriverWait(driver, 10).until(
            expe_conditon.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[2]/div[1]/a')))

        login_icon.click()

        # 输入账号
        login_name_icon = WebDriverWait(driver, 10).until(
            expe_conditon.presence_of_element_located((By.XPATH, '//*[@id="TANGRAM__PSP_11__userName"]')))
        login_name_icon.send_keys(login_uname)
        driver.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_11__password"]').send_keys(login_pwd)
        driver.find_element(By.XPATH, '//*[@id="TANGRAM__PSP_11__submit"]').click()
        # time.sleep(50)
        input('验证完毕后按任意键继续')
        account_cookies = driver.get_cookies()

        # 创建一个账户对象 然后写出json
        account_cookies_path = os.path.join('cookies/',  "cookies_"+login_uname+".txt")
        with open(account_cookies_path, 'w') as f:
            f.write(json.dumps(account_cookies))
        print(f"{login_uname}的cookies保存成功！保存到：{account_cookies_path}")
    except Exception as e:
        print("Fail:自动读取账号"+login_uname+"账户失败", e)
    finally:
        driver.quit()


# 不断读取账户信息 准备写出
def main(name,password):
    login_baidu(name,password)


# 启动写出cookie程序
if __name__ == "__main__":
    main()
