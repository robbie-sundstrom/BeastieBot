#must first sudo pip install wikipedia 
#must also be run from terminal, don't cntrl+B in a text editor
import wikipedia 
import ast

def content(title):
	#make sure the article exists first
	if wikipedia.search(title):
		page = wikipedia.page(title)
		content=(page.content)
		content_list =content.split(' ')
		for word in content_list:
			if word =='American': # replace with an expression that generalizes for words rhyming with user input
				return word

	else:
		raise ValueError 

if __name__ == '__main__':
	print content('Beastie Boys')
