import base64
import yfinance as yf
from flask import Flask, render_template, jsonify
from flask_cors import cross_origin
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__)


def curve_individual_stock(ticket, *, interval='1y', index='SPY'):
    index_df = yf.Ticker(index).history(period=interval)['Close']
    stock_df = yf.Ticker(ticket).history(period=interval)['Close']
    stock_df /= index_df
    fill_val = stock_df.loc[stock_df.first_valid_index()]
    stock_df = stock_df.fillna(fill_val)
    stock_df /= stock_df.iloc[0]
    return stock_df


def png_data(df, title):
    fig = Figure()
    ax = fig.subplots()
    ax.plot(df)
    ax.axhline(y=1, c="grey")
    fig.suptitle(title)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


@app.route('/api/<ticket>/<history>', methods=['GET'])
@cross_origin(origin='*')
def handle_request(ticket, history):
  stock_df = curve_individual_stock(ticket, interval=history)
  response_data = {'src': f'data:image/png;base64,{png_data(stock_df, ticket)}'}
  return jsonify(response_data)


if __name__ == "__main__":
    app.run()