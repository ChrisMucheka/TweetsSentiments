import sys, tweepy,csv
from textblob import TextBlob
import string
import re
import operator
import pygal
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from flask import Flask, request, render_template, flash,redirect,Markup
from form import TweetForms

hashWordTable = {}
hashTable  =  {}
hashRetweetTable = {}
cachedStopWords  =  stopwords.words("english")

app = Flask(__name__)
app.config['SECRET_KEY']='key'

#ploting graphs on the result page
@app.route('/results',methods=['GET','POST'])
def results():
    form1 = TweetForms ()

    m = request.form['wordTopic']
    h = request.form['noOfTopHash']
    n = request.form['noOfTweet']
    w = request.form['noOfTopWords']
    rt = request.form['noOfTopRetweets']
    data=""
    if n.isdigit()==False or h.isdigit()==False or w.isdigit()==False or rt.isdigit()==False:
        flash ( 'You enter a string instead of a number ', 'error' )
        return render_template ( "index.html", title="Home-Querry", form=form1 )
    else:
        # Sentiment analysis on the topic
        labels = ["Positive", "Negative", "Neutral"]
        if sentimentAnalysis ( getTopic ( connection (), m, n ) )[0] == 0 and \
                        sentimentAnalysis ( getTopic ( connection (), m, n ) )[1] == 0 and \
                        sentimentAnalysis ( getTopic ( connection (), m, n ) )[2] == 0:
            flash ( 'You request could not bring any result try another topic', 'error' )
            return render_template ( "index.html", title="Home-Querry", form=form1 )
        else:
            values = list ( sentimentAnalysis ( getTopic ( connection (), m, n ) ) )
            pie_chart = pygal.Pie ()
            pie_chart.title = "The rection of people on " + str ( m ) + " by analysing on " + str ( n ) + " tweets"
            for i, v in zip ( labels, values ):
                pie_chart.add ( i, float ( v ) )
                #data = pie_chart.render_data_uri ()
            pie_chart.render_to_file('static/sentiment.svg')
            # top used hastags in tweets about the topic
            hashTag_bar_chart = pygal.Bar ()
            hashTag_bar_chart.title = 'The top ' + h + ' used hastags'
            for key1, values1 in topHash ( getTopic ( connection (), m, n ), int ( h ) ).items ():
                hashTag_bar_chart.add ( key1, values1 )
            hashTag_bar_chart.render_to_file ( 'static/hashTags.svg' )

            # top used words in tweets about the topic
            topWord_bar_chart = pygal.Bar ()
            topWord_bar_chart.title = 'The top ' + w + ' used words'
            for key2, value2 in topWords ( getTopic ( connection (), m, n ), int ( w ) ).items ():
                topWord_bar_chart.add ( key2, value2 )
            topWord_bar_chart.render_to_file ( 'static/topWord.svg' )

            # top used retweeded tweets about the topic
            """ topRetweeded_bar_chart = pygal.Bar ()
            topRetweeded_bar_chart.title = 'The top ' + rt + ' retweeted tweets'
            for key2, value2 in topRetweets ( getTopic ( connection (), m, n ), int ( rt ) ).items ():
                topRetweeded_bar_chart.add ( key2, value2 )
            topRetweeded_bar_chart.render_to_file ( 'static/topRetweeded.svg' )"""
            #for key2, value2 in topRetweets ( getTopic ( connection (), m, n ), int ( rt ) ).items ():
              #  topRetweeded_bar_chart.add ( key2, value2 )
            hastags=topRetweetsPrint ( getTopic ( connection (), m, n ), int ( rt ) )
            return render_template ( "results.html",hastags=hastags, title="Results", form=form1 )

#querring from the home page
@app.route('/',methods=['GET','POST'])
def query():
    form=TweetForms()
    return render_template("index.html",title="Home-Querry",form=form)

#remove abbreviation and short-hand words and replace with the actual word
def translator(user_string):
    user_string = user_string.split(" ")
    j = 0
    for _str in user_string:
        # File path which consists of Abbreviations.
        fileName = "C:\\Users\\Fifofa\\Desktop\\slang.txt"
        # File Access mode [Read Mode]
        accessMode = "r"
        with open(fileName, accessMode) as myCSVfile:
            # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
            dataFromFile = csv.reader(myCSVfile, delimiter="=")
            # Removing Special Characters.
            _str = re.sub('[^a-zA-Z0-9-_.]', '', _str)
            for row in dataFromFile:
                # Check if selected word matches short forms[LHS] in text file.
                if _str.upper() == row[0]:
                    # If match found replace it with its appropriate phrase in text file.
                    user_string[j] = row[1]
            myCSVfile.close()
        j = j + 1
    # Replacing commas with spaces for final output.
    user_string=' '.join(user_string)
    return user_string
def topRetweetsPrint(topic1,no):
    hashRetweets = {}
    for tweet in topic1:
        origina_tweet=tweet.retweet_count
        text1=tweet.text
        if origina_tweet>0:
           hashRetweets[text1]=origina_tweet
    hashRetweetTableSorted = dict (sorted ( hashRetweets.items (), key=operator.itemgetter ( 1 ), reverse=True )[:no] )
    return hashRetweetTableSorted
#calculating the top retweeted tweets
def topRetweets(topic1,no):
    for tweet in topic1:
        text2 = tweet.text
        username=tweet.author._json['screen_name']
        text2 = text2.lower ()
        text2 = translator ( text2 )
        text2 = ' '.join ( [word for word in text2.split () if word not in cachedStopWords] )
        text2 = text2.replace ( text2, re.sub ( r'@[A-Za-z0-9]+', '', text2 ) )
        text2 = text2.replace ( text2, re.sub ( r'http\S+', '', text2 ) )
        tokenizer = RegexpTokenizer ( r'\w+' )
        tokenizer.tokenize ( text2 )
        #if str(text2) in hashRetweetTable and len(str(text2))>1:
         #    hashRetweetTable[str(text2),str(text2),str(username)]+= 1
        #else:
         #   if len(str(text2))>1:
         #       hashRetweetTable[str(text2),str(username)]  =  1
    #hashRetweetTableSorted = dict(sorted(hashRetweetTable.items(),key = operator.itemgetter(1),reverse = True)[:int(no)])
    #return hashRetweetTableSorted
        print(username,text2)

#calculating the top used words
def topWords(topic1,no):

    for tweet in topic1:
        text2 = tweet.text
        text2 = text2.lower ()
        text2 = translator ( text2 )
        text2 = text2.replace ( text2, re.sub ( r'@[A-Za-z0-9]+', '', text2 ) )
        text2 = text2.replace ( text2, re.sub ( r'http\S+', '', text2 ) )
        text3 = ' '.join ( [word for word in str ( text2 ).split () if word not in cachedStopWords] )
        tokenizer = RegexpTokenizer ( r'\w+' )
        tokenizer.tokenize ( text3 )
        splitedTweet = text3.split ()
        for word in splitedTweet:
            if word in hashWordTable and len(word)>2:
                hashWordTable[word]+= 1
            else:
                if len(word)>2:
                   hashWordTable[word]  =  1
    hashWordTableSorted = dict(sorted(hashWordTable.items(),key = operator.itemgetter(1),reverse = True)[:no])
    return hashWordTableSorted

#calculating the top hastags used
def topHash(topic,no):
    for tweet in topic:
        text2  =  tweet.text
        text2  =  text2.lower ()
        text2 = translator (text2 )
        tweetArray  =  text2.split ()
        for word in tweetArray:
            if word[0:1] == "#" and len ( word ) > 1:
                hashTag  =  word.translate ( string.punctuation )
                if hashTag in hashTable:
                    hashTable[hashTag]+=  1
                else:
                    hashTable[hashTag]  =  1
    hashTableSorted  =  dict(sorted ( hashTable.items (), key = operator.itemgetter ( 1 ), reverse = True )[:no] )
    return hashTableSorted

#establishing a connection to twitter
def connection():

     access_token  =  "622906360-e6dIBC0oIDWP2GXhO6KYIGVd3gExnOiMfqb1mmUM"
     access_token_secret  =  "8sYrRbdJ6ZzaHX6ZoCQx1K3JNF7wv65fa3PFzA4XEw8yF"
     consumer_key  =  "Gbh036wNRda2EU6KpH9YyS7sn"
     consumer_secret  =  "m4upmcexHeM3jfCm1GjK8ygmkBiC3g0tqOSP9WoiTEGt5aVfn1"
     auth  =  tweepy.OAuthHandler(consumer_key, consumer_secret)
     auth.set_access_token(access_token, access_token_secret)
     api =  tweepy.API(auth)
     return api

#computing the general sentiment on the topic
def sentimentAnalysis(topic):

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
    if total_tweets==0:
        results=[0,0,0]
    else:
         positive = format(positive/total_tweets*100, '.2f')
         negative = format(negative/total_tweets*100, '.2f')
         neutral = format(neutral/total_tweets*100, '.2f')
         results=[positive,negative,neutral]
    return results

#Return the tweet data according to the topic and number of tweets requested
def getTopic(api, topicWord, noOfTweets):

        fromWhichLang = "en"
        noOfTweets = int ( noOfTweets )
        topic = tweepy.Cursor ( api.search, q=topicWord, lang=fromWhichLang ).items ( noOfTweets )
        return topic

#main method
if __name__ == "__main__":
    app.run(debug = True)
