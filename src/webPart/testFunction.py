'''
Created on 17/03/2014

@author: chengyu
'''

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from django.db import models
from webPart import models
from webPart import Parser
import json
from webPart.models import TweetsSentiment
from webPart.models import Region
import time
from datetime import date
from LearningModel import NaiveBayesClassifierBernoulli

def search( query):
    query = query.strip()
    i = 0
    print query
    tweets = TweetsSentiment.objects.filter(text__contains=query)
    for tweet in tweets:
        i += 1
        
        print tweet.text
        print tweet.sentimentLabel,
        
        if  tweet.region != None:
            print tweet.region.regionName
        
        print i
        
    positiveTweets = tweets.filter(sentimentLabel = 1)
    
    for tweet in positiveTweets:
        i += 1
        print tweet.text
        print tweet.sentimentLabel,
        
        if  tweet.region != None:
            print tweet.region.regionName
        
        print i
    print len(positiveTweets)    
        

search("")