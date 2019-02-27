# Dependencies
import pymongo
import pandas as pd
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import numpy as np
from pprint import pprint
import time

def scrape():

    mars_data = {}
    # ### NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())
    #news_title = soup.find("div", {"class":"content_title"}).find("a").text.strip()
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find("div", class_="rollover_description_inner").text.strip()
    #print(news_title)
    #print(news_p)
    mars_data ['title'] = news_title
    mars_data ['paragraph'] = news_p

    # ### JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    executable_path = {'executable_path':'./chromedriver.exe'}  
    browser = Browser("chrome", **executable_path, headless=False)
    #browser = init_browser()
        # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_id('full_image')
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())
    full_article =soup.find('article', class_="carousel_item")
    #print(full_article)
    trim_article = full_article['style'].lstrip("background-image: url('")
    relative_path = trim_article.strip("'');")
    relative_path = relative_path.strip ("'")
    #print(url)
    #print(relative_path)
    featured_image_url = url + relative_path
    #print(featured_image_url)
    #if soup.find("meta", property= "og:description")is not None:
    #    relative_path = soup.find("img", class_="fancybox-image")
    #rel_path = soup.find("img", class_ = "fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open")
    #print(rel_path["src"])
    mars_data ['featured_image_url'] = featured_image_url

    # ### Mars Weather
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    weather_clean = weather.rstrip(" hPapic.twitter.com/1msjBvhiu7'")
    weather_clean = weather_clean.replace('\n','')
    mars_weather = weather_clean
    #mars_weather
    mars_data ['weather'] = mars_weather

    # ### Mars Facts
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    mars_facts_df = pd.read_html(url)
    #mars_facts_df
    mars_facts = mars_facts_df[0]
    mars_facts.columns = ["Item", "Measurements"]
    mars_facts.set_index(["Item"])
    mars_facts_html = mars_facts.to_html(classes=None, border=None, justify=None)

    mars_data ['mars_facts_html'] = mars_facts_html

    # ### Mars Hemispheres
    # URL of page to be scraped
    executable_path = {'executable_path':'./chromedriver.exe'}  
    browser = Browser("chrome", **executable_path, headless=False)
    #browser = init_browser()
        # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #browser.click_link_by_id('full_image')
    #print(soup.prettify())
    hemisphere_list = []

    for counter,x in enumerate(soup.find_all("a",class_ = "itemLink product-item"),1):
        for img in x.find_all("img", alt=True):
            hemisphere_dictionary = {}
            scraped_title = (img['alt'])
            cleaned_title = scraped_title.replace(' Enhanced thumbnail','')
            img_clean_title = scraped_title.replace(' Hemisphere','')
            img_clean_title = img_clean_title.replace(' thumbnail','')
            img_clean_title = img_clean_title.replace(' ','_') 

        #print(cleaned_title)
            hemisphere_dictionary['atitle'] = cleaned_title
            #print(img_clean_title)
            executable_path = {'executable_path':'./chromedriver.exe'}  
            browser = Browser("chrome", **executable_path, headless=False)
            img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/'+img_clean_title
            #print(img_url)
            browser.visit(img_url)
            time.sleep(1)
            browser.find_link_by_text('Sample').first.click()
            time.sleep(1)
            browser.windows.current = browser.windows[-1] #the image window is set as the current window
            img_html = browser.html  #the html for the image window is pulled
            browser.windows[0].close() # closes the original window,leaving only the image window
            img_soup = BeautifulSoup(img_html, "html.parser")
            #pprint(img_soup)
            #print(img_html)
            #print(img_soup)
            final_img_url = img_soup.find('img')['src']
            print(final_img_url)
            hemisphere_dictionary['image_url'] = final_img_url
            
            hemisphere_list.append(hemisphere_dictionary)
            mars_data['hemisphere_list'] = hemisphere_list

            return mars_data        
