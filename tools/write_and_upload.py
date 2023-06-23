import time
import json
import os
import shutil
from loguru import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from tools.article import main as article
from tools.webtool import goto_sort
from tools.webtool import get_max_page
from tools.webtool import goto_page
from tools.upload_number import main as upload_number
from tools.titleselect import main as is_good_title
from tools.upload import main as upload
from tools.get_time_now import get_time
from tools.get_ac_name import get_name
from tools.write_log import main as write_log
from tools.get_path import get_article_log_path
import csv
from tools.article_log import write_article_log
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support import expected_conditions as expe_conditon

# 获得标题和序号的信息
def get_info(driver):
    dic = {}
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[3]/div[@class="content"]/div[@class="doc-row"]/div[1]/div[1]/span')))
    infos = driver.find_elements(
        By.XPATH, '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[3]/div[@class="content"]/div[@class="doc-row"]/div[1]/div[1]/span')
    for i in range(int(len(infos)/2)):
        dic[infos[2*i+1].text] = int(infos[2*i+0].text)
    return dic
    pass


# 获取指定序号的上传按钮
def get_upload_bottom(driver, numb, name,params):
    xpath = '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[3]/div[@class="content"]/div'
    try:
        button = driver.find_element(
            By.XPATH, f'{xpath}[{str(numb)}]/div[2]/div/button')
    except:
        info = '没有找到上传按钮,该任务可能已经被完成,或者请检查xpath路径是否正确'
        logger.info(info)
        write_log(name, get_time()+' '+info,params)
        button = None
    return button


def write_and_upload(driver: webdriver, params: dict, name: str):

    dic, _ = get_name()
    path = f'{get_article_log_path()}/{dic[name]}.csv'
    sorts = params['sort']
    exam = 0  # 用于判断异常是否过多
    full = 0  # 用于判断是否传到上限
    for sort in sorts:
        if sort == ' ':
            info = f'{name}: 所有任务已经爬取完成'
            logger.info(info)
            write_log(name, get_time()+' ' + info,params)
            return 1

        if full == 1:
            return 2

        if exam == 1:
            return 3
        info = f'{name}: 当前爬取的种类是{sort}'
        logger.info(info)
        write_log(name, get_time()+' ' + info,params)
        goto_sort(driver, sort)
        time.sleep(2)
        div_class = driver.find_element(
            By.XPATH, '/html/body/section/div[1]/section/main/div[1]/div[2]/div[3]')
        # logger.info(div_class.text)
        if div_class.text == "尊敬的创作者，当前分类任务已被其他作者抢先占领，平台正加急补充任务中，请耐心等待":
            info = f'{name}: 当前分类没有任务,跳过'
            logger.info(info)
            write_log(name, get_time()+' ' + info,params)
        else:
            next_page = driver.find_element(
                By.XPATH, '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[4]/div/button[2]/i')
            max_page = get_max_page(driver, sort)
            for page in range(1, int(max_page)+1):
                if exam == 1 or full == 1:
                    break
                try:
                    goto_page(driver, page)
                    info = f'{name}: 正在爬取 {sort} 类的第{str(page)}页'
                    logger.info(info)
                    write_log(name, get_time()+' ' + info,params)
                    time.sleep(1)
                    infos = get_info(driver)  # 返回这一页的标题:序号的字典(未被完成的)
                except Exception as e:
                    print(str(e))
                    logger.warning(f"{name}: 获取第{str(page)}页标题时发生异常，跳过该页")
                    continue
                for title in infos.keys():  # 遍历该页每一个标题
                    article_label = 0
                    with open(path, mode='r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)  # 以字典的方式进行读取，返回的是一个迭代器
                        for item in reader:
                            title_record = item['title']
                            label_record = item['label']
                            if title_record == title and label_record == '1':
                                info = f"关于《{title}》的文章已经上传过了，执行下一个任务"
                                logger.info(info)
                                write_log(name, get_time() + ' ' + info, params)
                                article_label = 1
                                break
                    if article_label == 1:
                        continue
                    if is_good_title(name, title, params):
                        # 写文章 返回值为是否出错，0为没有错误,1为错误过多
                        exam = article(title, params, name)
                        if exam == 1:  # 如果错误过多,返回检查
                            break


                        # 上传并返回创作中心 返回值为判断是否满100篇
                        full, label = upload(driver, title, infos[title], name, params)
                        if full == 1:  # 如果传满,返回传满
                            break

                        write_article_log(name, title, label)  # 写入数据

                        # 判断该账号写了多少篇了 返回篇数
                        number = upload_number(name)
                        info = f'{name}: 今日已经上传{number}篇'
                        logger.info(info)
                        write_log(name, get_time()+' ' + info,params)

                        # 返回当前种类
                        goto_sort(driver, sort)

                        # 返回当前页码
                        goto_page(driver, page)

                        # shutil.rmtree(f'temp/{params["account_name"]}')
                        # os.mkdir(f'temp/{params["account_name"]}')
                    else:
                        if params['title_info']:
                            info = f'{name}: {title}不是好标题'
                            logger.info(info)
                            write_log(name,get_time()+' ' + info,params)
                        pass
                time.sleep(2)
        time.sleep(5)
    pass


def main(driver, params, name):
    params['sort'].append(' ')
    situ = write_and_upload(driver, params, name)
    return situ, driver
