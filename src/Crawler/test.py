'''
Created on 26/02/2014

@author: chengyu
'''

from webPart import Parser
import re
from stemming.porter2 import stem
import tweepy
from tweepy import OAuthHandler

# from stemming.porter2 import stem
# a = stem("factionally")
# 
# print a

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="OQrOsQkuiXFH5dUrCKHfvg"
consumer_secret="7pF6PH6PFGeBLlAHsxMbTGinw2bfYIw4aF6vwWsLok"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="781737260-uJejBgaVA8NDGxj6oipjlp6K7fl89fvQdJQS6357"
access_token_secret="TZUCXTGg2SRBplHPaTs0aht2gGIsIwaRX1v6hBRSfJrzj"

'''test re functions:'''

test_str = "\u0643\u0645 \u0644\u064a \u0648\u0627\u0646\u0627 \u0627\u0637\u0644\u0628 \u062d\u0633\u064a\u0646 \u0627\u0644\u062c\u0633\u0645\u064a \u064a\u0633\u0648\u064a \u0644\u064a \u0631\u062a\u0648\u064a\u062a \u0639\u0627\u062f \u0634\u0643\u0644\u0647 \u062d\u0646\u064a\u0651\u0646"


ma = Parser.MatrixParserForLearning()
  
k = ma.preExtractWords(test_str)
  
print k

print test_str.find(r'\\u[\w]{4}')


test_str2 = " Hahaha, pompommu lhoo mesti dtg pas aku gini :D RT@sagitaenggar: Hahaha lak yo malu seh aku X.X "

a = ma.preProcessString(test_str2)
print a

print "RT @zaynmalik: Meet my friend ... Jack Daniels :) he's cool, ha".startswith("RT")

print stem("I'm")

import pickle

a = {
  'a': 1,
  'b': 2
}

with open('file.txt', 'wb') as handle:
    pickle.dump(a, handle)

with open('file.txt', 'rb') as handle:
    b = pickle.loads(handle.read())

print a == b # True


# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#  
# 
# api = tweepy.API(auth)
# i = 0
# geocode_melb = "37.814251,144.963165,300km";
# 
# for tweet in tweepy.Cursor(api.search,
#                            q="iphone",
#                            rpp=100,
#                            pages = 10,
#                            geocode = geocode_melb,
#                            result_type="recent",
#                            include_entities=True,
#                            lang="en").items():
#     print tweet.created_at, repr(tweet.text)
#     i = i+1
#     print i
import time
from datetime import date

a = date(2007, 12, 5)
b = date.today()
c = b - a

print a,b, c.days



