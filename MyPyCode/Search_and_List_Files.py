import glob
import os
import urllib.request
import urllib.parse
import urllib.error
import urllib
from bs4 import BeautifulSoup
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

def call_main_func(url):
    files = os.listdir (url)
    print (files)

if __name__== "__main__":
    url = input ("Please enter the url")
    #Enter: D:\Adv SQL - 2015 directly
    call_main_func (url)

