# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    img_urls_titles = mars_hemisphere(browser)
    
    data = {
        'news_title' : news_title,
        'news_paragraph' : news_paragraph,
        'featured_image' : featured_image(browser),
        "facts" : mars_facts(),
        'hemispheres' : img_urls_titles,
        'last_modified' : dt.datetime.now()
    }
    browser.quit()
    return data

def mars_news(browser):
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe    
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemisphere(browser):
    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for hem in range(4):
        # Browse through each article
        browser.links.find_by_partial_text('Hemisphere')[hem].click()
        
        # Parse the HTML
        html = browser.html
        hem_soup = soup(html,'html.parser')
        
        # Scraping
        title = hem_soup.find('h2', class_='title').text
        img_url = hem_soup.find('li').a.get('href')
        
        # Store findings into a dictionary and append to list
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        
        # Browse back to repeat
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())