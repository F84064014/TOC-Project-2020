import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
from bs4 import BeautifulSoup
import re
import random

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_two_message(reply_token, text1, text2):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [TextSendMessage(text1), TextSendMessage(text2)])

    return "OK"

def func_test(reply_token, username)
    url = "http://www.twitter.com/" + username
    respone = None
    respone = request.get(url)
    soup = BeautifulSoup(respoonse.text, 'lxml')
    tweets = get_tweets_data(username, soup)
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, "test not failed")

def get_tweets_data(username, soup)
    tweets_list = list()
    tweets_list.extend(get_this_page_tweets(soup))

def get_this_page_tweets(soup)
    tweets_list = list()
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data = get_tweet_text(tweet)
        except Exception as e:
            continue #ignore if any loading or tweet err

        if tweet_data:
            tweets_list.append(tweet_data)
            
    return tweets_list

def get_tweet_text(tweet):
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')

    return tweet_text

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
