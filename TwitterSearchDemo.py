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
        consumer_key = 'IIS9bxYviganFNmhRI16FpOAW',
        consumer_secret = 'Av9guGhtBTSMyYXAZZgYzSQMNSDgBtHfG3aYrO8L4Uzix7704a',
        access_token = '218702250-J5CiB7cfx8jhIKIB2wQqR1ZBV6o0yPN57x5cF4Gp',
        access_token_secret = '23SnU89U18ftyoMJTaJYgEKc5jMCJNfDq1WKXDiz1gAYG'

    )

    counter = 0
    tweetlist = []

    for tweet in ts.search_tweets_iterable(tso):
        if counter >= limit:
            break

        thistweet = tweet['text']
        if '@' not in thistweet and thistweet[-(len(sourceword)):] == sourceword:
            tweetlist.append(str(thistweet))
            counter += 1
    return tweetlist

print find_tweets('flame.',4)