#!/usr/bin/env python
# coding: utf-8


# In[62]:


import pandas as pd


# In[63]:


# check the input file should be csv file
def is_csv(filename):
    try:
        # try to read csv file
        pd.read_csv(filename)
        return True
    except(Exception):
        print("Input file is not csv or doesn't exist such csv")


is_csv("test_demo.csv")


# In[55]:


is_csv("not_exist.csv")


# In[ ]:


# is it unicode? Yes, In python3, all string are unicode by default


# In[82]:


# you can replace "test_error_demo.csv" with any file you want to test
df = pd.read_csv("test_error_demo.csv")

# find every rows that all Associated Twitter Handle is incorrect
df.loc[~(df["Associated Twitter Handle"].isnull() | df["Associated Twitter Handle"].str.startswith('@'))]  # nopep8


# In[81]:


# find every rows that all Associated Twitter Handle is incorrect
# and print the row number
def check_ATH():
    print(df.loc[~(df["Associated Twitter Handle"].isnull() | df["Associated Twitter Handle"].str.startswith('@'))].index)  # nopep8


# find every rows that Type is not "News Source" or "Twitter Handle"
df.loc[~((df["Type"] == "Twitter Handle") | (df["Type"] == "News Source"))]


# In[83]:


# find every rows that Type is not "News Source" or "Twitter Handle"
# and print its row number
def check_Type():
    print(df.loc[~((df["Type"] == "Twitter Handle") | (df["Type"] == "News Source"))].index)  # nopep8


# find the source is incorrect format
df.loc[~((df["Source"].str.startswith('@') | (df["Source"].str.contains("http://|https://"))))]  # nopep8


# In[85]:


# find the source is incorrect format and return index
def check_Source():
    print(df.loc[~((df["Source"].str.startswith('@') | (df["Source"].str.contains("http://|https://"))))].index)  # nopep8


type(u'תל אביב, ישראל')
