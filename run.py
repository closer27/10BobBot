#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient
import time


def get_menu():
    url = 'http://supportportal.skplanet.com/Main/Main.aspx'
    values = {}
    with open("cookie.txt") as f:
        for line in f:
            (key, val) = line.split()
            values[str(key)] = val

    s = requests.Session()
    try:
        source_code = s.get(url, cookies=values, timeout=5)
    except requests.exceptions.RequestException:
        return "지금은 알려드릴 수가 없어요 :cry:"

    return process_data(source_code)


def process_data(source_code):
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    picnic = soup.find(id="box07")
    menu = picnic.get_text()
    return menu


def create_bot():
    token = open("token.txt")
    sc = SlackClient(token)
    sc.rtm_connect()
    while True:
        new_evts = sc.rtm_read()
        for evt in new_evts:
            print(evt)
            if "type" in evt:
                if evt["type"] == "message" and "text" in evt:
                    message = evt["text"]
                    channel = evt["channel"]
                    print(message)
                    if "점심메뉴" in message or "십밥" in message or "10층" in message or "10밥" in message:
                        sc.rtm_send_message(channel=channel, message=get_menu())
                    elif "명령어" in message:
                        sc.rtm_send_message(channel=channel, message="10밥봇 명령어 : 점심메뉴, 십밥, 10층, 10밥")
        time.sleep(.1)


if __name__ == '__main__':
    create_bot()
