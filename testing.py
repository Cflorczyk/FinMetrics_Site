import pandas as pd
from datetime import date
import yfinance as yf

years = 1
end_date = date.today()
start_date = date.today() - pd.DateOffset(years=years)
ticker_id = "AAPL"


def prepare_data_stock():
    tickers = [ticker_id]
    stock_data = yf.download(tickers, start_date, end_date)
    return stock_data


def get_CAGR_stock():
    df = prepare_data_stock()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod()
    trading_days = 252
    n = len(df) / trading_days
    cagr_stock = round((df['cumulative_returns'][-1]) ** (1 / n) - 1, 3)
    return cagr_stock

print(f'%{get_CAGR_stock()*100}')