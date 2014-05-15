'''
Created on 01/03/2014

@author: chengyu
'''


from sklearn.datasets import load_svmlight_file
from sklearn.naive_bayes import BernoulliNB
# from  webPart import Parser
import Parser
import pickle
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os



fileDirectory = os.path.dirname(os.path.abspath(__file__))
fileDirectory = os.path.dirname(fileDirectory)
matrixFilePath = os.path.join(fileDirectory, "data/matrixForLearning")
dictFilePath = os.path.join(fileDirectory, "data/dictionary")




class NaiveBayesClassifierBernoulli:
    def __init__(self, matrixFileName = matrixFilePath, dicFileName = dictFilePath):
        self.X,self.Y = load_svmlight_file(matrixFileName)
        self.dictionary = pickle.load(open(dicFileName, "rb"))
        self.bernoulliNB = BernoulliNB()
        self.bernoulliNB.fit(self.X, self.Y)
        self.matrixParser = Parser.MatrixParserForLearning()
        
    def classifyOneSentence(self, string):
        row = self.matrixParser.getRowForClassify(string, self.dictionary)
        if row != None:
#             return self.bernoulliNB.predict(row)
            return self.bernoulliNB.predict(row)
        else : return None
    
    def classifyOneSentenceWithProbability(self,string):
        row = self.matrixParser.getRowForClassify(string, self.dictionary)
        if row != None:
#             return self.bernoulliNB.predict(row)
            a = self.bernoulliNB.predict_proba(row)
            return a[0][1] - a[0][0]
        else : return None
    
#     def classifySentences(self, strings):
#         rows = []
#         for string in strings:
#             row = self.matrixParser.getRowForClassify(string, self.dictionary)
#             if row != None: rows.append(row)
#             
    
class NaiveBayesClassifierBernoulliListener(StreamListener):
    def __init__(self, matrixFileName = matrixFilePath, dictFileName = dictFilePath):
        self.naiveBayesClassifierBernoulli = NaiveBayesClassifierBernoulli(matrixFileName, dictFileName)
        self.matrixParser = Parser.MatrixParserForLearning()
        
    def on_data(self, data):
        tweetJson = json.loads(data)
        string = repr(tweetJson["text"])

        a = self.naiveBayesClassifierBernoulli.classifyOneSentence(string)
        if a != None:
            print a

if __name__ == "__main__":
    NBB = NaiveBayesClassifierBernoulli()
    print NBB.classifyOneSentenceWithProbability("I loves You")


# # Go to http://dev.twitter.com and crIdeaVim plugineate an app.
# # The consumer key and secret will be generated for you after
# consumer_key="OQrOsQkuiXFH5dUrCKHfvg"
# consumer_secret="7pF6PH6PFGeBLlAHsxMbTGinw2bfYIw4aF6vwWsLok"
#  
# # After the step above, you will be redirected to your app's page.
# # Create an access token under the the "Your access token" section
# access_token="781737260-uJejBgaVA8NDGxj6oipjlp6K7fl89fvQdJQS6357"
# access_token_secret="TZUCXTGg2SRBplHPaTs0aht2gGIsIwaRX1v6hBRSfJrzj"
#      
#      
# if __name__ == '__main__':
#     l = NaiveBayesClassifierBernoulliListener()
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#   
#     stream = Stream(auth, l)
# #     stream.filter(track=[positiveEmoticons])
#     trackList = []
#     trackList.append("australia")
#     stream.filter(track=trackList, languages = ["en"])
#     
    