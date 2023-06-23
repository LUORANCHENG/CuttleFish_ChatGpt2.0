import os
import datetime
from tools.get_path import get_temp_path,get_log_path
from tools.get_ac_name import main as get_name

def creat_temp(cookie):
    path = get_temp_path()
    name = cookie.strip(".txt").split("_")[1]
    path = f'{path}/{name}'
    if not os.path.exists(path):
        os.mkdir(path)
    pass

def create_log(cookie):
    name = cookie.strip(".txt").split("_")[1]
    path = f'{get_log_path()}/{str(datetime.date.today())}'
    if not os.path.exists(path):
        os.mkdir(path)
    with open(f'{path}/{name}.txt','a+',encoding='utf-8') as f:
        f.write('\n')
        f.close()
    pass

def main(cookie,params):
    creat_temp(cookie)
    if params['log']:
        create_log(cookie)