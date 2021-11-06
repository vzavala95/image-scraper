# citations used:
# https://stackoverflow.com/questions/28006690/getting-a-particular-image-from-wikipedia-with-beautifulsoup
# https://towardsdatascience.com/a-tutorial-on-scraping-images-from-the-web-using-beautifulsoup-206a7633e948
# https://www.geeksforgeeks.org/image-scraping-with-python/

from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
import requests
import re

app = Flask(__name__)


def wikimage_scraper(query):
    query = query.replace(" ", "_")
    url = 'https://en.wikipedia.org/wiki/' + query
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for cover in soup.findAll("img"):
        src = cover.get('src')
        if re.search('wikipedia/.*/thumb/', src) and not re.search('.svg', src):
            return src
    return "Sorry, we can't locate that image. Please try again!!"


@app.route('/')
def home():
    return "Hello! You have reached Victoria's Wikipedia Image Scraper! Search for an image with '/get_wikimage/query'"


@app.route('/get_wikimage/')
def search():
    return "Hello! Please search for an image using this format: '/get_wikimage/query'. Example: '/get_wikimage/apple'"


@app.route('/get_wikimage/<query>')
def get_wikimage(query):
    img = wikimage_scraper(query)
    return jsonify(img)