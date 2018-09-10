#!/usr/bin/env python3
# Michael Honsel 12/2017
import sys
import praw
import json
import time;
import datetime;
import calendar;
import os, errno;
import psycopg2
import pprint
import pytz
from collections import defaultdict

reddit = praw.Reddit(client_id='cx0Rhc8hfD-2cA',
                     client_secret='gP-QBQDaC4h8IL8QqI2iQ9ZYzqs',
                     username='',
                     password='',
                     user_agent='py:rcrawler:v0.4'
)

def unixt(zeit="1987-08-07 00:00:00"):
    "Zeitangabe YYYY-MM-DD HH:MM:SS in Sekunden seit 01.01.1970"
    epoch = int(calendar.timegm(time.strptime(zeit, '%Y-%m-%d %H:%M:%S')))
    return epoch;

#Datenbankverbindung herstellen

conn = psycopg2.connect(host='192.168.56.1',dbname='crawlerdb',user='postgres',password='sa',connect_timeout='3')
# Erstelle einen cursor welcher querys executen kann
cursor = conn.cursor()

reddit.read_only = "true"
forum = "all"
#forum = "darkjokes"
#forum = "dark"
#forum = "talesfromtechsupport"
#forum = "france"
#forum = "de"


sub_start = unixt("2017-12-21 00:00:00")
sub_end   = unixt("2017-12-21 23:59:59")

subreddit = reddit.subreddit(forum)

#OutputDirectory
directory = 'output/' + str(forum)+ '-' + str(sub_start) + '-' + str(sub_end)
directorysql = str(forum)+ '-' + str(sub_start) + '-' + str(sub_end)

if not os.path.exists(directory):
            os.makedirs(directory)

cursor.execute("""insert into tbl_crawl (CrawlBezeichnung) Values(%s)""",(directorysql,))
conn.commit()

cursor.execute("""SELECT crawlid from tbl_crawl order by crawlid desc Limit 1""")
latestCrawlID = cursor.fetchone()
conn.commit()

crawlid = (latestCrawlID[0])

# Assoziativer Arrays zum Zählen der aktiven Teilnehmer und deren Up und
# Downvotes
dictSubreddit = defaultdict(int)
dictAuthoren = defaultdict(int)
dictAuthorenUps = defaultdict(int)
dictCAuthoren = defaultdict(int)
dictCAuthorenScore = defaultdict(int)

summary = open(directory + '/00-Zusammenfassung.txt', 'w')

for index, submission in enumerate(subreddit.submissions(sub_start, sub_end), start=1):
#        file = open(directory + '/' + str(index) + '-' + str(submission.id)+'.txt', 'w')

        try:
           sauthor = str(submission.author.name)
        except:
           sauthor = '[Deleted]'



        print('{} {}-{} Ratio: {}: r/{}: {}'.format(
                              datetime.datetime.fromtimestamp(submission.created_utc, tz=pytz.utc),
                              index,
                              submission.id,
                              submission.upvote_ratio,
                              submission.subreddit,
                              submission.title
                              ))
        summary.write('{} {}-{} Ratio: {}: r/{}: {}'.format(
                              datetime.datetime.fromtimestamp(submission.created_utc, tz=pytz.utc),
                              index,
                              submission.id,
                              submission.upvote_ratio,
                              submission.subreddit,
                              submission.title+'\n'
                              ))



        uniquesubid = str(crawlid)+'-'+str(index)+'-'+submission.name # Praw liefert bei /r/all unter Umständen doppelte Beiträge zurück

        query = """INSERT INTO tbl_submission (id, crawlid, index, title, ups, upvote_ratio, author, timestamp_utc, url, selftext, subreddit, is_reddit_media_domain, over_18, is_self, stickied) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (
        uniquesubid,
        crawlid,
        index,
        submission.title,
        submission.ups,
        submission.upvote_ratio,
        sauthor,
#        submission.author.name,
        submission.created_utc,
        submission.url,
        submission.selftext,
        submission.subreddit.display_name,
        submission.is_reddit_media_domain,
        submission.over_18,
        submission.is_self,
        submission.stickied,
        )

        cursor.execute(query, values)
        conn.commit()

#        file.write('SubID: {}, No: {}, Titel: {}, ups: {}, ratio: {}, author: {}, Zeitpunkt {}, URL {}, Message: {},'.format(
#                                                                            submission.id,
#                                                                            index,
#                                                                            submission.title,
#                                                                            submission.ups,
#                                                                            submission.upvote_ratio,
#                                                                            submission.author,
#                                                                            datetime.datetime.fromtimestamp(submission.created_utc),
#                                                                            submission.url,
#                                                                            '\n=='+submission.selftext+'\n\n'
#                                                                            ))
        dictSubreddit[submission.subreddit] += 1
        dictAuthoren[submission.author] += 1
        dictAuthorenUps[submission.author] += submission.ups
        submission.comments.replace_more(limit=None)
        comments=submission.comments.list()
        for cindex, comment in enumerate(submission.comments.list(), start=1):
#            file.write('{}CNo: {}, CZeitpunkt: {}, Score: {}, CAuthor: {}, CMessage: {}: '.format(
#                                            '\n-->',
#                                            cindex,
#                                            datetime.datetime.fromtimestamp(comment.created_utc),
#                                            comment.score,
#                                            comment.author,
#                                            comment.body
#                                            ))
#
            try:
                cauthor = str(comment.author.name)
            except:
                cauthor = '[Deleted]'


            query = """INSERT INTO tbl_comment (cindex, submissionid, timestamp, score, author, body, crawlid, name, parent_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            values = (
            uniquesubid+'-'+comment.name,
            uniquesubid,
            comment.created_utc,
            comment.score,
            cauthor,
            comment.body,
            crawlid,
            comment.name,
            comment.parent_id,
            )

            cursor.execute(query, values)

            dictCAuthoren[submission.author] += 1
            dictCAuthorenScore[submission.author] += comment.score
#        file.close()

print ('--> Subreddit nach Häufigkeit:\n')
s = [(k, dictSubreddit[k]) for k in sorted(dictSubreddit, key=dictSubreddit.get, reverse=True)]
file = open(directory + '/' + str('00-Subreddit.txt'), 'w')
file.write('Subreddit nach Häufigkeit:\n\n')
for k, v in s:
    print (k,v)
    file.write('{} {} {}'.format(
                    k,
                    v,
                    '\n'
                    ))
file.close()


print ('--> Submissions nach Author:\n')
s = [(k, dictAuthoren[k]) for k in sorted(dictAuthoren, key=dictAuthoren.get, reverse=True)]
file = open(directory + '/' + str('00-Authoren.txt'), 'w')
file.write('Submissions nach Author:\n\n')
for k, v in s:
    print (k,v)
    file.write('{} {} {}'.format(
                    k,
                    v,
                    '\n'
                    ))


s = [(k, dictAuthorenUps[k]) for k in sorted(dictAuthorenUps, key=dictAuthorenUps.get, reverse=True)]
print ('\n\n\n--> Upvote-Werte:\n')
file.write('\n\nUpvote-Werte:\n\n')
for k, v in s:
    print (k,v)
    file.write('{} {} {}'.format(
                    k,
                    v,
                    '\n'
                    ))
file.close()


#############################
print ('\n\n\n--> Kommentare nach Author:\n')
file = open(directory + '/' + str('00-CAuthoren.txt'), 'w')
file.write('Kommentare nach Author:\n\n')
s = [(k, dictCAuthoren[k]) for k in sorted(dictCAuthoren, key=dictCAuthoren.get, reverse=True)]
for k, v in s:
    print (k,v)
    file.write('{} {} {}'.format(
                    k,
                    v,
                    '\n'
                    ))


s = [(k, dictCAuthorenScore[k]) for k in sorted(dictCAuthorenScore, key=dictCAuthorenScore.get, reverse=True)]
print ('\n\n\n--> Kommentar-Score-Werte:\n')
file.write('\n\nKommentar-Score-Werte:\n\n')
for k, v in s:
    print (k,v)
    file.write('{} {} {}'.format(
                    k,
                    v,
                    '\n'
                    ))
file.close()
#############################
summary.close()

cursor.close()
conn.close()
