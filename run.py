#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 14:50:13 2018

@author: gabrielapinto
"""

from scraping_functions import *
import psycopg2
import bs4  # Beautiful Soup library helps us parse the content into objects. 
import requests
import re
from psql_upload_data import *

t0 = time.time()
list_foreclosures = get_foreclosures() #list of scrapped foreclosures. file: scraping_functions.py
upload_data(list_foreclosures)

t1 = time.time()
print('Done')
print(t1-t0)
