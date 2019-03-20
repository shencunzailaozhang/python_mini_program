import requests
import os
import time
import chardet
from bs4 import BeautifulSoup
from Email import send_ms
def get_web_data(url):#获取网页数据
    headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb"
                          "Kit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
    html=requests.get(url,headers=headers)
    Encoding=chardet.detect(html.content)['encoding']
    html.encoding=Encoding
    web_data=html.text
    return web_data
# print(get_web_data('https://news.baidu.com/'))
def get_titles(web_data):#获取标题及对应链接
    title_hrefs={}
    soup=BeautifulSoup(web_data,'lxml')
    titles_data=soup.find_all({'a':{'target':'_blank'}})#titles_data的类型是<class 'bs4.element.ResultSet'>
    for title in titles_data:
        title_text=title.get_text()
        #过滤一些无关的标签等
        if len(title_text)>=10:
            if title.has_attr('href'):#title的类型是<class 'bs4.element.Tag'>
                href=title['href']
                # print(type(title))
            else:
                href='Cannot find link...'
            title_hrefs[title_text]=href
    return title_hrefs

def get_roi(title_hrefs,key_words):#筛选自己想了解的信息
    roi={}
    for title in title_hrefs:
        for key_word in key_words:
            if key_word in title:
                roi[title]=title_hrefs[title]
    return roi

def send_report(roi):
    length=len(roi)
    s1='本次供探测到'+str(length)+'条相关新闻'+'\n'
    s2=''
    for title in roi:
        s2+=title
        s2+=roi[title]
        s2+='\n'
    send_ms(s1+s2)

# web=get_web_data('https://news.baidu.com/')
# hrefs=get_titles(web)
# print(get_roi(hrefs,'华为'))
if __name__=='__main__':
    web_data=get_web_data('https://news.baidu.com/')
    titles=get_titles(web_data)
    key_words=['iPhone','华为']
    roi=get_roi(titles,key_words)
    print(type(roi))
    print(roi)
    print(roi.items())
    if len(roi)!=0:
        for item in roi.items():
            send_ms(item[0]+':'+item[1])