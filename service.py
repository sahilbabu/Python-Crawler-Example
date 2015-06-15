__author__ = 'coeus'

import sys
import requests
import httplib2
import urllib.request
import urllib.parse
#import urllib2
from bs4 import BeautifulSoup
import pprint

url = 'http://pixgood.com'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'From': 'youremail@domain.com',  # This is another valid field
    'Referer' : 'http://www.namestation.com/domain-search?autosearch=1',
    'Connection': 'keep-alive',
    'Content-Type': 'text/html; charset=UTF-8',
    'Accept-Encoding': 'gzip'
}

response = requests.get(url, headers=headers)
plain_text = response.text
print(response.headers)
print(plain_text)
'''
opener = urllib.request.build_opener()
opener.addheaders=[
                    ('Accept', 'application/json, text/javascript, */*; q=0.01'),
                    #('X-Requested-With', 'XMLHttpRequest'),
                    ('Referer', 'http://www.namestation.com/domain-search?autosearch=1'),
                    #('Host', 'www.namestation.com'),
                    ('Content-Type', 'text/html; charset=UTF-8'),
                    ('Accept-Encoding', 'gzip'),
                    ('Connection', 'keep-alive')
                ]
#response = opener.open('http://www.imgwhoop.com')
with opener.open("http://pixgood.com") as f:
    print(f.read().decode('utf-8'))

#print(response.info())


#html = response.read()


req = urllib.request.Request('http://www.imgwhoop.com')
req.add_header('Referer', 'http://www.python.org/')
response = urllib.request.urlopen(req)

#url_content = urllib.request.urlopen("https://buckysroom.org/trade/search.php?page=1").read()
print(response)
'''
sys.exit()

'''
resp, content = httplib2.Http().request("https://buckysroom.org/trade/search.php?page=1")
print (resp)
print (content)
'''

def trade_spider(max_pages):
    print('function started')
    page = 1
    while page <= max_pages:
        print('while started')
        url = "https://buckysroom.org/trade/search.php?page=" + str(page)
        #url = "http://www.imgwhoop.com"
        source_code = requests.get(url)
        print (source_code.status_code)
        print (source_code.headers['content-type'])
        sys.exit('debugg')
        # just get the code, no headers or anything
        plain_text = source_code.text
        #print (plain_text)
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', {'class': 'feature-link'}):
            href = link.get('href')
            title = link.string  # just the text, not the HTML
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

#trade_spider(1)