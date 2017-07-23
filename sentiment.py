import nltk.classify.util
import csv
import re
import tweepy
from tweepy import OAuthHandler
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import numpy as np

class TwitterClient(object):
    def __init__(self):
        
        consumer_key = 'rJZZolsJu2PzBPN46Q7bd8Gh2'
        consumer_secret = 'GnLljkvSQXk5a78AeBx9ORHqUyztCiY20bUzA5Wk0u34e1ld6Q'
        access_token = '831182468074008576-seoqhzUoNwjhDir4vBrwDGCEmT1jXqp'
        access_token_secret = 'vlCRvOn46ZJxDfHuhWU6S8lRKPrsRhT5ZE1W7kXTIFZBt'
        
        # attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
    
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def get_tweets(self, query, count = 1000):
        tweets = []
        
        try:
            fetched_tweets = self.api.search(q = query, lang = 'en', count = count, result_type = 'recent')
            
            for tweet in fetched_tweets:
                if tweet not in tweets:
                    tweets.append(tweet.text)
            return tweets
        
        except tweepy.TweepError as e:
            print("Error : " + str(e))


topic = raw_input("What is your topic?")
api = TwitterClient()
input = api.get_tweets(query = topic, count = 1000)
print(input)

pos_tweets = []
neg_tweets = []

inpTweets = csv.reader(open('sampleTweets.csv','rb'), delimiter = ',')
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    if sentiment == 'positive':
        pos_tweets.append((tweet,sentiment))
    else:
        neg_tweets.append((tweet,sentiment))

for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered,sentiment))

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = nltk.classify.apply_features(extract_features, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)

pos_opi = 0
neg_opi = 0

for item in input:
    opinion = classifier.classify(extract_features(item.split()))
    if opinion == "positive":
        pos_opi += 1
    elif opinion == "negative":
        neg_opi += 1

print("Total number of tweets regarding to " + str(topic) + " is " + str(pos_opi + neg_opi) + " tweets")
print("Positive tweets percentage: {} %".format(100*pos_opi/(pos_opi+neg_opi)))
print("Negative tweets percentage: {} %".format(100*neg_opi/(pos_opi+neg_opi)))

labels = 'Positive' , 'Negative'
sizes = [pos_opi,neg_opi]
colors = ['yellowgreen','lightcoral']

plt.pie(sizes, labels = labels, colors = colors, autopct = '%1.3f%%', shadow = True, startangle = 90)
plt.axis('equal')
plt.title(str(topic))
plt.show()







