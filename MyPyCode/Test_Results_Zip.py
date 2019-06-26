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
import os
from os.path import basename
import zipfile
import shutil
import sys
import time
import datetime
import re

# Main function to identify the required result files
#def call_main_func(path, random):
def call_main_func(path):
    #path=sys.argv[1]
    #print (random)
    MyFileList = []
    SeleniumScreenshotPattern = 'selenium-screenshot'
    RobotLogFile = 'log.html'
    RobotOutputFile = 'output.xml'
    RobotReportFile = 'report.html'
    RobotResultRecipients = ['vmundlye@verasolutions.org', 'nsambamurty@verasolutions.org']  

#Find all Selenium screenshot files
    for root, directories, files in os.walk(path):
        for myfile in files:
            if SeleniumScreenshotPattern in myfile:
                MyFileList.append(os.path.join(root, myfile))

    #Find Robot Output file
    for root, directories, files in os.walk(path):
        for myfile in files:
            if RobotOutputFile in myfile:
                MyFileList.append(os.path.join(root, myfile))

    #Find Robot Log file
    for root, directories, files in os.walk(path):
        for myfile in files:
            if RobotLogFile in myfile:
                MyFileList.append(os.path.join(root, myfile))

    #Find Robot Report file
    for root, directories, files in os.walk(path):
        for myfile in files:
            if RobotReportFile in myfile:
                MyFileList.append(os.path.join(root, myfile))
    
    # for f in MyFileList:
    #     print (f)

    # print (MyFileList)  #is printing all the required files in the list
    ZipRobotResultFiles (path, MyFileList)
### Create zip forlder in the same path with all the required files:
def ZipRobotResultFiles (path, MyFileList):
    DesiredZipFolder = 'RobotResults_' + datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')+ '.zip'
    zip_name = zipfile.ZipFile(DesiredZipFolder, 'w', zipfile.ZIP_DEFLATED)
    for i, val in enumerate(MyFileList):
        zip_name.write(val, basename(MyFileList[i]))

    zip_name.close()    


if __name__== "__main__":
    try:
        path=sys.argv[1]
        call_main_func (path)
    except:
        print ('Please pass path')
    #random = sys.argv[2]
    #call_main_func (path, random)
    #call_main_func ('C:\\VMVSSampleSFProject\\robot\\VMVSSampleSFProject\\results\\')    
    #call_main_func (path)


###Notes###
#Functionalities provided:
    #1. Folder path gets passed to the main func - done
    #2. Script identifies the required files to be zipped - done
    #3. Script zips the required files - done
    #4. Script reads the recipient emails.
    #5. Script emails this zipped folder to the recipients.
    #6. Script displays the success message.
    #7. Script should work on windows, macOS and linux.
