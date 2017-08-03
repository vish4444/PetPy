############################
# Purpose of the script: Pass url or the web page link along with local username to the script and it
# downloads all the images on the page to the disk.
# Author: Vishal Mundlye
# Date: 28-July-2017
# Platforms supported, tested on: Mac OS Sierra 10.12.4, Windows 7 Professional
# Script version: v1.0
# Pre-requisites: Place this script file along with the Image_Types.py file on your desktop.
# Running Instructions:
# 1. Open the terminal/prompt
# 2. Navigate to the desktop directory
# 3. type python3 <script_name.py>
# 4. hit enter
# 5. provide the web page url and hit enter
# 6. provide the local username and hit enter
# Python versions supported: Py 3.5/3.4, for 2.7 code changes will be required to support urllib2
# Dependencies: BeautifulSoup, certifi, pyintaller
# Comments: Please read the bottom section for key functionalities, validations provided and open issues.
############################
#!/usr/bin/env python
import glob
import os
import urllib
import urllib.request
import urllib.parse
import urllib.error
#import urllib2 >> for py 2.7
from bs4 import BeautifulSoup, Comment
import zipfile
import shutil
import http.client
import certifi
import ssl
import sys
import time
import datetime
import re
import unittest
import sqlite3
import getpass

# Main function to open the webpage and find the right urls for image.
def call_main_func(url,username):
    # Code to access the webpage
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req=urllib.request.Request(url,None, headers=hdr)
    conn = urllib.request.urlopen(req)
    #req = urllib2.Request(url,None, headers=hdr) >> for py2.7
    #conn = urllib2.urlopen(req) >> for py2.7
    html = conn.read()
    str1, str2 = url.split(':')
    url_start = str1

    # Code to initialize a local DB for storing the image urls
    conndb = None
    try:
        conndb = sqlite3.connect('ImageStorage.db')
    except:
        pass
    try:
        conndb.execute('''CREATE TABLE tblImageUrls
       (SERIAL_NUM INTEGER PRIMARY KEY AUTOINCREMENT, IMAGE_URL TEXT, INSERT_DATE DEFAULT CURRENT_TIMESTAMP);''')
        conndb.commit
    except:
        pass

    # Code to find the image urls
    zips = []
    Img_Types = []
    Download_Status = []
    ElementTypes = ['href', 'src']
    #Img_Types = ['gif', 'tif', 'jpg', 'png', 'bmp', 'jpeg', 'tiff', ....] >> hard code image types if required else use below code

    # Use below code if external file needs to be used for passing different image format types.
    #Format_Type = open("/Users/"+username+"/Desktop/Image_Types.py","r") # for mac
    Format_Type = open("C:\\Users\\"+username+"\\Desktop\\Image_Types.py","r")#>> for windows
    Img_Type_File = Format_Type.readlines()
    for line in Img_Type_File:
        Img_Types.append(line.rstrip("\r\n"))

    # BeautifulSoup library has been used to parse through html page and to find the tags and required elements.
    soup = BeautifulSoup(html,"html.parser")
    links = soup.findAll(["link", "img"])
    for tag in links:
        for element in ElementTypes:
            link = tag.get(element)
            for IMGType in Img_Types:
                if link is not None and IMGType in link:
                    zips.append(link)

    if zips ==[]:
        print ("No images found on the webpage !!")
        sys.exit(0)
    else:
        for i in range(len(zips)):
            if url_start not in zips[i]:
                zips[i] = url + zips[i]              

    for i in range(len(zips)):
        Status = DownloadImgUrl(zips[i])
        Download_Status.append(Status)
        if Download_Status[i] == 'True' :
            InsertImgUrl(zips[i])
    
# Code to download the images locally.
def DownloadImgUrl (url):
    ImageName = url.split('/')[-1]
    try:
        r = urllib.request.urlretrieve(url, "C:\\Users\\"+username+"\\Desktop\\"+ImageName) #>> for windows
        #r = urllib.request.urlretrieve(url, "/Users/"+username+"/Desktop/"+ImageName) # >> for mac
        return 'True'
    except Exception:
        print ("Bad image url detected, ignoring download!!")
        return 'False'

# Code to store the downloaded image urls in the local database.
def InsertImgUrl (url):
    conndb = sqlite3.connect('ImageStorage.db')
    # Code to check if a image url already exist in database
    conndb.row_factory = lambda cursor, row: row[0]
    curs = conndb.cursor()
    dburls = curs.execute('select IMAGE_URL from tblImageUrls').fetchall()
    if url in dburls:
        print ( url, '>> This image has already been downloaded from the website, not recording the entry again!')
    else:
        conndb.execute('insert into tblImageUrls (IMAGE_URL) values (?)', [url])
        conndb.commit()
        print (url, '>> The entry for this new image url has been recorded successfully in the local database.')
    conndb.close()

    
if __name__== "__main__":
    #username = getpass.getuser()
    #call_main_func ("https://www.bountysource.com/issues/42616824-mac-issue-with-running-the-red_start-command", username)
    #call_main_func ("http://www.greens.org/about/software/editor.txt", username)
    #call_main_func ("http://blog.teamtreehouse.com/how-to-fix-a-broken-image", username)
    #call_main_func ("http://www.lipsum.com", username)
    #call_main_func ("https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Images_in_HTML", username)
    #call_main_func("http://robotframework.org/robotframework/latest/libraries/Collections.html", username)
    #call_main_func ("https://en.wikipedia.org/wiki/F-Secure", username)
    #call_main_func ("https://www.f-secure.com", username)
    url = str(input('Please provide the url: '))
    username = str(input ('Please provide your local username: '))
    call_main_func (url, username)    


###Notes###
#Functionalities provided:
    #1. User can input web url and local username at runtime.
    #2. If user provides same url again, local DB does not record entry and displays an info message.
    #3. Exe for this script has been created for windows, so that it can run w/o python by simply passing url and username.
    #4. Only those images which were downloaded will be recorded in the local DB.
    #5. A supporting SearchDB.py script has been provided to verify the urls recorded in the DB.
    #6. User can add as many image types in the Image_Types.py file.
        

#Validations provided:
    #1. If a web page has images and the url is not accessible/unsecured, then a user friendly message is displayed.
        # example call_main_func ("http://www.greens.org/about/software/editor.txt", username)
    #2. If a webpage does not have any images, then a user friendly message is displayed and execution is stopped.
        # example: call_main_func("http://robotframework.org/robotframework/latest/libraries/Collections.html", username)
    #3. If a webpage has just the image.format and not the absolute path then complete url is appended to it for download.
        # example: call_main_func ("http://www.lipsum.com", username)
    #4. Only those images which are downloaded are recorded in the local DB.

#Open Issues:
    #1. ssl c 720 issue exist for mac, ref: https://stackoverflow.com/questions/38670295/homebrew-refusing-to-link-openssl
        #Affects: #call_main_func ("https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Images_in_HTML", username)
    #2. unsecured url error is fixed by passing headers, however images in the web page which open in unsecured manner are not downloaded
        #Example: http://blog.teamtreehouse.com/how-to-fix-a-broken-image"
    #3. urls from wikipedia are not supported for downloads since, the wiki images append a different string the original url, this is not handled so far in the script.
