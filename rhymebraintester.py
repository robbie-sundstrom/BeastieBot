"""
Generates a list of rhymes sorted by popularity and rhyme distance.

"""

import urllib2, json, pprint

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