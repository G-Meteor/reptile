# -*- coding: utf-8 -*-
import re
import requests
from urllib import error
from bs4 import BeautifulSoup
from xpinyin import Pinyin
import os

num = 0
numPicture = 0
file = ''
List = []


def Find(url, A):
    global List
    print('正在检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            # 这里搞了下
            Result = A.get(Url, timeout=7, allow_redirects=False)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('url=https:(.*?)"', result, re.S)  # 先利用正则表达式找到图片url
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s


def recommend(url):
    Re = []
    try:
        html = requests.get(url, allow_redirects=False)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re


def dowmloadPicture(html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    print(pic_url)
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            # string = file + r'\\' + Pinyin().get_pinyin(keyword) + '_' + str(num) + '.jpg'
            string = os.path.join(file, Pinyin().get_pinyin(keyword) + '_' + str(num) + '.jpg')
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return

def dowmloadPicture2(html, keyword):
    global num
    # t =0
    pic_url = re.findall('url=https:(.*?)"', html, re.S)  # 先利用正则表达式找到图片url
   # pic_url =
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    print(pic_url)
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，'+ keyword + '的图片地址:  https:' + str(each))
        try:
            if each is not None:
                each="https:"+each
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            # string = file + r'\\' + Pinyin().get_pinyin(keyword) + '_' + str(num) + '.jpg'
            string = os.path.join(file, Pinyin().get_pinyin(keyword) + '_' + str(num) + '.jpg')
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return

if __name__ == '__main__':  # 主函数入口
    import sys

    numPicture = 150
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]} name.txt")
        print(f"{sys.argv[0]} name.txt 100")
        sys.exit(1)
    name_file = sys.argv[1]
    if len(sys.argv) == 3:
        numPicture = int(sys.argv[2])

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Upgrade-Insecure-Requests': '1'
    }

    A = requests.Session()
    A.headers = headers

    tm = numPicture
    line_list = []
    with open(name_file, encoding='utf-8') as file:
        line_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格

    for word in line_list:
        url = 'https://pic.sogou.com/d?query=' + word + '&did='
        #tot = Find(url, A)
        Recommend = recommend(url)  # 记录相关推荐
        #print('经过检测%s类图片共有%d张' % (word, tot))
        file = word
        y = os.path.exists(file)
        if y == 1:
            print('该文件已存在，请重新输入')
            file = word + '_sougou'
            os.mkdir(file)
        else:
            os.mkdir(file)
        t = 0
        tmp = url
        while t <= 150:
            try:
                url = tmp + str(t)
                # result = requests.get(url, timeout=10)
                # 这里搞了下
                result = A.get(url, timeout=10, allow_redirects=False)
                print(url)
                dowmloadPicture2(result.text, word)
                t = t + 50
            except error.HTTPError as e:
                print('网络错误，请调整网络后重试')
                t = t + 50
            #else:
               # if(t==0):
                   # print(result.text)

        numPicture = numPicture + tm


    print('当前搜索结束，感谢使用')
