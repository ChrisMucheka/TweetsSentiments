import sys, tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import string
import re
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from flask import Flask

class Retweet():

 cachedStopWords  =  stopwords.words("english")
 def topFiveRetweets(topic1,no):
    #topic = topic1.split()
    hashRetweetTable = {}
    for tweet in topic1:
        text2 = tweet.text
        #text3= text1.split()
        #text2 = text3.lower()
        text2  = ' '.join ( [word for word in text2.split () if word not in cachedStopWords] )
        text2  =  text2.replace ( text2, re.sub ( r'@[A-Za-z0-9]+', '', text2 ) )
        text2  =  text2.replace ( text2, re.sub ( r'http\S+', '', text2 ) )
        tokenizer  =  RegexpTokenizer ( r'\w+' )
        tokenizer.tokenize ( text2 )
        if str(text2) in hashRetweetTable and len(str(text2))>1:
             hashRetweetTable[str(text2)]+= 1
        else:
            if len(str(text2))>1:
                hashRetweetTable[str(text2)]  =  1
    hashRetweetTableSorted = dict(sorted(hashRetweetTable.items(),key = operator.itemgetter(1),reverse = True)[:no])
    return hashRetweetTable