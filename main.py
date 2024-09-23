"""
Stock Trading News Alert

Author: Alan
Date: September 23rd 2024

This sends messages using the Twilio service with the latest info about some stock news of Tesla.
This uses the APIs of
Alpha Vantage Inc. for stock data
News API for news data
"""

from requests import get
from twilio.rest import Client

# Twilio account data
ACCOUNT_SID = "your sid"
AUTH_TOKEN = "your auth token"
TWILIO_PHONE = "your account phone"

# Phone you are going to send the message to
YOUR_PHONE = "your phone number"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "your key"
NEWS_API_KEY = "your key"

def get_stock_data():
    """
    Gets the stock data from the alphavantage API
    :return: Float with the closed value per each day
    """
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY,
    }

    response = get(url=STOCK_ENDPOINT, params=parameters)

    stock_data = response.json()["Time Series (Daily)"]

    return [value for (key, value) in stock_data.items()]

def get_news():
    """
    Gets news about a company using the Newsapi API
    :return: List with three recent articles of newsapi
    """
    parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    response = get(url=NEWS_ENDPOINT, params=parameters)

    articles = response.json()["articles"]

    return articles[:3]

def send_messages(articles):
    """
    Uses the twilio library to send a message via SMS
    :return:
    """

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for article in articles:
        client.messages.create(
            body=article,
            from_=TWILIO_PHONE,
            to=YOUR_PHONE,
        )

stock_data_list = get_stock_data()

# Gets the stock price from yesterday
yesterday_stock_price = stock_data_list[0]["4. close"]

# Gets the stock price from the day before yesterday
before_yesterday_stock_price = stock_data_list[1]["4. close"]

# Finds the difference between yesterday and today
stock_difference = float(yesterday_stock_price) - float(before_yesterday_stock_price)

up_down = None

if stock_difference > 0:
    up_down = "🔺"

else:
    up_down = "🔻"

# Get the stock different percentage between yesterday and the stock difference
stock_difference_percentage = round((stock_difference / yesterday_stock_price) * 100)

if stock_difference_percentage > 1:

    # Gets a list with three recent news articles
    three_articles = get_news()

    # Format each of the fetched article
    formatted_articles = [f"{STOCK_NAME}: {up_down}{stock_difference_percentage}%\nHeadline: {article["title"]}. \nBrief: {article["description"]}" for article in three_articles]

    send_messages(formatted_articles)
