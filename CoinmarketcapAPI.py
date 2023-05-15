#!/usr/bin/env python
# coding: utf-8

# In[10]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


    
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
     'start':'1',
    'limit':'15',
     'convert':'USD'
  }
headers = {
 'Accepts': 'application/json',
 'X-CMC_PRO_API_KEY': 'f784b299-dc57-44b5-8815-25b1d4132444',
  }

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[3]:


import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[8]:


df=pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now', utc=True)

df


# In[11]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os

def api_runner():
    global df
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
         'start':'1',
        'limit':'15',
         'convert':'USD'
      }
    headers = {
     'Accepts': 'application/json',
     'X-CMC_PRO_API_KEY': 'f784b299-dc57-44b5-8815-25b1d4132444',
      }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
 # I had to go in and put jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10
 #in the anaconda prompt to allow this to pull data
    
#This appends to a dataframe
df=pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now', utc=True)
df

#this appends to a csv files
if not os.path.isfile(r'C:\Users\aklas\Documents\ApiCsv\API.csv'):
    df.to_csv(r'C:\Users\aklas\Documents\ApiCsv\API.csv', header = 'column_names')
else:
    df.to_csv(r'C:\Users\aklas\Documents\ApiCsv\API.csv', mode='a', header=False)


# In[31]:


import os
from time import time
from time import sleep

for i in range(333):
    api_runner()
    print('API Runner completed')
    sleep(60) #Sleep for 1 minute
exit()


# In[32]:


df72=pd.read_csv(r'C:\Users\aklas\Documents\ApiCsv\API.csv')
df72


# In[33]:


# make it easier to read circulating supply and others
pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[15]:


df


# In[34]:


#group by Name and Percent changes
df3=df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3


# In[16]:


df4= df3.stack()
df4


# In[35]:


# converts df4 from a series to a dataframe
df5=df4.to_frame(name='values')
df5


# In[36]:


#Counts how many values there are which is 90
# df5.count()

#creats an index
index=pd.Index(range(90))
df6=df5.reset_index()
df6


# In[37]:


#rename column
df7=df6.rename(columns={'level_1':'percent_change'})
df7


# In[38]:


#change the titles of each item in percent_change
df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'],['1h','24h','7d','30d','60d','90d'])
df7


# In[20]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[39]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# In[42]:


df10= df[['name','quote.USD.price','timestamp']]
df10.query("name == 'Bitcoin'")


# In[43]:


# line graph that would show bitcoin on a line chart over time. bases off how many loops were ran from above
sns.lineplot(x='timestamp', y='quote.USD.price', data=df10)


# In[ ]:




