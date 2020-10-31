#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import dependencies
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests


# In[3]:


# Chromedriver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# website to scrape
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[5]:


# Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
# print(soup.prettify())
# Using BS, we can execute standard functions to capture the page's content

news_title=soup.find('li', attrs={'class': 'slide'}).find('h3').text
print(news_title)

news_p = soup.find('div', class_='article_teaser_body').text
print(news_p)      


# In[7]:


# website to scrape
img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(img_url)

# Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

featured_image_url = img_url + soup.find('li', class_='slide').find('a', class_='fancybox')['data-fancybox-href'] 
print(featured_image_url)
# print(soup.prettify())




# In[8]:


# Scrape Mars hemisphere image url and title
hemisphere_facts_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere_facts_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# capture all of the items in the item results
titles = soup.find_all('div', class_='item')

# find the list of categories in the left pane
lists = soup.find('div', class_='description')

image_urls = {}
try:
    for title in titles:

            for list in lists:

                # find the list of categories in the left pane
                lists = soup.find('div', class_='description')

                # Capture the category names and their URLs
                list = lists.find('h3').text
                image_urls[list] = lists.find('a')['href']
    # image_url I get one whoop! I do not know why it will not loop
    print(list + " "+ hemisphere_facts_url + image_urls[list])

except AttributeError as e:
    print(e)

                  




# In[191]:


#     # Dictionary to be inserted into MongoDB
    
hemisphere_image_urls = [
    {"Cerberus Hemisphere": list, "hemi_urls": hemisphere_facts_url + image_urls[list]},
]
hemisphere_image_urls


# In[9]:


# website to scrape
table_url = 'https://space-facts.com/mars/'
browser.visit(table_url)

# Capture Table
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

table = pd.read_html(table_url) 
print(table[0])
# print(soup.prettify())


# In[10]:


df = table[0]
df.columns = ['Description', 'Data']
df.set_index('Description', inplace=True)
df.head()


# In[ ]:




