import numpy as np #Numpy is the main mathematics library used in Python (Array's, mathematical operations, random number generators, etc.)
import pandas as pd #Pandas is the main matrix operations library used in python (You can use this to read in files)
import os #Provides a way of using operating system dependent functionality. (Setting the working directory)
import matplotlib.pyplot as plt
import datetime

#Collect data from FRED
#Please go to FRED and replace my key with your key
#pip install fredapi
from fredapi import Fred
fred = Fred(api_key='d35fa924f1f9c72ef0bde2926305ec53')
data = fred.get_series('SP500')

#Simple plot
data.plot(grid=True)
#More complex plot#
#Works generically for all vectors
fig, axs = plt.subplots(1, 1)
axs.plot(data.index.values, data.values)
axs.set_xlabel('Time')
axs.set_ylabel('Price')
plt.title('S&P 500 Price Data from FRED')
axs.grid(True)
plt.show()

#Collect multiple data sets from fred and store them in a list
data = [fred.get_series(x) for x in ['A191RL1Q225SBEA','CPIAUCSL','UNRATE','USREC','DGS10']]
#Convert the CPI index into a percent change
data[1] = data[1].pct_change(periods = 12)*100
#Interest Rates are Daily we need to convert them to Monthly 
data[4] = data[4].resample('M',convention = 'start').last()
data[4].index = data[4].index + pd.offsets.MonthBegin(1)
#Turn the list into a data frame, stick each dataset as a column (axis =1)
macro_data = pd.concat(data,axis = 1) 
#remove missing values
macro_data.dropna(inplace = True)
#Change the column names
macro_data.columns = ['realGdp','cpi','unrate','recession','tenYearRate']
print(macro_data.tail())
#We can generate a plot for all of our data as follows:
macro_data.plot(grid = True)
#We can apply functions to all columns:
#Average values of macro data during recession
macro_data[macro_data['recession'] == 1].apply(np.mean)
#Average values of macro data during expansion
macro_data[macro_data['recession'] == 0].apply(np.mean)


#Access World Bank Data
#pip install wbdata
import wbdata
#We can search for keys as follows:
wbdata.search_indicators("unemployment")
data_date = (datetime.datetime(1950, 1, 1), datetime.datetime(2019, 2, 10))
unemployment_data = wbdata.get_data("UNEMPSA_",data_date=data_date)
country_data = pd.DataFrame(unemployment_data)

#Access data from quandl
#pip install quandl
import quandl
#Please replace my key with your key
quandl.api_config.ApiConfig.api_key =  '1zm1xSnnoqFeAGksg3S1'
oil_prices = quandl.get("OPEC/ORB")
oil_prices.plot(grid=True,title = 'OPEC Reference Basket')


## IEX exchange (A simple API)
import requests
import io
url = 'https://api.iextrading.com/1.0/stock/aapl/chart/date/20190129'
s=requests.get(url).content
values = pd.read_json(io.StringIO(s.decode('utf-8')))
values.head()


#Get SP500 companies from Wikipedia
df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = df[1]

print(df.columns.values)
df.columns = df.iloc[0]
print(df.columns.values)
df.drop([0],inplace = True)
print(df.head())

#Read HTML Lists
#pip install beautifulsoup4
from bs4 import BeautifulSoup
url = 'https://en.wikipedia.org/wiki/List_of_mental_disorders'
s = requests.get(url)
b = BeautifulSoup(s.text, 'lxml')
#create an empty list where those list objects
main_disorders = []

# grab all of the li tags and store the text
for i in b.find_all(name = 'li'):
    main_disorders.append(i.text)
#Subset out the ones we care about
main_disorders = main_disorders[26:216]

### Collect Wikipedia Page Views

#https://en.wikipedia.org/wiki/Wikipedia:Pageview_statistics#Pageviews_Analysis

#https://tools.wmflabs.org/pageviews/?project=en.wikipedia.org&platform=all-access&agent=user&range=latest-20&pages=Cat|Dog

import json
all_urls = ['https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/' + x + '/daily/2010010100/2019020900' for x in main_disorders]

url = all_urls[0]
s=requests.get(url).content
json_string = s.decode('utf-8').replace("'", "\"")
d = json.loads(json_string)
values = pd.DataFrame.from_dict(d['items'])
values.head()

#Clean up the dates
dates = values['timestamp'].values
dates = [x[0:8] for x in dates]
values['timestamp'] = dates
values['timestamp'] = pd.to_datetime(values['timestamp'],format = '%Y%m%d')
values.set_index('timestamp', inplace=True)

values['views'].plot(grid = True,title = 'Acute Stress Disorder')

#Collect all data 
    #This code has been ran and the results are stored in the csv file below
#time package will be used to sleep
#import time
#hold_all_data = []
#for i in range(len(all_urls)):
#    try:
#        url = all_urls[i]
#        s=requests.get(url).content
#        json_string = s.decode('utf-8').replace("'", "\"")
#        d = json.loads(json_string)
#        values = pd.DataFrame.from_dict(d['items'])
#        values.head()
#        
#        #Clean up the dates
#        dates = values['timestamp'].values
#        dates = [x[0:8] for x in dates]
#        values['timestamp'] = dates
#        values['timestamp'] = pd.to_datetime(values['timestamp'],format = '%Y%m%d')
#        values.set_index('timestamp', inplace=True)
#        hold_all_data.append(values)
#    except:
#        print('---No Results for Iteration ' + str(i) + '--- :(')
#        pass
#    time.sleep(np.random.uniform(1,8,1)[0])
#    print(np.round(i/len(all_urls),2))
#                
#all_disability_page_views = pd.concat(hold_all_data)
#all_disability_page_views.to_csv('all_disability_page_views.csv')

#Load in the saved dataset
all_disability_page_views = pd.read_csv('all_disability_page_views.csv')
#Convert the dates into a date format
all_disability_page_views['timestamp'] = pd.to_datetime(all_disability_page_views['timestamp'],format = '%Y-%m-%d')

#pick a disorder index and plot out the results
ind = 54
plt_disorder = main_disorders[ind].replace(' ','_')
sub = all_disability_page_views[all_disability_page_views['article'] ==  plt_disorder]
fig, axs = plt.subplots(1, 1)
axs.plot(sub.timestamp.values, sub.views.values)
axs.set_xlabel('Time')
axs.set_ylabel('Page Views')
plt.title(main_disorders[ind])
axs.grid(True)
plt.show()



