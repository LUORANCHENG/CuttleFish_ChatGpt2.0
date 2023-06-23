import datetime 

with open('1.txt','a+',encoding='utf-8') as f:
    f.write(str(1))
    f.write('\n')
    f.close

with open('1.txt','a+',encoding='utf-8') as f:
    f.write(str(2))
    f.close