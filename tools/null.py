import pandas as pd

def null():
    f = pd.read_csv('account.csv', encoding='utf-8')
    a = 0
    for i in range(f.shape[0]):
        if pd.isnull(f['用户名'][i]):
            a += 1
            f['用户名'][i] = f'未命名账号{str(a)}'
    f.to_csv('account.csv',encoding='utf-8',index=False)

def main():
    null()

if __name__ == '__main__':
    main()