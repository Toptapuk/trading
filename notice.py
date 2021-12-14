import yfinance as yf
import tkinter as tk
from tkinter import ttk
import time


stock_symbol = 'U.BK'
data = yf.download(tickers= stock_symbol, period= '1d', interval= '1m',progress=False)

NORM_FONT = ('Verdana', 12)

def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()
    
    popup.wm_title("!")
    popup.geometry("500x200")
    label = ttk.Label(popup, text = msg, font = NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup, text='Okay', command= leavemini)
    B1.pack()
    popup.mainloop()
print('Running')
while True:
    data = yf.download(tickers= stock_symbol, period= '1d', interval= '1m',progress=False)
    try:
        print(str(data['Adj Close'].iloc[-1])+' '+str(data.index[-1]))

        time.sleep(60)
        if data['Adj Close'].iloc[-1] >= 2.27 or data['Adj Close'].iloc[-1] < 2.06:
            popupmsg('SELL IT!!')
            break
    except KeyboardInterrupt:
        break