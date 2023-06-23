import json
from tools.get_path import get_settings


def change_key():
    settings = get_settings()
    used_key = settings['openai']['api_key']
    key = settings['openai']['api_keys'][0]
    settings['openai']['api_keys'].remove(settings['openai']['api_keys'][0])
    settings['openai']['api_key'] = key
    settings['openai']['used_keys'].append(used_key)
    #print(settings['openai']['api_keys'])
    with open('conf/settings.json','w',encoding='utf-8') as f:
        json.dump(settings, f, indent=2, sort_keys=True, ensure_ascii=False)
    pass

def main():
    change_key()

if __name__ == '__main__':
    main()