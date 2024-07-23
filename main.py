from datetime import datetime, timedelta
import time

now = datetime.now()
future_date = now + timedelta(days=10)
future_date_at_6am = future_date.replace(hour=6, minute=0, second=0, microsecond=0)
date_string_at_6am = future_date_at_6am.strftime(f'%Y-%m-%d')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

trip_com_q_string = f'https://uk.trip.com/trains/list?departurecitycode=GB2278&arrivalcitycode=GB1594&departurecity=Sheffield&arrivalcity=London%20(Any)&departdate={date_string_at_6am}&departhouript=06&departminuteipt=00&scheduleType=single&hidadultnum=1&hidchildnum=0&railcards=%7B%22YNG%22%3A1%7D&isregularlink=1&biztype=UK&locale=en-GB&curr=GBP'

data = [] # [[time0, time1, price],[...]]

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

def get_time_and_price_data():
    """
    It looks at the website and searches the <span> and <h4> tags
    which contain the time and price of the journey respectively.
    Once the data is found, it changes the global variable 'data'
    by appending to it.
    """
    global data
    all_span_elements = driver.find_elements(By.TAG_NAME, 'span')
    
    all_pound_elements = [el for el in all_span_elements if '£' in el.text]
    actual_pound_elements = [el for el in all_pound_elements if el.value_of_css_property('color') == 'rgba(15, 41, 77, 1)']
    
    all_h4_elements = driver.find_elements(By.TAG_NAME, 'h4')
    all_time_elements = [el for el in all_h4_elements if ':' in el.text]
    time_elements_in_pairs = [[all_time_elements[i], all_time_elements[i + 1]] for i in range(0, len(all_time_elements), 2)]

    for i in range(len(actual_pound_elements)):
        data.append([time_elements_in_pairs[i][0].text,time_elements_in_pairs[i][1].text,actual_pound_elements[i].text])

def find_view_later_trains_btn():
    """
    Selenium locates the btn 'View later trains' which will allow me
    to load more train data to cover the whole day.
    """
    all_divs = driver.find_elements(By.TAG_NAME, 'div')
    _ = [el for el in all_divs if 'View later trains' in el.text]
    return list(filter(lambda el: len(el.text) < 19, _))[0]
    
try:
    driver.get(trip_com_q_string)
    
    time.sleep(3)
    
    get_time_and_price_data()

    while len(data) < 151:
        view_later_trains_btn = find_view_later_trains_btn()
        view_later_trains_btn.click()
        time.sleep(3)
        get_time_and_price_data()

    print(len(data))

    # assigning dates to the times and prices
    time0_list = [arr[0] for arr in data]
    dates = assign_dates(time0_list, future_date_at_6am)
    dates_as_strings = [date.strftime(f'%Y-%m-%d') for date in dates]

    # date will be inserted in the time_price data called 'data'
    for i in range(len(dates_as_strings)):
        data[i].insert(0, dates_as_strings[i])

    import json
    with open('data.json','w') as f:
        f.write(json.dumps(data, indent=2))
finally:
    driver.quit()