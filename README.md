# Mission To Mars 

## Overview
Using BeautifulSoup and Splinter to scrape full-resolution images of Mars’s hemispheres and the titles of those images, store the scraped data on a Mongo database, use a web application to display the data, and alter the design of the web app to accommodate these images.

## Summary 
The Scraping was a success!! 

![scrapeing_successful](/Resources/scrapeing_successful.png)

Mars Hemispheres: Cerberus Hemisphere, Schiaparelli Hemisphere, Syrtis Major Hemisphere, and Valles Marineris Hemisphere

![Mars_Hemispheres](/Resources/Mars_Hemispheres.png)

## On different devices
The two images below shows how it would look on the following devices: 

**1. iPhone 12 Pro**

![iPhone12pro](/Resources/iPhone12pro.png)


**2. Surface Pro 7** 

![surfacepro7](/Resources/surfacepro7.png)

## Coding 

The following code was inserted to add the Mars hemispheres on to the website: 

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

This is the code in app.py:

    from flask import Flask, render_template, url_for
    from flask_pymongo import PyMongo
    import scraping


    app = Flask(__name__)

    # Use flask_PyMongo to set up mongo connection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
    mongo = PyMongo(app)

    @app.route("/")
    def index():
        mars = mongo.db.mars.find_one()
        return render_template("index.html", mars=mars)

    @app.route("/scrape")
    def scrape():
        mars = mongo.db.mars    
        mars_data = scraping.scrape_all()
        mars.update_one({}, {"$set": mars_data}, upsert=True)
        return "Scraping Successful!"
        
    if __name__ == "__main__":
        app.run(debug=True)
