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
	def matchMoney(result):
		if result:
			return result.group(1)
		else:
			return "0"

	pq = PyQuery(filename=filename)
	product_id = re.search(r'\d{4}_([^\.]{10})', filename).group(1)
	product_name = pq("#productTitle").text() or ""
	product_brand = pq("#brand").text() or ""
	# product_list_price = pq("#price .a-text-strike").eq(0).text().replace("$", "") or "0"
	# product_price = pq("#price .a-text-strike").eq(1).text().replace("$", "") or "0"
	# product_sale = pq("#priceblock_saleprice").text().replace("$", "") or "0"
	# print(pq("table.a-lineitem").text())

	price_table = pq("table.a-lineitem").text().replace(r'List Price: \$[\d\.]+', "")
	product_price = matchMoney(re.search(r'Price: \$([\d\.]+)', price_table))
	product_sale = matchMoney(re.search(r'Sale: \$([\d.]+)', price_table))

	product_detail = pq("#featurebullets_feature_div li").text() or ""

	review_num = re.match(r'\d+', pq("#acrCustomerReviewText").text() or "0").group()
	review_rate = re.match(r'\d+', pq("#acrPopover").text() or "0").group()
	# print(product_price)
	# print(product_sale)
	#print "num:%s\nrate:%s" % (review_num, review_rate)
	return tuple([product_id, product_name, product_brand, product_detail, product_price, product_sale , review_num, review_rate])

def writeCSV(tuples):
	csvwriter = csv.writer(sys.stdout)
	csvwriter.writerow(tuple(['product_id', 'product_name', 'product_brand', 'product_detail', 'product_price', 'product_sale' , 'review_num', 'review_rate']))
	for t in tuples:
		row = [ s.encode('utf-8') for s in t]
		csvwriter.writerow(row)


if __name__ == '__main__':
	files = getFiles()
	# files = files[:5] #DEBUG
	results = map(parsePage, files)
	# print(results)


	writeCSV(results)