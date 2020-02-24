import sys, tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import string
import re
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from flask import Flask
class Word():
 cachedStopWords = stopwords.words ( "english" )
 def topFiveWords(topic1,no):
    #topic = topic1.split()
    hashWordTable = {}
    for tweet in topic1:
        text2 = tweet.text
        #text2= str(text1.split())
        #text2 = text3.lower()

        text2  =  text2.replace ( text2, re.sub ( r'@[A-Za-z0-9]+', '', text2 ) )
        text2  =  text2.replace ( text2, re.sub ( r'http\S+', '', text2 ) )
        text2 = ' '.join ( [word for word in str ( text2 ).split () if word not in cachedStopWords] )
        tokenizer  =  RegexpTokenizer ( r'\w+' )
        tokenizer.tokenize ( text2 )
        splitedTweet=text2.split()
        for word in splitedTweet:
            if word in hashWordTable and len(word)>2:
                hashWordTable[word]+= 1
            else:
                if len(word)>2:
                   hashWordTable[word]  =  1
    hashWordTableSorted = dict(sorted(hashWordTable.items(),key = operator.itemgetter(1),reverse = True)[:no])
    return hashWordTableSorted