#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scraping_functions import *
import psycopg2
import bs4  # Beautiful Soup library helps us parse the content into objects. 
import requests
import re
from psql_upload_data import *

list_foreclosures = get_foreclosures() #list of scrapped foreclosures. file: scraping_functions.py
upload_data(list_foreclosures)
