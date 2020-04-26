import pandas as pd
import requests
import json
import csv
import time
import datetime

begin_time = datetime.datetime.now()

def getPushshiftData(after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?size=1000&after=' + \
        str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    print (url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def writeSubData(subm):
    #print(subm)
    subData = []  # list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"
    author = subm['author']
    stickied = subm['stickied']
    pinned = subm['pinned']
    over_18 = subm['over_18']
    try:
        selftext = subm['selftext']
    except KeyError:
        selftext = 'Nan'
    
    spoiler = subm['spoiler']
    sub_id = subm['id']
    score = subm['score']
    num_crossposts = subm['num_crossposts']
    is_video = subm['is_video']
    created = datetime.datetime.fromtimestamp(subm['created_utc'])  # 1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']

    #new_line= (sub_id,title,url,author,score,created,numComms,permalink,flair)

    with open('data_final.csv', 'a+', newline='') as csvfile:
        fieldnames = ['sub_id', 'title', 'url', 'author', 'score', 'created', 'numComms', 'permalink', 'flair',
                      'stickied', 'pinned', 'over_18', 'selftext', 'spoiler', 'num_crossposts', 'is_video']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'sub_id': sub_id, 'title': title, 'url': url, 'author': author, 'score': score, 'created': created, 'numComms': numComms, 'permalink': permalink, 'flair': flair, 'stickied': stickied,
                         'pinned': pinned,'over_18': over_18, 'selftext': selftext, 'spoiler': spoiler, 'num_crossposts': num_crossposts, 'is_video': is_video})

    # subData.append(new_line)

    #csvfile=open('newdoc.csv','a+', newline='')
    # obj=csv.writer(csvfile)
    # obj.writerow(new_line)
    # csvfile.close()
    #subStats[sub_id] = subData

sub = 'india'
before = "1586524763"  # April 10, 2020 1:19:23 PM
after = "1559740124"  # Wednesday, January 10, 2018 7:09:04 PM
subCount = 0
subStats = {}

data = getPushshiftData(after, before, sub)

while len(data) > 0:
    for submission in data:
        #print (submission)
        writeSubData(submission)
        subCount += 1

    # print(len(data))
    # print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(after, before, sub)

print('finished scraping, total time taken:')

print(datetime.datetime.now() - begin_time)
