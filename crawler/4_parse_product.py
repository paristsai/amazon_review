"""
parse
"""
from pyquery import PyQuery
import HTMLParser
import os
import re
import csv
import sys

def getFiles(path='product_page'):
	all_files = []
	for path, dirs, files in os.walk(path):
		all_files += map(lambda s: os.path.join(path, s), files)

	return all_files

def parsePage(filename):
	pq = PyQuery(filename=filename)
	product_name = pq("#productTitle").text() or ""
	product_brand = pq("#brand").text() or ""
	product_list_price = pq("#price .a-text-strike").eq(0).text().replace("$", "") or "0"
	product_price = pq("#price .a-text-strike").eq(1).text().replace("$", "") or "0"
	product_sale = pq("#priceblock_saleprice").text().replace("$", "") or "0"
	product_detail = pq("#featurebullets_feature_div li").text() or ""

	review_num = re.match(r'\d+', pq("#acrCustomerReviewText").text() or "0").group()
	review_rate = re.match(r'\d+', pq("#acrPopover").text() or "0").group()

	#print "num:%s\nrate:%s" % (review_num, review_rate)
	return tuple([product_name, product_brand, product_list_price, product_price, product_sale, product_detail, review_num, review_rate])

def writeCSV(tuples):
	csvwriter = csv.writer(sys.stdout)
	for t in tuples:
		row = [ s.encode('utf-8') for s in t]
		csvwriter.writerow(row)

if __name__ == '__main__':
	files = getFiles()
	#files = files[:5] #DEBUG
	# print(files)
	results = map(parsePage, files)
	#print(results)

	writeCSV(results)