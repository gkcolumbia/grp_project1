#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import sys
# Username for the PostgreSQL database. The username value should be changed to the user's own username in the system

username = 'josehija'


# Create the tools_project database

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = None
con = connect(dbname='postgres', host='localhost', user=username)

dbname = "tools_project"

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute('CREATE DATABASE ' + dbname)
cur.close()
con.close()

# Connect to the tools_project database

conn = psycopg2.connect(dbname='tools_project', user=username)

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
columns = "id SERIAL PRIMARY KEY, address TEXT, year_built INT, num_of_bedrooms INT, num_of_bathrooms INT, sqft FLOAT, last_year_sold INT, last_price_sold FLOAT" 
create_table(name, columns)

name2 = "plaintiff"
columns_pl = "id SERIAL PRIMARY KEY, name VARCHAR"
create_table(name2, columns_pl)

table2 = "foreclosure"
columns_table2 = "sheriff_id TEXT PRIMARY KEY, property_id INT, initial_status VARCHAR, initial_status_date DATE, last_status VARCHAR, last_status_date DATE, plaintiff_id INT, defendant TEXT, default_amount FLOAT, sale_date DATE, FOREIGN KEY(property_id) REFERENCES property(id), FOREIGN KEY(plaintiff_id) REFERENCES plaintiff(id)"
create_table(table2, columns_table2)

#make changes permanent
conn.commit()
# Close communication with the database
cur.close()
conn.close()

    
    
