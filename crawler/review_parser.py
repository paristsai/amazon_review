import re
from pyquery import PyQuery
import sqlite3 as lite
con = lite.connect('review.db')
# cur = conn.cursor()
# Create table
# con.execute('''CREATE TABLE reviews
#              (id TEXT, pid TEXT, author TEXT, rate INTEGER, title TEXT, content TEXT, date TEXT, verified INTEGER, color TEXT, vote INTEGER)''')
# from sys import getsizeof

VERIFIEDPATTERN = re.compile(r'Verified Purchase')
COLORPATTERN = re.compile(r'Color: ([^ ]+)')
VOTEPATTERN = re.compile(r'(person)|(people) found this helpful')

month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def addComma(dom):
	print(type(dom.text()))
	lists = []
	# for d in dom:
		# print(d.text())
		# lists.append(d.text())
	return lists
	# return ",".join(lists)
def isVerified(words):
	if VERIFIEDPATTERN.findall(words):
		return 1
	else:
		return 0
def numVote(words):
	# print(VOTEPATTERN.search(words))
	if VOTEPATTERN.search(words):
		num = words.split()[0]
		if num == "One":
			num = 1
	else:
		num = 0
	return int(num)
def convertTime(date):
	parts = date.split(" ")
	return "{0}-{1}-{2}".format(parts[3], int(month.index(parts[1])) + 1, parts[2][:-1])
def findColor(words):
	color = COLORPATTERN.findall(words)
	if len(color) > 0:
		return color[0]
	else:
		return ""
def findAuthor(words):
	return words.replace("By ", "")

class Review():
	def __init__(self, pid, html):
		pq = PyQuery(html)
		# pq = PyQuery(filename="Amazon_review_test.htm") #DEBUG
		# if using method1, I need to implement:
		# total_page = pq(".page-button").eq(-1).text()
		self.id = [i.attr("id") for i in pq(".a-section.review").items()]
		self.pid = pid
		self.author = map(findAuthor, [i.text() for i in pq(".reviews-content .review-byline").items()])
		self.rate = map(lambda i: i[0], [i.text() for i in pq(".reviews-content .review-rating").items('span')])
		self.title = [i.text() for i in pq(".reviews-content .review-title").items("a")]
		self.content = [i.text() for i in pq(".reviews-content .a-size-base.review-text").items("span")]
		self.date = [convertTime(i.text()) for i in pq(".reviews-content .review-date").items("span")]
		self.verified = map(isVerified, [i.text() for i in pq(".reviews-content .a-row.a-spacing-mini.review-data").items("div")])
		self.color = map(findColor, [i.text() for i in pq(".reviews-content .a-row.a-spacing-mini.review-data").items("div")])
		self.vote = map(numVote, [i.text() for i in pq(".reviews-content span.cr-vote-buttons").items()])
		# print(self.color)
	def rows(self):
		rows = list()
		#need to determine length of each array? not sure
		print "%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n" % (len(self.id),len(self.author),len(self.rate),len(self.title),len(self.content),len(self.date),len(self.verified),len(self.color),len(self.vote))
		for idx in range(0, len(self.id)):
			rows.append(tuple([self.id[idx], self.pid, self.author[idx], self.rate[idx], self.title[idx], self.content[idx], self.date[idx], self.verified[idx], self.color[idx], self.vote[idx]]))
		return rows
	def save(self):
		#connect sql db
		# print(self.rows())
		# Successful, con.commit() is called automatically afterwards
		# con.rollback() is called after the with block finishes with an exception, the
		# exception is still raised and must be caught
		try:
			with con:
				cur = con.cursor()
				#inserts many records at a time
				cur.executemany('INSERT INTO reviews VALUES (?,?,?,?,?,?,?,?,?,?)', self.rows())
		except lite.Error, e:
		    if con:
				con.rollback()
				print "Error %s:" % e.args[0]

if __name__ == '__main__':
	r = Review("test123","")