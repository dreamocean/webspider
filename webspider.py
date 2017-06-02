#coding=utf-8
import urllib2
import os
import shutil
import requests
from bs4 import BeautifulSoup
import lxml
import docx
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_html_soup(url):#获取解编码后的HTML
    html = None
    request = urllib2.Request(url)
    try:
        html = urllib2.urlopen(request)
    except Exception, e:
        print e
        soup = None
    else:
        soup = BeautifulSoup(html, 'lxml')
   
    #s = requests.Session()
    #r = s.get(url)
    #print r.status_code
    #if r.status_code == 200:
        #soup = BeautifulSoup(r.content, 'lxml')
    #else:
        #soup = None
    #s.close()
    return soup

def get_title_link(url):#获取新闻的标题和正文链接
    soup = get_html_soup(url)
    if soup == None:
        return None
    #print soup
    news_link = {}
    for link in soup.find_all("a", href=re.compile("http://")):
        if len(link.get_text().strip()) > 0 and link.get("href")!= -1:
            news_link[link.get_text().decode('utf-8')] = link.get('href')
            #print link.get_text().decode('utf-8') + link.get('href')
    return news_link

def get_news_body(url):#抓取新闻主体内容
    content_text = []
    article_div = ""
    #print "================== " + url + " ====================="
    soup = get_html_soup(url)
    if soup == None:
        return None
    for content in soup.find_all("p"):
        if len(content.get_text().strip()) > 0:
            content_text.append(content.get_text().strip())    
            #print content.get_text().decode('utf-8')
    ''' 
    article_div = str(soup.find("div", attrs = {"class": "article"}))
    soup = BeautifulSoup(article_div, 'lxml')
    for content in soup.find_all("p"):
        if len(content.get_text().strip()) > 0:
            content_text.append(content.get_text().strip())    
            print content.get_text().decode('utf-8')
    '''
    return content_text

########################################################################
website = [
           "http://www.news.cn/tech/",
           "http://www.news.cn/sports/",
           "http://www.news.cn/fortune/",
           "http://www.news.cn/fashion/",
           "http://www.news.cn/food/",
           "http://www.news.cn/world/",
           "http://www.news.cn/politics/",
           "http://www.news.cn/house/",
           "http://www.news.cn/info/"
           ]
    
f_src = open("src.txt",'wb')
f_split = open("split.txt",'wb')
f_filter = open("filter.txt",'wb')
count = 0
for site in website:
    print "======================= " + site + " ======================="
    #获取新闻的标题和链接
    news_url_dic = get_title_link(site)
    if news_url_dic == None:
        continue
    #获取新闻的内容主体并写入文件
    for x in news_url_dic:
        url = news_url_dic[x]
        if re.match(r'^https?:/{2}\w.+$', url):
            news_list = get_news_body(url)
            if news_list == None:
                continue
            for news in news_list:      
                split_text_list = re.split(ur'[,.，。？：；【】！、| \s]', news)
                for split_text in split_text_list:
                    #split
                    if split_text != "":
                        #print split_text.decode('utf-8')
                        f_split.write("%s\n"%(split_text))
                        f_split.flush()
                        #filter
                        filter_chinese = re.compile(ur'[^\u4e00-\u9fa5]')
                        filter_text = re.sub(filter_chinese, "", split_text)
                        if filter_text != "":
                            count = count + 1
                            print filter_text.decode('utf-8')
                            f_filter.write("%s\n"%(filter_text))
                            f_filter.flush()
                f_src.write("%s\n"%(news))
                f_src.flush()
f_src.close()  
f_split.close()
f_filter.close()
print "Finished! Line count: %d"%(count)