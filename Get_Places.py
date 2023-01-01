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
import xml.etree.ElementTree
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pprint
import time
from datetime import datetime
from xml.dom import minidom
import pickle

driver = None
places = None
uncompletedData = None

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

def RetrievePlaces():
     xmldoc = minidom.parse('places.xml')
     pretty_xml_as_string = xmldoc.toprettyxml()
     hebrewItems = xmldoc.getElementsByTagName('שם_ישוב')
     englishItems = xmldoc.getElementsByTagName('שם_ישוב_לועזי')
     places = list()
     
     for heb,eng in zip(hebrewItems,englishItems):
        places.append({'hebrew name': heb.firstChild.data.lstrip().rstrip(),'english name': eng.firstChild.data.lstrip().rstrip()})

     return places   
     
def GetDataForPlace(ThePlace):
    global driver
    global uncompletedData
    
    place = ' ישוב ' + ThePlace['hebrew name']
    data = {'hebrew name': ThePlace['hebrew name'], 'english name': ThePlace['english name'], 'incentiation': None, 'type': None}
    
    try:
      driver.get('http://www.google.com/ncr')

      element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//input[@title = 'Search']")))

      SendKeysToElement(element,place, Enter = True)

      element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//span[contains(text(),'ויקיפדיה')]")))
        
      element.click()

      try:
        element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//b[contains(text(),'תאריך ייסוד')]/..//../td[2]")))
         
        incentiation = element.text

        data['incentiation'] = incentiation
      except WebDriverException:
        uncompletedData = uncompletedData + 1

      try:
        element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//b[contains(text(),'סוג יישוב')]/..//../td[2]")))
         
        theType = element.text

        data['type'] = theType
      except WebDriverException:
        uncompletedData = uncompletedData + 1

    except WebDriverException:
      uncompletedData = uncompletedData + 2

    return data

def GetDataForPlaces(ThePlaces):
        global places
        places = list()

        for place in ThePlaces:
          places.append(GetDataForPlace(place))

def ProcessUnCompletePlaces():
        global places
        global uncompletedData

        incentationComplete = False
        typeComplete = False
        
        print('Attempting to complete ',uncompletedData,' Data ====>')

        
        for place in places:
                if place['incentiation'] == None and incentationComplete == True:
                  place['incentiation'] = input("Enter " + place['name'] + " Incentiation ? ")

                if place['type'] == None and typeComplete == True:
                  place['type'] = input("Enter " + place['name'] + " type ? ")

                SaveData()
        
def SaveData():
        global places
        places_file = open('places.pckl','wb')
        pickle.dump(places,places_file)
        places_file.close()

def GetDataForPlacesDEMO(ThePlaces):
        global places
        places = list()

        counter = 0
        
        for place in ThePlaces:
          counter = counter + 1
          places.append(GetDataForPlace(place))

          if counter == 20:
            break
          
def ShutDown():
    global driver 
    try:
        driver.quit()
    except  WebDriverException:
        pass

if __name__ == "__main__":
    global uncompletedData
    
    uncompletedData = 0
    
    Initialize()
    places = RetrievePlaces()
    GetDataForPlaces(places)
    ShutDown()
    SaveData()
    ProcessUnCompletePlaces() 
