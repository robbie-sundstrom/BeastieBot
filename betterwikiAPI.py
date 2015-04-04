#must first sudo pip install wikipedia 
#must also be run from terminal, don't cntrl+B in a text editor
import wikipedia 
import ast

def content(title):
	"""
	takes a wikipedia article and returns the content of the article as a list of words
	"""
	#make sure the article exists first
	if wikipedia.search(title):
		page = wikipedia.page(title)
		content=(page.content)
		content_list =content.split(' ')
		return content_list	
	else:
		raise ValueError 

def get_rhymes_indicies(key_word):
	"""
	takes the selected input and finds all instances within article
	returns a list of indicies 
	"""
	search_criteria = content('Beastie Boys') 
	key_word_indicies=[x.encode('UFT8') for x in search_criteria]
	return key_word_indicies
	

	#u'rap' in search_criteria.values()


	"""
	for word in content('Beastie Boys'):
		if word ==key_word: # replace with an expression that generalizes for words rhyming with user input
			key_word_indicies.append(content('Beastie Boys')[word])

	"""

 def make_sentence():
 	"""
 	will take indicies in get_rhymes_indicies and work for the n words preceeding the key_word
 	returns a list of strings, with each string as a line of the rap 
	"""
if __name__ == '__main__':
	#print content('Beastie Boys')
	print get_rhymes_indicies(u'rap')