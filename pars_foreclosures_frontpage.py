import bs4  # Beautiful Soup library helps us parse the content into objects. 
import requests
import re

response = requests.get('https://salesweb.civilview.com/Sales/SalesSearch?countyId=2')
soup = bs4.BeautifulSoup(response.content, 'html.parser')

list_of_trs = soup.find_all('tr')
list_of_foreclosures = []

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
                                     plaintiff,',',owner,',',address,',',str(link)])


with open ('Foreclosure_extract.txt', 'w') as fp:
    for foreclosure in list_of_foreclosures:
        for details in foreclosure:
            fp.write(details)
        fp.write('\n')
