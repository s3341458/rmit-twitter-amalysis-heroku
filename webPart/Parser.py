'''
Created on 25/02/2014

@author: chengyu
'''



import demjson
import json
from stemming.porter2 import stem
import re

import pickle

DEBUG = True



class TweetJsonParser(object):
    
    def parseJsonString(self,jsonString):
        return demjson.decode(jsonString)
    
    def parseJsonStrings(self, jsonStrings, limit=1000000, lang= "en"):
        returnList = []
        count = 0
        for jsonObject in jsonStrings:
            decodedJsonObject = demjson.decode(jsonObject)
            if decodedJsonObject.has_key('lang') and decodedJsonObject['lang'] == lang and decodedJsonObject['text'].startswith("RT") == False:
                returnList.append(decodedJsonObject)
                count += 1
            if  count > limit :break
            
        return returnList
    
    def parseJsonStringsInFile(self, fileName, limit = 1000000, lang= "en"):
        file = open(fileName,"r")
        jsonStrings = []
        i = 0
 
        while i < limit:
            jsonString = file.readline()
            
            if jsonString=="":
                break
            elif jsonString != "\n":
                jsonStrings.append(jsonString)
            
            i += 1
            
        jsonObjects = self.parseJsonStrings(jsonStrings, limit, lang)
        
        return jsonObjects
    
    def onlineParseFileToFile(self, inputJsonFileName, outputFileName, keys = ['created_at', 'id', 'text', 'lang']):
        inputFile = open(inputJsonFileName, "r") 
        outputFile = open(outputFileName, "w")
        
        while True:
            jsonString = inputFile.readline()
            if DEBUG :print repr(jsonString)
            if DEBUG :print jsonString != '\n'
            
            try: 
                if jsonString=="":
                    break
                elif jsonString != '\n':
                    oldJsonObject = self.parseJsonString(jsonString)
                    newJsonDict = {}
                    for key in keys:
                        if oldJsonObject.__contains__(key):
                            newJsonDict[key] = oldJsonObject[key]
                    outputFile.write( json.dumps(newJsonDict)+"\n" )
            except Exception as e:
                print e
                print "throw : " + jsonString 
            
            


class MatrixParserForLearning:
    
    def __init__(self, positiveEmoticons=":),:-),:),:D,=)",negativeEmoticons = ":(, :-(, : (" ):
        self.positiveEmoticonList = positiveEmoticons.split(',')
        self.negativeEmoticonList = negativeEmoticons.split(',')
        self.emoticonList = []
        self.emoticonList.append(self.positiveEmoticonList)
        self.emoticonList.append(self.negativeEmoticonList)
        
    
    
    def preProcessString(self, string):
   
        positive = False
        negative = False
        
        if DEBUG:
            
            print type(string)
        
        for positiveEmoticon in self.positiveEmoticonList:
            
            
            if string.find(positiveEmoticon) != -1:
                string.replace(positiveEmoticon,"")
                positive = True

        for negativeEmoticon in self.negativeEmoticonList:
            if string.find(negativeEmoticon) != -1:
                string.replace(negativeEmoticon,"")
                negative = True
                
        if positive == True and negative == True:
            return ""       


        regx = re.compile("RT[@ ]")
        patternList = regx.findall(string)
    
        if len(patternList) != 0:
            index = string.index(patternList[0])
            string = string[0:index]
        if DEBUG:print string    
        return string
    
    def postProcessString(self, string): 
        string = re.sub("[0-9\?]"," ",string)
        string = string.lower()        
        return string
    
    
   
    def preExtractWords(self, string, regularExpressions=['\\u[0-9a-f]{4}',]):
        wordList = []
        
        for regularExpression in regularExpressions:
            regx = re.compile(regularExpression)
            words = regx.findall(string)
            #print words
            
            if len(words) > 0:
                wordList.extend(words)
        
        if DEBUG:print wordList
        return wordList
    

    
    def getFeaturesOfString(self, string):
        words = []
        
        string = self.preProcessString(string)      
        uniqueFeatures = self.preExtractWords(string)
        string = self.postProcessString(string)
        words.extend(uniqueFeatures)   
        words.extend(string.split(" ")  ) 
        
        return words
                
             
    def getDictionaryOfStrings(self, strings, frequentLimit = 2, lengthOfWord = 3):
        dict = {}
        preDict = {}
        featureID = 0
        for string in strings:
            words = self.getFeaturesOfString(string)
                    
            for word in words:
                word = stem(word)
                if len(word) > lengthOfWord:
                    if preDict.has_key(word):
                        preDict[word] +=1
                    else :
                        preDict[word] = 1
                        
        for k in preDict:
            if preDict[k] > frequentLimit:
#                 if DEBUG : print featureID
                featureID += 1
                dict[k] = featureID
        
        if DEBUG:
            file = open("debugDic", "w")
            file.write(repr(dict))
                              
        return dict
    
    def getRowForMatrix(self, string, dictionary, label):
        featureDict = {}
        words = self.getFeaturesOfString(string)
#         if len(words) == 0: return None
        for word in words:
            word = stem(word)
            if dictionary.has_key(word):
                wordID = dictionary[word]
                if featureDict.has_key(wordID) == False:
                    featureDict[wordID] = 1
                    
        return (label,featureDict)
    
    def getRowForClassify(self,string,dictionary):
        returnTuple = self.getRowForMatrix(string, dictionary, 1)
        featureDict = returnTuple[1]
        if len(featureDict) == 0: return None
        if DEBUG: print featureDict
        array = [0]* len(dictionary)
        for k in featureDict:
            array[k-1] = 1
            
        return array
        
        
    
    
    
    def rowToString(self, row):
        template = "{0}:{1} "
        rowString = ""
        if row[0]  == 1:
            rowString += "+1 "
        else: 
            rowString += "-1 "
            
        features = row[1]
        
        for k,v in sorted(features.items()):
            rowString += template.format(k,v)
        
        
        return rowString
            
        
    def matrixToString(self, matrix):
        matrixString = ""
        for row in matrix:
            matrixString += self.rowToString(row) + "\n"
        
        return matrixString      
        
    
    def getMatrixFromStrings(self, positiveComments, negativeComments, frequentLimit = 3, lengthOfWord = 3):
        totalComments = []
        matrix = []
        totalComments.extend(positiveComments)
        totalComments.extend(negativeComments)
        
        dict = self.getDictionaryOfStrings(totalComments, frequentLimit, lengthOfWord)
        
        for positiveComment in positiveComments:
            row = self.getRowForMatrix(positiveComment, dict, 1)
            if len(row[1].items()) > 0:
                matrix.append(row)
            
        for negativeComment in negativeComments:
            row = self.getRowForMatrix(negativeComment, dict, -1)
            if len(row[1].items()) > 0:
                matrix.append(row)
                
        return (matrix,dict)
            
            
                    
    def getMatrixFromFile(self, positiveFileName, negativeFileName, tweetsLimit = 10000, lang = "en", ratio = 1):

        JsonParser = TweetJsonParser()
        
        positiveJsons = JsonParser.parseJsonStringsInFile(positiveFileName, tweetsLimit, lang)
        negativeJsons = JsonParser.parseJsonStringsInFile(negativeFileName, tweetsLimit*ratio, lang)
        positiveComments = []
        negativeComments = []
#         for positiveJson in positiveJsons:
  
        for positiveJson in positiveJsons:
#             if DEBUG : print positiveJson["text"]
            positiveComments.append( repr(positiveJson["text"]) )
#             positiveComments.append( "asdas asdas sss \u1234asds :)" )
#             if positiveJson[lang] != "en":
#                 raise Exception("something wrong with lang")
        for negativeJson in negativeJsons:
#             if DEBUG : print negativeJson["text"]
              negativeComments.append(repr( negativeJson["text"] )) 
#             negativeComments.append( "asdas assss sdsds ssds :( ") 
            
        matrix,dict = self.getMatrixFromStrings(positiveComments, negativeComments)   
        
        return matrix,dict
    
    def outputMatrixFromFile(self, matrix, fileName = "matrix"):
        matrixString = self.matrixToString(matrix)
#         print "matrix:"
#         print matrix
#         print "here1"
#         print matrixString
#         print "here2"

        if DEBUG:
            file = open("debugMatrix","w")
            file.write(repr(matrix) )
        
        outputFile = open(fileName,"w")
        outputFile.write(matrixString)
        outputFile.close() 
            
        
                           
            
            
            
#             
# if __name__ == '__main__':
#     tweetParser = TweetJsonParser()
#     tweetParser.onlineParseFileToFile("/Users/chengyu/Documents/python/data/positiveTweetsForTrainingNew", "/Users/chengyu/Documents/python/data/positiveSentimentTweetsInfoNew")
#       
#                       
              

positiveFileName = "/Users/chengyu/Documents/python/data/positiveSentimentTweetsInfoNew"
negativeFileName = "/Users/chengyu/Documents/python/data/negativeSentimentTweetsInfoNew"
 
if __name__ == '__main__':
  
    mpl = MatrixParserForLearning()
    matrix,dict = mpl.getMatrixFromFile(positiveFileName, negativeFileName, 150000 )
    mpl.outputMatrixFromFile(matrix, "/Users/chengyu/Documents/python/data/matrixForLearning")
    pickle.dump(dict,open("/Users/chengyu/Documents/python/data/dictionary", "wb"))
    b = pickle.load(open("/Users/chengyu/Documents/python/data/dictionary", "rb"))
    if b == dict:
        print True
    

    
     
                    
        
    
# if __name__ == '__main__':
#     tweetParser = TweetParser()
#     jasonObjects = tweetParser.parseJsonStringsInFile("positiveMiniSample")
#     
#     for jasonObject in jasonObjects:
#         print jasonObject['created_at'] + " "

                
       
