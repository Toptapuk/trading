import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, ssl

path = "https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=SET&type=S&language=en&country=TH"
SET_raw = pd.read_html(path)

SET = SET_raw[1].append(SET_raw[2])
for i in range(3,len(SET_raw)):
    SET = SET.append(SET_raw[i])

final_data = pd.DataFrame()
final_data['symbols'] = SET['Symbol']
path = "https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=mai&type=&language=en&country=TH"
MAI_raw = pd.read_html(path)
MAI = MAI_raw[1].append(MAI_raw[2])
for i in range(3,len(MAI_raw)):
    MAI = MAI.append(MAI_raw[i])
NMAI = pd.DataFrame()
NMAI['symbols'] = MAI['Symbol']

final_data = final_data.append(NMAI)
final_data.sort_values('symbols', inplace= True)
final_data.reset_index(drop= True, inplace = True)
final_data['symbols'] = final_data['symbols'].astype(str)+'.BK'
final_data

os.chdir('D:\TWorks\Trade') #change it to your work directory

final_data.to_csv('stock_symbols.csv',encoding="TIS-620")