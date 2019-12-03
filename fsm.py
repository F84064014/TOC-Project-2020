from transitions.extensions import GraphMachine

from utils import send_text_message

import requests
from bs4 import BeautifulSoup
import re


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "go to nigga state"

    def return_to_user(self, event):
        text = event.message.text
        return text.lower() == "return to user"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

        resp = requests.get('https://tw.yahoo.com/')
        soup = BeautifulSoup(resp.text, 'html.parser')
        stories = soup.find_all('a', class_='story-title')
        for s in stories:
            reply_token = event.reply_token
            send_text_message(reply_token, "Yo nigga")
            #line_bot_api.reply_message(
            #        event.reply_token, [TextSendMessage(text = s.text), TextSendMessage(text = s.get('href'))]
            #)
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")
