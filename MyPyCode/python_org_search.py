from selenium import webdriver
#The Keys class provide keys in the keyboard like RETURN, F1, ALT etc.
from selenium.webdriver.common.keys import Keys

#instance of "Firefox" WebDriver is created.
#Download the following geckodriver: https://github.com/mozilla/geckodriver/releases/
#unzip it and place the exe in C:\Python34\Scripts in PATH > System Environment Variables
#Set browser zoom = 100%
#driver = webdriver.Firefox()

#instance of "Ie" WebDriver is created.
#Download the following Iedriver: http://selenium-release.storage.googleapis.com/index.html/3.0
#unzip it and place the exe in C:\Python34\Scripts in PATH > System Environment Variables
#Set browser zoom = 100%
#driver = webdriver.Ie() 

#instance of "Chrome" WebDriver is created.
#Download the following chromedriver: http://chromedriver.storage.googleapis.com/index.html?path=2.24/chromedriver_win32.zip
#unzip it and place the exe in C:\Python34\Scripts in PATH > System Environment Variables
#Set browser zoom = 100%
driver = webdriver.Chrome() 


#The driver.get method will navigate to a page given by the URL.
#WebDriver will wait until the page has fully loaded (that is, the “onload” event has fired) before returning control to your test or script. 
driver.get("http://www.python.org")
#print (driver.title)

#assert "WebDriver" in driver.title #assertion to confirm that title has “WebDriver” word in it for Ie
assert "Python" in driver.title #assertion to confirm that title has “Python” word in it for FF

#WebDriver offers a number of ways to find elements using one of the find_element_by_* methods.
#For example, the input text element can be located by its name attribute using find_element_by_name method
elem = driver.find_element_by_id("id-search-field")

#We are sending keys. Special keys can be send using Keys class imported from selenium.webdriver.common.keys.
#To be safe, we’ll first clear any prepopulated text in the input field (e.g. “Search”) so it doesn’t affect our search results
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

assert "No results found." not in driver.page_source #assertion to check if submitting the page displayn any output.

#You can also call quit method instead of close.
#The quit will exit entire browser whereas close` will close one tab, but if just one tab was open, by default most browser will exit entirely
driver.close()
