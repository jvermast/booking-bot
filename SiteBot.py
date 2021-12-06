#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tabulate import tabulate
from datetime import datetime
from random import randrange
import time
import sys
import pybase64
import warnings
import logging
from contextlib import suppress


warnings.filterwarnings("ignore", category=DeprecationWarning) 
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

username = "m"
password = ""

numcampers = 3
firstname_of_camper2 = ""
lastname_of_camper2 = ""
firstname_of_camper3 = ""
lastname_of_camper3 = ""

#Month must have a pre and post blank character for now. eg " APR "
month = " MAY "
#Date must have a pre and post blank character for now. eg " 29 "
date = " 2 "
#List of Lakes eg ["H49", "H48"]
desiredlakes = ["H49", "H48"]
tentcolors = "Two White"
numnights = len(desiredlakes)


driver = webdriver.Chrome("C:/chromedriver.exe")
driver.get("https://reservations.ontarioparks.com/")
title = driver.title
timeout = 10
format = '%Y-%m-%d %I:%M %p'
time.sleep(2) 
def waitfor(element):
    try:
        element_present = EC.presence_of_element_located((By.ID, element))
        ()
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        logging.info("Timed out waiting for page to load")
    finally:
        logging.info("Page loaded")        

def confirmdetails():
    with suppress(Exception):
        logging.info("Accepting Account Details if Required...")
        driver.find_element_by_css_selector("button[class='mat-focus-indicator button mat-flat-button mat-button-base mat-primary']").click()
        time.sleep(0.2)
    
def enterdates():
    try:
        logging.info("\nOpening Ontario Parks...")
        waitfor("tab-group-0")
        waitfor("tab-group-0")
        driver.find_element_by_id("consentButton").click()
        #Sign In
        driver.find_element_by_xpath("//*[contains(text(), 'Backcountry')]").click()
        waitfor("tab-group-0")
        #Hiking
        driver.find_element_by_id("mat-label-1").click()
        #Select Park
        driver.find_element_by_id("mat-input-5").click()
        driver.find_element_by_id("mat-option-115").click()
        #Num Campers
        driver.find_element_by_id("mat-input-7").send_keys(Keys.BACKSPACE)
        driver.find_element_by_id("mat-input-7").send_keys(numcampers)
        #Access point
        driver.find_element_by_id("mat-select-value-5").click()
        driver.find_element_by_id("mat-option-123").click()
        #Date
        driver.find_element_by_css_selector("input[formcontrolname='arrivalDate']").click()
        driver.find_element_by_id("monthDropdownPicker").click()
        driver.find_element_by_id("nextYearButton").click()
        driver.find_element_by_xpath( "(//*[contains(text(), '" + month + "')] | //*[@value='" + month + "'])").click()
        driver.find_element_by_xpath( "(//*[contains(text(), '" + date + "')] | //*[@value='" + date + "'])").click()
        #Click Search
        driver.find_element_by_id("actionSearch").click()
        waitfor("map")
        time.sleep(2) 
    except TimeoutException:
        logging.info("Failed to Load Page")

def checksiteavailable(desiredlakes, day):
    failed = 0
    for lake in desiredlakes:
        logging.debug("Num Failed:" + str(failed))
        if failed == numnights:
            logging.info("No more lakes to try, bailing out.")
            exit
        else:
            time.sleep(2)
            #Click Available Site 1
            driver.find_element_by_id("mat-input-9").clear()
            driver.find_element_by_id("mat-input-9").send_keys(lake)
            time.sleep(0.2)
            dropdown = driver.find_element_by_id("mat-autocomplete-2")
            count = dropdown.get_attribute("childElementCount")
            logging.debug(count + ' is the count')
            if count == "0":
                logging.info("Day " + day + ", Site " + lake + ": Site not available, trying next site")
                failed = failed + 1
            else:
                time.sleep(0.5)  
                driver.find_element_by_id("mat-autocomplete-2").click()  
                time.sleep(0.5)  
                try:
                    driver.find_element_by_xpath("//*[contains(@id, 'mat-error')]")
                except NoSuchElementException:
                    driver.find_element_by_id("addToItineraryButton").click()   
                    logging.info("Day " + day + ", Site " + lake + ": Site booked!")
                    time.sleep(0.5)  
                    break
                else:
                    logging.info("Day " + day + ", Site " + lake + ": Site not available, trying next site")
                    failed = failed + 1

        

def reserve():
    #Click Reserve
    time.sleep(1)
    driver.find_element_by_id("reserve-itinerary-btn").click()
    waitfor("confirmButton")
    #Confirm COVID Shit
    time.sleep(1)
    driver.find_element_by_id("confirmButton").click()
    #Confirm Other SHit
    time.sleep(1)
    driver.find_element_by_id("mat-checkbox-1").click()
    driver.find_element_by_id("mat-checkbox-2").click()
    #Confirm Reservation Details
    time.sleep(1)
    driver.find_element_by_id("confirmReservationDetails").click()
    waitfor("proceedToCheckout")
    #Proceed to Checkout
    driver.find_element_by_id("proceedToCheckout").click()
    time.sleep(1)
    #Sign In
    logging.info("Logging In...")
    driver.find_element_by_id("email").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(2)
    driver.find_element_by_css_selector("button[class='mat-focus-indicator mat-raised-button mat-button-base mat-primary']").click()
    time.sleep(2)
    #Accept some SHit
    logging.info("Confirming Acknolwdgements...")
    confirmdetails() 
    driver.find_element_by_id("mat-checkbox-3").click()
    time.sleep(0.2)
    driver.find_element_by_xpath("//*[contains(text(), 'Confirm Acknowledgements')]").click()
    time.sleep(1)
    #Confirm Account Details
    driver.find_element_by_id("confirmAccountDetails").click()
    time.sleep(1)
    #Confirm Occupant
    driver.find_element_by_id("confirmOccupant").click()
    time.sleep(2)
    if numcampers == 2: 
        #Enter Second Camper Name
        logging.info("Entering " + firstname_of_camper2 + " " + lastname_of_camper2 + " as second camper...")
        driver.find_element_by_id("firstName-1").send_keys(firstname_of_camper2)
        driver.find_element_by_id("lastName-1").send_keys(lastname_of_camper2)
    if numcampers == 3:
        #Enter Second Camper Name 
        logging.info("Entering " + firstname_of_camper2 + " " + lastname_of_camper2 + " as second camper...")
        driver.find_element_by_id("firstName-1").send_keys(firstname_of_camper2)
        driver.find_element_by_id("lastName-1").send_keys(lastname_of_camper2)
        #Enter Third Camper Name
        logging.info("Entering " + firstname_of_camper2 + " " + lastname_of_camper2 + " as third camper...")
        driver.find_element_by_id("firstName-2").send_keys(firstname_of_camper3)
        driver.find_element_by_id("lastName-2").send_keys(lastname_of_camper3)
    driver.find_element_by_id("mat-input-12").send_keys(tentcolors + " Tents")
    time.sleep(0.2)
    driver.find_element_by_id("partyInfoButton").click()
    time.sleep(1)
    driver.find_element_by_id("confirmAdditionalInformation").click()
    time.sleep(1)
    driver.find_element_by_id("addOnsOptions").click()

    #Pay
    logging.info("Ready for Payment")


logging.info("Welcome to Site Booking Bot!")
logging.info("Booking trip starting"+ month + date + "for " + str(numnights) + " nights")
logging.info("Sites: ")
logging.info('\n'.join(map(str, desiredlakes)))

enterdates()
for day in range(numnights):
    logging.debug("Day " + str(day))
    checksiteavailable(desiredlakes, str(day))
time.sleep(2)
reserve()


#driver.quit()
