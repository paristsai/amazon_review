import re

PRODUCTID_PATTERN = re.compile(r'li id="result_\d+" data-asin="([^"]+)')
PRODUCTNAME_PATTERN = re.compile(r'result.*data-asin="(.+)"')
PRODUCT_URL = "http://www.amazon.com/dp/{0}"
PAGE_NUM = 400

def getProductIdPage(page):
	with open('menu_page/%s.html' % page) as fp:
		content = fp.read()
		result = PRODUCTID_PATTERN.findall(content)
	return result


if __name__ == '__main__':
	pages= range(1, PAGE_NUM + 1)

	result = reduce(lambda a, b: set(list(a) + list(b)), map(getProductIdPage, pages))
	links = map(lambda s: PRODUCT_URL.format(s), result)

	#for l in links:
	#	print l

	with open('product_links.txt', 'w') as fp:
		for link in links:
			fp.write("{}\n".format(link))