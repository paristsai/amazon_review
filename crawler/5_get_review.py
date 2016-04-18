import urllib
import urllib2
import re
import time
import random
import multiprocessing
import fileinput
from review_parser import Review

N = 0

LOCAL = "http://localhost:8080/proxy"

GETNAME = re.compile(r'product-reviews/(.+)/')
REVIEWURL = "http://www.amazon.com/product-reviews/{0}/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber={1}&pageSize=50"

def formUrl(line):
	[pid, pnum] = line.split(",")
	urls = []
	for page in range(1, int(pnum) + 1):
		urls.append(REVIEWURL.format(pid, page))
	return urls
def proxyGetPage(url):
	global N

	#product id
	name = GETNAME.search(url).group(1)
	#avoid blocked
	timeToSleep = float(random.randint(15, 30)) / 15
	time.sleep(timeToSleep)

	N += 1
	print "%4d: fetching %s..." % (N, url.strip())
	server = PROXY[random.randint(0, len(PROXY) - 1)]
	proxy_url = "".join([LOCAL, "?", urllib.urlencode({"data":url.encode()})])
	# proxy_url = "".join(server, "?", urllib.urlencode({"data":url.encode()}))

	try:
		content = urllib.urlopen(proxy_url).read()
		print "size:%s, from:%s" % (len(content), server)
		if len(content) > 5000:
			return content
		else:
			#record link need to reparse
			with open("review_error_links", "a") as fp:
				fp.write(url + "\n")
			return False
	except Exception as e:
		print e, e.message
		return False

	return content

def getReview(urls):
	contents = map(proxyGetPage, urls)
	for html in contents:
		# print(html)
		#parse
		reviews = Review(html)
		# print(reviews.date)
		#insert to database
		reviews.save()

if __name__ == '__main__':
	lines = []

	for line in fileinput.input():
		lines.append(line)

	startPoint = 1
	lines = lines[startPoint - 1:]
	lines = lines[:1]#DEBUG
	links = map(formUrl, lines)
	# print(links)
	result = map(getReview, links)
