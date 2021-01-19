import requests
import time
import random
import decimal
import json
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib3

def getURL(url):
	# set some other values
	requests.packages.urllib3.disable_warnings()
	useragent = UserAgent()
	results_obj = {}
	referrer = 'https://www.github.com/'
	page = 1
	startnum = 0
	
	# get cookies (nom)
	session = requests.session()
	response = session.get(url)
	cookies = session.cookies.get_dict()

	# set default headers
	headers = {'user-agent': useragent.random, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Referer': referrer,'Upgrade-Insecure-Requests': '1'}
	# add cookies to headers
	for k, v in cookies.items():
		headers[k] = v

	webobject = BeautifulSoup(requests.get(url, headers=headers, verify=False).content, "lxml")

	return webobject

def getLocalFile(file):
	file = open(file, 'r', encoding="ISO-8859-1")
	page=file.read()
	webobject = BeautifulSoup(page, features="lxml")	

	return webobject


def searchGoogle(webobject):
	base="https://www.google.de/search?&"
	limiter="&num=100"
	query="q=site%3Apastebin.*+%22gmx.de"
	timer="&tbs=qdr:d"
	url = base + query + limiter + timer
	print(url)

	req="online search temporarily disabled -> local file mode"
	print(req)

	# temporarily work with local html webarchive test.webarchive

	#soup = BeautifulSoup(req.content, "lxml")
	
	# webarchive="test2.html"
	# file = open(webarchive, 'r', encoding="ISO-8859-1")
	# page=file.read()

	#soup = BeautifulSoup(req.content, "lxml")
	#soup = BeautifulSoup(page, features="lxml")
	resultbody = webobject.find('div', {'id': 'search'})
	
	# parse resultbody and extract headings h3 and links to search results
	resultList=[]
	

	if len(resultbody) >= 1:
		items=resultbody.find_all(class_="g")
		for i in items:
			resultDict={}
			links=i.find_all('a', href=True)
			for l in links:
				headings=l.find_all('h3')
				for h in headings:
					if 'webcache' not in l['href'] and '#' not in l['href'] and '?q=related:' not in l['href'] and 'translate.google' not in l['href']:
						spans=h.find_all('span')
						for s in spans:
							resultDict["heading"]=s.text
							resultDict["link"]=l['href']
			resultList.append(resultDict)

		

	return resultList

def parsePastebin(webobject):

	result={}

	return result



def main():
	print(json.dumps(searchGoogle(getLocalFile("test2.html")), indent=4))
	#getURL("https://pastebin.pl/view/08478ae1")
	#parsePastebin(getURL("https://pastebin.pl/view/08478ae1"))


if __name__ == '__main__':
	main()


