# coding:utf-8

import json
import time

from code import interact

from app.utils.logger import logger


import app.core.varspool.storage as storage
print(storage.vars)
exit()


logger.info("test")
logger.debug("test")
logger.warning("test")
logger.error("test")
logger.critical("test")
print(logger.name)

exit()

while True:
    time.sleep(3)
    with open('stop.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
    if data.get("stop"):
        break

exit()

def play(a:str):
    
    if a[:2] == "gr":
        print(a)
        if a[-1] in "23":
            exec_times = int(a[-1])
        else:
            exec_times = 1
        for i in range(exec_times):
            print("graze!")
    elif a[:2] == "sk":
        print(a)
        for skill in list(a[2:]):
            print(skill)



# Open and read the JSON file
with open('assets/battlescript/1.json', 'r', encoding='UTF-8') as file:
    data = json.load(file)

# Print the data
print(data)

d1 = data.get("difficulty")
a = data.get("actions") #dict
start_area = "area1"
b_area_matched = False
for area, rec in a.items():
    if (not b_area_matched) and (area == start_area):
        b_area_matched = True
    if not b_area_matched:
        continue
    print("Replaying ", area)
    for line in rec:
        print(line)
        if isinstance(line, str):
            for act in line.split():
                play(act)

exit()

x1 = 1
while True:
    match x1:
        case 1:
            print(x1)
            l1 = [1,2,3]
        case 2:
            print(x1)
            print(l1)
        case 3:
            break
    x1 += 1
    

exit()

with open('./MLW-config.json', 'r', encoding='UTF-8') as file:
    conf = json.load(file)
print(conf)


exit()




#interact(local=locals())
