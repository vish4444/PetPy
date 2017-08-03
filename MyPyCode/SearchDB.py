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
import re #regular expressions
import unittest
import sqlite3

def call_main_func ():
    conndb = None
    try:
        conndb = sqlite3.connect('NPPESFileStorage.db')
        curs = conndb.cursor()
        curs.execute('select * from tblNPPESWeeklyUrls')
        print (curs.fetchall())
        curs.execute('select * from tblNPPESMonthlyUrls')
        print (curs.fetchall())
        ####Code to delete a record####
        #curs.execute('delete from tblNPPESWeeklyUrls where SERIAL_NUM = 5')
        #conndb.commit()
        #print (curs.fetchone())
        ####----####
        ####Drop Monthly table####
        curs.execute('DROP TABLE IF EXISTS tblNPPESMonthlyUrls')
        conndb.commit()
        curs.execute('select * from tblNPPESMonthlyUrls')
        print (curs.fetchall())
        ####----####
        ####Drop Weekly table####
        #curs.execute('DROP TABLE IF EXISTS tblNPPESWeeklyUrls')
        #conndb.commit()
        #curs.execute('select * from tblNPPESWeeklyUrls')
        #print (curs.fetchall())
        conndb.close()

    except:
        pass

    
    
if __name__== "__main__":
    call_main_func ()
    #print (input("Do you want to continue type('y')"))
