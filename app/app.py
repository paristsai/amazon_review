from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import re
import datetime, time
from operator import itemgetter

SKUPATTERN = re.compile(r'/product/([^/]+)')

app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Feelings/Programming/amazon-review/app/flask/review.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
	__tablename__ = 'reviews'
	id = db.Column(db.String(20),primary_key=True)
	pid = db.Column(db.String(20))
	author = db.Column(db.String(20))
	rate = db.Column(db.Integer)
	title = db.Column(db.Text)
	content = db.Column(db.Text)
	date = db.Column(db.Text)
	verified = db.Column(db.Integer)
	color = db.Column(db.String(20))
	vote = db.Column(db.Integer)

	def __init__(self, id, pid, rate):
		self.id = id

	def __repr__(self):
		return '<Rate %r>' % self.rate
# class Record(db.Model):
# 	__tablename__ = 'records'



@app.route('/')
def hello():
	# return "Hello World!"
	return render_template('index.html')

@app.route('/review', methods=['GET', 'POST'])
def hello_reivew():
	errors = []
	results = {}
	if request.method == "POST":
		url = request.form['url']
		pid = re.search(r'amazon.*/(gp/product)|(dp)/([A-Za-z0-9]+)', url)
		if pid:
			try:
				pid = pid.group(3)
				print(pid)
				reviews = Review.query.filter(Review.pid==pid).all()#B00001W0DF

				verified = [i for i in reviews if i.verified == 1]
				unverified = [i for i in reviews if i.verified == 0]

				verified_rate = np.array([i.rate for i in verified])
				unverified_rate = np.array([i.rate for i in unverified])
				# total, date
				results = {
					"Yes": [verified_rate.size,round(float(verified_rate.size)/len(reviews),3)*100,round(verified_rate.mean(),2)],
					"No": [unverified_rate.size,round(float(unverified_rate.size)/len(reviews),3)*100,round(unverified_rate.mean(),2)]
				}

				# Data for Chart1
				rates = {"verified":{1:0, 2:0, 3:0, 4:0, 5:0}, "unverified":{1:0, 2:0, 3:0, 4:0, 5:0}}
				for rate in verified_rate:
					rates["verified"][rate] += 1
				for rate in unverified_rate:
					rates["unverified"][rate] += 1
				# Data for Chart2
				testseries = [[1214179200000,24.74],[1214265600000,24.75],[1214352000000,25.34], [1214438400000,24.04], [1214524800000,24.30], [1214784000000,23.92]]
				# convert time to timestamp

				def convertToTS(dt_str):
					dt_obj  = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
					time_tuple = dt_obj.timetuple()
					ts = int(time.mktime(time_tuple) * 1000)
					return ts

				time_series = []
				time_series.append([[convertToTS(i.date), i.rate] for i in reviews])
				time_series.append([[convertToTS(i.date), i.rate] for i in reviews if i.verified == 1])
				time_series.append([[convertToTS(i.date), i.rate] for i in reviews if i.verified == 0])

				for i in range(len(time_series)):
					time_series[i] = sorted(time_series[i], key=itemgetter(0))
				

				api_type, chartID, chart_type, chart_height, chart, series, title, xAxis, yAxis, tooltip, legend = ([], [], [], [], [], [], [], [], [], [], [])

				# Chart 1
				api_type.append('Chart')
				chartID.append('chart1_ID')
				chart_type.append('bar')
				chart_height.append(350)
				chart.append({"renderTo": chartID[0], "type": chart_type[0], "height": chart_height[0]})
				series.append([{"name": 'Yes', "data": rates["verified"].values()}, {"name": 'No', "data": rates["unverified"].values()}])
				title.append({"text": 'Cusomer Reviews'})
				xAxis.append({"categories": ['1', '2', '3', '4', '5']})
				yAxis.append({"title": {"text": 'Number'}})

				# Chart2
				api_type.append('StockChart')
				chartID.append('chart2_ID')
				chart_type.append({})
				chart_height.append({})
				chart.append({})
				series.append([{"name": 'All', "data": time_series[0]},{"name": 'Verified', "data": time_series[1]},{"name": 'Unverified', "data": time_series[2]}])
				title.append({"text": 'Review Rate Time Series'})
				xAxis.append({})
				yAxis.append({"title": {"text": 'Rate'}})

				# Text Analysis

			except:
				errors.append("Unable to get URL. Please make sure it's valid and try again.")
				return render_template('review.html', errors=errors)

	return render_template('review.html', errors=errors, results=results.items(), api_type=api_type, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

if __name__ == '__main__':
	app.debug = True
	app.run()