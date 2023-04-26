import numpy as np
import datetime
from flask import Flask, render_template
from flask import request, redirect
from pathlib import Path
import yfinance as yf
from beautiful_date import *
from predict import getData, stock_prediction_Server

app = Flask(__name__)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route("/")
def first_page():
    return render_template("index.html")


@app.route("/predict", methods=["post"])
def predictOnPost():
    stockName = request.form['data'].upper()
    # print(stockName)

    stockData = getData(stockName)
    # print(stockData.index)
    # print(list(stockData['Volume']))
    # print([int(i) for i in list(stockData.index)])
    # return render_template("errorPage.html", stockName=stockName)

    if stockData.shape[0]:
        # send to page with the data on it
        result = stock_prediction_Server(stockData)
        return render_template("result.html", 
            dates ={'start':D.today() - 30*days,
                    'end': D.today() }, 
            GraphData={
                'x': list(stockData['Volume']), 
                'y': [datetime.datetime.strptime(str(i).split(' ')[0], "%Y-%m-%d").timestamp() for i in list(stockData.index)]},
            prediction=result,
            stockName=stockName
        )
    else:
        # show the render page with not correct name error
        return render_template("errorPage.html", stockName=stockName)



'''
if __name__ == "__main__":
    main()
'''

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
