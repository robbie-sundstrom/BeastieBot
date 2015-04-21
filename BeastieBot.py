"""
THE FINAL CODE
"""
from TwitterSearch import *
from countsyl import count_syllables
import time, urllib2, json, random, sys

apinum = 0
apis_done = 0
#### PUT apidict HERE ####

def find_rhymes(sourceword):
	url = "http://rhymebrain.com/talk?function=getRhymes&word=" + sourceword
	f = urllib2.urlopen(url)
	rawrhymes = f.read()

	rhymes_dicts_list = json.loads(rawrhymes)

	perfect_rhymes_dicts_list = []

	for diction in rhymes_dicts_list:
		if diction['score'] >= 300:
			perfect_rhymes_dicts_list.append(diction)
	sorted_list = sorted(perfect_rhymes_dicts_list, key=lambda k: k['freq'], reverse=True)

	wordlist = []
	for diction in sorted_list:
		wordlist.append(str(diction['word']))
	return wordlist

def find_tweets(sourceword, limit):
    """
    Generates a list of the limit number of tweets ending in the sourceword.

    limit: maximum number of seconds to search for
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
            if elapsed >= limit:
                break

            thistweet = tweet['text']
            sylcount = count_syllables(thistweet)

            if thistweet[-(len(sourceword)):] == sourceword\
            or thistweet[-(len(sourceword)+1):] == sourceword+'.':
                if sylcount <= 10 and sylcount >= 5\
                and '@' not in thistweet and 'http' not in thistweet:
                    return thistweet
            elapsed = time.time() - start
    except TwitterSearchException:
        apinum = (apinum + 1) % 3
        apis_done += 1
        if apis_done >= 3:  # if we exhausted all api keys
            print 'All api keys have reach their rate limit. Please try again in 15 minutes.'
            sys.exit(0)
        return find_tweets(sourceword, limit)

    return ""

def beastie_it_up(sourceword, limit):
    rhymelist = find_rhymes(sourceword)
    print rhymelist
    start = time.time()
    elapsed = 0

    i = 0
    while i < limit and i < len(rhymelist):
    	thisword = rhymelist[i]
        thistweet = find_tweets(thisword, 2)
    	if thistweet == "":
    		# make sure we still get 4 lines if it doesn't find a tweet
    		limit += 1
    	else:
            try:
                print thistweet
            except UnicodeEncodeError:
                limit += 1 # if there's an emoticon, skip this one
    	i += 1

beastie_it_up('pole', 16)