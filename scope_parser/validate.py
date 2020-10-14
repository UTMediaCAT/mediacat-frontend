#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import urllib.request
import sys
import chardet

import scope_parser as sp


# check the input file should be csv file
def is_csv(filename):
    """
    check input file is csv or not, if it is, change it to unicode
    :param filename: a csv file name
    :rtype: Boolean if it is correct, exit process if it isn't csv
    """
    try:
        # try to read csv file
        df = pd.read_csv(filename)
        # restore it as unicode
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return True
    except(Exception):
        print("Input file is not csv or doesn't exist such csv")
        exit(1)


def check_unicode(filename):
    """
    check the csv file is unicode or not
    :param filename: a csv file name
    :rtype: None
    """
    with open(filename, 'rb') as detect_file_encoding:
        detection = chardet.detect(detect_file_encoding.read())
        print('Chardet:', detection)


# In[4]:


def check_ATH(df):
    """
    find every rows that all Associated Twitter Handle
    is incorrect and print the row number
    :param df: a dataframe
    :rtype: data frame
    """
    return(df.loc[~(df["Associated Twitter Handle"].isnull() | df["Associated Twitter Handle"].str.startswith('@'))])  # nopep8


# In[5]:


def url_is_alive(url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except(Exception):
        return False


def check_domain(df):
    """
    Checks that a given df's url is reachable and return invalid dataframe.
    :param df: A dataframe
    :rtype: a dataframe
    """

    domain = df.loc[df["Type"] == "News Source"].copy(deep=True)
    result = domain["Source"].apply(url_is_alive)
    domain.loc[:, 'domain_valid'] = result
    domain = domain.loc[domain["domain_valid"] == False]  # nopep8
    del domain['domain_valid']
    return domain


def check_ATH(df):  # silence pyflakes
    """
    Checks that all Associated Twitter Handle is valid or not
    and return invalid dataframe.
    :param df: A dataframe
    :rtype: a dataframe
    """
    return(df.loc[~(df["Associated Twitter Handle"].isnull() | df["Associated Twitter Handle"].str.startswith('@'))])   # nopep8


def check_Type(df):
    """
    find every rows that Type is not "News Source" or "Twitter Handle"
    and return invalid rows as a new dataframe.
    :param df: A dataframe
    :rtype: a dataframe
    """
    new = df.loc[~((df["Type"] == "Twitter Handle") | (df["Type"] == "News Source"))]  # nopep8
    return(new)


# find the source is incorrect format and return index
def check_Source(df):
    """
    Checks that all source(Twitter Handle part) is valid or not
    and return invalid rows as a new dataframe.
    :param df: A dataframe
    :rtype: a dataframe
    """
    new = df.loc[df["Type"] == "Twitter Handle"]
    return(new.loc[~(df["Source"].str.startswith('@'))])


def insert_error_type(error_name):
    """
    Create a new dataframe stand for error name
    :param error_name: A string of error name
    :rtype: A dataframe
    """

    df = pd.DataFrame({'Source': [error_name],
                       "RSS feed URLs (where available)": np.nan,
                       'Type': np.nan,
                       'Tags': np.nan,
                       'Associated Twitter Handle': np.nan,
                       'Associated Publisher': np.nan,
                       'Name': np.nan,
                       'Text aliases': np.nan})
    return(df)


def validation(file):
    """
    validate file is valid or not,
    if it is valid, generate twitter.csv and domain.csv
    if it is invalid, print error type and size and generate error.csv
    :param df: A dataframe
    :rtype: None
    """
    # check whether the file has error or not
    error_key = 0
    # test does it is csv file and convert file into unicode
    is_csv(file)
    print("It is valid csv file")
    # read the file as data frame
    df = pd.read_csv(file)
    # create a new_dataframe for error records
    Error = pd.DataFrame(columns=['Source', 'RSS feed URLs (where available)', 'Type', 'Tags', 'Associated Twitter Handle', 'Associated Publisher', 'Name', 'Text aliases'])  # nopep8

    print("check Type")
    error_type = check_Type(df)
    print("There are %d lines with Type errors" % error_type.index.size)
    if error_type.index.size != 0:
        error_key = 1
        type_error_name = insert_error_type("Type error")
        Error = Error.append(type_error_name)
        Error = Error.append(error_type)

    print("check Url")
    error_Url = check_domain(df)
    print("There are %d lines with invaild Url errors" % error_Url.index.size)
    if error_Url.index.size != 0:
        error_key = 1
        Url_error_name = insert_error_type("URL error")
        Error = Error.append(Url_error_name)
        Error = Error.append(error_Url)

    print("check Associate Twitter Handle")
    error_ATH = check_ATH(df)

    print("There are %d lines with incorrect Associate Twitter Handle errors" % error_ATH.index.size)  # nopep8
    if error_ATH.index.size != 0:
        error_key = 1
        ATH_error_name = insert_error_type("Associate Twitter Handle error")
        Error = Error.append(ATH_error_name)
        Error = Error.append(error_ATH)

    print("check Twitter Handle")
    error_TH = check_Source(df)
    print("There are %d lines with incorrect Twitter Handle errors" % error_TH.index.size)  # nopep8
    if error_TH.index.size != 0:
        error_key = 1
        TH_error_name = insert_error_type("Twitter Handle error")
        Error = Error.append(TH_error_name)
        Error = Error.append(error_TH)

    # if it has error, generate error.csv
    if error_key == 1:
        print("csv exists some errors, please fix it")
        print("generate error.csv")
        Error.to_csv('error.csv', index=True, encoding='utf-8-sig')
        return None
    else:
        sp.scope_parser(file)
        print("Valid")


if __name__ == '__main__':

    inFile = sys.argv[1]
    validation(inFile)
