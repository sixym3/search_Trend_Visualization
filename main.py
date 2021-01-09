import os

import pandas as pd
import pandas_datareader.data as dr
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from pytrends.dailydata import get_daily_data

pd.options.display.float_format = '{:,.1f}'.format

start = datetime.datetime(2016, 1, 1)  # start date
end = datetime.date.today()  # end date
csv = "data_10year"


# db = pd.DataFrame(np.array([["BTC-USD", "bitcoin"]]), columns=["trading sign", "search terms"])
# db.set_index("trading sign")
# print(db)
# sign = "BTC-USD"

def ticker_vs_time(ticker, start, end):
    stock = dr.DataReader(ticker, "yahoo", start, end)  # get stock data_10year
    plt.plot(stock.index, stock["Adj Close"])
    plt.title(ticker)
    fig = plt.gcf()
    fig.set_size_inches(20, 3)
    plt.show()

def update_interest_over_time(ticker, start, end):
    try:
        pd.read_csv(csv, index_col=0)
    except FileNotFoundError:
        get_daily_data(ticker, start.year, start.month, end.year, end.month, geo="US", verbose=True).to_csv(csv)
    finally:
        df = pd.read_csv(csv, index_col=0)
        last = df.index[len(df) - 1]
        last = datetime.datetime.strptime(last, '%Y-%m-%d').date()
        if last != end:
            get_daily_data(ticker, last.year, last.month, end.year, end.month, geo="US", verbose=True).to_csv("temp")
            new_df = pd.read_csv("temp", index_col=0)
            os.remove("temp")
            df = df.append(new_df)
            df.to_csv(csv)

    # define a different start date for update function


def plot_interest_over_time(ticker, start, end):
    df = pd.read_csv(csv)
    # print(len(df))
    plt.plot(df.index, df["bitcoin"])
    plt.title("Interest Over Time")
    fig = plt.gcf()
    fig.set_size_inches(20, 3)
    plt.savefig("Interest_chart")

    """
    
    pytrend = Trendreq()
    pytrend.build_payload(kw_list=[ticker], # len(kw_list) <= 5
                          timeframe=start.strftime("%Y-%m-%d")+" "+end.strftime("%Y-%m-%d"),
                          geo = 'US')
    interest_over_time_df = pytrend.interest_over_time()
    plt.plot(interest_over_time_df.index, interest_over_time_df[ticker])
    """


def interest_and_price_over_time(ticker, start, end):
    fig, ax1 = plt.subplots()
    fig.set_size_inches(20, 4)
    plt.title(ticker)
    # plot stock price
    stock = dr.DataReader(ticker, "yahoo", start, end)  # get stock data_10year
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Bitcoin Price', color=color)
    ax1.plot(stock.index, stock["Adj Close"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    # plot Google trends index on the twin y axis
    df = pd.read_csv(csv, index_col=0)
    color = 'tab:blue'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-a
    ax2.set_ylabel('Google Trends Index', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    df.index = df.index.astype('datetime64[ns]')
    df = df[df.index > start]
    plt.plot(df.index, df["bitcoin"])
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig("BTC-USD")


# plot_interest_over_time("BTC/USD", start, end)
update_interest_over_time("bitcoin", start, end)
# plot_interest_over_time("BTC-USD", start, end)

interest_and_price_over_time("BTC-USD", start, end)

# stocks = ["AAPL", "AMZN", "TSLA", "NVDA", "MSFT", "LULU", "BRK-B"]

# for ticker in stocks:
#    interest_and_price_over_time(ticker, start, end)

# interest_and_price_over_time("BTC/USD", datetime.datetime(2020, 12, 1), end)
