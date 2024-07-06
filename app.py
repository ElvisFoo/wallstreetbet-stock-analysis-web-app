from flask import Flask, request, render_template, redirect
import requests
from datetime import datetime, date, timedelta
import pytz

app = Flask(__name__)

@app.route("/")
def index():
    yesterday = datetime.now(pytz.timezone('America/New_York')).date() - timedelta(days = 1)
    response = requests.get('https://tradestie.com/api/v1/apps/reddit')
    yesterday_response = requests.get(f'https://tradestie.com/api/v1/apps/reddit?date={yesterday}')
    if response.status_code != 200 or yesterday_response.status_code != 200:
        return redirect('/error')

    stocks = response.json()
    yesterday_stocks = yesterday_response.json()

    average_sentiment = 0
    for stock in stocks:
        average_sentiment += stock['sentiment_score']

    average_sentiment /= 50

    return render_template('index.html', stocks=stocks, yesterday_stocks=yesterday_stocks, average_sentiment=average_sentiment)

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/yesterday")
def yesterday():
    yesterday = datetime.now(pytz.timezone('America/New_York')).date() - timedelta(days = 1)
    response = requests.get(f'https://tradestie.com/api/v1/apps/reddit?date={yesterday}')
    if response.status_code != 200:
        return redirect('/error')
    stocks = response.json()

    average_sentiment = 0
    for stock in stocks:
        average_sentiment += stock['sentiment_score']

    average_sentiment /= 50

    return render_template('yesterday.html', stocks=stocks, average_sentiment=average_sentiment)
