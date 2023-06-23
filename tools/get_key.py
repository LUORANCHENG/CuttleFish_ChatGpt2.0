import json

def get_key():
    f = open('conf/settings.json','r',encoding='utf-8')
    setting = json.loads(f.read())
    return setting['openai']['api_key']

def main():
    key = get_key()
    return key

if __name__ == '__main__':
    main()