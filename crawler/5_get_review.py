import urllib
import urllib2
import re
import time
import random
import multiprocessing
# import httplib2
# http = httplib2.Http()

URL = "http://my-amazon-project.appspot.com/reviews"
# URL = "http://127.0.0.1:8080/reviews"

def sendDataToServer(para):
	payload = urllib.urlencode(para)
	# print(payload)
	req = urllib2.Request(URL, payload)
	response = urllib2.urlopen(req).read()
	print(response)
	print(type(response))

	return response

	# response, content = http.request(URL)
def saveReview(data, output_folder="./review_page")

if __name__ == '__main__':
	data = {}
	data["startpoint"] = 6
	data["steps"] = 2


	sendDataToServer(data)
	# content = urllib.urlopen(URL).read()
	# print(content)