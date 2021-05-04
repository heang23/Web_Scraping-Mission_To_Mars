from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

############################################################
### Visit the NASA Mars news site
############################################################
def scrape_data():
# Set Executable Path & Initialise chrome browser
    executable_path = {"executable_path": ChromeDriverManager()}
    browser = Browser("chrome", **executable_path, headless=False) # set headless to True once we done with the testing

    url_mars = 'https://mars.nasa.gov/news/'
    browser.visit(url_mars)
    time.sleep(1)
# Scrape  page into Soup
    html_mars = browser.html
    soup_Mars = BeautifulSoup(html_mars, "html.parser")
# Get first mars news title and first new paragraph
    try:
        results_Mars = soup_Mars.select_one("ul.item_list li.slide")
        results_Mars.find("div", class_="content_title")
# Scrape the latest news title
        title_Mars = results_Mars.find("div", class_="content_title").get_text()
# Scrape the latest paragraph text
        para_Mars = results_Mars.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

############################################################
### Visit JPL Mars Space Images - Featured Image
############################################################

    url_JPL = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_JPL)
    time.sleep(1)
    # Scrape  page into Soup
    html_JPL = browser.html
    # Parse HTML results with Soup
    try:
        soup_JPL = BeautifulSoup(html_JPL, 'html.parser') 
        full_img = soup_JPL.find("div", class_="header")
        image_url = full_img.find("img", class_="headerimage fade-in").get("src")
    # Use base URL to obtain absolute URL
    except AttributeError:
        return None
############################################################
### Visit Mars Facts
############################################################

    url_facts  = 'https://space-facts.com/mars/'
    Mars_table = pd.read_html(url_facts)
    time.sleep(1)
    table_df = Mars_table[1]
    table_df.columns = ["Mars - Earth Comparison", "Mars", "Earth"]
    table_df = table_df.iloc[0:]
    table_df.set_index('Mars - Earth Comparison', inplace=True)

############################################################
### Mars Hemispheres
############################################################

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    results = hemi_soup.find_all("div", class_='item')
# Loop over result to get title and image url of products
    for result in results:
    # Error handling
        try:
            img_hemi = result.find('a', class_='itemLink product-item')
            img_url_hemi = img_hemi.find('img', class_='thumb').get("src")
            title_hemi = result.find('div', class_='description')
            title_text = title_hemi.a.h3.text
        except AttributeError:
            return None, None

############################################################
### Web Scraping
############################################################

    web_data = {
        "News_title": title_Mars,
        "New_paragraph": para_Mars,
        "Featured_image": image_url,
        "Mars_facts": table_df,
        "Hemisphere_url": img_url_hemi,
        "Hemisphere_title": title_text
    }
    # Close the browser after scraping
    browser.quit()

    # return results
    return web_data


 

