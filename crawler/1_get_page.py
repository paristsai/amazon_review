"""
Get menu page back
"""
import urllib
import urllib2
import multiprocessing
import random

LINK = "http://www.amazon.com/s?rh=n%3A2407776011&page={0}&ie=UTF8"
LAST_PAGE = 400
LOCAL = "http://localhost:8080/proxy"
PROXY = ["http://amazon-app-1258.appspot.com/proxy","http://proxy2-1262.appspot.com/proxy","http://proxy3-1262.appspot.com/proxy"]

def getPage(page, output_folder="./menu_page"):
	server = PROXY[random.randint(0, len(PROXY) - 1)]
	url = server + "?data=" + urllib.urlencode(LINK.format(page))
	print(url)
	print "fetching %s" % url
	try:
		content = urllib.urlopen(url).read()
		with open("%s/%s.html" % (output_folder, page), 'w') as fp:
			#'w': Opens a file for writing only
			fp.write(content)
	except Exception as e:
		print e, e.message
		print False
		return False
	else:
		print True
		return True

def proxyPage(page, output_folder="./menu_page"):
	#method: get 
	# url = PROXY + "?data=" + LINK.format(page)
	# print("prodxyPage")
	# content = urllib.urlopen(url).read()
	# return content

	#method: post
	para = {}
	para["data"] = LINK.format(page)
	payload = urllib.urlencode(para)
	# print(payload)
	server = PROXY[random.randint(0, len(PROXY) - 1)]
	server = LOCAL
	req = urllib2.Request(server, payload)
	response = urllib2.urlopen(req).read()
	return response


def reParse(page, folder="./menu_page"):
	try:
		with open("%s/%s.html" % (folder, page), 'w') as fp:
			#'r+': Opens a file for both reading and writing. The file pointer placed at the beginning of the file.
			#'w+': Opens a file for both writing and reading. Overwrites the existing file if the file exists. If the file does not exist, creates a new file for reading and writing.
			# length = len(fp.read())
			# if (length >= 1378):

			content = proxyPage(page)
			fp.write(content)

	except Exception as e:
		print e, e.message
		return False
	else:
		return True

# def IOFile(file, filename, folder, mode):
# 	try:
# 		with open("%s/%s.html" % (folder, filename), mode) as fp:
# 			#'r+': Opens a file for both reading and writing. The file pointer placed at the beginning of the file.
# 			length = len(fp.read())
# 			if (length <= 1378):
# 				return proxyPage(page)
# 	except Exception as e:
# 		print e, e.message
# 		return False	

if __name__ == '__main__':
	pageNums = range(1, LAST_PAGE + 1)

	# pool = multiprocessing.Pool(processes=40)
	# result = pool.map(getPage, pageNums)
	result = map(reParse, pageNums)
	print(result)
	print "total: %s" % len(result)
	print "fetched: %s" % len(filter(lambda x:x, result))
