import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json
import pprint 

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data
def gen_url(article_title):
	"""
	Given an article title, will generate url to access
	"""
	base_url="http://en.wikipedia.org/w/api.php?action=query"
	get_revisions = "&prop=revisions"
	define_pg_titles='&titles=' +article_title #'Boston_Red_Sox' #example, replace with articletitle 
	content = 'rvprop=content'
	json = '&format=json'
	section = '&rvsection = 0' #chose article section 
	parse_html= '&rvparse=1'

	input_url = base_url+get_revisions+define_pg_titles + content + json +section +parse_html

	return get_json(input_url)
if __name__ == '__main__':
	pprint.pprint(gen_url('Boston_Red_Sox'))