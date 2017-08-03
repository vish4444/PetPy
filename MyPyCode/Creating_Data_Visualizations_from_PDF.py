#!/usr/bin/env python

# Algorithm:
# Pick up a PDF file from a folder/location on the machine.
# Open the PDF file and extract/convert the content into readable lines for python.
# Grab statements from this content which have numbers, etc in them and post onto a web page.
# Find a way to aggregate these statements and create visualizations from them (display onto a local webpage)


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
import PyPDF2
#from PyPDF2 import PdfFileReader, PdfFileWriter


#Opens the CMS website and finds the .zip links for the NPPES files on the page.
def call_main_func(path):

    content = ""
    
    # Load PDF into pyPDF
    pdf = PyPDF2.PdfFileReader (path, "rb")

    #Now that you have created a pdf object, see what all methods it has
    print ([method for method in dir(pdf) if callable(getattr(pdf, method))])
    PDFPages = pdf.getNumPages()
    print (PDFPages)

    #Display the text content of the PDF
    for i in range(0,PDFPages):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    #return content - this can be used to return the content to the calling function in the main with the print
    print (content)


if __name__== "__main__":
    #username = getpass.getuser()
    #call_main_func ("http://download.cms.gov/nppes/NPI_Files.html", username)
    #print(call_main_func("D:\\Python 2015\\2016 State of Industrial Internet Application Development.pdf").encode("ascii", "ignore"))
    call_main_func("D:\\Python 2015\\2016 State of Industrial Internet Application Development.pdf")
