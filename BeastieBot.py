"""
THE FINAL CODE

"""

# import TwitterSearchDemo
# import rhymebraintester
from rhymebraintester import find_rhymes
from TwitterSearchDemo import find_tweets

def beastie_it_up(sourceword, limit):
	rhymelist = find_rhymes(sourceword)
	
	for i in range(limit):
		thisword = rhymelist[i]
		print find_tweets(thisword, 10)

beastie_it_up('tack', 4)