#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4  # Beautiful Soup library helps us parse the content into objects. 
import requests
import re

# get_foreclosures function scrapes the Sheriff's office website and gets the information of houses on auction
def get_foreclosures():
    
    # Creates a session object
    session = requests.Session()
    
    # Scrapes the Sheriff's office main page and returns a BeautifulSoup object
    response = session.get('https://salesweb.civilview.com/Sales/SalesSearch?countyId=2')
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    
    # Necessary to get into the foreclosures' details pages later
    session_id = response.cookies['ASP.NET_SessionId'] 
    list_of_trs = soup.find_all('tr')
    list_of_foreclosures = []
    
    # Loop through all the trs tags in the page, where information of the houses and the auction status inbedded
    for data_row in list_of_trs:
        td_children = data_row.findChildren('td')
        if td_children:
            link = str(td_children[0].contents)[10:-14]
            
            # Get the unique Sheriff ID, plaintiff, defendant and address of the house
            sheriff_id = str(td_children[1].contents)[2:-2] 
            sales_date = str(td_children[2].contents)[2:-2]
            plaintiff = str(td_children[3].contents)[2:-2]
            plaintiff2 = plaintiff.replace("'","") #Remove posible ' signs in the string to aboid conflicts
            defendant = str(td_children[4].contents)[2:-2]
            defendant2 = defendant.replace("'","") #Remove posible ' signs in the string to aboid conflicts
            address = str(td_children[5].contents)[2:-2]
            address2 = address.replace("'","") #Remove posible ' signs in the string to aboid conflicts
            
            # Get into the details page
            url = 'https://salesweb.civilview.com/'+str(link) 
            response2 = session.get(url)
            soup2 = bs4.BeautifulSoup(response2.content, 'html.parser')
            list_of_tds = soup2.find_all('td')
            length_tds = len(list_of_tds)
            
            # Get the default amount, initial status and date, last status and date of the auction
            default_amount = str(list_of_tds[15])[4:-5]
            default_amount2 = default_amount.replace("$","").replace(",","") #Remove $ and thousand separators so the amount can be easily turned into a float
            initial_status = str(list_of_tds[20])[4:-5]
            initial_status_date = str(list_of_tds[21])[4:-5]
            last_status = str(list_of_tds[length_tds-2])[4:-5]
            last_status_date = str(list_of_tds[length_tds-1])[4:-5]
            list_of_foreclosures.append([sheriff_id, address2, initial_status, initial_status_date, last_status, last_status_date, plaintiff2, defendant2, default_amount2,sales_date])
    return list_of_foreclosures

# Given an address of a house, the get_property function returns the address, year built, 
# number of bedrooms, number of bathrooms, size, last sold year for the house, last_sold_price for the house
# from Zillow
def get_property(address):
    
    # Generate the the appropriate url for Zillow to do the search
    link_address = address.replace(' ','-')
    url = 'https://www.zillow.com/homes/for_sale/' + link_address + '_rb/'
    
    # Using a browser mechanism to scrapping Zillow
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    
    # Get the response from Zillow and use a BeautifulSoup Object
    response = requests.get(url, headers=headers)
    result = bs4.BeautifulSoup(response.content,'lxml')
    
    # Given the address of the house, find the number of bedrooms, bathrooms, size and year built for the house
    try:
        bedroom_n = result.find('h3', 'edit-facts-light').find_all('span', {'class' : None})[0].get_text().split(' ')[0]
        #print(bedroom_n)
        bathroom_n = result.find('h3', 'edit-facts-light').find_all('span', {'class' : None})[1].get_text().split(' ')[0]
        size = result.find('h3', 'edit-facts-light').find_all('span', {'class' : None})[2].get_text().split(' ')[0]
        size2 = size.replace(",","") #Remove thousand separators so the square footage can be easily turned into a float
        year_built = result.find_all('div', {'class': 'fact-value'})[1].get_text()
        divs_text = ''
        
        # Get all the divs tags with 'fact-value' class within the page
        all_divs = result.find_all('div', {'class': 'fact-value'})
        for div in all_divs:
            text = div.get_text()
            divs_text += text + ' '
        
        # Define a Regex expression to find the last sold year and price for the house
        pattern = r'\w{3} \d{4} \w{3} \S+'
        match = re.findall(pattern, divs_text)  
        
        # Get the last sold year and price for the house
        last_sold_year = match[0].split(' ')[1]
        last_sold_price = match[0].split(' ')[3]
        last_sold_price2 = last_sold_price.replace("$","").replace(",","") #Remove $ and thousand separators so the amount can be easily turned into a float
        for data in year_built, bedroom_n, bathroom_n, size, last_sold_year, last_sold_price2:
            if data == '--':
                data = 'NULL'
    except:
        year_built, bedroom_n, bathroom_n, size2, last_sold_year, last_sold_price2 = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'
    return [address, year_built, bedroom_n, bathroom_n, size2, last_sold_year, last_sold_price2]
