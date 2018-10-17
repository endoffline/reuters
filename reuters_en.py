# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:55:01 2018

@author: Andreas Stöckl
"""
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

import sqlite3

conn = sqlite3.connect('C:/sqlite/test.db')
cur = conn.cursor()


for i in range(1,20):
    url = "https://www.reuters.com/news/archive?view=page&page=" + str(i) + "&pageSize=10"
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    teaser = soup.find_all("div", class_="story-content")
    for art in teaser:
        link = art.find("a")
        link = "https://de.reuters.com" + link.get('href')
        cur.execute('''INSERT OR IGNORE INTO Links (url) VALUES ( ? )''', (link, ) )
conn.commit()
cur.close()


def loadArtikelReut(url):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    kat = soup.find_all("div", class_="ArticleHeader_channel")

    if kat != []:
        kat = kat[0].get_text()
    else:
        return None    
    date = soup.find_all("div", class_="ArticleHeader_date")

    if date != []:
        date = date[0].get_text()
    else:
        return None
    title = soup.find_all("h1", class_="ArticleHeader_headline")
 
    if title != []:
        title = title[0].get_text()
    else:
        return None
    body = soup.find_all("div", class_="StandardArticleBody_body")

    if body != []:
        body = body[0].get_text()
    else:
        return None
    
    cur.execute('''INSERT OR REPLACE INTO Links (url,Kategorie,Titel, Body, Datum, crawled) VALUES (?,?,?,?,?,?)''', (url,kat,title,body,date,"1" ) )
    return None

conn = sqlite3.connect('C:/sqlite/test.db')
cur = conn.cursor()

cur.execute('SELECT url,crawled FROM Links')
sel = cur.fetchmany(400)
for row in sel:
    if row[1] != "1":
        loadArtikelReut(row[0])
conn.commit()
cur.close()
