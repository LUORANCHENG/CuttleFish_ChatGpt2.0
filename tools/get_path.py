import json

def get_settings():
    f = open('conf/settings.json','r',encoding='utf-8')
    settings = json.loads(f.read())
    return settings

def get_temp_path():
    settings = get_settings()
    return settings['path']['temp_path']

def get_backup_path():
    settings = get_settings()
    return settings['path']['backup_path']

def get_log_path():
    settings = get_settings()
    return settings['path']['log_path']

def get_article_log_path():
    settings = get_settings()
    return settings['path']['article_log_path']
