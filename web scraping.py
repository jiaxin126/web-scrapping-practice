#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install beautifulsoup4')


# In[2]:


get_ipython().system(' pip install lxml')


# In[3]:


get_ipython().system(' pip install requests')


# In[4]:


from bs4 import BeautifulSoup
import lxml
import requests


# # basics of beautifulsoup

# In[5]:


url= 'https://webscraper.io/test-sites/e-commerce/allinone/computers'


# In[9]:


#can we grab,200 can
page=requests.get(url)
page.text


# In[10]:


soup=BeautifulSoup(page.text,'lxml') 
#put it back as html format
soup
#run alone to check i get html webpage


# In[11]:


#tag
soup.header


# In[18]:


#navigable strings
tag=soup.header.p.string
tag


# In[21]:


#attributes
tag=soup.header.a
tag.attrs
tag['data-toggle']


# In[22]:


#add new attribute
tag['attrinute_new']='this is a new attribute'
tag.attrs


# In[23]:


tag


# # section 4: searching and extracting from the html

# In[24]:


url='https://webscraper.io/test-sites/e-commerce/allinone/phones/touch'
page=requests.get(url)
page


# In[25]:


soup=BeautifulSoup(page.text,'lxml')
soup


# In[26]:


soup.header.attrs


# In[27]:


#find mutiple tags
soup.find('header')
soup.find('div',{'class':'container test-site'})


# In[28]:


soup.find('h4',{'class':'pull-right price'})
#first occurence


# In[30]:


#find_all,output is different,all things
soup.find_all('h4',{'class':'pull-right price'})


# In[33]:


soup.find_all('p',{'class':'pull-right'})
#put everything in a list


# In[34]:


#the second one
soup.find_all('h4',{'class':'pull-right price'})[1]


# In[38]:


soup.find_all(id=True)
#find something with id


# In[40]:


#find in string
soup.find_all(string='Iphone')


# In[41]:


import re
soup.find_all(string=re.compile('Iph'))


# In[42]:


soup.find_all(string=re.compile('Nok'))


# In[49]:


#top 3
soup.find_all('p',class_=re.compile('pull'),limit=3)


# In[66]:


#make a table
product_name=soup.find_all('a',class_='title')
product_name


# In[53]:


price=soup.find_all('h4',class_='pull-right price')
price


# In[54]:


reviews=soup.find_all('p',class_=re.compile('pull'))
reviews


# In[56]:


description=soup.find_all('p',class_='description')
description


# In[65]:


#for loop
product_name_list=[]
for i in product_name:
    name=i.text
    product_name_list.append(name)
    
price_list=[]
for i in price:
    price2=i.text
    price_list.append(price2)
    
    
reviews_list=[]
for i in reviews:
    reviews2=i.text
    reviews_list.append(reviews2)
    

description_list=[]
for i in description:
    description2=i.text
    description_list.append(description2)


# In[68]:


import pandas as pd
table=pd.DataFrame({'Product Name':product_name_list,'Description':description_list,'Price':price_list,'Reviews':reviews_list})
table


# In[72]:


#extracting data from nested html tags
#get all informations for the third product
boxes=soup.find_all('div',class_='col-sm-4 col-lg-4 col-md-4')[2]
boxes


# In[75]:


boxes.find('a').text


# In[76]:


boxes.find('p',class_='description').text
#reduce html,to get what we want


# In[80]:


box2=soup.find_all('ul',class_='nav',id='side-menu')[0]
box2


# In[82]:


box2.find_all('li')[1].text #computer  ,with white space


# # section 5: project 1-scraping a table

# In[84]:


url = 'https://www.worldometers.info/world-population/'
requests.get(url)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

#Subsets the HTML to only get the HTML of our table needed
table = soup.find('table', class_ = 'table table-striped table-bordered table-hover table-condensed table-list')
table


# In[87]:


#coloumn name
headers=[]
for i in table.find_all('th'):
    header2=i.text
    headers.append (header2)
headers


# In[89]:


df=pd.DataFrame(columns=headers)
df


# In[92]:


#body
for j in table.find_all('tr')[1:]:
    #find each data
    row_data=j.find_all('td')
    #each row
    row=[td.text for td in row_data]
    #generate a dataframe
    length=len(df)
    df.loc[length]=row
    
df


# In[93]:


#df.to_csv('path')


# # section 6: project 2-dealing with multiple pages

# In[102]:


url='https://www.airbnb.com/s/Honolulu--Oahu--Hawaii--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&query=Honolulu%2C%20Oahu%2C%20HI&place_id=ChIJTUbDjDsYAHwRbJen81_1KEs&date_picker_type=calendar&checkin=2022-08-28&checkout=2022-08-31&source=structured_search_input_header&search_type=autocomplete_click'
page=requests.get(url)
page


# In[100]:


soup=BeautifulSoup(page.text,'lxml')


# In[105]:


df=pd.DataFrame({'links':[''],'title':[''],'price':[''],'rating':[''],'details':['']})
df


# In[ ]:


while True:
    
    posting=soup.find_all('div',class_='_8ssblpx')
    
#for loop go through each posting
#get everything in this posting
    for post in postings:
        try:
            link=post.find('a',class_='_gjfo10').get('href')
            link_full='https://www.airbnb.com'+link
            title=post.find('a',class_='_gjfo10').get('aria-label')
            price=post.find('span',class_='_1p7iugi').text
            rating=post.find('span',class_='10fy1f8').text
            details=post.find_all('div',class_='_kqh46o')[0].text
            df=df.append({'links':link_full,'title':title,'price':price,'rating':rating,'details':details},ignore_index=True)
        except:
            pass
        #some posting dosen't have rating, code will accept pass and go next loop
        
    #this part also in the while loop    
    next_page=soup.find('a',{'aria-label':'Next'}).get('href')
    next_page_full='https://www.airbnb.com'+next_page
    next_page_full
    #get next page url and scraping next page
    url=next_page_full
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'lxml')
    
df.to_csv('path')


# # section 7: javascript driven webpages

# In[106]:


#if we get a blank page, may be this is a javascript driven pages
#selenium is a browser automation tool,has many special functions

#1.click on a button
#2.sending text to an input box
#3.create a wait time for the page to load
#4.take a screenshot
#5.self scrolling


# In[114]:


import selenium
from selenium import webdriver


# # section 8: selenium

# In[123]:


from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://www.goat.com/sneakers')


# ### 1. xpath

# In[125]:


#xpath- path to access html documents ,keep going down the tree
#easy to find specific elements

#find_element
#price
driver.find_element('xpath','//*[@id="grid-body"]/div/div[1]/div[4]/a/div[1]/div[2]/div').text


# In[132]:


#see more
#driver.find_element('xpath','xpath').click()

#12 prices
for i in range(1,12):
    price=driver.find_element('xpath','//*[@id="grid-body"]/div/div[1]/div['+str(i)+']/a/div[1]/div[2]/div/div[1]').text
    print(price)


# ### 2. sending text into an inout box

# In[133]:


from selenium.webdriver.common.keys import Keys


# In[136]:


#sending text into an inout box
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.google.com/')


# In[139]:


#find the box
box=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
#input something
box.send_keys('what is webscraping')
#enter,begin searching
box.send_keys(Keys.ENTER)


# ### 3. click on a button

# In[140]:


#second way to search
box=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys('what is webscraping')

button=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
button.click()


# In[141]:


#click next button,just do one more time,exvery button we can click
link=driver.find_element('xpath','//*[@id="rso"]/div[1]/div/div/div/div[1]/div/a').click()


# ### 4. taking a sreenshot 

# In[142]:


driver.save_screenshot('/Users/wangjiaxin/Desktop/study program/data analysis/web scrping/screenshot.png')


# In[ ]:


#only a picture, only a title
driver.find_element('xpath','//*[@id="rso"]/div[1]/div/div/div/div[1]/div/a').save_screenshot('/Users/wangjiaxin/Desktop/study program/data analysis/web scrping/screenshot.png')


# In[148]:


#example-giraffe
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.google.com/')

box=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys('giraffe')
box.send_keys(Keys.ENTER)

driver.find_element('xpath','//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
driver.save_screenshot('/Users/wangjiaxin/Desktop/study program/data analysis/web scrping/screenshot2.png')


# ### 5. self-scrolling

# In[149]:


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.google.com/')

box=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys('giraffe')
box.send_keys(Keys.ENTER)

driver.find_element('xpath','//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()


# In[150]:


#return the height of the entire document
driver.execute_script('return document.body.scrollHeight')


# In[151]:


#scroll to a specific height, goes down and more images
driver.execute_script('window.scrollTo(0,6000)')
driver.execute_script('return document.body.scrollHeight')


# In[153]:


#combination of two,rerun the code until to the very buttom
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
#reach the end


# ### 6. wait time

# In[165]:


#some website need some time to load all things
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# In[166]:


#good way for some wibesites need long time to loading
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.google.com/')

box=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys('giraffe')
box.send_keys(Keys.ENTER)

#wait time code-
#wait 10 seconds to next page until we find the specific element
#until we find something(class,id,link...) match on this page
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'cntratet')))
#until find ID

#id is wrong, so there's nothing happen
#timeout exception

#image
driver.find_element('xpath','//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()


# In[167]:


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.google.com/')

box=driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
box.send_keys('giraffe')
box.send_keys(Keys.ENTER)

#wait 3 seconds and to the next page
#just to make sure we didn't miss something
time.sleep(3)

driver.find_element('xpath','//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()


# # section 9: project3-infinite scrolling

# In[169]:


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


# In[183]:


#nike
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.nike.com/w/road-running-shoes-37v7jz8kwewzy7ok')


# In[184]:


last_height=driver.execute_script('return document.body.scrollHeight')

while True:
    #scroll to the very bottum of the page
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)
    new_height=driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height=new_height
    


# In[185]:


#using beautifulsoup to get data

soup=BeautifulSoup(driver.page_source,'lxml')
product_card=soup.find_all('div',class_='product-card__body')
len(product_card)


# In[192]:


product=product_card[0]
price=product.find('div',class_='product-price is--current-price css-11s12ax').text
price


# In[194]:


#build a dataframe
df=pd.DataFrame({'link':[''],'name':[''],'subtitle':[''],'price':['']})

for product in product_card:
    #if there's any error, like missing value,code keeps going down
    try:
        link=product.find('a',class_='product-card__link-overlay').get('href')
        name=product.find('div',class_='product-card__title').text
        subtitle=product.find('div',class_='product-card__subtitle').text
        price=product.find('div',class_='product-price is--current-price css-11s12ax').text
        df=df.append({'link':link,'name':name,'subtitle':subtitle,'price':price},ignore_index=True)
    except:
        pass
    
df    


# In[195]:


df


# In[ ]:


df.to_csv('path')

