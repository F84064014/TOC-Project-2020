from transitions.extensions import GraphMachine

from utils import send_text_message, send_two_message

import requests
from bs4 import BeautifulSoup
import re
import json
import random

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "twitter"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "news"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text.lower() == "exit"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        tweets_list = list()
        resp = requests.get('https://twitter.com/realDonaldTrump')
        soup = BeautifulSoup(resp.text, 'html.parser')
        tweets = soup.find_all('li', {"data-item-type": "tweet"})
        for tweet in tweets:
            tweet_data = None
            tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
            images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
            #for image_in_tweet_tag in images_in_tweet_tag:
            #    tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')
            tweets_list.append(tweet_text_box.text)

        rand_tweet = random.randint(0, len(tweets_list))
        reply_token = event.reply_token
        send_text_message(reply_token, tweets_list[rand_tweet])
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

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
    #    print("Leaving state3")

    def on_enter_state4(self, event):
        print("I'm entering state4")

        reply_token = event.reply_token
        send_text_message(reply_token, "exit state")
        self.go_back()

    def on_exit_state4(self):
        print("Leaving state4")

