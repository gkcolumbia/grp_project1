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
- psycopg2
2.  install Postgres (More info: https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb).

## Each File Explained
1. scraping_functions.py

This file contains two web scraping functions. 

get_foreclosures() scrapes the Sheriff's office website (https://salesweb.civilview.com/Sales/SalesSearch?countyId=2) and gets the information of houses on auction.

get_property(address) scrapes Zillow (https://www.zillow.com/). Given an address of a house, the get_property function returns the address, year built, number of bedrooms, number of bathrooms, size, last sold year for the house, last_sold_price for the house


2. psql_create_tables.py

This file is run once in order to create the database and the tables. The user must change its name in line 8. There are 3 tables: foreclosure, property and plaintiff.


3. psql_upload_data.py

This file contains the function that upload the information to the database.
upload_data(list_foreclosures) iterates over the list and check if the foreclosure, property or plantiff already exist and depending on the result it is updated or inserted into the repective table.

Please notice that the page Zillow.com does not allow a significant number of data extractions via scraping, this is why when the initial data is inserted into the database (over 1,000 addresses), most of the property data will appear as NULL when it actually is available. For this reason, there is another function for scraping the complete information once the table is already built and the data (only the Id and address) is inserted. This function is called fix_property(start,end) and the command instructions to use it can be found at the bottom of the script. This function is necessary only to create the initial data base, as for when it’s being updated it won’t need to run as many scraping queries.


4. dbexport.pgsql

This is a psql database that resulted after running the run.py file, which serves as an example here.

5. auto_execute.sh

This file creates a loop that runs this entire program once a week.

## Run Instructions

1. Download this repo master branch to your local machine or cloud.

2. Change the username and password variables to your own SQL user name and password in both psql_create_tables.py and psql_upload_data.py files. This step is necessary to avoid password-related issues

3. Run the following comand line in terminal:

   bash bin/auto_execute
   
   Note: The initial process to pull the necessary data from the web and update the database takes approximately 10 to 15 mins. Once the initial load is complete, subsequent inserts and updates do not last long



