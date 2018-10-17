# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:09:08 2018

@author: Andreas Stöckl
"""

import sqlite3
import re
import pandas as pd

conn = sqlite3.connect('C:/sqlite/reutersdata_clean.db')
cur = conn.cursor()

def bereinigeReuters(txt):
    if txt != None:
        txt = re.sub(".*\(Reuters\) - ","",txt)
        txt = re.sub("Unsere Werte:Die Thomson Reuters Trust Principles","",txt)
        txt = re.sub("Editing by.*","",txt)
        txt = re.sub("Writing by.*","",txt)
        txt = re.sub("Reporting by.*","",txt)
        txt = re.sub("Additional reporting by.*","",txt)

    return txt

def datumReuters(txt):
    if txt != None:
        txt = txt.split("/")[0]
        txt = pd.to_datetime(txt)
    return str(txt)
    

conn2 = sqlite3.connect('C:/sqlite/reutersdata.db')
cur2 = conn2.cursor()

sqlstr = 'SELECT url,Kategorie,Titel,Body,Datum FROM Links'
for row in cur2.execute(sqlstr):
    if row[1] != None:
        cur.execute('''INSERT OR REPLACE INTO Artikel 
                (url,Kategorie,Titel,Body,Datum,Quelle,Fake) VALUES ( ?,?,?,?,?,?,? )''', (row[0],row[1],row[2],bereinigeReuters(row[3]),datumReuters(row[4]),"Reuters",0 ) )
conn.commit()    
cur2.close()
cur.close()