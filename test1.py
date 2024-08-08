from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from firebase_admin import credentials
from firebase_admin import firestore
import time
import firebase_admin
import asyncio
import json 
import os

def find_elements(selector, query):
    """ Tries to find an element within 15 secs and returns it. """
    attempts = 0
    while attempts < 10:
        try:
            return WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((selector, query)))
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            attempts += 1
            time.sleep(1)
    return "Could not find element you were looking for"


driver = webdriver.Chrome()
driver.get('https://www.bbc.co.uk/news')
time.sleep(1)
all_spans = find_elements(By.TAG_NAME, 'span')
home = list(filter(lambda el: 'InDepth' in el.text and len(el.text) == 7, all_spans))[0]

ac = ActionChains(driver, 750)
print(dir(ac))

ac.move_to_element(home).scroll_by_amount(0, 100)
ac.perform()