# -*- coding: utf-8 -*-
"""
Maneuvering.py
This is going to try to maneuver thru the database on the internet
Created on Wed Sep 19 11:49:59 2018

@author: abrehm
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

#open the start page
driver = webdriver.Chrome(executable_path=r'C:/Users/abrehm/Downloads/chromedriver_win32/chromedriver.exe')
driver.get('https://aviation-safety.net/database/events/event.php?code=AC');

#this is the list of links on the database I want to go to
"""
'Airplane - Airframe','Airplane - Engines',
'Airplane - Flight control surfaces','Airplane - Instruments',
'Airplane - Systems','Airplane - Undercarriage'
"""
issue_list = ['Airplane - Engines',
              'Airplane - Flight control surfaces','Airplane - Instruments',
              'Airplane - Systems','Airplane - Undercarriage']
for category in issue_list:
    #enter the link
    category_link = driver.find_element_by_link_text(category)
    time.sleep(0.1)
    category_link.click()
    
    #get the page source for that link
    list_source = driver.page_source
    #pass that into Beautiful Soup
    events_list = BeautifulSoup(list_source, 'lxml')

    for event_dates in events_list.find_all('a',href=re.compile('/database/record.php\W')):
        #so if there are two crashes on the same day, they will have the same text for the link which means,
        #when the program looks for the link, it will find only the first instance
        print(event_dates.text)
        date_link = driver.find_element_by_link_text(event_dates.text)
        time.sleep(0.1)        
        date_link.click()
        
        #get this pages source code
        event_source = driver.page_source
        #soup it
        event_soup = BeautifulSoup(event_source, 'lxml')
        
        time.sleep(0.1)
        driver.back()
    
    time.sleep(0.1)
    driver.back()

driver.close()