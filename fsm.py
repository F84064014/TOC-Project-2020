from transitions.extensions import GraphMachine

from utils import send_text_message, send_two_message

import requests
from bs4 import BeautifulSoup
import re
import json
import random
from collections import Counter



class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.cur_url = "test"
        self.cur = 0
        self.news_url_list = list()
        self.news_tit_list = list()

    def is_going_to_state_hello(self, event):
        text = event.message.text
        return text.lower() == "是在哈囉?"

    def is_going_to_state_search(self, event):
        text = event.message.text
        return text.lower().find("search ") >= 0

    def is_going_to_state_random_news(self, event):
        text = event.message.text
        return text.lower() == "rand news"

    def is_going_to_state_exit(self, event):
        text = event.message.text
        return text.lower() == "exit"

    def is_going_to_state_count(self, event):
        text =event.message.text
        return text.lower().find("count ") >= 0

    def is_going_to_state_content(self, event):
        text = event.message.text
        return text.lower() == "content"

    def is_going_to_state_scrapy_search(self, event):
        text = event.message.text
        return text.lower().find("scrapy ") >= 0

    def is_going_to_state_next(self, event):
        text = event.message.text
        return text.lower() == "next"

    def on_enter_state_hello(self, event):
        print("I'm entering state_hello")

        reply_token = event.reply_token
        send_text_message(reply_token, "哈囉你媽")
        self.go_back()

    def on_exit_state_hello(self):
        print("Leaving state_hello")

    def on_enter_state_search(self, event):
        print("I'm entering state_search")

        search = event.message.text
        search = search[7:len(search)]
        url = "https://tw.news.search.yahoo.com/search;?p="+search
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        surls = soup.find_all('a', class_="thmb")
        self.news_url_list.clear()
        self.news_tit_list.clear()
        for surl in surls:
            self.news_tit_list.append(surl.get('title'))
            self.news_url_list.append(surl.get('href'))
        self.cur_url = self.news_url_list[0]
        reply_token = event.reply_token
        send_two_message(reply_token,self.news_tit_list[0], self.news_url_list[0])

    #def on_exit_state_search(self):
    #    print("Leaving state_search")

    def on_enter_state_random_news(self, event):
        print("I'm entering state_random_news")

        resp = requests.get('https://tw.yahoo.com/')
        soup = BeautifulSoup(resp.text, 'html.parser')
        stories = soup.find_all('a', class_='story-title')
        self.news_tit_list.clear()
        self.news_url_list.clear()
        for s in stories:
            self.news_tit_list.append(s.text)
            self.news_url_list.append(s.get('href'))
        self.cur = random.randint(0, len(self.news_url_list))
        reply_token = event.reply_token
        send_two_message(reply_token, self.news_tit_list[self.cur], self.news_url_list[self.cur])
        self.auto_go_back()

    #def on_exit_state_random_news(self):
    #    print("Leaving state_random_news"

    def on_enter_state_exit(self, event):
        print("I'm entering state_exit")

        reply_token = event.reply_token
        send_text_message(reply_token, "exit state")
        self.go_back()

    def on_exit_state_exit(self):
        print("Leaving state_exit")

    def on_enter_state_count(self, event):
        print("I'm entering state_count")

        target = event.message.text
        target = target[6:len(target)]
        url = self.cur_url
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        articles = soup.find_all('div', 'caas-body')
        if not articles:
            articles = soup.find_all('p')
        if not articles:
            articles = "sorry, can't read ths article"
        c = 0
        for article in articles:
            c += article.text.count(target)
        #c = articles[0].text.count(target)
        m = "the number of " + target + " is "
        m = m + str(c)
        reply_token = event.reply_token
        send_text_message(reply_token, m)
        self.auto_go_back()

    def on_enter_state_content(self, event):
        print("I'm entering state_content")

        url = self.cur_url
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        articles = soup.find_all('div', 'caas-body')
        if not articles:
            articles = soup.find_all('p')
        if not articles:
            articles = "sorry, can't read ths article"
        reply_token = event.reply_token
        #sar = list()
        #for article in articles:
        #    sar.append(article.text)
        send_text_message(reply_token, articles[0].text)
        self.auto_go_back()

    def on_enter_state_next(self, event):
        print("I'm entering state_next")

        self.cur += 1
        if self.cur >= (len(self.news_url_list)-1):
            self.cur = 0
        self.cur_url = self.news_url_list[self.cur]
        reply_token = event.reply_token
        send_two_message(reply_token, self.news_tit_list[self.cur], self.cur_url)
        self.auto_go_back()       

    def on_enter_state_scrapy_search(self, event):
        print("I'm entering state_scrapy_search")

        search = event.message.text
        search = search[7:len(search)]
        m = "scraping " + search + "..."
        temp = []
        self.cur_url = "https://tw.news.search.yahoo.com/search;?p="+search
        resp = requests.get(self.cur_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        surls = soup.find_all('a', class_="thmb")
        self.news_tit_list.clear()
        self.news_url_list.clear()
        for s in surls:
            self.news_url_list.append(s.get('href'))
            self.news_tit_list.append(s.get('title'))       
        for i in range(0, len(self.news_url_list)):
            temp.append(self.news_tit_list[i])
        #    t += temp
            temp.append(self.news_url_list[i])
        #    t += temp
        reply_token = event.reply_token
        send_two_message(reply_token, m, tmep[0])

    def on_enter_state_scrapy_count(self, event):
        print("I'm entering state_scrapy_count")

        target = event.message.text
        target = target[6:len(target)]
        c = 0
        for s in self.news_url_list:
            resp = requests.get(s)
            soup = BeautifulSoup(resp.text, 'html.parser')
            articles = soup.find_all('div', 'caas-body')
            for article in articles:
                c+= article.text.count(target)
        m = "the number of " + target + " is " + str(c)
        m = m + " in totally " + str(len(self.news_url_list)) + " reports"  
        reply_token = event.reply_token
        send_text_message(reply_token, m)
        self.auto_go_back_scrapy()
