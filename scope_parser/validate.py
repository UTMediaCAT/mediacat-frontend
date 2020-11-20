#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import urllib.request
import sys
import chardet
import validators
import scope_parser as sp
from colorama import Fore
from colorama import Style


# In[2]:


def url_is_alive(url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',  # nopep8
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # nopep8
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    print(url)
    sys.stdout.flush()

    try:
        request = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(request, timeout=30)
        if str(response.status)[0] == "2":
            print("True")
            sys.stdout.flush()
            return True
        else:
            return False
    except(Exception):

        return False


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
        print("filename; " + filename)
        print(Fore.RED +
              'Input file is invalid.' +
              ' It is not a csv file or it is corrupted.' +
              Style.RESET_ALL)
        sys.stdout.flush()
        raise


# In[4]:


def check_unicode(filename):
    """
    check the csv file is unicode or not
    :param filename: a csv file name
    :rtype: None
    """
    with open(filename, 'rb') as detect_file_encoding:
        detection = chardet.detect(detect_file_encoding.read())
        print('Chardet:', detection)
        sys.stdout.flush()


# In[5]:


def url_format(url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    if validators.url(url) == True:  # nopep8
        return True
    else:
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


# In[7]:


def check_ATH(df):
    """
    Checks that all Associated Twitter Handle is valid or not
    and return invalid dataframe.
    :param df: A dataframe
    :rtype: a dataframe
    """
    return(df.loc[~(df["Associated Twitter Handle"].isnull() | df["Associated Twitter Handle"].str.startswith('@'))])   # nopep8


# In[8]:


def check_Type(df):  # silence pyflakes
    """
    find every rows that Type is not "News Source" or "Twitter Handle"
    and return invalid rows as a new dataframe.
    :param df: A dataframe
    :rtype: a dataframe
    """
    new = df.loc[~((df["Type"] == "Twitter Handle") | (df["Type"] == "News Source"))]  # nopep8
    return(new)


# In[9]:


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


# In[10]:


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
    url_error_key = 0
    print(Fore.BLUE + "checking CSV:" + Style.RESET_ALL)
    sys.stdout.flush()
    # test does it is csv file and convert file into unicode
    is_csv(file)
    print("It is a valid csv file")
    sys.stdout.flush()
    # read the file as data frame
    df = pd.read_csv(file)
    # create a new_dataframe for error records
    Error = pd.DataFrame(columns=['Source', 'RSS feed URLs (where available)', 'Type', 'Tags', 'Associated Twitter Handle', 'Associated Publisher', 'Name', 'Text aliases'])  # nopep8

    print(Fore.BLUE + "checking Type:" + Style.RESET_ALL)
    sys.stdout.flush()
    error_type = check_Type(df)
    print("There are %d lines with Type errors" % error_type.index.size)
    sys.stdout.flush()
    if error_type.index.size != 0:
        error_key = 1
        type_error_name = insert_error_type("Type error")
        Error = Error.append(type_error_name)
        Error = Error.append(error_type)

    print(Fore.BLUE + "checking URL:" + Style.RESET_ALL)
    sys.stdout.flush()
    error_Url = check_domain(df)
    print("There are %d lines with invaild Url errors" % error_Url.index.size)
    sys.stdout.flush()
    if error_Url.index.size != 0:
        url_error_key = 1
        Url_error_name = insert_error_type("URL error")
        Error = Error.append(Url_error_name)
        Error = Error.append(error_Url)

    print(Fore.BLUE + "checking Associate Twitter Handle:" + Style.RESET_ALL)
    sys.stdout.flush()
    error_ATH = check_ATH(df)

    print("There are %d lines with incorrect Associate Twitter Handle errors" % error_ATH.index.size)  # nopep8
    sys.stdout.flush()
    if error_ATH.index.size != 0:
        error_key = 1
        ATH_error_name = insert_error_type("Associate Twitter Handle error")
        Error = Error.append(ATH_error_name)
        Error = Error.append(error_ATH)

    print(Fore.BLUE + "checking Twitter Handles:" + Style.RESET_ALL)
    sys.stdout.flush()
    error_TH = check_Source(df)
    print("There are %d lines with incorrect Twitter Handle errors" % error_TH.index.size)  # nopep8
    sys.stdout.flush()
    if error_TH.index.size != 0:
        error_key = 1
        TH_error_name = insert_error_type("Twitter Handle error")
        Error = Error.append(TH_error_name)
        Error = Error.append(error_TH)

    # if it has error, generate error.csv
    if error_key == 1:
        print(Fore.RED + "Generating error.csv..." + Style.RESET_ALL)
        sys.stdout.flush()
        Error.to_csv('error.csv', index=True, encoding='utf-8-sig')
        raise Exception(Fore.RED + "There exists some csv formating errors," +
                        "please refer to the error file to fix" + Style.RESET_ALL)  # nopep8
    else:
        if url_error_key == 1:
            print(Fore.RED + "Generating error.csv...only url error" + Style.RESET_ALL)  # nopep8
            sys.stdout.flush()
            Error.to_csv('error.csv', index=True, encoding='utf-8-sig')
        sp.scope_parser(file)
        print(Fore.GREEN +
              "Finished Validating and Scope Parsing." + Style.RESET_ALL)
        sys.stdout.flush()


# In[12]:


if __name__ == '__main__':
    # inFile = sys.argv[1]
    validation("input_scope_final.csv")
