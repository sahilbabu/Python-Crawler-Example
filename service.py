__version__ = "0.1"
__copyright__ = "CopyRight (C) 2015 by Mudassar Ali"
__license__ = "MIT"
__author__ = "Mudassar Ali"
__author_email__ = "sahil_bwp@yahoo.com"

import sys
import requests
from bs4 import BeautifulSoup


def request_handler(url, headers=False):
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'From': 'youremail@domain.com',  # This is another valid field
            'Referer' : 'http://www.namestation.com/domain-search?autosearch=1',
            'Connection': 'keep-alive',
            'Content-Type': 'text/html; charset=UTF-8',
            'Accept-Encoding': 'gzip'
        }
    response = requests.get(url, headers=headers)
    return response


def trade_spider(max_pages):
    print('function started')
    page = 1
    while page <= max_pages:
        print('while started')
        #url = "https://buckysroom.org/trade/search.php?page=" + str(page)
        url = 'http://pixgood.com'
        res = request_handler(url)
        plain_text = res.text
        #print(res.headers)
        #print(plain_text)
        # just get the code, no headers or anything
        #plain_text = source_code.text
        #print (plain_text)
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', {'class': 'image-link'}):
            href = link.get('href')
            #title = link.string  # just the text, not the HTML
            title = link.get('title')
            print(href)
            print(title)
            # get_single_item_data(href)
        page += 1
    print('end function')

'''
def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    # if you want to gather information from that page
    for item_name in soup.findAll('div', {'class': 'i-name'}):
        print(item_name.string)
    # if you want to gather links for a web crawler
    for link in soup.findAll('a'):
        href = "https://buckysroom.org" + link.get('href')
        print(href)
'''

trade_spider(1)
sys.exit()