# http://ashishkhan.com/blog/extract-facebook-twitter-data-with-python

import urllib3
import json
import datetime
import csv
import time
import tweepy
from oauthlib.oauth1.rfc5849.endpoints import access_token
from tweepy import OAuthHandler

app_id = "abhinavvarshney946"
app_secret = "Abhinav@20"  # DO NOT SHARE WITH ANYONE!

access_token_fb = app_id + "|" + app_secret  # NEVER EXPIRES

consumer_key = '7451986172'
consumer_secret = 'Abhihts@20'
access_token_tw = 'your_twitter_access_token'
access_secret = 'your_twitter_access_secret'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_tw, access_secret)

api = tweepy.API(auth)

fb_page = "manchesterunited"
twitter_page = "@manutd"

base = "https://graph.facebook.com/v2.11"
node = "/" + fb_page
parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (2, access_token)
url = base + node + parameters


def request_until_succeed(url):
    req = urllib3.Request(url)
    success = False
    while success is False:
        try:
            response = urllib3.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return response.read()


test_status = json.loads(request_until_succeed(url))["data"][0]
print(json.dumps(test_status, indent=4, sort_keys=True))


def processFacebookPageFeedStatus(status):
    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else status['message'].encode('utf-8')
    link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else status['link']

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5)  # EST
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs

    # Nested items require chaining dictionary keys.

    num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']

    # return a tuple of all processed data
    return (status_id, status_message, link_name, status_type, status_link,
            status_published, num_likes, num_comments, num_shares)


processed_test_status = processFacebookPageFeedStatus(test_status)
print(processed_test_status)

for x in tweepy.Cursor(api.user_timeline, screen_name=twitter_page).items(1):
    tweet = x.text

    print(tweet)