"""
Get all product pages back
"""
import urllib
import multiprocessing
import fileinput
import re
import time
import random
import sys

N = 1
GETNAME = re.compile(r'dp/(.+)')
HOSTNAME = "www.amazon.com"
IPADRESS = ["54.239.25.200", "54.239.25.192", "54.239.17.7", "54.239.26.128", "54.239.17.7", "54.239.26.128", "54.239.25.208"]


def getPage(url, output_folder="./product_page"):
	global N
	name = GETNAME.search(url).group(1)

	# random sleep for avoiding spider detection
	timeToSleep = float(random.randint(15, 50)) / 15
	time.sleep(timeToSleep)

	print "%4d: fetching %s..." % (N, url.strip())

	try:
		content = urllib.urlopen(url).read()
	except Exception as e:
		print e, e.message
		return False

	N += 1
	#blocked
	if len(content) == 1378:
		#raise Exception("No.%s not fetched, our spider got blocked")
		with open("%s/error_list_1000.txt" % output_folder, 'a') as fp:
			fp.write("%s" % IPtoHostname(url))
			print "No.%s not fetched, our spider got blocked...t=%.2f\nurl:%s" % (N, timeToSleep, url)
			return False

	with open("%s/%04d_%s.html" % (output_folder, N, name), 'w') as fp:
		fp.write(content)

	print "fetched %s bits and N=%.2f" % (len(content), timeToSleep)
	return True

def hostnameToIP(url):
	num = len(IPADRESS)
	ip = IPADRESS[random.randint(0, num - 1)]
	url = re.sub(HOSTNAME, ip, url)
	return url

def IPtoHostname(url):
	url = re.sub(r'[^/]+/dp', HOSTNAME, url)
	return url

if __name__ == '__main__':
	links = []

	for line in fileinput.input():
		links.append(hostnameToIP(line))

	startPage = 1950

	links = links[startPage - 1:]
	links = links[:50] #DEBUG
	#print links
	N = startPage

	result = map(getPage, links)

	print "total: %s" % len(result)
	print "fetched: %s" % len(filter(lambda x: x, result))

