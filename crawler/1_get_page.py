"""
Get menu page back
"""
import urllib
import multiprocessing

LINK = "http://www.amazon.com/s?rh=n%3A2407776011&page={0}&ie=UTF8"
LAST_PAGE = 400

def getPage(page, output_folder="./menu_page"):
	url = LINK.format(page)

	print "fetching %s" % url
	try:
		content = urllib.urlopen(url).read()
		with open("%s/%s.html" % (output_folder, page), 'w') as fp:
			fp.write(content)
	except Exception as e:
		print e, e.message
		#why
		print False
		return False
	else:
		print True
		return True

if __name__ == '__main__':
	pageNums = range(1, LAST_PAGE + 1)

	pool = multiprocessing.Pool(processes=40)
	result = pool.map(getPage, pageNums)

	print "total: %s" % len(result)
	print "fetched: %s" % len(filter(lambda x:x, result))
