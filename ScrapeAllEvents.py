"""
ScrapeAllEvents.py
This script is going to access every event that relates to airplane part failure. Unfortunately, the links are not all on the same 
page which means I have to figure out a way to go to the next page once there are no more event links on that page. It also means I 
need to write a for loop at the end of the main for loop that has the driver click the back button the correct amount of times. The 
last thing I need to figure out is how to put the output into an organized file (most likely a csv file).
Created on Wed Sep 19 11:49:59 2018

@author: Aaron Brehm
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

# Tell the program where 'chromedriver.exe' is
driver = webdriver.Chrome(executable_path=r'C:/Users/abrehm/Downloads/chromedriver_win32/chromedriver.exe')

# Tell the driver to go the initial page of the database
driver.get('https://aviation-safety.net/database/events/event.php?code=AC');

# This is the list of links on the database I want to go to
# There are more links than this but the others are just more specific

issue_list = ['Airplane - Airframe','Airplane - Engines',
              'Airplane - Flight control surfaces','Airplane - Instruments',
              'Airplane - Systems','Airplane - Undercarriage']

# This is the main loop of the program
for category in issue_list:
    # Get and enter the category link where the list of events will be
    category_link = driver.find_element_by_link_text(category)
    category_link.click()
    
    # Get the list of events page's source code
    list_source = driver.page_source
    # Pass that into Beautiful Soup
    events_list = BeautifulSoup(list_source, 'lxml')

    # This for loop will get all of the links and save them in event_dates one at a time
    for event_dates in events_list.find_all('a',href=re.compile('/database/record.php\W')):        
        # Very first thing to do is get the date value from the text of the link since it's better formatted than 
        # the date value on the actual event page
        print(event_dates.text)
        
        # Get and enter the link to where the data will be
        date_link = driver.find_element_by_link_text(event_dates.text)
        date_link.click()
        
        # Get the event page's source code
        event_source = driver.page_source
        # Pass it into Beautiful Soup
        event_soup = BeautifulSoup(event_source, 'lxml')
        
        # Before Scraping just a note: I am probably going to have a file with column headers already in them.
        # The thing is, I don't know how to write a single observation for a single factor.
        # There's csv_writer(csv_file).writerow() and that would work if I was able to save all of the scraped
        # values into variables, but the following for loop doesn't allow me to do that
        
        #SCRAPING THE DATA
        for desc in event_soup.find_all('td', class_='desc'):
            #print(desc.text)
            pass #for now
            
        narr = event_soup.find('span', lang='en-US').text
        #print(narr)
        
        classification = event_soup.find_all('a',href=re.compile('/database/events/dblist.php\W'))
        for i in range(len(classification)):
            classification[i] = classification[i].text
        #print(classification)
        #SCRAPING THE DATA
        
        driver.back()
    
    driver.back()

driver.close()
