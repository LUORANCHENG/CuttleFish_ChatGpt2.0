from tools.get_path import get_article_log_path
from tools.get_ac_name import get_name
import datetime
import os

def create_article_log(name):
    dic, _ = get_name()
    path = f'{get_article_log_path()}/{dic[name]}.csv'
    if not os.path.exists(path):
        with open(path, mode="w", encoding='utf-8') as f:
            f.writelines("title,label,time\n")



def write_article_log(name, title, label):
    time = str(datetime.date.today())
    dic, _ = get_name()
    path = f'{get_article_log_path()}/{dic[name]}.csv'
    with open(path, mode='a+', encoding='utf-8') as f:
        f.write(f'{title},{label},{time}\n')



