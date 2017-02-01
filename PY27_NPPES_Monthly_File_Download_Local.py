#!/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         PY27_NPPES_Monthly_File_Download_Local.py
# Version:      1.0.0
# Purpose:      The script downloads the NPI Monthly files from external URL, Unzips them locally and
#               exports the required file to given target location.
# Doc:          TBD
# Authors:      vmundlye
# Created:      July-2016
# -------------------------------------------------------------------------------

import glob
import os
#import urllib.request
#import urllib.parse
#import urllib.error
import urllib
import urllib2
from bs4 import BeautifulSoup, Comment
import zipfile
import shutil
#import http.client
import sys
import time
import datetime
import re
import unittest
import sqlite3
import getpass

#Opens the CMS website and finds the .zip links for the NPPES files on the page.
def call_main_func(url,username):
    
    #conn = urllib.request.urlopen(url)
    req = urllib2.Request(url)
    conn = urllib2.urlopen(req)
    html = conn.read()
    conndb = None
    try:
        conndb = sqlite3.connect('NPPESFileStorage.db')
    except:
        pass
            
    try:
        conndb.execute('''CREATE TABLE tblNPPESMonthlyUrls
       (SERIAL_NUM INTEGER PRIMARY KEY AUTOINCREMENT, NPPES_URL TEXT UNIQUE, INSERT_DATE DEFAULT CURRENT_TIMESTAMP);''')
        conndb.commit
    except:
        pass

    ###Code to find the exact url of the Monthly File###
    zips = []
    Pattern = 'NPPES_Data_Dissemination_[a-zA-Z]'
    soup = BeautifulSoup(html,"html.parser")#BeautifulSoup library has been used to parse through html page.
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    links = soup.findAll("a")#method of BS used to find elements with tag a.
    for tag in links:
        link = tag.get("href")        
        if link is not None and ".zip" in link:
            zips.append("http://download.cms.gov/nppes/" + link.strip("./"))

    New_Zip = [x for x in zips if re.search(Pattern, x)]
    for item in New_Zip:
        FindLatestMonthlyFile(New_Zip)
        break

    if len(New_Zip)==0:
        print ("Monthly file was not found on the NPPES Website!")    

   
###Finds the latest Monthly file and passes the url further:
def FindLatestMonthlyFile (urls):
    conndb = sqlite3.connect('NPPESFileStorage.db')
    ###Code to print/fetch data into list###
    conndb.row_factory = lambda cursor, row: row[0]
    curs = conndb.cursor()
    dburls = curs.execute('select NPPES_URL from tblNPPESMonthlyUrls').fetchall()
    for i in urls:
        if i in dburls:
            print ( i, '>> This NPPES Monthly file has already been downloaded from the website!')
        else:
            try:
                conndb.execute('insert into tblNPPESMonthlyUrls (NPPES_URL) values (?)', [i])
                conndb.commit()
                print (i, '>> The entry for this new NPPES Monthly file has been recorded successfully in the local database.')
                MonthlyIncrementalFile (i)
                Outpath = UnZipFile ("C:\\Users\\"+username+"\\Downloads\\MonthlyIncrementalFile.zip")
                CopyMonthlyFileToTarget(Outpath, "C:\\Users\\"+username+"\\Desktop\\")
                
                
            except sqlite3.IntegrityError:
                print('Record already exists')
    conndb.close()

### Downloads the file locally:    
def MonthlyIncrementalFile(url):
    r = urllib.urlretrieve(url, "C:\\Users\\"+username+"\\Downloads\\MonthlyIncrementalFile.zip")
    


### Unzips the file locally:
def UnZipFile (path):
    fh1 = open(path, 'rb')
    zip_ref1 = zipfile.ZipFile(fh1)
    for name1 in zip_ref1.namelist():
        Outpath = "C:\\Users\\"+username+"\\Downloads\\" + "MonthlyIncrementalFile_UnZipped_" + datetime.datetime.now().strftime('%m-%d-%Y') + "\\"
        
        zip_ref1.extract(name1, Outpath)
    zip_ref1.close()
    return (Outpath)

### Copies the file from local folder to Target location:
def CopyMonthlyFileToTarget(src, dest):
    files = glob.glob(src+"*.csv")
    for i in [files for files in glob.glob(src+"*.csv") if not files.endswith("FileHeader.csv")]:
        src_file_1 = i
        shutil.copy(src_file_1, dest)

if __name__== "__main__":
    username = getpass.getuser()
    call_main_func ("http://download.cms.gov/nppes/NPI_Files.html", username)

#Scenario #1: No Monthly files are present.
#Solution: Handled in code via info msg.
    
#Scenario #2: Same Monthly files are present.
#Solution: Handled in code via lookup in DB, DB will would not record dupe entries and display info msg when same file appears.

#Scenario #3: Along with active links sometime older links are commented on the CMS WebPage in the html code.
#Solution: Handled in code via filtration of commented HTML code; ideally these will already be recorded in database and hence info msg will be displayed when encountered.
