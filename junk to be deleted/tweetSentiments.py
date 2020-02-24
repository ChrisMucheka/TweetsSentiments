import sys, tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import string
import re
import operator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from flask import Flask

hashTable  =  {}

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
def connection():

     access_token  =  "622906360-e6dIBC0oIDWP2GXhO6KYIGVd3gExnOiMfqb1mmUM"
     access_token_secret  =  "8sYrRbdJ6ZzaHX6ZoCQx1K3JNF7wv65fa3PFzA4XEw8yF"
     consumer_key  =  "Gbh036wNRda2EU6KpH9YyS7sn"
     consumer_secret  =  "m4upmcexHeM3jfCm1GjK8ygmkBiC3g0tqOSP9WoiTEGt5aVfn1"
     auth  =  tweepy.OAuthHandler(consumer_key, consumer_secret)
     auth.set_access_token(access_token, access_token_secret)
     api =  tweepy.API(auth)
     return api
def sentimentAnalysis(api):

    topicWord  =  input("Enter the topic you want to get its sentiment")
    noOfTweets  =  int(input("Enter the number of tweets you want to get"))
    topMsg = int(input("Enter the number of top words used by people on your product"))
    topHash  =  int ( input ( "Enter the number of top hashtag used by people on your product" ) )
    fromWhichLang  =  "en"
    #fromWhen  =  input("Enter the date from which you want the topic to be searched from within 7 day:format->YYYY-MM-DD")#until	optional	Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD. Keep in mind that the search index has a 7-day limit. In other words, no tweets will be found for a date older than one week.		2015-07-19
    #fromWhichLang  =  input("Enter which language the tweets where tweeted in")
    #fromWhichLocation  =  input("Enter which location the tweets where tweeted in")
    #fromWhichLocation = "-24.653257,25.906792,1000"
    #fromWhen = "2019-01-12"
    #topic  =  tweepy.Cursor(api.search, q = topicWord,lang = fromWhichLang,geocode = fromWhichLocation,until = fromWhen).items(noOfTweets)

    topic  =  tweepy.Cursor(api.search, q = topicWord,lang = fromWhichLang).items(noOfTweets)
    positive  =  0
    negative  =  0
    neutral  =  0
    polarity  =  0
    for tweet in topic:
        tweet.text =  tweet.text.replace(tweet.text,re.sub(r'@[A-Za-z0-9]+','',tweet.text))
        tweet.text  =  tweet.text.replace(tweet.text, re.sub(r'http\S+', '', tweet.text ))
        print(tweet.text)
        analysis = TextBlob(tweet.text)
        polarity = analysis.sentiment.polarity

        if analysis.sentiment.polarity>0.0:
           positive+= 1
        elif analysis.sentiment.polarity<0.0:
            negative+= 1
        else:
            neutral+= 1
    total_tweets = neutral+negative+positive
    positive = format(positive/total_tweets*100, '.2f')
    negative = format(negative/total_tweets*100, '.2f')
    neutral = format(neutral/total_tweets*100, '.2f')
    polarity = format(polarity, '.2f')
    print(positive)
    if float(polarity) > 0.0:
      print("Positive")
    elif float(polarity) < 0.0:
       print("Negative")
    else:
        print("Neutral")
    labels = ['Positive['+str(positive)+'%]','Negative['+str(negative)+'%]','Neutral['+str(neutral)+'%]']
    size = [positive,negative,neutral]
    color = ['blue','red','green']
    patches,text = plt.pie(size,colors = color,startangle = 90)
    plt.legend(patches,labels,loc = 'best')
    plt.title("The rection of people on "+str(topicWord)+" by analysing on "+str(total_tweets)+" tweets")
    plt.axis('equal')

    plt.tight_layout()
    plt.show()
    topic2  =  tweepy.Cursor ( api.search, q = topicWord, lang = fromWhichLang ).items ( noOfTweets )
    topic3 = tweepy.Cursor ( api.search, q=topicWord, lang=fromWhichLang ).items ( noOfTweets )

    if len(topFiveHash(topic2,topHash))>0:
       print(topFiveHash(topic2,topHash))
       plt.bar(range(len(topFiveHash(topic2,topHash))),list(topFiveHash(topic2,topHash).values()),width = 1.5)
       plt.xticks(range(len(topFiveHash(topic2,topHash))),list(topFiveHash(topic2,topHash).keys()))
       plt.show()
    else:
         print("/n There were no hashtag")
    if 1>0:#len(topFiveWords(topic2, topMsg))>0:
       print(topFiveWords(topic3, topMsg))
       #plt.bar(range(len(topFiveWords(topic2, topMsg))), list(topFiveWords(topic2, topMsg).values()),width = 1.5)
       #plt.xticks(range(len(topFiveWords(topic2, topMsg))), list(topFiveWords(topic2, topMsg).keys()))
       #plt.show()
    else:
         print("/n There is no popular thing people are saying about your product")

if __name__== '__main__':
    sentimentAnalysis(connection())
    app.run()