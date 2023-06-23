import os
from tools.get_path import get_temp_path
from tools.get_ac_name import main as get_name


def upload_number(name):
    dic,_ = get_name()
    path1 = get_temp_path()
    path = f'{path1}/{name}'
    if not os.path.exists(path):
        path = f'{path1}/{dic[name]}'
    number = len(os.listdir(path))
    return number

def main(name):
    return upload_number(name)

if __name__ == '__main__':
    print(main('15178791525'))