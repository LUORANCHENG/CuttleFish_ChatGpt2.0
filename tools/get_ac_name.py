import pandas as pd


def get_name():
    dic1 = {}
    dic2 = {}
    f = pd.read_csv('account.csv', encoding='utf-8')
    for i in range(f.shape[0]):
        dic1[str(f['用户名'][i])] = str(f['账号'][i])#用户名:账号的字典
    for i in range(f.shape[0]):
        dic2[str(f['账号'][i])] = str(f['用户名'][i])#账号:用户名的字典
    return dic1,dic2

# 返回字典
def main():
    dic1,dic2 = get_name()
    return dic1,dic2

if __name__ == '__main__':
    dic1,_ = main()
    _,dic2 = main()
    print(dic1)
    print(dic2)
