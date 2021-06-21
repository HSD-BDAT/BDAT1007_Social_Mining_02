# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:18:32 2021

@author: 007
"""

#%%
from flask import Flask, request, render_template, url_for, redirect
import praw
import pandas as pd
import tweepy
import html2text
from pymongo import MongoClient

#%%
consumer_key = "ifw5Uzvta4k8YvyKJJiBBMxNq" 
consumer_secret = "0XzYrX1ClvlmFIDKkRMs2mfo2v46G8NmA38wRHOck5TNGPAKMw"
access_key = "1392220044373872641-Z5fv2UZiSF4yFlPdf7Wauup4Mi9n0V"
access_secret = "UqCKaGoVrg02Gs7I0h3saXZBH38x64DzcD6y4kXhDKbtJ"

#%%
# Twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)   
auth.set_access_token(access_key, access_secret) 
  
# Creating an API object 
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
#%%
reddit1 = praw.Reddit(client_id='LDBzgY0k74p-pw', 
                 client_secret='vly4cy2W0Qt0NFD6Bjpej9CPWq3kIQ', 
                 user_agent='bdat_1007_HSD',
                 username="bdatHSD_007", 
                 password="`Y<XS/9HDV][@{f^")  

#%%
app = Flask(__name__)

#%%
client = MongoClient("mongodb+srv://bdatAdmin:HCjquZSkonIiojmi@cluster0.zbfiq.mongodb.net/socialMining_02?retryWrites=true&w=majority")
db = client.socialMining_02

#%%
@app.route('/')
def home():
    return redirect(url_for('reddit'))

#%%
@app.route('/twitter', methods = ['GET'])
def twitter():
    mention_tweets = tweepy.Cursor(api.search, q="@ManUtd", tweet_mode='extended').items(5)
    
    for tweet in mention_tweets:
        posts = dict()
        posts['_id'] = tweet.id
        posts['created'] = tweet.created_at        
        posts['post'] = tweet.full_text
        posts['author'] = tweet.user.name
        posts['twitterName'] = tweet.user.screen_name
        posts['tweetsCount'] = tweet.user.statuses_count
        posts['retweets'] = tweet.retweet_count
        posts['url'] = 'https://twitter.com/twitter/statuses/' + str(tweet.id)

        try: posts['likes'] = tweet.retweeted_status.favorite_count
        except: posts['likes'] = tweet.favorite_count
            
        try: db.tweets.insert_one(posts)
        except: continue
        
    tweets = api.user_timeline(screen_name='Harmila41333232', count=200, include_rts = False, tweet_mode = 'extended')

    for tweet in tweets[:10]:
        posts = dict()
        posts['_id'] = tweet.id
        posts['created'] = tweet.created_at        
        posts['post'] = tweet.full_text
        posts['author'] = tweet.user.name
        posts['twitterName'] = tweet.user.screen_name
        posts['tweetsCount'] = tweet.user.statuses_count
        posts['retweets'] = tweet.retweet_count
        posts['url'] = 'https://twitter.com/twitter/statuses/' + str(tweet.id)

        try: posts['likes'] = tweet.retweeted_status.favorite_count
        except: posts['likes'] = tweet.favorite_count
            
        try: db.tweets.insert_one(posts)
        except: continue
    
    obs = db.tweets.find()
    posts = [ob for ob in obs]
    
    return render_template('twitter.html', **locals())

#%%
@app.route('/reddit', methods = ['GET'])
def reddit():
    reddit1 = praw.Reddit(client_id='LDBzgY0k74p-pw', 
                 client_secret='vly4cy2W0Qt0NFD6Bjpej9CPWq3kIQ', 
                 user_agent='bdat_1007_HSD',
                 username="bdatHSD_007", 
                 password="`Y<XS/9HDV][@{f^")  
    
    new_bets = reddit1.subreddit("football").new(limit=30)

    for post in new_bets:
        posts = dict()
        posts['_id'] = post.id
        posts['author'] = post.author.name
        posts['title'] = post.title
        posts['score'] = post.score
        posts['num_comments'] = post.num_comments
        posts['selftext'] = post.selftext
        posts['created'] = pd.to_datetime(post.created, unit='s')
        posts['url'] = post.url
        
        try:
            db.reddit.insert_one(posts)
        except:
            continue
        
    user = reddit1.redditor("bdatHSD_007")
    submissions = user.submissions.new(limit=None) 
    for post in submissions:
        posts = dict()
        posts['_id'] = post.id
        posts['author'] = post.author.name
        posts['title'] = post.title
        posts['score'] = post.score
        posts['num_comments'] = post.num_comments
        posts['selftext'] = post.selftext
        posts['created'] = pd.to_datetime(post.created, unit='s')
        posts['url'] = post.url
        
        try:
            db.reddit.insert_one(posts)
        except:
            continue
        
    obs = db.reddit.find()
    posts = [ob for ob in obs]
    
    return render_template('reddit.html', **locals())

#%%
@app.route('/postTwitter', methods = ['POST'])
def postTwitter():
    api.update_status(status = html2text.html2text(''.join(request.json['tweet'])))
    return ""
    
#%%
@app.route('/postReddit', methods = ['POST'])
def postReddit():
    sub = reddit1.subreddit('u_bdatHSD_007')
    title = 'Good Morning'
 
    selftext = html2text.html2text(''.join(request.json['reddit']))
    sub.submit(title,selftext=selftext)
    
    return ""

#%%
if __name__ == "__main__":
    app.run()