import yfinance as yf
import time
import datetime

symbol = input('Symbol:')
periods = input('Enter the period: (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max):')
intervals = input('Enter the interval: (1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo):')
# time_stamp = datetime.datetime.now()
time_stamp = input('Enter starting date: Y-M-D, ex: 2021-08-01'+' ')
# time_stamp = time_stamp.strftime('%Y-%m-%d')

try:
    while True:
        data = yf.download(tickers= str(symbol), start=str(time_stamp), period= str(periods), interval= str(intervals)) #start='2021-08-01'
        
        data['MA20'] = data['Close'].rolling(20).mean()
        data['MA50'] = data['Close'].rolling(50).mean()
        # data['MA100'] = data['Close'].rolling(100).mean()
        # data['MA200'] = data['Close'].rolling(200).mean()

        data.to_csv('stock data.csv', mode = 'w', header=True)

        print('Running...')

        time.sleep(1)

except KeyboardInterrupt:
    pass