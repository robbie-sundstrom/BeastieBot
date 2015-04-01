"""
Generates a list of rhymes sorted by popularity and rhyme distance.
"""

import urllib2, json
from pprint import pprint

sourceword = 'hand'	# CHANGE THIS TO FIND DIFFERENT RHYMES


url = "http://rhymebrain.com/talk?function=getRhymes&word=" + sourceword
f = urllib2.urlopen(url)
rawrhymes = f.read()

# split the text into a list of lines, ignore leading '['
# NOTE: does not take care of last ']'
lines = rawrhymes[1:].splitlines()
for i in range(len(lines)):
	lines[i] = lines[i][2:-2]	# get rid of brackets on either side

wordlist = []
for line in lines:
	startchar = 8	# start at the actual word
	for i in range(8, len(line[7:])):
		if line[i] == '"':	# search for the closing quote
			stopchar = i
			break
	wordlist.append(line[startchar:stopchar])

print wordlist