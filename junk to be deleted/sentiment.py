import sys, tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import string
import re
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from flask import Flask
from word import Word
from hash import Hash
from retweet import Retweet



class Sentiment():
    def sentimentAnalysis(api,topicWord,noOfTweets,topMsg,topHash):
        w=Word()
        h=Hash()
        r=Retweet()
        #topicWord = input ( "Enter the topic you want to get its sentiment" )
        #noOfTweets = int ( input ( "Enter the number of tweets you want to get" ) )
        #topMsg = int ( input ( "Enter the number of top words used by people on your product" ) )
        #topHash = int ( input ( "Enter the number of top hashtag used by people on your product" ) )
        fromWhichLang = "en"
        # fromWhen  =  input("Enter the date from which you want the topic to be searched from within 7 day:format->YYYY-MM-DD")#until	optional	Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD. Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.		2015-07-19
        # fromWhichLang  =  input("Enter which language the tweets where tweeted in")
        # fromWhichLocation  =  input("Enter which location the tweets where tweeted in")
        # fromWhichLocation = "-24.653257,25.906792,1000"
        # fromWhen = "2019-01-12"
        # topic  =  tweepy.Cursor(api.search, q = topicWord,lang = fromWhichLang,geocode = fromWhichLocation,until = fromWhen).items(noOfTweets)
        topic = tweepy.Cursor ( api.search, q=topicWord, lang=fromWhichLang ).items ( noOfTweets )
        positive = 0
        negative = 0
        neutral = 0
        polarity = 0
        for tweet in topic:
            tweet.text = tweet.text.replace ( tweet.text, re.sub ( r'@[A-Za-z0-9]+', '', tweet.text ) )
            tweet.text = tweet.text.replace ( tweet.text, re.sub ( r'http\S+', '', tweet.text ) )
            print ( tweet.text )
            analysis = TextBlob ( tweet.text )
            polarity = analysis.sentiment.polarity

            if analysis.sentiment.polarity > 0.0:
                positive += 1
            elif analysis.sentiment.polarity < 0.0:
                negative += 1
            else:
                neutral += 1
        total_tweets = neutral + negative + positive
        positive = format ( positive / total_tweets * 100, '.2f' )
        negative = format ( negative / total_tweets * 100, '.2f' )
        neutral = format ( neutral / total_tweets * 100, '.2f' )
        polarity = format ( polarity, '.2f' )
        print ( positive )
        if float ( polarity ) > 0.0:
            print ( "Positive" )
        elif float ( polarity ) < 0.0:
            print ( "Negative" )
        else:
            print ( "Neutral" )
        labels = ['Positive[' + str ( positive ) + '%]', 'Negative[' + str ( negative ) + '%]',
                  'Neutral[' + str ( neutral ) + '%]']
        size = [positive, negative, neutral]
        color = ['blue', 'red', 'green']
        patches, text = plt.pie ( size, colors=color, startangle=90 )
        plt.legend ( patches, labels, loc='best' )
        plt.title (
            "The rection of people on " + str ( topicWord ) + " by analysing on " + str ( total_tweets ) + " tweets" )
        plt.axis ( 'equal' )

        plt.tight_layout ()
        plt.show ()
        topic2 = tweepy.Cursor ( api.search, q=topicWord, lang=fromWhichLang ).items ( noOfTweets )
        topic3 = tweepy.Cursor ( api.search, q=topicWord, lang=fromWhichLang ).items ( noOfTweets )

        if len ( h.topFiveHash ( topic2, topHash ) ) > 0:
            print ( h.topFiveHash ( topic2, topHash ) )
            plt.bar ( range ( len ( h.topFiveHash ( topic2, topHash ) ) ),
                      list ( h.topFiveHash ( topic2, topHash ).values () ), width=1.5 )
            plt.xticks ( range ( len ( h.topFiveHash ( topic2, topHash ) ) ),
                         list ( h.topFiveHash ( topic2, topHash ).keys () ) )
            plt.show ()
        else:
            print ( "/n There were no hashtag" )
        if 1 > 0:  # len(topFiveWords(topic2, topMsg))>0:
            print ( w.topFiveWords ( topic3, topMsg ) )
            # plt.bar(range(len(topFiveWords(topic2, topMsg))), list(topFiveWords(topic2, topMsg).values()),width = 1.5)
            # plt.xticks(range(len(topFiveWords(topic2, topMsg))), list(topFiveWords(topic2, topMsg).keys()))
            # plt.show()
        else:
            print ( "/n There is no popular thing people are saying about your product" )