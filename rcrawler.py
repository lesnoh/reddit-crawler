#!/usr/bin/env python3
# Michael Honsel 12/2017
import praw
import json
import time;
import datetime;
import os, errno;
from collections import defaultdict

reddit = praw.Reddit(client_id='cx0Rhc8hfD-2cA',
                     client_secret='gP-QBQDaC4h8IL8QqI2iQ9ZYzqs',
                     username='',
                     password='',
                     user_agent='py:rcrawler:v0.3'
)

reddit.read_only = "true"
#forum = "all"
#forum = "dark"
forum = "talesfromtechsupport"
#forum = "de"

sub_start = int(time.mktime(time.strptime('2017-09-15 18:00:00', '%Y-%m-%d %H:%M:%S')))
sub_end   = int(time.mktime(time.strptime('2017-12-15 23:59:59', '%Y-%m-%d %H:%M:%S')))
#sub_start = int(time.mktime(time.strptime('2017-12-08 00:00:00', '%Y-%m-%d %H:%M:%S')))
#sub_end   = int(time.mktime(time.strptime('2017-12-08 23:59:59', '%Y-%m-%d %H:%M:%S')))
#sub_start = int(time.mktime(time.strptime('2017-11-30 00:00:00', '%Y-%m-%d %H:%M:%S')))
#sub_end   = int(time.mktime(time.strptime('2017-11-30 23:59:59', '%Y-%m-%d %H:%M:%S')))

subreddit = reddit.subreddit(forum)

#OutputDirectory
directory = 'output/' + str(forum)+ '-' + str(sub_start) + '-' + str(sub_end)

if not os.path.exists(directory):
            os.makedirs(directory)

# Assoziativer Arrays zum Zählen der aktiven Teilnehmer und deren Up und
# Downvotes
dictSubreddit = defaultdict(int)
dictAuthoren = defaultdict(int)
dictAuthorenUps = defaultdict(int)
dictCAuthoren = defaultdict(int)
dictCAuthorenScore = defaultdict(int)

summary = open(directory + '/00-Zusammenfassung.txt', 'w')

for index, submission in enumerate(subreddit.submissions(sub_start, sub_end), start=1):
        file = open(directory + '/' + str(index) + '-' + str(submission.id)+'.txt', 'w')
        print('{} {}-{} Ratio: {}: r/{}: {}'.format(
                              datetime.datetime.fromtimestamp(submission.created_utc),
                              index,
                              submission.id,
                              submission.upvote_ratio,
                              submission.subreddit,
                              submission.title
                              ))
        summary.write('{} {}-{} Ratio: {}: r/{}: {}'.format(
                              datetime.datetime.fromtimestamp(submission.created_utc),
                              index,
                              submission.id,
                              submission.upvote_ratio,
                              submission.subreddit,
                              submission.title+'\n'
                              ))
        file.write('SubID: {}, No: {}, Titel: {}, ups: {}, ratio: {}, author: {}, Zeitpunkt {}, URL {}, Message: {},'.format(
                                                                            submission.id,
                                                                            index,
                                                                            submission.title,
                                                                            submission.ups,
                                                                            submission.upvote_ratio,
                                                                            submission.author,
                                                                            datetime.datetime.fromtimestamp(submission.created_utc),
                                                                            submission.url,
                                                                            '\n=='+submission.selftext+'\n\n'
                                                                            ))
        dictSubreddit[submission.subreddit] += 1
        dictAuthoren[submission.author] += 1
        dictAuthorenUps[submission.author] += submission.ups
        submission.comments.replace_more(limit=0)
        comments=submission.comments.list()
        for cindex, comment in enumerate(submission.comments.list(), start=1):
            file.write('{}CNo: {}, CZeitpunkt: {}, Score: {}, CAuthor: {}, CMessage: {}: '.format(
                                            '\n-->',
                                            cindex,
                                            datetime.datetime.fromtimestamp(comment.created_utc),
                                            comment.score,
                                            comment.author,
                                            comment.body
                                            ))

            dictCAuthoren[submission.author] += 1
            dictCAuthorenScore[submission.author] += comment.score
file.close()
#{
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
#}


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
