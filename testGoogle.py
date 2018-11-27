#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: María José Gamonal Sáenz
"""

import requests
from bs4 import BeautifulSoup

def get_web_adress(direction):


    research_later = direction + " site:realtor.com"
    goog_search = "https://www.google.com/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + research_later


    r = requests.get(goog_search)

    soup = BeautifulSoup(r.text, "html.parser")
    web = soup.find('cite').text
    w = web.split("/")
    new_adress = "https://www.realtor.com/realestateandhomes-detail/"+w[-1]
    return new_adress

direction = "212 VOSE AVENUE SOUTH ORANGE NJ 07079"
print(get_web_adress(direction))