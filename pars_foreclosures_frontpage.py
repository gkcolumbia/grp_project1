import bs4  # Beautiful Soup library helps us parse the content into objects. 
import requests
import re
import csv
import time

t0 = time.time()

session = requests.Session()
response = session.get('https://salesweb.civilview.com/Sales/SalesSearch?countyId=2')
soup = bs4.BeautifulSoup(response.content, 'html.parser')

session_id = response.cookies['ASP.NET_SessionId']

list_of_trs = soup.find_all('tr')
list_of_foreclosures = []
list_of_foreclosure_details = []

for item in list_of_trs:
    td_children = item.findChildren('td')
    if td_children:
        link = str(td_children[0].contents)[10:-14]
        sheriff_id = str(td_children[1].contents)[1:-1] #Sheriff ID
        sales_date = str(td_children[2].contents)[1:-1]
        plaintiff = str(td_children[3].contents)[1:-1]
        owner = str(td_children[4].contents)[1:-1]
        address = str(td_children[5].contents)[1:-1]
        list_of_foreclosures.append([sheriff_id,',',sales_date,',',
                                     plaintiff,',',owner,',',address,',',"'"+str(link)+"'"])
        

        
#Generation of Foreclosure summary extract from the Front Page
with open ('Foreclosure_extract.txt', 'w') as fp:
    for foreclosure in list_of_foreclosures:
        for details in foreclosure:
            fp.write(details)
        fp.write('\n')


#Extraction of Foreclosure details
list_of_foreclosures_details = []


for foreclosure in list_of_foreclosures:
    url = 'https://salesweb.civilview.com/'+foreclosure[10]
    response2 = session.get(url)
    soup2 = bs4.BeautifulSoup(response2.content, 'html.parser')
    list_of_tds = soup2.find_all('td')
    length_tds = len(list_of_tds)
    sheriff_id2 = str(list_of_tds[1])[4:-5] #Sheriff ID
    sales_date2 = str(list_of_tds[5])[4:-5]
    plaintiff2 = str(list_of_tds[7])[4:-5]
    owner2 = str(list_of_tds[9])[4:-5]
    address2 = str(list_of_tds[11])[4:-5].replace('<br/>', ' ')
    #description = str(list_of_tds[13])[4:-5]
    default_amount = str(list_of_tds[15])[4:-5]
    initial_status = str(list_of_tds[20])[4:-5]
    initial_status_date = str(list_of_tds[21])[4:-5]
    last_status = str(list_of_tds[length_tds-2])[4:-5]
    last_status_date = str(list_of_tds[length_tds-1])[4:-5]
    list_of_foreclosures_details.append([sheriff_id2,',',sales_date2,',',
                                     plaintiff2,',',owner2,',',address2,
                                ',',default_amount,',',initial_status,',',initial_status_date,
                                ',',last_status,',',last_status_date])

#Generation of Foreclosure details extract
with open ('Foreclosure_details_all.txt', 'w') as fp:
    for foreclosure in list_of_foreclosures_details:
        for details in foreclosure:
            fp.write(details)
        fp.write('\n')

# t1 = time.time()
# print('Done')
# print(t1-t0)

