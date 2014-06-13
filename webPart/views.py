# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from webPart.models import TweetsSentiment
from webPart.models import Region
import json
import decimal
from LearningModel import NaiveBayesClassifierBernoulli
from __init__ import NBB
from datetime import date, timedelta
import os


fileDirectory = os.path.dirname(os.path.abspath(__file__))
fileDirectory = os.path.dirname(fileDirectory)
# matrixFilePath = os.path.join(fileDirectory, "data/matrixForLearning")
# dictFilePath = os.path.join(fileDirectory, "data/dictionary")

def index(request):
#     return HttpResponse("This is index")
    context = RequestContext(request) 
    context_dict = {}
    dict_dump = {}
    dict_dump["ratio"] = [{"positiveRatio":0, "negRatio": 0}]
    
    if request.method == 'POST':
        query = request.POST['searchbox']
          
        context_dict['searchQuery'] = query
        query = query.lower()
        request.session["query"] = query
#         query = " "+query+" "
        tweetsRelated = TweetsSentiment.objects.filter(text__contains=query)

        context_dict["number"] = len(tweetsRelated)
        positiveTweets = tweetsRelated.filter(sentimentLabel = 1).order_by("sentimentScore")
        negativeTweets = tweetsRelated.filter(sentimentLabel = -1).order_by("-sentimentScore")
         
        ratio = TweetsRatio(positiveTweets, negativeTweets)
         
        dict_dump["ratio"] = ratio
         
        positiveCountRegion = TweetsRegion(positiveTweets)
        negativeCountRegion = TweetsRegion(negativeTweets)
        topPositiveTweets = TopTweets(positiveTweets)
        topNegativeTweets = TopTweets(negativeTweets)
        dict_dump["positiveCountRegion"] = positiveCountRegion
        dict_dump["negativeCountRegion"] = negativeCountRegion
        dict_dump["topPositiveTweets"] = topPositiveTweets
        dict_dump["topNegativeTweets"] = topNegativeTweets


    logPath = os.path.join(fileDirectory,"testlog")
    filelog = open(logPath, "wt+")
    filelog.write(repr(dict_dump))
    filelog.close()

    json_dump = json.dumps(dict_dump)

    jsonPath = os.path.join(fileDirectory,"data/test.json")
    file = open(jsonPath,"wt")
    file.write(json_dump)
    file.close()
    
    return render_to_response('app/index.html', context_dict, context)
    
def regionDetail(request):
    context = RequestContext(request) 
    
    
    cash = []
    dict_dump = {}
    
    query = request.session["query"]
    tweetsRelated = TweetsSentiment.objects.filter(text__contains=query)
    negativeTweets = tweetsRelated.filter(sentimentLabel = -1).order_by("-sentimentScore")
    positiveTweets = tweetsRelated.filter(sentimentLabel = 1).order_by("sentimentScore")
    context_dict = {}
    
    dict_dump["ratio"] = TweetsRatio(positiveTweets, negativeTweets)

    
    
    if  request.GET["label"] == "pos":
            
#     negativeTweets = tweetsRelated.filter(sentimentLabel = -1)
  
        context_dict["label"] = "positive"
        cash = TweetsRegion(positiveTweets)
        topTweets = TopTweets(positiveTweets)
        # topTweets = positiveTweets[0:10]
    else  :
        
        context_dict["label"] = "negative"
        cash = TweetsRegion(negativeTweets)
        topTweets = TopTweets(negativeTweets)
    dict_dump["cash"] = cash
    dict_dump["top"] = topTweets
    
    
    json_dump = json.dumps(dict_dump)

    jsonPath = os.path.join(fileDirectory,"data/test.json")
    file = open(jsonPath,"wt")
    file.write(json_dump)
    file.close()
     
    
    return render_to_response('app/regionDetail.html', context_dict, context)
        
def TweetsRatio(positiveTweets, negativeTweets):
    ratioPos = decimal.Decimal(len(positiveTweets))/(len(positiveTweets)+len(negativeTweets))*100
    ratioNeg = decimal.Decimal(len(negativeTweets))/(len(positiveTweets)+len(negativeTweets))*100
    return [{"positiveRatio":round(ratioPos,2),"negRatio":round(ratioNeg,2)}]

def TweetsRegion(tweets):
    regions = Region.objects.all()
    tweetsOfRegionArray = []
    for region in regions:
        tweetsForThisRegion = tweets.filter(region_id = region.id )
        dict = {}
        dict["id"] = region.id
        dict["name"] = region.regionName
        dict["count"] = len(tweetsForThisRegion)
        tweetsOfRegionArray.append(dict)
    return tweetsOfRegionArray

def TopTweets(tweets,num = 10):
    topTweets = tweets[0:num]
    returnContent = []
    for tweet in topTweets: returnContent.append(tweet.text)

    logFilePath = os.path.join(fileDirectory,"data/logScore.txt")
    logScoreFile = open(logFilePath,"at+")
    for tweet in topTweets:
        logScoreFile.write(repr(tweet.text) + " : " + repr(tweet.sentimentScore) + "\n" )
    logScoreFile.close()

    return returnContent
#     tweetsNum = len(tweets)
#     i = 0
#
#     recordDict = {}
#     while i < tweetsNum:
# #         if positiveTweets[i].text.find(" not ") == False:
#         pro = NBB.classifyOneSentenceWithProbability(tweets[i].text)
#         recordDict[i] = pro
#         i += 1
#
#     rank = sorted(recordDict, key=recordDict.__getitem__, reverse=isPos)
#
#     if len(rank) > num:
#         rank = rank[:num]
#     topTweets = []
#
#     for i in rank:
#         string = " \"" + tweets[i].text
#         string += "\""
#         if tweets[i].region != None: string += " from " + tweets[i].region.regionName
#         string += " on "
#         dateStart = date(2014, 3, 15)
#         dateTweet = dateStart + timedelta(days=tweets[i].date)
#         string += str(dateTweet)
#         topTweets.append(string)
#
#     return topTweets

    
    