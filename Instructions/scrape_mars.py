from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    context = {}
    context["p_data"] = scrape1()
    context["f_image"] = scrape2()
    context["m_facts"] = scrape3()
    context["h_images"] = scrape4()
    return context

# Scrape the data from the NASA site.
def scrape1():
    browser = init_browser()
    news = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)
    print(browser.html)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news["news_title"] = soup.find('div', class_="bottom_gradient").get_text()
    news["news_p"] = soup.find('div', class_="article_teaser_body").get_text()
    
    return news

# Scrape the data from the JPL site.
def scrape2():
    browser = init_browser()
    featured_image_url = {}

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)
    full_image = browser.find_by_id("full_image")
    full_image.click()
    more_info = browser.find_link_by_partial_text("more info")
    more_info.click()
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find('figure', class_ = "lede")

    featured_image_url = result.find('a')["href"]
    featured_image_url = f"https://www.jpl.nasa.gov{featured_image_url}"
    

    return featured_image_url

# Scrape the data from the Space Facts site.
def scrape3():
    browser = init_browser()
    mars_facts = {}

    import pandas as pd  # Is this going to work, importing pandas in python?
    url = "https://space-facts.com/mars/"
    facts_df = pd.read_html(url)[0]
    facts_df = facts_df.rename(columns={0:"Description", 1:"Data"})
    mars_facts = facts_df.to_html(index=False)
    

    return mars_facts

# Scrape the data from the USGS Astrogeology site.
def scrape4():
    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    test_1 = soup.find_all('div', class_ = "item")
    #print(test_1)

    result = []

    for item in test_1:
        title = item.find('h3').text
        
        url_test =  item.find('a')['href']
        url_1 = f"https://astrogeology.usgs.gov{url_test}"
        browser.visit(url_1)
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.prettify())
        image_url = soup.find("div", class_ = "downloads")
        #print(image_url)
        url = image_url.find('a')["href"]
        result.append({"title": title,  "img_url": url})
    

    return result
