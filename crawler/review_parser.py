import re
from pyquery import PyQuery
import sqlite3 as lite
con = lite.connect('review.db')
# When you first exute, you need to create table
# con.execute('''CREATE TABLE reviews
#              (id TEXT UNIQUE, author TEXT, rate INTEGER, title TEXT, content TEXT, date TEXT, verified INTEGER, color TEXT, vote INTEGER)''')

VERIFIEDPATTERN = re.compile(r'Verified Purchase')
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


class Review():
	def __init__(self, html):
		pq = PyQuery(html)
		# if using method1, I need to implement:
		# total_page = pq(".page-button").eq(-1).text()
		self.id = [i.attr("id") for i in pq(".a-section.review").items()]
		self.author = [i.text() for i in pq(".reviews-content .author").items("a")]
		self.rate = map(lambda i: i[0], [i.text() for i in pq(".reviews-content .review-rating").items('span')])
		self.title = [i.text() for i in pq(".reviews-content .review-title").items("a")]
		self.content = [i.text() for i in pq(".reviews-content .a-size-base.review-text").items("span")]
		self.date = [convertTime(i.text()) for i in pq(".reviews-content .review-date").items("span")]
		self.verified = map(isVerified, [i.text() for i in pq(".reviews-content .a-row.a-spacing-mini.review-data").items("div")])
		self.color = [i.text().split(" ")[1] for i in pq(".reviews-content .review-data .a-link-normal.a-color-secondary").items("a")]
		self.vote = map(numVote, [i.text() for i in pq(".reviews-content span.cr-vote-buttons").items()])

	def rows(self):
		rows = list()
		#need to determine length of each array? not sure
		for idx in range(0, len(self.id)):
			rows.append(tuple([self.id[idx], self.author[idx], self.rate[idx], self.title[idx], self.content[idx], self.date[idx], self.verified[idx], self.color[idx], self.vote[idx]]))
		return rows
	def save(self):
		# Successful, con.commit() is called automatically afterwards
		# con.rollback() is called after the with block finishes with an exception, the
		# exception is still raised and must be caught
		try:
			with con:
				cur = con.cursor()
				#inserts many records at a time
				cur.executemany('INSERT INTO reviews VALUES (?,?,?,?,?,?,?,?,?)', self.rows())
		except lite.Error, e:
		    if con:
				con.rollback()
				print "Error %s:" % e.args[0]