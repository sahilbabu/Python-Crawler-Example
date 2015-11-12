__version__ = "0.1"
__copyright__ = "CopyRight (C) 2015 by Mudassar Ali"
__license__ = "MIT"
__author__ = "Mudassar Ali"
__author_email__ = "sahil_bwp@yahoo.com"

import sys
import requests
from bs4 import BeautifulSoup
from datetime import  datetime
import time
import re
import mysql.connector

config = {
  'user': 'root',
  'password': 'pass123',
  'host': '127.0.0.1',
  'database': 'scrapper',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
# cnx.close()

today = datetime.now().date()

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
        base_url = 'http://www.mangareader.net'
        url = 'http://www.mangareader.net/naruto'
        res = request_handler(url)
        plain_text = res.text
        #print(res.headers)
        #print(plain_text)
        # just get the code, no headers or anything
        #plain_text = source_code.text
        #print (plain_text)
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text)
        # for link in soup.findAll('a', {'class': 'image-link'}):
        #     href = link.get('href')
        #     #title = link.string  # just the text, not the HTML
        #     title = link.get('title')
        #     print(href)
        #     print(title)
        # get_single_item_data(href)
        coverDiv = soup.findAll('div', attrs={'id' : 'mangaimg'})
        for div in coverDiv:
            cover  = div.img['src']
            print(cover)
        nameh2 = soup.findAll('h2', attrs={'class' : 'aname'})
        for h2 in nameh2:
            title  = h2.text
            cleanString = re.sub('\W+','', title )
            print(cleanString)
        # altNames = soup.find('td', attrs={'class':'propertytitle'}).findNext('td').text
        # print(altNames)
        DATA_SET = {}
        table = soup.find("div",{"id":"mangaproperties"}).find("table")
        rows = table.findAll('tr')
        # rows = table.find("tbody")
        for row in rows:
            cells = row.find_all("td")
            # print (cells[0].get('class'))
            # print (cells[1].get('class'))
            cellTitle = cells[0].get_text()
            cellValue = cells[1].get_text()
            if cellTitle == 'Name:':
                manga_title = cellValue
                print(cellValue + ": name")
            if cellTitle == 'Alternate Name:':
                manga_names = cellValue
                print(cellValue + ": Alternate Name:")
            if cellTitle == 'Year of Release:':
                manga_release = cellValue
                print(cellValue + ": Release")
            if cellTitle == 'Status:':
                manga_status = cellValue
                print(cellValue + ": Status")
            if cellTitle == 'Author:':
                manga_author = cellValue
                print(cellValue + ": Author")
            if cellTitle == 'Artist:':
                manga_artist = cellValue
                print(cellValue + ": Artist")
            if cellTitle == 'Genre:':
                manga_genre = ""
                print(cellValue + ": Genre")
                for link in cells[1].findAll('span', {'class': 'genretags'}):
                    genra = link.get_text()
                    manga_genre += genra + ', '
                    print (genra);
            # if cellTitle == 'Status:':
            #     print(cellTitle + ": name")
        synope = soup.find('div', attrs={'id':'readmangasum'}).find('p').text
        print (synope);

        # adding the data into mysql
        # add manga main data
        now = time.strftime('%Y-%m-%d %H:%M:%S');
        add_manga = "INSERT INTO manga (title,status,author,artist,genre,cover,synopsis,release_year,fetched,names,manga_url,from_url) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data_manga = (cleanString, manga_status, manga_author, manga_artist, manga_genre, cover,synope,manga_release,now,manga_names,url,base_url)
        # cursor.execute(add_manga, data_manga)
        # manga_id = cursor.lastrowid
        # print (manga_id)
        # cnx.commit()
        manga_id = 0


        table = soup.find("div",{"id":"chapterlist"}).find("table")
        rows = table.findAll('tr')
        # rows = table.find("tbody")
        for row in rows:
            cells = row.find_all("td")
            if cells:
                # print (cells)
                print ('---------------------------------------')
                # print (cells[1].get('class'))

                link = cells[0].find("a")
                href = link.get('href')
                title = link.text
                label = cells[0].text
                labelFormated = label.replace(title, '').replace(':', '').strip()
                cellValue = cells[1].get_text()
                print (labelFormated)
                print(href)
                print(title)
                print(cellValue)
                chapter_url = base_url + href

                # naive_dt = datetime.strptime(cellValue, '%d/%m/%Y')
                # print(naive_dt)

                # adding the data into mysql
                # add manga main data
                now = time.strftime('%Y-%m-%d %H:%M:%S');
                add_chapter = "INSERT INTO chapter (m_id,title,url_needle,url_base,url_full,fetched) " \
                        "VALUES (%s,%s,%s,%s,%s,%s)"
                data_chapter = (manga_id,labelFormated,href,base_url,chapter_url,now)
                # cursor.execute(add_chapter, data_chapter)
                # chapter_id = cursor.lastrowid
                # print (manga_id)
                # cnx.commit()

        page += 1
        # closing connection
        cursor.close()
        cnx.close()
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