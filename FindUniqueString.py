#Implement an algorithm to determine if a string has all unique characters.
from collections import defaultdict, Counter
import glob
import os
import urllib.request
import urllib.parse
import urllib.error
import urllib
from bs4 import BeautifulSoup, Comment
import zipfile
import shutil
import http.client
import sys
import time
import datetime
import re
import unittest
import sqlite3
import getpass


def call_main_func(s):
    s_list = list(s)
    Unique = "True"
    for i in range(0, len(s_list)-1):
        A = s_list [i]
        j = i+1
        for k in range(j, len(s_list)):
            B = s_list [k]
            if A == B:
                Unique = "False"
                break
            else:
                continue
            break
    if Unique == "False":
        print ("Your string is not unique")

    else:
        print ("Your string is unique")
            
    
        
if __name__== "__main__":
    username = getpass.getuser()
    s = input("Enter your string >> ")
    call_main_func (s)
    
