from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from firebase_admin import credentials
from firebase_admin import firestore
import time
import firebase_admin
import asyncio

cred = credentials.Certificate(r"firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

now = datetime.now()
tomorrow_morning = now.replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)

date_str = tomorrow_morning.strftime(f'%Y-%m-%d')
trip_com_q_string = f'https://uk.trip.com/trains/list?departurecitycode=GB2278&arrivalcitycode=GB1594&departurecity=Sheffield&arrivalcity=London%20(Any)&departdate={date_str}&departhouript=06&departminuteipt=00&scheduleType=single&hidadultnum=1&hidchildnum=0&railcards=%7B%22YNG%22%3A1%7D&isregularlink=1&biztype=UK&locale=en-GB&curr=GBP'
 
data = []
driver = webdriver.Chrome()

def find_elements(selector, query):
    """ Tries to find an element within 15 secs and returns it. """
    try:
        return WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((selector, query)))
    except NoSuchElementException:
        print('Error: There is no such element')
    except TimeoutException:
        print('Error: Time to find an element has elapsed')
   
def decline_cookies():
    try:
        decline_btn = find_elements(By.CLASS_NAME, 'cookie-banner-btn-more')[0]
        decline_btn.click()
    except NoSuchElementException:
        print('No cookie banner was found')

# START OF DRIVER

driver.get(trip_com_q_string)
decline_cookies()

all_h4s = find_elements(By.TAG_NAME, 'h4')
all_spans = find_elements(By.TAG_NAME, 'span')
all_divs = find_elements(By.TAG_NAME, 'div')

times = list(map(lambda x:x.text, list(filter(lambda el: ':' in el.text, all_h4s)))) 
prices = list(map(lambda x:x.text, list(filter(lambda el: '£' in el.text and el.value_of_css_property('color')=='rgba(15, 41, 77, 1)', all_spans))))
next_trains_btn = list(filter(lambda el: 'View later trains' in el.text and len(el.text) == 17, all_divs))[0].text



driver.quit()
