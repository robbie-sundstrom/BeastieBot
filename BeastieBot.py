"""
THE FINAL CODE


"""
from TwitterSearch import *
from countsyl import count_syllables
import time, urllib2, json, random

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
    """
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([sourceword]) # word to search for
    tso.set_language('en') # English tweets only
    tso.set_include_entities(False) # don't give us entity information

    # PUT KEY FUNCTION HERE

    tweetlist = []
    start = time.time()
    elapsed = 0

    for tweet in ts.search_tweets_iterable(tso):
        if elapsed >=  limit:
            break

        thistweet = tweet['text']
        sylcount = count_syllables(thistweet)

        if sylcount <= 10 and sylcount >= 5 and '@' not in thistweet and thistweet[-(len(sourceword)):] == sourceword:
            tweetlist.append(thistweet)
            return thistweet
        elapsed = time.time() - start

    return ""

def beastie_it_up(sourceword, limit):
	rhymelist = find_rhymes(sourceword)
	print rhymelist
	start = time.time()
	elapsed = 0
	
	i = 0
	while i < limit:
		thisword = rhymelist[i]
		print 'finding rhymes for:',thisword

		thistweet = find_tweets(thisword, 5)
		if thistweet == "":
			# make sure we still get 4 lines if it doesn't find a tweet
			limit += 1
		else:
			print thistweet
		i += 1

beastie_it_up('store', 4)