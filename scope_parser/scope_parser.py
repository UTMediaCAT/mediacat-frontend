#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import sys


def insert_UniqueID(df):
    """
    insert a new column of Unique ID from 1,2,3,4,5,...to n
    :param df: a dataframe
    :rtype: None
    """
    df.insert(0, "UniqueID", range(1, len(df) + 1), True)


def expand_Twitter_Handle(df):
    """
    expand the records for all the associated twitter handle
    :param df: a dataframe
    :rtype: dataframe
    """

    # to find every non-empty Associate Twitter Handle's rows's index
    # and store into not_null_twitter
    # for example if row 0 exist associate twitter handle, then it will
    # be stored in not_null_twitter
    not_null_twitter = df.loc[pd.notna(df["Associated Twitter Handle"]), :].index  # nopep8

    # create new rows for every Associate Twitter Handle, in this case source
    # will be the old assciated twitter handle
    # Type to be "Twitter Handle", UniqueID, Tags and Name will keep same.
    new_df_to_add_twitter = pd.DataFrame({'UniqueID': df.iloc[not_null_twitter, 0],  # nopep8
                                  'Source': df.iloc[not_null_twitter, 5],  # nopep8
                                  "RSS feed URLs (where available)": np.nan,  # nopep8
                                  'Type': "Twitter Handle",  # nopep8
                                  'Tags': df.iloc[not_null_twitter, 4],  # nopep8
                                  'Associated Twitter Handle': np.nan,  # nopep8
                                  'Associated Publisher': np.nan,  # nopep8
                                  'Name': df.iloc[not_null_twitter, 7],  # nopep8
                                  'Text aliases': np.nan})

    # since some of associated twitter Handle will be 2 or 3,
    # so it use "|" to split
    # and make every twitter handle as a new record
    new_df_to_add_twitter["Source"] = new_df_to_add_twitter["Source"].str.split("|")  # nopep8
    new_df_to_add_twitter = new_df_to_add_twitter.explode("Source")
    return new_df_to_add_twitter


def separate_by_type(df):
    """
    separate the dataframe that group by Type
    :param df: a dataframe
    :rtype: list of dataframe
    """

    Object = [x for _, x in df.groupby('Type')]
    return Object


def get_twitter_csv(file1):
    """
    generate twitter.csv with unicode version
    :param df: a dataframe
    :rtype: None
    """
    file1.to_csv('twitter.csv', index=False, encoding='utf-8-sig')


def get_domain_csv(file0):
    """
    generate domain.csv with unicode version
    :param df: a dataframe
    :rtype: None
    """
    file0.to_csv('domain.csv', index=False, encoding='utf-8-sig')


# In[6]:


def scope_parser(file):
    """
    do the whole scoper_parser's process
    :param file: a csv file
    :rtype: list of dataframe
    """
    # read the csv file
    df = pd.read_csv(file)

    # create a new column named "UniqueID" from 1,2,3,4,5,
    # ...to n(n is # of rows we have)
    # UniqueID is using to link the Source and Associate Twitter Handle,
    # which should create by system
    # usually it is used by system only
    insert_UniqueID(df)

    expand_records = expand_Twitter_Handle(df)
    # add expand_records into dafaframe and reset the index to 0,1,2,3....
    df = df.append(expand_records)
    df = df.sort_values(by=['UniqueID'])
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace=True)

    # separate dataframe that group by Type
    Object = separate_by_type(df)
    # generate twitter csv
    print("generate twitter.csv")
    get_twitter_csv(Object[1])
    # generate domain csv
    print("generate domain.csv")
    get_domain_csv(Object[0])

    print("Congratulations, you could move to next step!")
    # returen dataframe
    return df


if __name__ == '__main__':
    inFile = sys.argv[1]
    dataframes = scope_parser("test_demo.csv")
