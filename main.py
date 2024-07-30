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
tomorrow = now + timedelta(days=1)
tomorrow_at_6am = tomorrow.replace(hour=6, minute=0, second=0, microsecond=0)
date_str = tomorrow_at_6am.strftime(f'%Y-%m-%d')
trip_com_q_string = f'https://uk.trip.com/trains/list?departurecitycode=GB2278&arrivalcitycode=GB1594&departurecity=Sheffield&arrivalcity=London%20(Any)&departdate={date_str}&departhouript=06&departminuteipt=00&scheduleType=single&hidadultnum=1&hidchildnum=0&railcards=%7B%22YNG%22%3A1%7D&isregularlink=1&biztype=UK&locale=en-GB&curr=GBP'
 
def find_elements(selector, query):
    """ Tries to find an element within 15 secs and returns it. """
    try:
        return WebDriverWait(driver, 15).until(EC.presence_of_an_element_located((selector, query)))
    except NoSuchElementException:
        print('Error: There is no such element')
    except TimeoutException:
        print('Error: Time to find an element has elapsed')



def find_elements_w(by_what, string):
    for i in range(15):
        try:
            return driver.find_elements(by_what, string)
        except:
            time.sleep(1)

def assign_dates(data, initial_date):
    """ 
    It takes the data collected from the train times and returns the
    corresponding date when the journeys starts. This accounts for 
    rollover days.

    params:
        data (list) - start times of journey in a single list as 
        string of time initial date - datetime obj of initial 
        date at 00:00:00
        initial_date - datetime obj of initial date.
    returns:
        (list) - list of same length as data with datetime objs 
        representing which day that journey had started
    """
    dates = [initial_date]

    for i in range(1, len(data)):
        time0 = int(data[i-1][:2])
        time1 = int(data[i][:2])
        
        if time1 < time0:
            next_day = dates[-1] + timedelta(days=1)
            dates.append(next_day)
        else:
            dates.append(dates[-1])

    return dates

def add_date_to_time_n_price_data(data, date_str):
    global data
    # assigning dates to the times and prices
    time0_list = [arr[0] for arr in data]
    dates = assign_dates(time0_list, date_str)
    dates_as_strings = [date.strftime(f'%Y-%m-%d') for date in dates]

    # date will be inserted in the time_price data called 'data'
    for i in range(len(dates_as_strings)):
        data[i].insert(0, dates_as_strings[i])

def get_time_and_price_data():
    """
    It looks at the website and searches the <span> and <h4> tags
    which contain the time and price of the journey respectively.
    Once the data is found, it changes the global variable 'data'
    by appending to it.
    """
    global data
    time.sleep(3)
    all_span_elements = driver.find_elements(By.TAG_NAME, 'span')
    all_pound_elements = [el for el in all_span_elements if '£' in el.text]
    actual_pound_elements = [el for el in all_pound_elements if el.value_of_css_property('color') == 'rgba(15, 41, 77, 1)']
    
    all_h4_elements = driver.find_elements(By.TAG_NAME, 'h4')
    all_time_elements = [el for el in all_h4_elements if ':' in el.text]
    time_elements_in_pairs = [[all_time_elements[i], all_time_elements[i + 1]] for i in range(0, len(all_time_elements), 2)]

    for i in range(len(actual_pound_elements)):
        data.append([time_elements_in_pairs[i][0].text, time_elements_in_pairs[i][1].text, actual_pound_elements[i].text])
        print([time_elements_in_pairs[i][0].text, time_elements_in_pairs[i][1].text, actual_pound_elements[i].text])

def find_view_later_trains_btn():
    """
    Selenium locates the btn 'View later trains' which will allow me
    to load more train data to cover the whole day.
    """
    for i in range(5):
        try:
            all_divs = driver.find_elements(By.TAG_NAME, 'div')
            _ = [el for el in all_divs if 'View later trains' in el.text]
        except:
            time.sleep(3)

    return list(filter(lambda el: len(el.text) < 19, _))[0]
    
def decline_cookies():
    try:
        time.sleep(3)
        decline_btn = driver.find_element(By.CLASS_NAME, 'cookie-banner-btn-more')
        decline_btn.click()
    except NoSuchElementException:
        print('No cookie banner was found')

def upload_data_to_firebase(db, data):
    batch = db.batch()

    for journey in data:
        data_to_upload = {
            'date': journey[0],
            'time0': journey[1],
            'time1': journey[2],
            'price': journey[3],
        }
        
        doc_ref = db.collection('dates_times_n_prices').document()
        batch.set(doc_ref, data_to_upload)

    batch.commit()

def get_all_divs_and_span_elements():
    alls_divs = find_elements_w(By.TAG_NAME, 'div')
    alls_spans = find_elements_w(By.TAG_NAME, 'span')

data = []
current_date = tomorrow_at_6am

driver = webdriver.Chrome()
driver.get(trip_com_q_string)
decline_cookies()

while current_date < tomorrow_at_6am + timedelta(days=80):
    


driver.quit()


try:
    driver.get(trip_com_q_string) # Load the page
    decline_cookies()

    get_time_and_price_data() # 1st get of time and price data
    view_later_trains_btn = find_view_later_trains_btn()
    view_later_trains_btn.click()

    print(len(data))

    while len(data) < 3000:
        get_time_and_price_data()
        view_later_trains_btn = find_view_later_trains_btn()
        view_later_trains_btn.click()

    add_date_to_time_n_price_data(data, date_str)
    upload_data_to_firebase(db, data)
finally:
    print(40*'=')
    print()
    driver.quit()