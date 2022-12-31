# Symbol lookup: https://finance.yahoo.com/lookup

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# constants
INDEX = '^GSPC' # S&P 500
INTERVAL = '20y'

def curve_individual_stock(ticket, name=''):
    index_df = yf.Ticker(INDEX).history(period=INTERVAL)['Close']
    stock_df = yf.Ticker(ticket).history(period=INTERVAL)['Close']
    stock_df /= index_df
    fill_val = stock_df.loc[stock_df.first_valid_index()]
    stock_df = stock_df.fillna(fill_val)
    stock_df /= stock_df.iloc[0]

    return stock_df, name if name else ticket


def curve_portfolio(tickets, weights, name=''):
    assert (len(tickets) == len(weights))
    assert (sum(weights) == 1)
    index_df = yf.Ticker(INDEX).history(period=INTERVAL)['Close']
    stock_df = pd.Series(np.zeros(index_df.shape[0]), index=index_df.index)  # series
    for _, (ticket, weight) in enumerate(zip(tickets, weights)):
        single_asset = yf.Ticker(ticket).history(period=INTERVAL)['Close'].mul(weight)  # series
        stock_df += single_asset
    stock_df /= index_df
    fill_val = stock_df.loc[stock_df.first_valid_index()]
    stock_df = stock_df.fillna(fill_val)
    stock_df /= stock_df.iloc[0]

    return stock_df, name if name else tickets[0]


def plot_curves(curves, title='', output_path='./output/demo_output.png'):
    fig, ax = plt.subplots(figsize=(12, 8))
    for df, label in curves:
        ax.plot(df, label=label)
    plt.axhline(y=1, color='grey')
    plt.title(title)
    plt.legend()
    fig.savefig(output_path)


def demo():
    curves = []
    curves.append(curve_individual_stock('GOOG'))
    curves.append(curve_portfolio(['UPRO', 'TMF'], [0.55, 0.45], 'Hedgefundie\'s Excellent Adventure'))
    plot_curves(curves, title=f"Demo INDEX={INDEX}")

if __name__ == "__main__":
    demo()
