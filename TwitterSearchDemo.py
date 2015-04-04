from TwitterSearch import *

def find_tweets(sourceword,limit):
    """
    Generates a list of the limit number of tweets ending in the sourceword.
    """
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([sourceword]) # word to search for
    tso.set_language('en') # we want to see English tweets only
    tso.set_include_entities(False) # don't give us all those entity information

    # create TwitterSearch object
    ts = TwitterSearch(
        ### PASTE KEYS HERE ###
    )

    counter = 0
    tweetlist = []

    for tweet in ts.search_tweets_iterable(tso):
        if counter >= limit:
            break

        thistweet = tweet['text']
        if '@' not in thistweet and thistweet[-(len(sourceword)):] == sourceword:
            tweetlist.append(thistweet)
            counter += 1
    return tweetlist

print find_tweets('flame.',4)