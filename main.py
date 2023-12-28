
import requests
from twilio.rest import Client

account_sid = "account_sid_twilio"
auth_token = "auth_token_twilio"

STOCK = "MSFT"
COMPANY_NAME = "Microsoft"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
API_KEY_STOCK = "YOUR_API_KEY_STOCK"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY_NEWS = "YOUR_API_KEY_NEWS"

parameters_stocks = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}

response = requests.get(STOCK_ENDPOINT, params=parameters_stocks)
response.raise_for_status()
data_stock = response.json()

daily = []
for stocks in {**data_stock['Time Series (Daily)']}.items():
    daily.append(stocks)
today = daily[0][0]

open_close_list = []

for high_low in daily:
    open_close_list.append(float(high_low[1]['4. close']))
open_close_list = open_close_list[:3]


value_difference = abs(open_close_list[0] - open_close_list[-1])
value = (value_difference/open_close_list[0]) * 100


def get_value(value_, val1, val2):
    if val1 - val2 > 0:
        return f"🔺{round(value_, 3)}"
    elif val1 - val2 < 0:
        return f"🔻{round(value_, 3)}"


parameters_news = {
    "q": COMPANY_NAME,
    "from": today,
    "sortBy": "polularity",
    "apiKEY": API_KEY_NEWS
}


def get_news(value_, val1, val2):
    response_news = requests.get(NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    data_news = response_news.json()
    news = data_news['articles'][0]['title']
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"{COMPANY_NAME}: {get_value(value_, val1, val2)}%\nHeadline: {news}",
        from_='twilio_number',
        to='your_number'
    )

    print(message.status)


get_news(value, open_close_list[0], open_close_list[-1])

