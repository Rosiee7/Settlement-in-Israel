from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.events import EventFiringWebDriver
from seleniumrequests import Chrome as seleniumRequestChrome
from seleniumrequests import Firefox as seleniumRequestFirefox
from seleniumrequests import Remote as seleniumRequestRemote
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pprint
import time
from datetime import datetime

driver = None

# Sending Keys To Element
def SendKeysToElement(theElement,theKeys,**kwargs):
        # Initializing Variables
        enterRequest = False
        submitRequest = False
        clearRequest = True
        
        # Checking For Special Requests -->

        # Checking Enter Special Request
        if 'Enter' in kwargs:
            if kwargs['Enter'] == True:
                # Declaring True For Enter Request
                enterRequest = True
            
        # Checking Submit Special Request
        if 'Submit' in kwargs:
            if kwargs['Submit'] == True:
                # Declaring True For Submit Request
                submitRequest = True

        # Checking Clear Special Request
        if 'Clear' in kwargs:
            if kwargs['Clear'] == True:
                # Declaring True For Clear Request
                clearRequest = True
                
        # Checking For Special Requests <--
        
        # Executing Clear If Requested
        if clearRequest == True:
            theElement.clear()
        
        # Sending Keys To Element
        theElement.send_keys(theKeys)

        # Executing Enter If Requested
        if enterRequest == True:
            theElement.send_keys(Keys.ENTER)

        # Executing Submit If Requested
        if submitRequest == True:
            theElement.submit()

def Initialize():
    global driver
    driver = seleniumRequestFirefox()

def GetDataForPlace(ThePlace):
    global driver

    ThePlace =  'ישוב ' + ThePlace
    
    driver.get('http://www.google.com/ncr')

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//input[@title = 'Search']")))

    SendKeysToElement(element,ThePlace, Enter = True)

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//span[contains(text(),'ויקיפדיה')]")))

    element.click()

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//b[contains(text(),'תאריך ייסוד')]/..//../td[2]")))
     
    incentiation = element.text

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//span[@class = 'longitude']")))

    longitude = element.text

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//span[@class = 'latitude']")))

    latitude = element.text

    return {'incentiation': incentiation, 'longitude':longitude, 'latitude':latitude}

def ShutDown():
    global driver 
    try:
        driver.quit()
    except  WebDriverException:
        pass

'''
WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//li[@id = 'history']//a[contains(text(),'History')]"))).click()

time.sleep(5)

WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//button[@class = 'chartModeSelectorButton' and contains(text(),'All')]"))).click()

time.sleep(5)
bsObj = BeautifulSoup(driver.page_source,'html.parser')
        
tags = bsObj.findAll('ul')

newTags = []

for tag in tags:
    if tag.find('li',{'class' : 'rowvalue date'}) != None:
        newTags.append(tag.findAll())

stockData = []
defRow = []

for columnDef in newTags[0]:
    defRow.append(columnDef.attrs['class'][1])

stockData.append(defRow)

for tag in newTags:
    rowData = []
    for dataTag in tag:
        rowData.append(dataTag.get_text())

    stockData.append(rowData)

# for i in reversed(a):
#    i.find('li',{'class' : 'rowvalue row'}.get_text()

for rowIndex in range(1,len(stockData)):
    for colIndex in range(len(stockData[rowIndex])):
        if '/' in stockData[rowIndex][colIndex]:
            stockData[rowIndex][colIndex] = datetime.strptime(stockData[rowIndex][colIndex], '%m/%d/%Y')
        elif(is_number(stockData[rowIndex][colIndex]) == True):
            stockData[rowIndex][colIndex] = ConvertStringToFloat(stockData[rowIndex][colIndex])
        else:
            print('\n\n\nError !!!!!!!!!!!! : {}.'.format(stockData[rowIndex][colIndex]))

pprint.pprint(stockData)
'''

if __name__ == "__main__":
    
    Initialize()
    data = GetDataForPlace('אומץ')
    
    ShutDown()
    
