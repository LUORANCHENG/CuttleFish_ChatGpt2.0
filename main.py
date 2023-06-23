import os
import datetime
from loguru import *
from tools.null import main as null
from tools.cleartemp import main as clear
from tools.get_cookies import main as get_cookies
from tools.login import main as login
from tools.create_temp_folder import main as create_f
from tools.write_and_upload import main as write_and_upload
from concurrent.futures import ThreadPoolExecutor
from tools.article_log import create_article_log
from tools.get_path import get_article_log_path
from tools.write_log import main as write_log
import threading
import time

# 部分参数
params = {

    # 最大文章数量 这个没啥用 还没写 现在只会跑满
    "max_article": 100,

    # 文章种类排序
    "sort": ['生活娱乐', '实用模板', '行业资料', '互联网', '推荐', '基础教育', '学前教育', '高校与高等教育', '语言/资格考试', '建筑', '商品说明书', '政务民生', '法律'],
    # "sort":['基础教育','学前教育','高校与高等教育','推荐','实用模板','语言/资格考试','建筑'],

    # 是否显示浏览器窗口 True为显示,False为不显示
    "display": False,

    # 是否使用用户名作为消息提醒开启则为用户名,关闭则为账号提示(用于提醒每个账号在干嘛便于监控)
    "use_name": True,

    # 标题信息显示 True会显示爬取到的标题是否为好标题(未被过滤机制过滤)
    "title_info": False,

    # 备份开关,true为开启备份,false为不开启
    "backup_switch": False,

    # 自动关机,true为跑完自动关机,false为不关机
    "shutdown": False,

    # 是否上传pdf格式的文件 多线程自动关闭
    "use_pdf": False,

    # 多线程开关 True为开启多线程 False为关闭
    "Multithreading": True,

    # 线程数 同时跑多少个账号
    "num": 4,

    #写入日志(包含每个账号运行时产生的各种信息)
    "log":True
}


# 处理用户名缺失值
null()
# 获取账号cookie 返回各个账号cookie的地址
cookies = get_cookies()
for cookie in cookies:
    create_f(cookie,params)
clear()

def main(cookie, params):
    # 登录并进入后台,返回网页对象
    web, name = login(cookie, params)
    # 创建article_log文件夹
    create_article_log(name)

    # 写文章加上传 返回判断 如果写完了或者到达上传上限break
    situ, driver = write_and_upload(web, params, name)
    #judge = write_and_upload(web,params['sort'])
    if situ == 1:
        info = f'{name}:所有分类任务爬取完毕,未满100篇'
        logger.warning(info)
        write_log(name, info, params)
        driver.quit()
        exit()
    elif situ == 2:
        info = f'{name}:已满100篇,停止上传'
        logger.warning(info)
        write_log(name, info, params)
        driver.quit()
        exit()
    elif situ == 3:
        info = f'{name}:出现异常过多,请检查'
        logger.warning(info)
        write_log(name, info, params)
        driver.quit()
        exit()



if params['Multithreading']:
    #params['use_pdf'] = False
    with ThreadPoolExecutor(params['num']) as t:
        # 对每个账号操作
        for cookie in cookies:
            t.submit(main, cookie=cookie, params=params)
else:
    # 对每个账号操作
    for cookie in cookies:
        main(cookie, params)


if params['shutdown']:
    logger.info('所有账号任务已完成,将在10秒后关机')
    os.system('shutdown -s -t 10')
