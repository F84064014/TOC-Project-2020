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
        stitles = soup.find_all('li', 'ov-a fst')
        surls = soup.find_all('a', class_="thmb")
        self.news_url_list.clear()
        self.news_tit_list.clear()
        for s in stitles:
            self.news_tit_list.append(s.text)
        for surl in surls:
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
        title = list()
        title_url = list()
        for s in stories:
            title.append(s.text)
            title_url.append(s.get('href'))
        rand_title = random.randint(0, len(title))
        reply_token = event.reply_token
        send_two_message(reply_token, title[rand_title], title_url[rand_title])


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
        c = 0
        for article in articles:
            c += article.text.count(target)
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
        sart = list()
        articles = soup.find_all('div', 'caas-body')
        for article in articles:
            sart.append(article.text)
        reply_token = event.reply_token
        send_text_message(reply_token, sart[0])
        self.auto_go_back()

    def on_enter_state_next(self, event):
        print("I'm entering state_next")

        #self.cur++
        #self.cur_url = self.news_url_list[self.cur]
        reply_token = event.reply_token
        #send_two_message(reply_token, self.news_tit_list[self.cur], self.cur_url)
        send_two_message(reply_token, "你好", "你是臭假")
        self.auto_go_back()       

    def on_enter_state_scrapy_search(self, event):
        print("I'm entering state_scrapy_search")

        search = event.message.text
        search = search[7:len(search)]
        m = "scraping" + search + "..."
        t = "ok"
        self.cur_url = "https://tw.news.search.yahoo.com/search;?p="+search
        resp = requests.get(self.cur_urlurl)
        soup = BeautifulSoup(resp.text, 'html.parser')
        stitles = soup.find_all('li', 'ov-a fst')
        surls = soup.find_all('a', class_="thmb")
        self.news_url_list.clear()
        #for s in surls:
        #    self.news_url_list.append(s.get('href'))
        #for st in stitles
        #    t += st.text
        #    t += '\n'
        reply_token = event.reply_token
        send_two_message(reply_token, m, "working?")

    def on_enter_state_scrapy_count(self, event):
        print("I'm entering state_scrapy_count")

        reply_token = event.reply_token
        send_text_message(reply_token, "countS")
