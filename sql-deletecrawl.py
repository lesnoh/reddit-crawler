#!/usr/bin/env python3
# Michael Honsel 12/2017
import sys
import os, errno;
import psycopg2

#Datenbankverbindung herstellen

conn = psycopg2.connect(host='192.168.56.1',dbname='crawlerdb',user='postgres',password='sa',connect_timeout='3')
# Erstelle einen cursor welcher querys executen kann
cursor = conn.cursor()

def deletecrawlid(crawlid):
    #### Tabellen leeren (nur für Testphase)!!
    cursor.execute("""delete from tbl_comment where crawlid="""+str(crawlid))
    conn.commit()
    cursor.execute("""delete from tbl_submission where crawlid="""+str(crawlid))
    conn.commit()
    cursor.execute("""delete from tbl_crawl where crawlid="""+str(crawlid))
    conn.commit()
    return (0);

deletecrawlid(141)
cursor.close()
conn.close()
