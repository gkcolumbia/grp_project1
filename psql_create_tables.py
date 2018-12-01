#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 17:19:37 2018

@author: María José Gamonal Sáenz

"""

import psycopg2
conn = psycopg2.connect(dbname='tools_project', user='josehija')

# Open a cursor to perform database operations
cur = conn.cursor()

def create_table(name,columns):
    """
    columns = 'id TYPE PRIMARY KEY, col2 TYPE2, col3 TYPE3 '
    """
    #query for creating table
    query = "CREATE TABLE "+ name +" (" + columns + ");"
    
    #execute query
    cur.execute(query)

name = "property"
columns = "property_id SERIAL PRIMARY KEY, address TEXT, year_built INT, num_of_bedrooms INT, num_of_bathrooms INT, sqft INT" 
#create_table(name, columns)


table2 = "foreclosure"
columns_table2 = "foreclosure_id SERIAL PRIMARY KEY, sheriff_num TEXT, initial_status TEXT, initial_status_date TEXT, last_status TEXT, last_status_date TEXT, last_update_date TEXT, plaintiff_id INT, defendant_id INT, default_amount INT, last_sale_date TEXT,property_id INT"
create_table(table2, columns_table2)

#make changes permanent
conn.commit()
# Close communication with the database
cur.close()
conn.close()

    
    