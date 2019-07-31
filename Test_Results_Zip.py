############################
# Purpose of the script: Emails Robot Framework test results to intended recipients.
# Author: Vishal Mundlye
# Date: June-2019
# Platforms supported, tested on: Mac OS Sierra 10.12.4, Windows 10
# Script version: v1.0
# Pre-requisites: Pass the folder path of the results
# Running Instructions:
# 1. Open the terminal/prompt
# 2. Navigate to the desktop directory
# 3. type python3 <script_name.py>
# 4. hit enter
# 5. provide the web page url and hit enter
# 6. provide the local username and hit enter
# Python versions supported: Py 3.7.2
# Dependencies: 
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
import smtplib
import tempfile
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Main function to identify the required result files
#def call_main_func(path, random):
def call_main_func(mydir):
    #path=sys.argv[1]
    #print (random)
    MyFileList = []
    SeleniumScreenshotPattern = 'selenium-screenshot'
    RobotLogFile = 'log.html'
    RobotOutputFile = 'output.xml'
    RobotReportFile = 'report.html'
    RobotResultRecipients = ['vmundlye@verasolutions.org']

#Find all Selenium screenshot files
    for root, directories, files in os.walk(mydir):
        for myfile in files:
            if SeleniumScreenshotPattern in myfile:
                MyFileList.append(os.path.join(root, myfile))

    #Find Robot Output file
    for root, directories, files in os.walk(mydir):
        for myfile in files:
            if RobotOutputFile in myfile:
                MyFileList.append(os.path.join(root, myfile))

    #Find Robot Log file
    for root, directories, files in os.walk(mydir):
        for myfile in files:
            if RobotLogFile in myfile:
                MyFileList.append(os.path.join(root, myfile))

    #Find Robot Report file
    for root, directories, files in os.walk(mydir):
        for myfile in files:
            if RobotReportFile in myfile:
                MyFileList.append(os.path.join(root, myfile))
    
    # for f in MyFileList:
    #     print (f)

    # print (MyFileList)  #is printing all the required files in the list
    MyZipfolder = ZipRobotResultFiles (mydir, MyFileList)
    print ('Zipped successfully')
    #ZipRobotResultFiles (mydir, MyFileList)
    EmailRobotResultsZip (MyZipfolder,RobotResultRecipients)
    print ('Emailed successfully')

### Create zip forlder in the same path with all the required files:
def ZipRobotResultFiles (mydir, MyFileList):
    DesiredZipFolder = 'RobotResults_' + datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')+ '.zip'
    zip_name = zipfile.ZipFile(DesiredZipFolder, 'w', zipfile.ZIP_DEFLATED)
    for i, val in enumerate(MyFileList):
        zip_name.write(val, basename(MyFileList[i]))
    zip_name.close()    
    
    return DesiredZipFolder

# Create the email message
def EmailRobotResultsZip (MyZipfolder, RobotResultRecipients, sender='vmundlye@verasolutions.org'):
    zf = open(MyZipfolder, 'rb')
    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['Subject'] = 'Robot automation test results'
    msg['To'] = ', '.join(RobotResultRecipients)
    msg['From'] = sender
    body = 'This is an email with attachment sent from Python'

    # Add body to email
    msg.attach(MIMEText(body, "plain"))

    # Attaching file from the same directory as script:
    part = MIMEBase('application', 'zip')
    part.set_payload(zf.read())
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
    "Content-Disposition",
    f"attachment; filename= {MyZipfolder}",
    )
    #part.add_header('Content-Disposition', 'attachment', filename=MyZipfolder)
    
    # Add attachment to message and convert message to string
    msg.attach(part)
    themsg = msg.as_string()
    
    # for root, dirs, files in os.walk('./'):
    #     #print (files)
    #     for MyZipfolder in files:
    #         file_path = os.path.join(os.curdir, MyZipfolder)
    #         print (file_path)
    #         attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="zip")
    #         attachment.add_header('Content-Disposition','attachment', filename=MyZipfolder)
    #         msg.attach(attachment)
    #         themsg = msg.as_string()
        

    # send the message
    smtp = smtplib.SMTP()
    smtp.connect()
    smtp.sendmail(sender, RobotResultRecipients, themsg)
    smtp.close()    


if __name__== "__main__":
    try:
        mydir=sys.argv[1]
        call_main_func (mydir)
    except:
        print ('Please pass the directory')
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
