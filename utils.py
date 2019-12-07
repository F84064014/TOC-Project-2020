import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
from bs4 import BeautifulSoup
import re
import random

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

#global u

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_two_message(reply_token, text1, text2):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, [TextSendMessage(text1), TextSendMessage(text2)])

    return "OK"

def set_u(text):
    u = text
    return 'OK'

def get_u():
    return u

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
