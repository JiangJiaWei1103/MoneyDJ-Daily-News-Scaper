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

#%%
# varible definitions
base_url = "https://blog.moneydj.com/news/page/"   # url base of the target webpage
date_today = "2020-09-21"#dt.today().strftime("%Y-%m-%d")   # date today 
article_link = []   # list to store links of all the news today

#%%
# function definitions
def news_scraper():   # financial news scraper
    # new dir (named as date today) in directory "news"
    #os.mkdir("/Users/wei1103/Desktop/financial_news/" + date_today)
    
    # parse elements and store all the news today in newly created dir 
    web_el_parser()
    news_processor()

def web_el_parser():   # parse basic web elements
    page_count = 1
    today_end = False   # indicate the ending of today's news
    while not today_end:
        page = requests.get(base_url + str(page_count) + "/")
        page_count += 1
        if page.status_code == 200:
            print("Page" + str(page_count - 1) + "Success!!")
            soup = BeautifulSoup(page.content, "html.parser")
        else:
            print("Error code: ", page.status_code)
        
        articles = soup.find_all("article", {"class": "mh-loop-item"})   # articles in single page
        for article in articles:
            date = article.find("span", {"class": "mh-meta-date"}).text
            if end_proc(date):
                today_end = True
                break
            else: 
                article_link.append(article.h3.a["href"])
                continue

def end_proc(date):   # determine whether the news scraping should stop
    return True if date < date_today else False

def news_processor():   # process news' content and store into the right dir
    for link in article_link:
        print(link)
        news_dic = {}   # store all elements of a single news
        content = []   # news content text
        single_news = requests.get(link)
        soup = BeautifulSoup(single_news.content, "html.parser")
        article_title = soup.find("h1", {"class": "entry-title"}).text
        article_date = soup.find("span", {"class": "entry-meta-date"}).a.text
        article_content = soup.find("div", {"class": ["entry-content", "article"]}).children
        #print(article_content)
        for p in article_content:
            content.append(p.text)
        news_dic.update([("title", article_title.replace("/", "-")), ("date", article_date), ("content", content)])
        news_file_generator(news_dic)   # generate single news file, ans store to right dir
        
def news_file_generator(news_dic):   # generate single news file, ans store to right dir
    with open("/Users/wei1103/Desktop/financial_news/" + date_today + ".txt", "a") as file:  #"/" + news_dic["title"] + 
        for key, value in news_dic.items():
            if key == "content":
                file.write("%s:\n" % key)
                for p in value:
                    file.write("%s\n" % p)
            else: 
                file.write('%s: %s\n' % (key, value))
        file.write("\n\n")
        #print(news_dic, file=file)
        #file.write(json.dumps(news_dic))   # dumps will serialize the format of obj to json str
    
        
if __name__ == "__main__":
    news_scraper()
    

