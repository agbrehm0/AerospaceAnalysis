"""
ScrapeSingleEvent.py
Scrapes information from 01-mar-2003.htmm which is just a random event page that I got from the database. It then writes the information
to a csv file called practice.csv.
Created on Tue Sep 18 16:40:58 2018

@author: abrehm
"""

from bs4 import BeautifulSoup
import csv
import re

with open('01-mar-2003.htm') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

csv_file = open('practice.csv','w', newline='')

csv_writer = csv.writer(csv_file)

#get the date field (even tho there will already be a date field in the table)
date = soup.find_all('tr')[1]
date = date.find_all('td')[1].text
csv_writer.writerow(['Date',date])

#get fields and values from the table
for label in soup.find_all('tr'):
    caption = label.find('td', class_='caption').text
    
    try:
        desc = label.find('td', class_='desc').text
    except Exception as e:
        desc = None
    
    csv_writer.writerow([caption,desc])

#narrative field  
narr = soup.find('span', lang='en-US').text
csv_writer.writerow(['Narrative',narr])

classification = soup.find_all('a',href=re.compile('/database/events/dblist.php\W'))

for i in range(len(classification)):
    classification[i] = classification[i].text
csv_writer.writerow(['Classification',classification])    
    
csv_file.close()
