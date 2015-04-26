"""
THE FINAL CODE

Created Apr 5, 2015

@authors Mackenzie Frackleton, Emily Mamula, Robert Siegel, Bill Wong
"""
from TwitterSearch import *
from profanity_list import bad_words
from profanity import profanity
profanity.load_words(bad_words)
from countsyl import count_syllables
import time, urllib2, json, random, sys

apinum = 0
apis_done = 0
filter_on = True
#### PUT apidict HERE ####

def find_rhymes(sourceword):
    """
    Generates a list of perfect rhymes of the sourceword, sorted by
    frequency in the English language.

    sourceword: the word to find rhymes of
    returns: A list of perfect rhymes
    """
    url = "http://rhymebrain.com/talk?function=getRhymes&word=" + sourceword
    f = urllib2.urlopen(url)
    rawrhymes = f.read()

    rhymes_dicts_list = json.loads(rawrhymes)

    perfect_rhymes_dicts_list = []

    for diction in rhymes_dicts_list:
    	if diction['score'] >= 300:
    		perfect_rhymes_dicts_list.append(diction)
    sorted_list = sorted(perfect_rhymes_dicts_list, key=lambda k: k['freq'],
                         reverse=True)

    wordlist = []
    for diction in sorted_list:
    	wordlist.append(str(diction['word']))
    return wordlist

def find_tweet(sourceword, timelimit):
    """
    Searches Twitter for a tweet ending in the sourceword. Only
    searches for tweets between 5 and 10 syllables long. Ignores
    tweets with '@' symbols or links to avoid retweets and unnecessary
    syllables.

    If no tweet is found before the timelimit, returns a blank string.

    sourceword: word that the tweets should end with
    timelimit: maximum number of seconds to search for
    returns: a string of the tweet, or an empty string if no tweet is
             found
    """
    global apinum, apis_done
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([sourceword]) # word to search for
    tso.set_language('en') # English tweets only
    tso.set_include_entities(False) # don't give us entity information

    ts = apidict[apinum]

    start = time.time()
    elapsed = 0

    try:
        for tweet in ts.search_tweets_iterable(tso):
            if elapsed >= timelimit:
                break

            thistweet = tweet['text']
            sylcount = count_syllables(thistweet)

            # check for ending word
            if (thistweet[-(len(sourceword)):] == sourceword or
                thistweet[-(len(sourceword)+1):] == sourceword+'.'):
                # check syllables, '@' symbols, and links
                if (sylcount <= 10 and sylcount >= 5 and
                    '@' not in thistweet and 'http' not in thistweet):
                    # profanity filter
                    if not filter_on:
                        return thistweet
                    # thesewords = thistweet.lower().split()
                    # if bad_words not in thesewords:
                    #     return thistweet
                    if not profanity.contains_profanity(thistweet):
                        return thistweet
                    print "PROFANE TWEET:",thistweet
            elapsed = time.time() - start
    except TwitterSearchException:
        apinum = (apinum + 1) % 3
        apis_done += 1
        if apis_done >= 3:  # if we exhausted all api keys
            print ('All api keys have reach their rate limit. Please '
                   'try again in 15 minutes.')
            sys.exit(0)
        return find_tweet(sourceword, timelimit)

    return ""

def beastie_it_up(sourceword, linelimit):
    """
    Prints tweets that end in a words that rhyme with the sourceword.
    Prints each tweet as it finds it. Stops after linelimit tweets, or
    after there are no more rhymes.

    sourceword: the word to rhyme with
    linelimit: the maximum number of lines to print
    returns: None
    """
    rhymelist = find_rhymes(sourceword)
    # print rhymelist
    start = time.time()
    elapsed = 0

    i = 0
    while i < linelimit and i < len(rhymelist):
    	thisword = rhymelist[i]
        thistweet = find_tweet(thisword, 2)
    	if thistweet == "":    # if it doesn't find a tweet
    		# make sure we still get the same number of lines
    		linelimit += 1
    	else:
            try:
                print thistweet
                #TODO: change this to display on gui
            except UnicodeEncodeError:
                linelimit += 1 # if there's an emoticon, skip this one
    	i += 1

# beastie_it_up('pole', 16)