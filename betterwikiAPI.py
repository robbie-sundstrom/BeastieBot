#must first sudo pip install wikipedia 
#must also be run from terminal, don't cntrl+B in a text editor
import wikipedia 
def content(title):
	#make sure the article exists first
	if wikipedia.search(title):

		page = wikipedia.page(title)
		return page.content
	else:
		raise ValueError 

if __name__ == '__main__':
	print content('Beastie Boys')
