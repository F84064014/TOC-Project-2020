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
    tweets_list = list()
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data  = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
        except Exception as e:
            continue #ignore if any loading or tweet err

        if tweet_data:
            tweets_list.append(tweet_data)
    
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, "test not failed")

return "OK"

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
