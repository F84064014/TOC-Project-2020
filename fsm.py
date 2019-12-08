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

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "是在哈囉?"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower().find("search ") >= 0

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "rand news"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text.lower() == "exit"

    def is_going_to_state5(self, event):
        text =event.message.text
        return text.lower().find("count ") >= 0

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "哈囉你媽")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        search = event.message.text
        search = search[7:len(search)]
        url = "https://tw.news.search.yahoo.com/search;?p="+search
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        stitles = soup.find_all('li', 'ov-a fst')
        surls = soup.find_all('a', class_="thmb")
        stit = list()
        sur = list()
        for s in stitles:
            stit.append(s.text)
        for surl in surls:
            sur.append(surl.get('href'))
        reply_token = event.reply_token
        send_two_message(reply_token,stit[0], sur[0])

    #def on_exit_state2(self):
    #    print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

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


    #def on_exit_state3(self):
    
    #    print("Leaving state3"

    def on_enter_state4(self, event):
        print("I'm entering state4")

        reply_token = event.reply_token
        send_text_message(reply_token, "exit state")
        self.go_back()

    def on_exit_state4(self):
        print("Leaving state4")

    def on_enter_state5(self, event):
        print("I'm entering state5")

        url = "https://tw.news.search.yahoo.com/search;?p=%E9%9F%93%E5%9C%8B%E7%91%9C"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        articles = soup.find_all('a', 'ov-a fst')
        for article in articles:
            c = article.count("國")
        reply_token = event.reply_token
        send_text_message(reply_token,c)
        self.goback()

