import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

from fsm import TocMachine
from utils import send_text_message

import requests
from bs4 import BeautifulSoup
import re

load_dotenv()

WEBHOOK_VERIFY_TOKEN = os.environ.get(
    "WEBHOOK_VERIFY_TOKEN", "webhook"
)

machine = TocMachine(
    states=["user", "state_hello", "state_search", "state_random_news", "state_exit", "state_count", "state_content", "state_scrapy_search", "state_scrapy_count", "state_next", "state_check"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state_hello",
            "conditions": "is_going_to_state_hello",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state_search",
            "conditions": "is_going_to_state_search",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state_random_news",
            "conditions": "is_going_to_state_random_news",
        },
        {
            "trigger": "advance",
            "source": ["state_search", "state_random_news", "state_scrapy_search"],
            "dest": "state_exit",
            "conditions": "is_going_to_state_exit",
        },
        {
            "trigger": "advance",
            "source": "state_search",
            "dest": "state_count",
            "conditions": "is_going_to_state_count",
        },
        {
            "trigger": "advance",
            "source": "state_search",
            "dest": "state_content",
            "conditions": "is_going_to_state_content",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state_scrapy_search",
            "conditions": "is_going_to_state_scrapy_search",
        },
        {
            "trigger": "advance",
            "source": "state_scrapy_search",
            "dest": "state_scrapy_count",
            "conditions": "is_going_to_state_count"
            
        },
        {
            "trigger": "advance",
            "source": "state_search",
            "dest": "state_next",
            "conditions": "is_going_to_state_next"    
        },
        {
            "trigger": "advance",
            "source": "state_scrapy_search",
            "dest": "state_check",
            "conditions": "is_going_to_state_check"    
        },        
        {
            "trigger": "go_back", 
            "source": ["state_hello", "state_exit"], 
            "dest": "user"
        },
        {
            "trigger": "auto_go_back",
            "source": ["state_count", "state_content", "state_next", "state_random_news", "state_check"],
            "dest": "state_search"
        },
        {
            "trigger": "auto_go_back_scrapy",
            "source": ["state_scrapy_count"],
            "dest": "state_scrapy_search"
        },        
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


@app.route("/test1", methods=["POST"])
def test1():

    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        resp = requests.get('https://tw.yahoo.com/')
        soup = BeautifulSoup(resp.text, 'html.parser')
        stories = soup.find_all('a', class_='story-title')
        #send_text_message(event.reply_token, stories.text)
        #for s in stories:
            #line_bot_api.reply_message(
            #        event.reply_token, [TextSendMessage(text = s.text), TextSendMessage(text = s.get('href'))]
            #)
    ImageSendMessage("https://imgur.com/BejelvG","https://imgur.com/BejelvG")

    return "OK"


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
