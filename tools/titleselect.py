import re
from loguru import logger
import json
from typing import List
from tools.write_log import main as write_log
from tools.get_time_now import get_time

f = open('conf/settings.json','r',encoding='utf-8')
settings = json.load(f)
ignore_words = settings['ignore_words']

def is_contains_words(s: str, words: List[str]) -> bool:
    for word in words:
        if s.find(word) != -1:
            return True
    return False

def is_rare_name(string):
    cop = re.compile(u"[~!@#$%^&* ]")
    match = cop.search(string)
    if match:
        return True
    try:
        string.encode('gb2312')
    except UnicodeEncodeError:
        return True
    return False

def get_stroke(c):
    # 如果返回 0, 则也是在unicode中不存在kTotalStrokes字段
    strokes = []
    with open(strokes_path, 'r') as fr:
        for line in fr:
            strokes.append(int(line.strip()))
 
    unicode_ = ord(c)
 
    if 13312 <= unicode_ <= 64045:
        return strokes[unicode_-13312]
    elif 131072 <= unicode_ <= 194998:
        return strokes[unicode_-80338]
    else:
        #print("想要查看 ",c," 的笔画,它应该是一个CJK字符,或者该字符应该在字典中.")
        return -1
strokes_path = 'tools\\strokes.txt'


def judge(name, title, params):

    skip = 0
    cop = re.compile("[\u4e00-\u9fa5]")
    a = ''.join(re.findall(cop,title))
    if len(a) == 0:
        info = f'{name}: {title}:不含中文,跳过'
        logger.info(info)
        write_log(name, get_time() + ' ' + info, params)
        # 匹配非汉外的其他字符
        return False

    else:
        for string in a:
            if is_rare_name(string):
                info = f'{name}: {title}:含有生僻字{string},跳过'
                logger.info(info)
                write_log(name, get_time() + ' ' + info, params)
                skip = 1
                break 
            if get_stroke(string) != -1:
                if get_stroke(string) >= 25:
                    info = f'{name}: {title}:标题中含笔画过多的汉字“{string}”跳过'
                    logger.info(info)
                    write_log(name, get_time() + ' ' + info, params)

                    skip = 1
                    break

    if skip == 1:
        return False
        
    number = re.findall(r"\d+\.?\d*", title)
    if number != []:
        # print("数字")
        if len(''.join([str(r) for r in number])) > 4:
            return False

    cop = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')
    a = ''.join(re.findall(cop,title))
    if len(a) > 0:
        info = f'{name}: {title}:含日文或韩文,跳过'
        logger.info(info)
        write_log(name, get_time() + ' ' + info, params)
        return False

    if len(title) < 6:
        # 标题长度不得小于5个字
        info = f'{name}: {title}:标题太短,跳过'
        logger.info(info)
        write_log(name, get_time() + ' ' + info, params)
        return False
    if is_contains_words(title, ignore_words):
        # 忽略标题含有某些字或字段
        info = f'{name}: {title}:标题中含过滤字,跳过'
        logger.info(info)
        write_log(name, get_time() + ' ' + info, params)
        return False
    return True
    pass

def main(name, title, params):
    return judge(name, title, params)

if __name__ == '__main__':
    print(judge(title="一二三四"))
    print(judge(title="一二三四五六"))
    print(judge(title="yieasdar"))
    print(judge(title="我爱你宝贝"))