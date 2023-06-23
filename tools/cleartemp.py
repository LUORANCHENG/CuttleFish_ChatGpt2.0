import shutil
import os
from tools.get_path import get_temp_path
import datetime

def main():
    # 所有文件的列表
    docxslst = []
    time = datetime.date.today()
    path = get_temp_path()
    folders = os.listdir(path)
    for folder in folders:
        folder_path = f'{path}/{folder}'
        for _, _, docxs in os.walk(folder_path):
            for docx in docxs:
                docx_path = f'{folder_path}/{docx}'
                docxslst.append(docx_path)
    for docx in docxslst:
        docx_time = datetime.date.fromtimestamp((os.path.getmtime(docx)))
        if docx_time < time:
            os.remove(docx)
            pass
    

if __name__ == '__main__':
    main()