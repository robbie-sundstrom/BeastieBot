"""
Finds rhymes for a user input word using natural language processing.
"""

import string
import nltk

def find_rhymes(inp, level):
	"""Function that returns rhymes of input word

	inp: the string to find rhymes of
	level: the number of phonemes that need to match 
	return: list of rhymes
	"""
	entries = nltk.corpus.cmudict.entries()
	syllables = [(word, syllable) for word, syllable in entries if word == inp]
	rhymes = []
	for (word, syllable) in syllables:
		rhymes += [word for (word, pron) in entries if pron[-level:] == syllable[-level:]]
	rhymes = [str(word) for word in rhymes if word != inp]
	return rhymes

print 'word?'
word = raw_input()
print 'level?'
level = input()
print find_rhymes(word, level)