#!/usr/bin/env python
# coding: utf-8

# In[76]:


import numpy as np
import pandas as pd


# In[77]:


#First load in the file, got to give it column titles as the data didnt have any
title_list = ["bloomberg_code", "unused", "bid_price", "ask_price", "trade_price", "bid_volume", "ask_volume", "trade_volume", "Update Type", "unused1" , "Date", "Time_secs_past_mid", "opening_price", "unused2", "condition_codes", "unused3"]
scandi_df = pd.read_csv(r"..\Python - Stock Data Analysis\scandi.csv", header = None)
#always good to have a quick look to understand whats going on
#scandi_df.head()


# In[78]:


scandi_df.columns = title_list
#scandi_df


# In[79]:


#from the spec only some of the columns have no labels or represent nothing of interest. So remove them
del scandi_df["unused"]
del scandi_df["unused1"]
del scandi_df["unused2"]
del scandi_df["unused3"]


# In[80]:


#just looking to see if this is comparible with the opening time for the swedish market which is about 9-5.30
#scandi_df["Time_secs_past_mid"].min()


# In[81]:


# the requirements state that only null and XT condition codes are required, so lets filter them out 
xt_df = scandi_df[scandi_df['condition_codes'] == "XT"]
nan_df = scandi_df[scandi_df['condition_codes'].isna()]
filt_df = pd.concat([xt_df, nan_df])


# In[82]:


#exclude auctions (remove cross spreads) - where the bid price is larger than the ask price
filt_df = filt_df[filt_df['ask_price'] >= filt_df['bid_price']]


# In[83]:


#just looking at the number of unique indentifiers
code_list = filt_df['bloomberg_code'].unique()


# In[84]:


#filtered based on 1 being a trade - 2 and 3 where only updates
filt_df = filt_df[filt_df['Update Type'] == 1]


# In[85]:


#function for checking the end of the price being a 0, required a seperate function as its a float, returns a % bias i.e 50% means half the numbers were round numbers
def zero_end_float(y):
    total = y.size
    zero_count = 0
    for i in y:
        x = ('{:.2f}'.format(i)).endswith('0')
        if x == True:
            zero_count+=1
            
    round_num_bias_price = (round(((zero_count/total)*100), 2))
    return round_num_bias_price


# In[86]:


#function for checking if the end of the trade volume being a zero, returns % bias, i.e 50% means half the numbers were round numbers
def zero_end_whole(y):
    total = y.size
    zero_count = 0
    for i in y:
        x = str(i).endswith('0')
        if x == True:
            zero_count+=1
            
    round_num_bias_volume = (round(((zero_count/total)*100), 2))
    return round_num_bias_volume


# In[87]:


def tickdata(df):
    ticktemp = df['trade_price'].diff()
    timetemp = df['Time_secs_past_mid']
    df1 = pd.DataFrame({'tickch': ticktemp, 'time': timetemp})
    df1.fillna(0, inplace=True)
    df1 = df1[(df1[['tickch']] != 0).all(axis=1)]
    tickchange = df1['time'].diff()
    return tickchange


# In[88]:


results_titles = ["Stock ID", "Mean Time between Trades (s)", "Median Time between trades (s)", "Longest Time between Trades (s)", "Mean Time between Tick Changes (s)", "Median Time between Tick Changes (s)", "Longest Time between Tick Changes (s)", "Mean Bid Ask Spread (£)", "Median Bid Ask Spread (£)", "Round Number Bias Trade Price (%)", "Round Number Bias Trade Volume (%)"]
Results = pd.DataFrame(columns=results_titles)
#now lets have a look at the removing the gaps in time everyday and therefore not skew figures
#we will do this by having a look at one of the stocks, will it be when the trade volume is 0 or a time period e.g. 9 - 5
#so checking for 0 trade volume returns no values, even if the you do it on the orginal data frame!
for i in range(len(code_list)):
    tempdf = filt_df[filt_df['bloomberg_code'] == code_list[i]]
    #for time data
    temp = tempdf['Time_secs_past_mid'].diff()
    temp.fillna(0, inplace=True)
    temp[temp< 0] = 0
    #for bid ask data
    bastemp = tempdf["ask_price"] - tempdf["bid_price"]
    #for tick changes
    tickchange = tickdata(tempdf)
    #for round number bias
    tp = tempdf['trade_price']
    tv = tempdf['trade_volume']
    price0 = zero_end_float(tp)
    volume0 = zero_end_whole(tv)
    #return the data
    data = [{'Stock ID' : code_list[i], 'Mean Time between Trades (s)': round(temp.mean(),2),'Median Time between trades (s)': round(temp.median(),2),'Longest Time between Trades (s)': round(temp.max(),2),'Mean Time between Tick Changes (s)':  round(tickchange.mean(),2), 'Median Time between Tick Changes (s)': round(tickchange.median(),2), 'Longest Time between Tick Changes (s)':round(tickchange.max(),2), 'Mean Bid Ask Spread (£)': round(bastemp.mean(),2), 'Median Bid Ask Spread (£)': round(bastemp.median(),2), "Round Number Bias Trade Price (%)" : price0, "Round Number Bias Trade Volume (%)": volume0}]    
    #print(data)
    Results = Results.append(data,sort=False, ignore_index = True)


# In[89]:


#check the dataframe
print(Results)


# In[90]:


Results.to_csv(r"..\Python - Stock Data Analysis\results_report.csv", index = False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




