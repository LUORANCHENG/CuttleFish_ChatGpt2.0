import datetime 

def get_time():
    return str(datetime.datetime.now()).split(' ')[1].split('.')[0]