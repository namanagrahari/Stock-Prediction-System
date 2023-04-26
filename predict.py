import yfinance as yf
from beautiful_date import *
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# pip install beautiful-date yfinance

def getData(ticket):
    ticket = ticket.upper()
    data = yf.download(ticket, 
            start=D.today() - 30*days, 
            end=D.today(), 
            progress=False)

    return data

def stock_prediction(ticket,data=None):
    # get the data 
    # print(stockData)
    if data.any():
        stockData = data
        stockData = np.array(stockData.iloc[: , -1:])
        # split the data
        trainX, trainY = np.array([stockData[n+1] for n in range(len(stockData)-2)]), stockData[2:]
        # print(trainX, trainY)
    else :
        stockData = getData(ticket)
        if type(stockData) is not tuple:
            # stockData.to_csv(f'{ticket}.csv')
            # print(stockData['Volume'][-1])
            # print(stockData.iloc[: , -1:])
            stockData = np.array(stockData.iloc[: , -1:])
            # split the data
            trainX, trainY = np.array([stockData[n+1] for n in range(len(stockData)-2)]), stockData[2:]
            # print(trainX, trainY)
        else:
            print("unable to get the data of ",ticket)
            exit()

        

    # print(stockData[0])
    # # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(6, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=20, batch_size=2, verbose=2)

    # Our prediction for tomorrow
    prediction = model.predict(np.array([stockData[0]]))
    result = 'The price will move from %s to %s' % (stockData[-1][0], prediction[0][0])
    if data.any():
        return prediction[0][0]
    
    print(result)
    return result

def stock_prediction_Server(data):
    stockData = data
    stockData = np.array(stockData.iloc[: , -1:])
    # split the data
    trainX, trainY = np.array([stockData[n+1] for n in range(len(stockData)-2)]), stockData[2:]
    # print(trainX, trainY)
    
    # print(stockData[0])
    # # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(6, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=20, batch_size=2, verbose=2)

    # Our prediction for tomorrow
    prediction = model.predict(np.array([stockData[0]]))
    # result = 'The price will move from %s to %s' % (stockData[-1][0], prediction[0][0])
    
    return prediction[0][0]


if __name__ == "__main__":
    stockName = input("Enter a stock quote from NASDAQ (e.j: AAPL, FB, GOOGL, TSLA):")
    print(stock_prediction(stockName))
    
