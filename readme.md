# Group Name: 
Python and Kobra are not the same - Section 1

## Team Members: 
Maria Jose Gamonal (UNI: mjg2268), Georges Kouame (UNI: nk2800), Jeff Lv (UNI: zl2731), and Gabriela Pinto (UNI: gpp2111)

# Description
This package extracts foreclosure property information from a public foreclosures website, enriches the data with information 
from a real estate website (adding features like number of bedrooms, bathrooms, year built, last sold year and price), and persists the enriched data into a database accessible from Python. The web parsin functionality are automated to run week a day and changes in property information are updated into the database.

This package essential consolidates the data betwwen the Sheriff's office website and Zillow, creates the foreclosure, plaintiff and property tables and updates them once a week.

## Requirements
1. Python Modules
- Beautiful Soup
- requests
- re
- csv
- time

## Each File Explained
1. scraping_functions.py

This file contains two web scraping functions. 

get_foreclosures() scrapes the Sheriff's office website (https://salesweb.civilview.com/Sales/SalesSearch?countyId=2) and gets the information of houses on auction.

get_property(address) scrapes Zillow (https://www.zillow.com/). Given an address of a house, the get_property function returns the address, year built, number of bedrooms, number of bathrooms, size, last sold year for the house, last_sold_price for the house


2. psql_create_tables.py

This file should be run once in order to create the database and the tables. The user must change its name in line 8. There are 3 tables: foreclosure, property and plaintiff.


3. psql_upload_data.py

This file contains the function that upload the information to the database.
upload_data(list_foreclosures) iterates over the list and check if the foreclosure, property or plantiff already exist and depending on this it is updated or inserted into the repective table.


4. dbexport.pgsql

This is a psql database that resulted after running the run.py file, which serves as an example here.

5. auto_execute.sh

This file creates a loop that runs this entire program once a week.

## Run Instructions

1. Download this repo master branch to your local machine or cloud

2. Change the username variable to your own SQL user name in both psql_create_tables.py and psql_upload_data.py

3. Run the following comand line in terminal:

   bash bin/auto_execute



