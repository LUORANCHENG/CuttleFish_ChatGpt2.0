import os
import datetime
from tools.get_path import get_log_path,get_settings
from tools.get_ac_name import get_name
def write(name,info):
    time = str(datetime.date.today())
    path = f'{get_log_path()}/{time}/{name}.txt'
    dic,_ = get_name()
    if not os.path.exists(path):
        path = f'{get_log_path()}/{time}/{dic[name]}.txt'
    with open(path,mode='a+',encoding = 'utf-8') as f:
        f.write(info)
        f.write('\n')
        f.close()
    pass


def main(name,info,params):
    if params['log']:
        write(name,info)
    else:
        pass