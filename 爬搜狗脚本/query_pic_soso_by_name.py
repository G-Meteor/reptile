# -*- coding: utf-8 -*- 
import re
import requests
import os
import sys
import traceback
import threading
from queue import Queue

THREAD_NUM=10
headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Upgrade-Insecure-Requests': '1'
            }

def download_pics(urls, headers, cate):
    count = 0
    if not os.path.exists(cate):
        os.makedirs(cate)
    for url in urls:
        try:
            res = requests.get(url, headers=headers)
            with open(os.path.join(cate, f'{word}_{count}.jpg'), 'ab') as f:
                f.write(res.content)
                count += 1
                print('download to ', os.path.join(cate, f'{word}_{count}.jpg'))
        except:
            print('failed to down', url)
            traceback.print_exc()

def download_pic(url, headers, cate, count):
    # count = 0
    if not os.path.exists(cate):
        os.makedirs(cate)
    try:
        res = requests.get(url, headers=headers)
        with open(os.path.join(cate, f'{cate}_{count}.jpg'), 'ab') as f:
            f.write(res.content)
            # count += 1
            print('download to ', os.path.join(cate, f'{cate}_{count}.jpg'))
    except:
        print('failed to down', url)
        traceback.print_exc()


def img_urls(word, search_num=1):
    all_urls = []
    for i in range(0, search_num*48, 48):
        url = 'https://pic.sogou.com/pics?query={0}&mode=1&start={1}&reqType=ajax&reqFrom=result&tn=0'.format(word, i)
        response = requests.get(url, headers=headers)
        url_list = re.findall('"thumbUrl":"(.*?)"', response.text)
        if len(url_list) == 0:
            print('no pic')
            continue
        print(url_list)
        all_urls.extend(url_list)
    return all_urls
        # download_pic(all_urls, headers, word)

line_list = []
with open('name2.txt', encoding='utf-8') as file:
    line_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格

result = dict()
for word in line_list:
    imgs = img_urls(word, 2)
    result[word] = imgs

print(result)
q = Queue()
for k, v in result.items():
    # q.put((k, v), False) # k --search_name, v, urls
    count = 0
    for url in v:
        count += 1
        q.put((k, url, count), False)

def consumer(qu):
    while not qu.empty():
        name, url, count = qu.get(False)
        download_pic(url, headers, name, count)

tasks=[]
for i in range(THREAD_NUM):
    t = threading.Thread(target=consumer, args=(q,))
    t.setDaemon(True)
    t.start()
    tasks.append(t)

for t in tasks:
    t.join()
print('当前搜索结束，感谢使用')
