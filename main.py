import os

import pandas as pd
import pandas_datareader.data as dr
import datetime
import matplotlib.pyplot as plt
from pytrends.dailydata import get_daily_data

pd.options.display.float_format = '{:,.1f}'.format

start = datetime.datetime(2020, 11, 1)  # start date
end = datetime.datetime.now()
# end = datetime.date.today()  # end date
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


def update_csv_data(ticker):
    start = datetime.date(2010, 1, 1) #datetime.date
    end = datetime.date.today() #datetime.date
    try:
        pd.read_csv(csv, index_col=0)
    except FileNotFoundError:
        get_daily_data(ticker, start.year, start.month, end.year, end.month, geo="US", verbose=True).to_csv(csv)
    finally:
        df = pd.read_csv(csv, index_col=0) #pandas.DataFrame
        last = df.index[len(df) - 1]
        last = datetime.datetime.strptime(last, '%Y-%m-%d').date() #datetime.date
        if last != end:
            get_daily_data(ticker, last.year, last.month, end.year, end.month, geo="US", verbose=True).to_csv("temp")
            new_df = pd.read_csv("temp", index_col=0) #pandas.DataFrame
            os.remove("temp")
            new = last + datetime.timedelta(days=1)
            new = new.strftime('%Y-%m-%d')
            if new in new_df.index:
                df = df.append(new_df.loc[new:])
            # if next.toString() in
            #if there is overlap of index from df and new_df, only add the parts of new_df that does not overlap
            df.to_csv(csv)


def plot_interest_over_time():
    df = pd.read_csv(csv)
    plt.plot(df.index, df["bitcoin"])
    plt.title("Interest Over Time")
    fig = plt.gcf()
    fig.set_size_inches(20, 3)
    plt.savefig("Interest_chart")


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
    df = df[df.index < end]
    plt.plot(df.index, df["bitcoin"])
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig("BTC-USD_2")
    plt.show()


# update_csv_data("bitcoin")
# plot_interest_over_time()
interest_and_price_over_time("BTC-USD", start, end)

# stocks = ["AAPL", "AMZN", "TSLA", "NVDA", "MSFT", "LULU", "BRK-B"]
# for ticker in stocks:
#    interest_and_price_over_time(ticker, start, end)
# interest_and_price_over_time("BTC/USD", datetime.datetime(2020, 12, 1), end)
