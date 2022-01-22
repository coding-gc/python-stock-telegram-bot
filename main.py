"""Stock trading news notification
   Collects price of a stock and latest news about the stock and sends collected message to a Telegram group.
"""
import requests
import urllib.parse

stock_dict = {
    #StockID : #Stock name
    "VOO" : "Vanguard S&P 500 ETF",
    "SPY" : "SPDR S&P 500 ETF Trust"
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TELEGRAM_ENDPOINT = "https://api.telegram.org/bot"

STOCKS_API = "<Your API KEY>"
NEWS_API = "<Your API KEY>"
TELEGRAM_API = "<Your API KEY>"
TELEGRAM_GROUP = "<Your API KEY>"

def get_stock_value(STOCK_NAME, STOCKS_API, STOCK_ENDPOINT):
    
    parameters = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : STOCK_NAME,
        "apikey" : STOCKS_API

    }
    r = requests.get(url=STOCK_ENDPOINT, params=parameters)
    data = r.json()
    return data

def get_stock_news(COMPANY_NAME, NEWS_API, NEWS_ENDPOINT):
    parameters = {
        "q" : COMPANY_NAME,
        # "from" : "2022-01-01",
        "sortBy" : "publishedAt",
        "language" : "en",
        "apiKey" : NEWS_API

    }
    n = requests.get(url=NEWS_ENDPOINT, params=parameters)
    data_n = n.json()
    return data_n

def telegram_message(TELEGRAM_API, TELEGRAM_GROUP, UnMessage):
    url = TELEGRAM_ENDPOINT +TELEGRAM_API+ "/sendMessage?chat_id=" +str(TELEGRAM_GROUP)+ "&text=" +UnMessage
   
    response = requests.request("POST", url)
    print(response)

def prepare_message(STOCK_NAME, STOCKS_API, COMPANY_NAME, NEWS_API):
    data = get_stock_value(STOCK_NAME, STOCKS_API, STOCK_ENDPOINT)
    YESTERDAY = list(data["Time Series (Daily)"])[1]
    DAY_B_YESTERDAY = list(data["Time Series (Daily)"])[2]

    YESTERDAY_CLOSE = data["Time Series (Daily)"][YESTERDAY]["4. close"]
    DAY_B_YESTERDAY = data["Time Series (Daily)"][DAY_B_YESTERDAY]["4. close"]

    Diff = float(YESTERDAY_CLOSE) - float(DAY_B_YESTERDAY)

    if Diff >= 0:
        symbol = "🔺"
    else:
        symbol = "🔻"

    Percentage = round((abs(float(YESTERDAY_CLOSE) - float(DAY_B_YESTERDAY)) / float(DAY_B_YESTERDAY)) * 100.0)

    data_n = get_stock_news(COMPANY_NAME, NEWS_API, NEWS_ENDPOINT)
    news_title = data_n["articles"][0]["title"]
    news_description = data_n["articles"][0]["description"]
    news_url = data_n["articles"][0]["url"]

    Message = f"{STOCK_NAME}: {symbol} {Percentage}% \nHeadline: {news_title} \nBreif: {news_description} \nurl: {news_url}"
    UnMessage = urllib.parse.quote(Message)
    return UnMessage

if __name__ == "__main__":
    for STOCK_NAME,COMPANY_NAME in stock_dict.items():
        print(STOCK_NAME)
        UnMessage = prepare_message(STOCK_NAME, STOCKS_API, COMPANY_NAME, NEWS_API)
        telegram_message(TELEGRAM_API, TELEGRAM_GROUP, UnMessage)
