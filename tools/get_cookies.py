import pandas as pd
import os
from tools.write_cookies import main as write_cookie

def get_cookies():
    #账号池
    cookies = []
    cookies_path = 'cookies'
    acs = {}
    f = pd.read_csv('account.csv',encoding='utf-8')
    for i in range(f.shape[0]):
        acs[f['账号'][i]] = f['密码'][i]

    cookies_name = os.listdir(cookies_path)
    for ac in acs.keys():
        cookies.append(f'cookies/cookies_{str(ac)}.txt')
        if f'cookies_{str(ac)}.txt' in cookies_name:
            print(f'{str(ac)}的cookie已经存在')
            continue
        write_cookie(str(ac),acs[ac])
        print(f'{str(ac)}的cookie保存成功!保存为cookies/{str(ac)}.txt')
    return cookies

def main():
    return get_cookies()