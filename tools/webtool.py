import csv
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expe_conditon

#去往浏览器底部
def goto_buttom(driver: webdriver.Chrome):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

#去往浏览器顶部
def goto_top(driver: webdriver.Chrome):
    driver.execute_script("var q=document.documentElement.scrollTop=0")

def get_sort_page(driver:webdriver,sort:str):
    pass

# 浏览器设置页面缩小
def zoom_in(driver: webdriver.Chrome):
    driver.execute_script("document.body.style.zoom='0.5'")

#跳转到指定类别
def goto_sort(driver:webdriver.Chrome,sort:str):
    zoom_in(driver)
    divs = driver.find_elements(By.XPATH,'/html/body/section/div[1]/section/main/div[1]/div[2]/div[2]/div[2]/div/div/div/div')
    for div in divs:
        if div.text == sort:
            driver.execute_script("$(arguments[0]).click()", div)
            break
    pass

#跳转到指定页码
def goto_page(driver:webdriver.Chrome,page:int):
    WebDriverWait(driver, 10).until(expe_conditon.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[4]/div/span/div/input')))

    input = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[4]/div/span/div/input')
    input.clear()
    input.clear()
    input.send_keys(page)
    input.send_keys('\n')
    pass

def get_max_page(driver:webdriver.Chrome,sort:str):
    max_page = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[4]/div/span/div/input').get_attribute('max')
    return max_page