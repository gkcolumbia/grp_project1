#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scraping_functions import *
import psycopg2


list_foreclosures = get_foreclosures() #list of scrapped foreclosures. file: scraping_functions.py

#common beginning of the querys for inserting data.
query_property_0 = "INSERT INTO property (id, address, year_built, num_of_bedrooms, num_of_bathrooms, sqft, last_year_sold, last_price_sold) VALUES (DEFAULT,'"
query_plaintiff_0 = "INSERT INTO plaintiff (id, name) VALUES (DEFAULT,'"
query_foreclosure_0 = "INSERT INTO foreclosure (sheriff_id, property_id,initial_status,initial_status_date,last_status,last_status_date,plaintiff_id, defendant, default_amount, sale_date) VALUES ( '"

#iterate the lists of foreclosures
for row in list_foreclosures:
    
    #open connection to database named tools_project using user josehija (change if necesary)
    conn = psycopg2.connect(dbname='tools_project', user='josehija')

    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    #check if there is any value for the foreclosure table that should be NULL
    for i in range(10):
        if row[i] == '--' or row[i] =='No Data':
            row[i] = 'NULL'
        
    #enrichment data from zillow. file: scraping_functions.py
    extra_data = get_property(row[1])
    
    #check if there is any value for the property or plaintiff table that should be NULL
    for j in range(7):
        if extra_data[j] == '--' or extra_data[j] =='No Data':
            extra_data[j] = 'NULL'
        
            
    #eliminate special characters from numeric variables, as $ and thousand separator
    sqft = extra_data[4].replace(',','')
    price = extra_data[6].replace(',', '')
    price = price.replace('$', '')
    price = str(price)
    amount= row[8].replace(',', '')
    amount= amount.replace('$', '')
    amount= str(amount)
    
    #Finish the property query and execute it
    query_property = query_property_0 + extra_data[0] + "'," + extra_data[1] + ","+extra_data[2]+","+extra_data[3]+","+sqft+","+extra_data[5]+","+price+");"           
    cur.execute(query_property)
    
    #Finish the plaintiff query and execute it
    query_plaintiff = query_plaintiff_0 + row[6]+"');"
    cur.execute(query_plaintiff)
    
    #find the foreign key from property
    cur.execute("SELECT id FROM property WHERE address = '"+extra_data[0]+"';")
    property_id = cur.fetchone()[0]
    
    #find the foreign key from plaintiff
    cur.execute("SELECT id FROM plaintiff WHERE name = '"+row[6]+"';")
    plaintiff_id = cur.fetchone()[0]
    
    #Finish the foreclosure query and execute it
    query_foreclosure = query_foreclosure_0 + row[0] + "',"+ str(property_id) + ",'"+row[2] +"','"+row[3]+"','"+row[4]+"','"+row[5]+"',"+str(plaintiff_id)+",'"+row[7]+"',"+amount+",'"+row[9]+"');"
    cur.execute(query_foreclosure)
    
    #print("success")
    
    #make changes permanent
    conn.commit()
    
    # Close communication with the database
    cur.close()
    conn.close()
        

