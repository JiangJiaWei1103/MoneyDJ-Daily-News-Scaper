'''Financial News Scraper (daily)'''
'''
Side project extensions:
    1. General news scraper
    2. NLP data collector for financial analysis or investment
'''
#%%
# import packages
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import time
import json 
import os 
import sys
import config

#%%
# varible definition
dir_path = config.path   # path to store scraped content
#base_url = "https://blog.moneydj.com/news/page/"   # url base of the target webpage
base_url = "https://www.moneydj.com/KMDJ/News/NewsRealList.aspx?index1="
suffix = "&a=MB010000"
news_url_prefix = "https://www.moneydj.com"
date_start = sys.argv[1]   # the scraping will start at this date given by user
news_urls = []   # list to store links of all the news today

#%%
# function definitions
def news_scraper():   # financial news scraper
    # new dir (named as date today) in directory "news"
    #os.mkdir("dir_path" + date_today)
    
    # parse elements and store all the news today in newly created dir 
    web_el_parser()
    news_processor()

def web_el_parser():   # parse basic web elements
    page_count = 1
    today_end = False   # indicate the ending of today's news
    while not today_end:
        page = requests.get(base_url + str(page_count) + suffix)   
        page_count += 1
        if page.status_code == 200:
            print("Page" + str(page_count - 1) + "Success!!")
            soup = BeautifulSoup(page.content, "html.parser")
        else:
            print("Error code: ", page.status_code)
        
        news_table = soup.find("table", {"id": "MainContent_Contents_sl_gvList"})   # news table in one page
        news_in_one_page = news_table.find_all("tr")[1:]   # all pieces of news in one page
        for news in news_in_one_page:
            details = news.find_all("td")[:-1]   # detailed information for a piece of news
            #print(details[0].text.strip())
            date = details[0].text.strip().split(" ")[0].replace("/", "-")   # date of news
            if date > date_start:
                continue
            elif date < date_start:
                today_end = True
                break   
            news_url = details[1].a["href"]    # news url
            news_urls.append(news_url_prefix + news_url)
  
def old():
    articles = soup.find_all("article", {"class": "mh-loop-item"})   # articles in single page
    for article in articles:
        date = article.find("span", {"class": "mh-meta-date"}).text()
        if end_proc(date):
            today_end = True
            break
        else: 
            article_link.append(article.h3.a["href"])
            continue

def news_processor():   # process news contents and write to txt file
    for news_url in news_urls:
        news_dict = {}   # store all elements of a single piece of news
        content = list()   # news conent text
        single_news = requests.get(news_url)
        soup = BeautifulSoup(single_news.content, "html.parser")
        news_title = soup.find("span", {"id": "MainContent_Contents_lbTitle"}).text
        #article_date = soup.find("span", {"class": "entry-meta-date"}).a.text
        news_content = soup.find("article", {"id": "MainContent_Contents_mainArticle"}).text
        print(news_title)
        #for p in article_content:
            #content.append(p.text)
        news_dict.update([("title", news_title), ("content", news_content)])
        news_file_generator(news_dict)   # generate single news file, ans store to right dir

def end_proc(date):   # determine whether the news scraping should stop
    return True if date < date_start else False

def news_processor_old():   # process news' content and store into the right dir
    for link in article_link:
        print(link)
        news_dict = {}   # store all elements of a single news
        content = []   # news content text
        single_news = requests.get(link)
        soup = BeautifulSoup(single_news.content, "html.parser")
        article_title = soup.find("h1", {"class": "entry-title"}).text
        article_date = soup.find("span", {"class": "entry-meta-date"}).a.text
        article_content = soup.find("div", {"class": ["entry-content", "article"]}).children
        #print(article_content)
        for p in article_content:
            content.append(p.text)
        news_dict.update([("title", article_title.replace("/", "-")), ("date", article_date), ("content", content)])
        try: 
            news_file_generator(news_dict)   # generate single news file, ans store to right dir
        except:
            print(news_dict["title"] + " fails!")
            continue        

def news_file_generator(news_dic):   # generate single news file, ans store to right dir
    with open(dir_path + date_start + ".txt", "a") as file:  #"/" + news_dic["title"] + 
        for key, value in news_dic.items():
            if key == "content":
                file.write("%s:\n" % key)
                #for p in value:
                file.write("%s\n" %value)
            else: 
                file.write('%s: %s\n' % (key, value))
        file.write("\n\n")
        #print(news_dic, file=file)
        #file.write(json.dumps(news_dic))   # dumps will serialize the format of obj to json str
    
        
if __name__ == "__main__":
    news_scraper()
    

