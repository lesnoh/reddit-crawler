#!/usr/bin/env python3
# Michael Honsel 12/2017
import sys
import time;
import datetime;
import os, errno;
import psycopg2 as pg
import pandas as pd
import calendar

conn = pg.connect(host='192.168.56.1',dbname='crawlerdb',user='postgres',password='sa',connect_timeout='3')
cursor = conn.cursor()

def queryme( query ):
    "SQL-Abfragen auf der Crawlerdb"
    ausgabe = pd.read_sql(query , conn)
    print (ausgabe)
    return ausgabe;


def unixt(zeit="1987-08-07 00:00:00"):
    "Zeitangabe YYYY-MM-DD HH:MM:SS in Sekunden seit 01.01.1970"
    epoch = int(calendar.timegm(time.strptime(zeit, '%Y-%m-%d %H:%M:%S')))
    return epoch;

def topauthorzeit(anfang, ende):
    "Top Authoren in Zeitspanne auflisten"
    print ("\nAuswertung für: "+anfang+" bis "+ende)
    start = unixt(anfang+" 00:00:00")
    stop  = unixt(ende  +" 23:59:59")
    a = queryme('select subreddit,author,count(author) as count, sum(ups) as score from tbl_submission where timestamp_utc >= '+str(start)+' and timestamp_utc <= '+str(stop)+' group by subreddit,author order by count desc limit 12;')
    b = queryme('select author,count(author) as count, sum(ups) as score from tbl_submission where timestamp_utc >= '+str(start)+' and timestamp_utc <= '+str(stop)+' group by author order by count desc limit 12;')

#    print(b.author[:])
#    print(b.score[:])
#    b.author[:].values_counts()[:].plot(kind='barh')
    return a, b;

#select subreddit,count(subreddit) as count from tbl_submission group by subreddit order by count desc;
#select subreddit,count(subreddit) as count from tbl_submission where crawlid=71 group by subreddit order by count desc limit 6;
#select subreddit,author,count(author) as count from tbl_submission where crawlid=72 group by subreddit,author order by count desc limit 6;
#select subreddit,author,count(author) as count, sum(ups) as score from tbl_submission group by subreddit,author order by count desc limit 12

#topauthorzeit("2017-12-01", "2017-12-07")
#topauthorzeit("2017-12-08", "2017-12-14")
#topauthorzeit("2017-12-14", "2017-12-24")

topauthorzeit("2017-12-12", "2017-12-12")

cursor.close()
conn.close()
