import numpy as np
import pandas as pd
import os, ssl
import datetime
import os.path
from time import sleep
from tqdm import tqdm

time_now  = datetime.date.today()
time_now.strftime('%Y-%m-%d')
filename = str(time_now)+'_holder'+'.csv'

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

path = "https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=SET&type=S&language=en&country=TH"
SET_raw = pd.read_html(path)

SET = SET_raw[1].append(SET_raw[2])
for i in range(3,len(SET_raw)):
    SET = SET.append(SET_raw[i])

path = "https://marketdata.set.or.th/mkt/commonstocklistresult.do?market=mai&type=&language=en&country=TH"
MAI_raw = pd.read_html(path)
MAI = MAI_raw[1].append(MAI_raw[2])
for i in range(3,len(MAI_raw)):
    MAI = MAI.append(MAI_raw[i])

SET_member = []
for row in range(len(SET.index)):
    SET_member.append(SET.iloc[row,0])


# Gathering stocks member in MAI
MAI_member = []
for row in range(len(MAI.index)):
    MAI_member.append(MAI.iloc  [row,0])  
    
# Combine all member of SET+MAI
ALL_member = SET_member + MAI_member
ALL_member.sort()

shareholder_df = pd.DataFrame()
someProblems = []
count = 0 


if os.path.isfile(filename):
    shareholder_df = pd.read_csv(filename) 
    # print(shareholder_df.head())
    print('Import list Done!!')
else:
    for each in tqdm(ALL_member):  
        try:
            if each=='F&D':
                path = 'https://www.set.or.th/set/companyholder.do?symbol=F%26D&ssoPageId=6&language=en&country=US'
            elif each=='L&E':
                path = 'https://www.set.or.th/set/companyholder.do?symbol=L%26E&ssoPageId=6&language=en&country=US'
            elif each=='S & J':
                path = 'https://www.set.or.th/set/companyholder.do?symbol=S+%26+J&ssoPageId=6&language=en&country=US'
            else:
                path = 'https://www.set.or.th/set/companyholder.do?symbol=%s&ssoPageId=6&language=en&country=US' % each
            df = pd.read_html(path, encoding='utf-8')
            df = df[2]
            df.drop(columns=['Rank'], inplace=True)
            df['Stocks'] = each
            shareholder_df = pd.concat([shareholder_df, df], ignore_index=True)
            # print(count)
            count += 1
        except IndexError:
            someProblems.append(each)
            pass
    shareholder_df.to_csv(filename)

    print('Import list: Done!!')
    # print(shareholder_df.head())
    
shareholder_df.dropna(inplace=True)
shareholder_df.rename(index=str, columns={'Major Shareholders':'source','Stocks':'target','% Shares':'weight'}, inplace=True)
shareholder_df['weight'] = shareholder_df['weight'].astype('float16')
shareholder_df.drop(columns=['# Shares'], inplace=True)
shareholder_df.sort_values(by=['weight'], ascending=False, inplace=True)
shareholder_df.reset_index(drop=True, inplace=True)
pd.set_option('display.expand_frame_repr', False)
while True:
    choice = int(input('Select your search mode: Type 1 = Shared_key 2 = Target Symbols CTRL+C: Exist:'))
    try:
        if choice == 1:
            filter = []
            fil_name = str(input('Enter the keyword:'))
            for i in range(len(shareholder_df.index)):
                name = shareholder_df.iloc[i,1]
                if fil_name.upper() in name:
                    
                    filter.append(shareholder_df.iloc[i,1])
                else:
                    filter.append(np.nan)
            filtered = shareholder_df.copy()
            filtered['Major Shareholders'] = filter
            filtered.dropna(inplace=True)
            filtered.drop(columns=['source'], inplace=True)
            filtered.drop(columns=['Unnamed: 0'], inplace=True)
            filtered.rename(index=str, columns={'Major Shareholders':'source','Stocks':'target','% Shares':'weight'}, inplace=True)
            filtered.drop_duplicates(subset='target',keep = 'first', inplace = True)
            print(filtered, len(filtered))
        elif choice == 2:
            target_name = str(input('Enter the target symbol:'))
            print(shareholder_df.loc[shareholder_df['target'] == target_name.upper()])
        else:
            print('Please enter the keywords')

    except KeyboardInterrupt:
        break