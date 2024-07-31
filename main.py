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

cred = credentials.Certificate(r"firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

now = datetime.now()
selected_date = now.replace(hour=22, minute=0, second=0, microsecond=0) + timedelta(days=1)
end_date = selected_date + timedelta(days=3)
print(selected_date)
print(end_date)

date_str = selected_date.strftime(f'%Y-%m-%d')
trip_com_q_string = f'https://uk.trip.com/trains/list?departurecitycode=GB2278&arrivalcitycode=GB1594&departurecity=Sheffield&arrivalcity=London%20(Any)&departdate={date_str}&departhouript=22&departminuteipt=00&scheduleType=single&hidadultnum=1&hidchildnum=0&railcards=%7B%22YNG%22%3A1%7D&isregularlink=1&biztype=UK&locale=en-GB&curr=GBP'
 
data = []
driver = webdriver.Chrome()

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
           
def decline_cookies():
    try:
        decline_btn = find_elements(By.CLASS_NAME, 'cookie-banner-btn-more')[0]
        decline_btn.click()
    except NoSuchElementException:
        print('No cookie banner was found')

def get_times():
    attempts = 0
    while attempts < 10:
        try:
            all_h4s = find_elements(By.TAG_NAME, 'h4')
            return list(map(lambda x:x.text, list(filter(lambda el: ':' in el.text, all_h4s))))[::2] 
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)

def get_prices():
    attempts = 0
    while attempts < 10:
        try:
            all_spans = find_elements(By.TAG_NAME, 'span')
            return list(map(lambda x:x.text, list(filter(lambda el: '£' in el.text and el.value_of_css_property('color')=='rgba(15, 41, 77, 1)', all_spans))))
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)

def click_next_btn():
    attempts = 0
    while attempts < 10:
        try:
            all_divs = find_elements(By.TAG_NAME, 'div')
            list(filter(lambda el: 'View later trains' in el.text and len(el.text) == 17, all_divs))[0].click()
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)

# START OF DRIVER

driver.get(trip_com_q_string)
decline_cookies()

start = time.time()

while selected_date < end_date:
    times = get_times()
    prices = get_prices()

    current_t = times[0]
    for i in range(0, len(times)):
        if int(times[i][:2]) < int(current_t[:2]):
            selected_date = selected_date + timedelta(days=1)
        current_t = times[i]
        data.append({
            'date': selected_date.strftime(r'%d/%m/%y'),
            'time0': times[i],
            'price': prices[i]
        })

    click_next_btn()
    
    time.sleep(1.5)
    print('current data length: ', len(data))

print(len(data))
print('-'*30)
print(time.time() - start, 'secs')

with open('real_data.json','w') as file:
    json.dump(data, file)


driver.quit()
