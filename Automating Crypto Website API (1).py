#!/usr/bin/env python
# coding: utf-8

# # Automating Crypto Website API

# **------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**

# **SETTING UP THE API**

# jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10

# In[90]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'INPUT YOUR KEY HERE!'   #Here you input your key!
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  


# In[91]:


type(data)


# In[92]:


import pandas as pd

pd.json_normalize(data['status'])


# In[93]:


#This allows you to see all the columns, not just like 15

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

pd.json_normalize(data['data'])



# In[94]:


#This normalizes the data and makes it all pretty in a dataframe

df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# **------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**

# **AUTOMATING THE DATA PULL**

# This version of code writes down the new values on a different csv file.

# In[6]:


import os 
from time import time
from time import sleep
import json
import pandas as pd
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# Inicializa el contador
file_counter = 1

def api_runner():
    global df
    global file_counter  # Accede a la variable global file_counter
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' 
    parameters = {
      'start':'1',
      'limit':'100',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'INPUT YOUR KEY HERE!'  #Here you input your key!'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

#NOTE:
# I had to go in and put "jupyter notebook --NotebookApp.iopub_data_rate_limit=1e10"
# Into the Anaconda Prompt to change this to allow to pull data        
        
        
        
    new_df = pd.json_normalize(data['data'])
    new_df['timestamp'] = pd.to_datetime('now')
    
    # Create a csv and append data to it, if you want to overwrite, dont use this  part of code and eliminate file_counter
    
    filename = fr'C:\Users\user\Desktop\Programacion\Portfolio Projects\Python Crypto API\Crypto_API_Data_{file_counter}.csv'

    new_df.to_csv(filename, index=False)
    
    # Incrementa el contador para el siguiente archivo
    file_counter += 1

# Main loop
for i in range(333):
    start_time = time()  # Record start time
    api_runner()
    print('API Runner completed')
    elapsed_time = time() - start_time
    remaining_time = max(0, 60 - elapsed_time)  # Ensure at least 1 minute gap
    sleep(remaining_time)  # Sleep for the remaining time in the minute

exit()


# This version of code writes down the new values under the previous data, reseting its index.

# In[11]:


import os
import time
import pandas as pd
import requests

# Function to get API data
def fetch_api_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '100',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'INPUT YOUR KEY HERE!'   #Here you input your key!'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        response.raise_for_status()
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects, requests.exceptions.HTTPError) as e:
        print(f"Error: {str(e)}")
        return None
    return data

# Function to save data to CSV

def save_data_to_csv(data):
    if not data:
        return

    df = pd.json_normalize(data['data'])
    df['Timestamp'] = pd.to_datetime('now')

    filename = 'C:\\Users\\user\\Desktop\\Programacion\\Portfolio Projects\\Python Crypto API\\Crypto_API_Data.csv'

    if os.path.isfile(filename):
        # Append new data to the existing file
        existing_df = pd.read_csv(filename)
        new_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        # Save new data to a new file
        new_df = df

    new_df.to_csv(filename, index=False)

# Main function
def main():
    iterations = 333  # Move the number of iterations to a configuration file
    interval_time = 60  # Interval time in seconds

    for i in range(iterations):
        start_time = time.time()
        data = fetch_api_data()
        if data:
            save_data_to_csv(data)
            print('API Runner completed')

        elapsed_time = time.time() - start_time
        remaining_time = max(0, interval_time - elapsed_time)
        time.sleep(remaining_time)

if __name__ == "__main__":
    main()


# In[99]:


dfN = pd.read_csv(fr'C:\Users\user\Desktop\Programacion\Portfolio Projects\Python Crypto API\Crypto_API_Data.csv')
dfN


# **------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**

# **TRANSFORMING DATA**

# Add scientific notation:

# In[88]:


pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[89]:


df


# Coin trends over time:

# In[71]:


df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d']].mean()
df3


# Stack rows on each crypto:

# In[72]:


df4 = df3.stack()
df4


# In[73]:


type(df4)


# Turn it back to a DataFrame:

# In[74]:


df5 = df4.to_frame(name='values')
df5


# In[75]:


df5.count()


# Set a index:

# In[76]:


index = pd.Index(range(600))

# Set the above DataFrame index object as the index

# using set_index() function
df6 = df5.set_index(index)
df6

# If it only has the index and values try doing reset_index like "df5.reset_index()"
df5.reset_index()


# Rename columns and Set Index:

# In[77]:


# Resetting index
df5_reset = df5.reset_index()

# Creating a new index
new_index = pd.Index(range(600))

# Setting the new index
df6 = df5_reset.set_index(new_index)

# Renaming columns
df7 = df6.rename(columns={'level_1': 'percent_change'})

# Now df7 should have the renamed columns
df7


# Replace percent_change value names:

# In[95]:


df7['percent_change'] = df7['percent_change'].replace({
    'quote.USD.percent_change_1h': '1h',
    'quote.USD.percent_change_24h': '24h',
    'quote.USD.percent_change_7d': '7d',
    'quote.USD.percent_change_30d': '30d',
    'quote.USD.percent_change_60d': '60d',
    'quote.USD.percent_change_90d': '90d'
})

df7


# **------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**

# **VISUALIZING DATA**

# In[79]:


import seaborn as sns
import matplotlib.pyplot as plt


# Coins percent change:

# In[80]:


sns.catplot(x='percent_change', y='values', hue='name', data=df7, kind='point')


# 15 coins with more percent change:

# In[97]:


# Group the data by the 'name' column
grouped = df7.groupby('name')

# Calculate the sum of the 'values' column for each group
sum_values = grouped['values'].agg('sum')

# Select the 15 largest groups based on the sum of the 'values' column
important_groups = sum_values.nlargest(15).index

# Filter the data to only include the rows from the important groups
df_important = df7[df7['name'].isin(important_groups)]

# Create the point plot using the filtered data
sns.catplot(x='percent_change', y='values', hue='name', data=df_important, kind='point')


# Bitcoin values:

# In[100]:


df10 = dfN[['name','quote.USD.price','Timestamp']]
df10 = df10.query("name == 'Bitcoin'")
df10


# In[102]:


sns.set_theme(style="darkgrid")

sns.lineplot(x='Timestamp', y='quote.USD.price', data = df10)


# In[ ]:




