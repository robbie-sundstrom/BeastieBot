#must first sudo pip install wikipedia 
#must also be run from terminal, don't cntrl+B in a text editor
import wikipedia, string,copy


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

def get_rhymes_list(title):
	"""
	takes the selected input and changes it into a list, then cleans it
	returns a list of words from the wikipedia article 
	"""
	#Makes output of content a python list 
	search_criteria = content(title) 
	content_list=[x.encode('utf-8') for x in search_criteria]

	#need to clean out the list for numbers and gibberish like \xe2\x80\x93. THis could potentially also go at the end
	npunc_text_list = []
	for element in content_list: 
		npunc_text_list.append(element.strip(string.punctuation))
	return npunc_text_list

	#is_integer = lambda s: s.isdigit() or (x[0] == '-' and x[1:].isdigit())
	#no_integers = filter(is_integer, content_list )
	#no_numbers_list= [x for x in content_list if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
	#return no_integers

def make_sentence(key_word,title):
 	"""
 	Takes a keyword and wikipedia article title as strings, calls get_rhymes_list to procure a python list version of the wikipedia article, then
 	scans the wikipedia article for the keyword and returns its index. For now, returns a *sentence* that is the key word plus the 
 	five words preceeding it. 

 	Returns a list of str lines of a rap 
	"""
	source_material = get_rhymes_list(title)
	ref_material = copy.deepcopy(source_material)
	index_list =[]
	for word in source_material:
		if word == key_word:
			index_list.append(source_material.index(key_word))
			source_material.remove(word)
	lines =[]
	for i in index_list:
		lines.append(ref_material[i]+ ref_material(i-1) + ref_material(i-2) + ref_material(i-3) +ref_material(i-4) +ref_material(i-5))
		index_list.remove(i)
	return lines
	pass
if __name__ == '__main__':
	#print content('Beastie Boys')
	#print get_rhymes_list(u'rap',title)
	print make_sentence('Beastie','Beastie Boys')