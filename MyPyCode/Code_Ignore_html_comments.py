#!/usr/bin/env python
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

#Opens the CMS website and finds the .zip links for the NPPES files on the page.
def call_main_func(url,username):
    
    conn = urllib.request.urlopen(url)
    html = conn.read()


    #soup = BeautifulSoup(html,"html.parser")#BeautifulSoup library has been used to parse through html page
    soup = BeautifulSoup(html, "html.parser")
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    print (soup)
    
if __name__== "__main__":
    username = getpass.getuser()
    call_main_func ("file:///D:/HTML%20and%20CSS/CT_Website.html", username)
    #call_main_func ("http://download.cms.gov/nppes/NPI_Files.html", username)

#Scenario #1: No Weekly files are present.
#Scenario #2: Same weekly files are present.
#Scenario #3: 4 weekly files are present.
#Scenario #4: Along with active links couple other links might be commented on the CMS WebPage. These will not be downloaded as the database will already have an entry for previous files.
