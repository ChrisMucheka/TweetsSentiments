import sys, tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import string
import re
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from flask import Flask

class Hash():
 cachedStopWords  =  stopwords.words("english")
 def topFiveHash(topic,no):

    for tweet in topic:
        text2  =  tweet.text
        text1  =  text2.lower ()
        tweetArray  =  text1.split ()
        for word in tweetArray:
            if word[0:1] == "#" and len ( word ) > 1:
                hashTag  =  word.translate ( string.punctuation )
                if hashTag in hashTable:
                    hashTable[hashTag]+=  1
                else:
                    hashTable[hashTag]  =  1
    hashTableSorted  =  dict(sorted ( hashTable.items (), key = operator.itemgetter ( 1 ), reverse = True )[:no] )
    return hashTableSorted