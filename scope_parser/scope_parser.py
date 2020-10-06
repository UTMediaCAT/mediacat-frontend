#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# read the csv "test_demo.csv" can be replace with
# any other filename you want to input
df = pd.read_csv("test_demo.csv")

# create a new column named "UniqueID" from
# 1,2,3,4,5,...to n(n is # of rows we have)
# UniqueID is using to link the Source and Associate Twitter Handle,
# which should create by system
# usually it is used by system only
df.insert(0, "UniqueID", range(1, len(df) + 1), True)

# showing the csv
df


# In[3]:


# to find every non-empty Associate Twitter Handle's rows's index
# and store into not_null_twitter
# for example if row 0 exist associate twitter handle,
# then it will be stored in not_null_twitter
not_null_twitter = df.loc[pd.notna(df["Associated Twitter Handle"]), :].index

# create new rows for every Associate Twitter Handle,
# in this case source will be the old assciated twitter handle
# Type to be "Twitter Handle", UniqueID, Tags and Name will keep same.
new_df_to_add_twitter = pd.DataFrame({'UniqueID': df.iloc[not_null_twitter, 0],  # nopep8
                              'Source': df.iloc[not_null_twitter, 5],  # nopep8
                              "RSS feed URLs (where available)": np.nan,  # nopep8
                              'Type': "Twitter Handle",  # nopep8
                              'Tags': df.iloc[not_null_twitter, 4],  # nopep8
                              'Associated Twitter Handle': np.nan,
                              'Associated Publisher': np.nan,  # nopep8
                              'Name': df.iloc[not_null_twitter, 7],  # nopep8
                              'Text aliases': np.nan})

# since some of associated twitter Handle will be 2 or 3,
# so it use "|" to split
# and make every twitter handle as a new record
new_df_to_add_twitter["Source"] = new_df_to_add_twitter["Source"].str.split("|")  # nopep8
new_df_to_add_twitter = new_df_to_add_twitter.explode("Source")
new_df_to_add_twitter


# In[4]:


# add the new rows into the origin dataframe and sorted by UniqueID
df = df.append(new_df_to_add_twitter)
df = df.sort_values(by=['UniqueID'])
df = df.reset_index()
df.drop(['index'], axis=1, inplace=True)
df


# In[5]:


Object = [x for _, x in df.groupby('Type')]
Object[0]


# In[6]:


Object[1]


# In[7]:


print('l1')
print(Object[1].iloc[0, ])
print('l2')
print(Object[1].iloc[1, ])
print('l3')
print(Object[1].iloc[2, ])
print('l4')
print(Object[1].iloc[3, ])


# In[8]:


def get_twitter_csv(file1):
    file1.to_csv('twitter.csv', index=False)


def get_domain_csv(file0):
    file0.to_csv('domain.csv', index=False)


get_twitter_csv(Object[1])
get_twitter_csv(Object[0])
