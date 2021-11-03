# -*- coding = utf-8 -*-
# @Time : 2021/5/25 12:21
# @Author : zgx
# @File : innovation(创新创业).py
# @Software : PyCharm

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import urllib
import wget


def main():


    # url ="http://www.lnpu.edu.cn/research.jsp?a23014t=124&a23014p=1&a23014c=15&a23014i=%E5%88%9B%E6%96%B0%E5%88%9B%E4%B8%9A&wbtreeid=12709&entrymode=1&researchvalue=false&condition=-1&INTEXT2=5Yib5paw5Yib5Lia&news_search_code=&wbtreeids=0&INTEXT="
    # pageList = getLink(url)
    # print(pageList)

    innoList = []
    for i in range(1, 125):
        url = "http://www.lnpu.edu.cn/research.jsp?a23014t=124&a23014p=" + str(i) + "&a23014c=15&a23014i=%E5%88%9B%E6%96%B0%E5%88%9B%E4%B8%9A&wbtreeid=12709&entrymode=1&researchvalue=false&condition=-1&INTEXT2=5Yib5paw5Yib5Lia&news_search_code=&wbtreeids=0&INTEXT="
        # "http://www.lnpu.edu.cn/research.jsp?a23014t=1714&a23014p="+str(i)+"&a23014c=15&wbtreeid=12709"
        pageList = getLink(url)
        innoList.extend(pageList)
    #print(innoList)
    n =0
    for annexUrl in innoList:
        n+=1
        getData(annexUrl,n)

    # head = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    #     # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    #     #  "Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.25 Safari / 537.36 Core / 1.70.3868.400 QQBrowser / 10.8.4394.400"
    # }
    #
    # url = "http://www.lnpu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=701058981&wbfileid=36795"
    # request = urllib.request.Request(url, headers=head)
    # urllib.request.urlretrieve(url,"4.xls")

    # url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    # urllib.request.urlretrieve(url, "./1.png")


# 获取指定URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        #  "Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.25 Safari / 537.36 Core / 1.70.3868.400 QQBrowser / 10.8.4394.400"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 获取公告的详情链接
def getLink(url):
    linkList = []
    html = askURL(url)

    bs = BeautifulSoup(html, "html.parser")
    eldiv1 = bs.select(".listContentBright > td > a")
    # print(eldiv1)
    for link in eldiv1:
        # print(eldiv1)
        if (link["href"][:4] != "http"):
            newLink = "http://www.lnpu.edu.cn/" + link["href"]
        else:
            newLink = link["href"]
        linkList.append(newLink)

    eldiv2 = bs.select(".listContentDark > td > a")
    for link in eldiv2:
        if (link["href"][:4] != "http"):
            newLink = "http://www.lnpu.edu.cn/" + link["href"]
        else:
            newLink = link["href"]
        linkList.append(newLink)
    # print(linkList)
    return linkList


# 获取详情页附件数据
def getData(url,n):
    html = askURL(url)
    bs = BeautifulSoup(html, "html.parser")
    annex = bs.select('td[align="left"] > span > span')
    annex2 = bs.select('td[align="left"] > span > span > a')
    # print(annex2[0]["href"])
    annexUrl = ""
    path = "./"

    if len(annex) > 0 and annex[0].text[:2] == "附件":
        if annex2[0]["href"][:4] == "http":
            annexUrl = annex2[0]["href"]
        else:
            annexUrl = "http://www.lnpu.edu.cn" + annex2[0]["href"]
        if annexUrl[:4] == "http":
            print(annexUrl)

            #urllib.request.urlretrieve(annexUrl, "./" + str(n) + ".xls")
        # wget.download(annexUrl, path)
        # urllib.urlretrieve(annexUrl, "1")


if __name__ == "__main__":
    main()
    print("爬取完毕！")
    # askURL("https://movie.douban.com/top250")
