from selenium.webdriver.common.by import By
from tools.get_path import get_temp_path
import time
import os
from loguru import *
from tools.to_pdf import main as to_pdf
from tools.get_ac_name import main as get_name
from tools.get_time_now import get_time
from tools.write_log import main as write_log
# 寻找上传按钮


def get_up_button(driver, numb, name, params):
    select = 1  # 默认左边
    xpath = '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[3]'
    if numb > 10:
        numb = numb - 10
        select = 3  # 选到右边
    try:
        button = driver.find_element(
            By.XPATH, f'{xpath}/div[{str(select)}]/div[{str(numb)}]/div[2]/div[1]/button')
    except:
        info = f'没有找到上传按钮'
        logger.info(info)
        write_log(name, get_time()+' '+info, params)
        button = None
    return button

# 上传按钮不可用的情况
def is_task_finish(driver, title, numb, name, params):
    select = 1  # 默认左边
    xpath = '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[3]'
    if numb > 10:
        numb = numb - 10
        select = 3  # 选到右边

    tips = driver.find_element(By.XPATH, f'{xpath}/div[{str(select)}]/div[{str(numb)}]/div/div[2]/span[2]')
    tips_html = tips.get_attribute('outerHTML')
    # print(tips_html)
    if "style" in tips_html:
        # 如果可以找到style元素，则表示任务还没有被完成
        return True
    else:
        # 如果找不到style元素，则表示任务已被完成
        info = f"{name}: 关于《{title}》的文章已被完成，跳过"
        logger.info(info)
        write_log(name, get_time()+' '+info, params)
        return False


# 提交信息丢失的窗口:
def get_lost_button(driver):
    button = None
    try:
        button = driver.find_element(
            By.XPATH, '/html/body/div[5]/div/div/div[2]/div[3]/button')
    except:
        pass
    return button

# 被其他人完成的窗口
def get_fail_button(driver):
    button = None
    try:
        button = driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div[2]/div[3]/button')
    except:
        pass
    return button

# 上传成功的窗口
def get_ok_button(driver):
    button = None
    try:
        button = driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[2]/div[3]/button')
    except Exception as e:
        pass
        # logger.info(str(e))
    return button


def get_submit_button(driver):
    button = None
    button = driver.find_element(
        By.XPATH, '//*[@id="app"]/div[1]/section/main/div[1]/div/div[3]/div[2]/button')
    return button


def get_upload_bottom(driver, numb):
    select = 1
    xpath = '//*[@id="app"]/div[1]/section/main/div[1]/div[2]/div[3]'
    if numb > 10:
        numb = numb - 10
        select = 3
    try:
        button = driver.find_element(
            By.XPATH, f'{xpath}/div[{str(select)}]/div[{str(numb)}]/div[2]/div/div/input')
    except:
        button = None
    return button


def upload(driver, title, numb, name, params):
    label = 0
    # 获取用户名和账号对应关系
    dic, _ = get_name()
    path = f'{get_temp_path()}/{name}/{title}.docx'
    if not os.path.exists(path):
        path = f'{get_temp_path()}/{dic[name]}/{title}.docx'
    upload_file = path
    if params['use_pdf']:
        info = f'{name}: 正在将文章转化为pdf格式'
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        while True:
            try:
                to_pdf(upload_file)  # 转化成pdf
            except Exception as e:
                print(str(e))
                time.sleep(3)
                pass
            else:
                break
        os.remove(upload_file)  # 删除word格式
        upload_file = f'{path.strip(".docx")}.pdf'
    input = get_upload_bottom(driver, numb)
    if input != None:
        info = f"{name}: 正在上传文章  {title}"
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        button = get_up_button(driver, numb, name, params)
        driver.execute_script("$(arguments[0]).click()",button)
        time.sleep(3)
        input.send_keys(upload_file)
        info = f'{name}: 文章上传完成  {title}'
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        time.sleep(6)

        info = f'{name}: 正在尝试提交'
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        button = get_submit_button(driver)
        driver.execute_script("$(arguments[0]).click()",button)
        time.sleep(5)
        info = f'{name}: 正在关闭窗口'
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        button = get_ok_button(driver)
        if button != None:
            driver.execute_script("$(arguments[0]).click()",button)
            info = f'{name}: 提交成功!'
            logger.info(info)
            write_log(name,get_time()+' '+info,params)
            label = 1
        else:
            button = get_fail_button(driver)
            if button != None:
                info = f'{name}: 提交失败,该任务已经被其他人完成'
                logger.info(info)
                write_log(name,get_time()+' '+info,params)
                driver.execute_script("$(arguments[0]).click()",button)
            else:
                button = get_lost_button(driver)
                if button != None:
                    info = f'{name}: 提交失败,提交信息丢失'
                    logger.info(info)
                    write_log(name,get_time()+' '+info,params)
                    driver.execute_script("$(arguments[0]).click()",button)
        info = f'{name}: 窗口关闭完成'
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        time.sleep(5)

        info = f'{name}: 正在返回创作中心'
        logger.info(info)
        write_log(name,get_time()+' '+info,params)
        button = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/aside/ul/li[2]/ul/li/ul/li/span')
        driver.execute_script("$(arguments[0]).click()", button)
        time.sleep(5)
    else:
        is_task_finish_flag = is_task_finish(driver, title, numb, name, params)
        if is_task_finish_flag:
            return 1, label
    return 0, label


def main(driver, title, numb, name, use_pdf):
    return upload(driver, title, numb, name, use_pdf)
