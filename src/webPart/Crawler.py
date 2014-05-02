'''
Created on 24/02/2014

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

# OQrOsQkuiXFH5dUrCKHfvg
# 7pF6PH6PFGeBLlAHsxMbTGinw2bfYIw4aF6vwWsLok
# 781737260-uJejBgaVA8NDGxj6oipjlp6K7fl89fvQdJQS6357
# TZUCXTGg2SRBplHPaTs0aht2gGIsIwaRX1v6hBRSfJrzj

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="OQrOsQkuiXFH5dUrCKHfvg"
consumer_secret="7pF6PH6PFGeBLlAHsxMbTGinw2bfYIw4aF6vwWsLok"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="781737260-uJejBgaVA8NDGxj6oipjlp6K7fl89fvQdJQS6357"
access_token_secret="TZUCXTGg2SRBplHPaTs0aht2gGIsIwaRX1v6hBRSfJrzj"


positiveEmoticons = ":),:-),:),:D,=)"
negativeEmoticons = ":(,:-(,: ("

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
This is a basic listener that just prints received tweets to stdout.

"""
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


class FileOutListener(StreamListener):

    def __init__(self, fileName):
        self.outPutFile = open(fileName,"w")
    
#     def on_data(self, data):
#         self.outPutFile.write(data+'\n')

    def on_data(self, status):
        self.outPutFile.write(status+'\n')
        
    
    def recordStream(self, features):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        stream.filter(track=features)


class DatabaseBaseSentimentListener(StreamListener):
    def __init__(self,  matrixFileName, dictName):
        
        self.classifier = NaiveBayesClassifierBernoulli(matrixFileName, dictName)
        
        
        self.regions = Region.objects.all()
        for region in  self.regions:
            print region
        
    def checkInside(self, place, latitude, longtitude):
        if place.latitudeBottom < latitude and place.latitudeTop > latitude and place.longtitudeBottom < longtitude and place.longtitudeTop > longtitude:
            return True
        return False     
        
    def on_data(self, data):
        
        decodedJson = json.loads(data)
        
        try:
#         if decodedJson.has_key("lang")== True and decodedJson["lang"] == 'en':
            if decodedJson.has_key("lang")== True and decodedJson["lang"] == 'en':
                tweetSentiment =  TweetsSentiment()
                tweetSentiment.JsonString = repr(data)
                tweetSentiment.sentimentLabel = self.classifier.classifyOneSentence( decodedJson["text"])
                print decodedJson
                print tweetSentiment.sentimentLabel
                tweetSentiment.text = decodedJson["text"].lower()
                tweetSentiment.tweetID = decodedJson["id"]
                tweetSentiment.tweetUserID = decodedJson["user"]["id"] 
                tweetSentiment.lang = decodedJson["lang"]
                
                a = date(2014, 3, 15)
                b = date.today()
                c = b - a
                tweetSentiment.date = c.days
                
                if decodedJson.has_key("geo") == True and decodedJson["geo"] != None and decodedJson["geo"]["type"] == "Point":
                    tweetSentiment.latitude =  decodedJson["geo"]["coordinates"][0]
                    tweetSentiment.longtitude = decodedJson["geo"]["coordinates"][1]
                    for region in self.regions:
                        if self.checkInside(region, tweetSentiment.latitude, tweetSentiment.longtitude) == True:
                            tweetSentiment.region = region  
    #                
                
            
                tweetSentiment.save()
        except Exception as e:
            print e
    
    def startListen(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
 
        stream = Stream(auth, self)
#     stream.filter(track=[positiveEmoticons])
        stream.filter(locations = [113.90625,-43.665217,157.148438,-13.35399])

#         stream.filter(track=self.trackFeatures,languages = ['en'],locations = [-122.75,36.8,-121.75,37.8])
#         stream.filter(track=self.trackFeatures,languages = ['en'],locations = [-122.75,36.8,-121.75,37.8] )


if __name__ == '__main__':
#     l = FileOutListener('/Users/chengyu/Documents/python/data/negativeTweetsForTrainingNew')
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#    
#     stream = Stream(auth, l)
#     stream.filter(track=[negativeEmoticons],languages=["en"])
# # [43.665217, 113.90625, 13.35399, 157.148438]
#       
# #     stream.filter(track=["Iphone"], locations=[-122.75,36.8,-121.75,37.8])
#     stream.filter(track=["Iphone"], locations=[113.90625,-43.665217,157.148438,-13.35399])
    l = DatabaseBaseSentimentListener("/Users/chengyu/Documents/python/data/matrixForLearning","/Users/chengyu/Documents/python/data/dictionary")
    l.startListen()

    

