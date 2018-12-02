#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scraping_functions import *
import psycopg2


def upload_data(list_foreclosures):

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
        
        #eliminate special characters from numeric variables, as $ and thousand separator
        amount= row[8].replace(',', '')
        amount= amount.replace('$', '')
        amount= str(amount)
        
        #check if the sheriff_id already exists in the foreclosure table

        cur.execute("SELECT sheriff_id FROM foreclosure WHERE sheriff_id = '"+row[0]+"';")
        foreclosure_id = cur.fetchone()
        try:
            foreclosure_id[0]
        except:
            foreclosure_id = [""]
        
        if row[0] == foreclosure_id[0] : #foreclosure_id != []:
            #if it is an update, execute the query
            query_update_foreclosure = "UPDATE foreclosure SET last_status = '"+row[4]+"' ,last_status_date = '"+row[5]+"',  default_amount = "+amount+", sale_date = '"+row[9]+"';"
            cur.execute(query_update_foreclosure)
                
        else: #insert row
            
            #check if the property already exist
            cur.execute("SELECT address FROM property WHERE address ='"+row[1]+"';")
            property_address = cur.fetchone()
            try:
                property_address[0]
            except:
                property_address=[""]
       
            if row[1] == property_address[0]:
                cur.execute("SELECT id FROM property WHERE address = '"+row[1]+"';")
                property_id = cur.fetchone()[0]
            else:
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
                
        
                #Finish the property query and execute it
                query_property = query_property_0 + extra_data[0] + "'," + extra_data[1] + ","+extra_data[2]+","+extra_data[3]+","+sqft+","+extra_data[5]+","+price+");"           
                cur.execute(query_property)
                #find the foreign key from property
                cur.execute("SELECT id FROM property WHERE address = '"+extra_data[0]+"';")
                property_id = cur.fetchone()[0]
            
            #check if the plaintiff exist
            cur.execute("SELECT name FROM plaintiff WHERE name = '"+row[6]+"';")
            plaintiff_names = cur.fetchone()
            try:
                plaintiff_names[0]
            except:
                plaintiff_names = [""]
   
            if row[6] == plaintiff_names[0]:
                cur.execute("SELECT id FROM plaintiff WHERE name = '"+row[6]+"';")
                plaintiff_id = cur.fetchone()[0]
            else:
                try:
                    extra_data
                except:
                    #enrichment data from zillow. file: scraping_functions.py
                    extra_data = get_property(row[1])
                    #check if there is any value for the property or plaintiff table that should be NULL
                    for j in range(7):
                        if extra_data[j] == '--' or extra_data[j] =='No Data':
                            extra_data[j] = 'NULL'
                
    
                #Finish the plaintiff query and execute it
                query_plaintiff = query_plaintiff_0 + row[6]+"');"
                cur.execute(query_plaintiff)
                #find the foreign key from plaintiff
                cur.execute("SELECT id FROM plaintiff WHERE name = '"+row[6]+"';")
                plaintiff_id = cur.fetchone()[0]
                    
    
            #Finish the foreclosure query and execute it
            query_foreclosure = query_foreclosure_0 + row[0] + "',"+ str(property_id) + ",'"+row[2] +"','"+row[3]+"','"+row[4]+"','"+row[5]+"',"+str(plaintiff_id)+",'"+row[7]+"',"+amount+",'"+row[9]+"');"
            cur.execute(query_foreclosure)
    

        #make changes permanent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()
def fix_property(start,end): #function to fix the problem with zillow blocking more than a number of scrapings and info being uploaded as NULL
    conn = psycopg2.connect(dbname='foreclosures_db', user='gabrielapinto') #connect to the data base
    cur = conn.cursor()
    for entry in range(start,end): #get the id we want to fix
        cur.execute("SELECT address FROM property WHERE id ='"+str(entry)+"';") #find the address for the entry
        property_address = cur.fetchone()[0] #get the address for the entry id
        get_data_zillow = get_property(property_address) #try to find the property
        for i in range(7):
            if get_data_zillow[i] == '--' or get_data_zillow[i] =='No Data':
                get_data_zillow[i] = 'NULL'
        query_update = "UPDATE property SET year_built = "+str(get_data_zillow[1])+" ,num_of_bedrooms = "+str(get_data_zillow[2])+",  num_of_bathrooms = "+str(get_data_zillow[3])+",  sqft = "+str(get_data_zillow[4])+",  last_year_sold = "+str(get_data_zillow[5])+", last_price_sold = "+str(get_data_zillow[6])+" WHERE id = '"+str(entry)+"';" #update the property's data
        cur.execute(query_update)
    conn.commit() #commit changes
    # Close communication with the database
    cur.close() #close database
    conn.close()

#list_foreclosures = get_foreclosures() #list of scrapped foreclosures. file: scraping_functions.py
#upload_data(list_foreclosures)

#conn = psycopg2.connect(dbname='foreclosures_db', user='gabrielapinto')
#cur = conn.cursor()
#cur.execute("SELECT COUNT(id) FROM property ;")
#entries = cur.fetchone()[0]
 # Close communication with the database
#cur.close()
#conn.close()


#iterations = int(entries/50)
#for i in range(iterations):
#    fix_property((i+1)*50,min((iterations+2)*50+1,entries+1))
#    time.sleep(300)
