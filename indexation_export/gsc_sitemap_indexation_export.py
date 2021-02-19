import time
import pandas as pd
import sys
import csv
import yaml 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime

# Defines timestamp
now = datetime.now()
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

# Loads login credentials from .yaml located in root ~user folder
with open('../../security_check_auth.yaml') as f:
        credentials = yaml.load(f, Loader=yaml.FullLoader)
        send_username = credentials['send_username']
        send_password = credentials['send_password']
        jobs_username = credentials['jobs_username']
        jobs_password = credentials['jobs_password']

# Logs into Google Search Console
driver = webdriver.Chrome() # Opens browser
time.sleep(2)
driver.get('https://accounts.google.com/ServiceLogin?service=sitemaps&passive=1209600&continue=https://www.google.com/webmasters/tools/home?hl%3Den&followup=https://www.google.com/webmasters/tools/home?hl%3Den&hl=en') # Opens webmaster tools
time.sleep(2)
username_login = driver.find_element_by_id('identifierId') # Finds email login input
time.sleep(2)
username_login.send_keys(jobs_username) # Types email login, GSC will add '@gmail.com' to the end automatically, login loaded from .yaml
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()  # Submits login email
time.sleep(2)
username_password = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input') # Finds password login input
username_password.send_keys(jobs_password) # Types password loaded from .yaml
driver.find_element_by_xpath('//*[@id="passwordNext"]').click()  # Submits password
time.sleep(2)

# Opens Google Search Console "indexed and submitted" page and exports URL sample set for that week
driver.get('https://search.google.com/search-console/index/drilldown?resource_id=https%3A%2F%2Fwww.indeed.com%2F&item_key=CAESSWh0dHBzOi8vd3d3LmluZGVlZC5jb20vc2l0ZW1hcHMvc2VycHNpdGVtYXBpbmRleC11c19zZXJwc2l0ZW1hcF9pbmRleC54bWwYASAB&hl=en')
driver.find_element_by_class_name("izuYW").click() # Clicks EXPORT 
time.sleep(2)
driver.find_element_by_class_name('z80M1').click() # Clicks "Google Sheet" in drop down
time.sleep(15) # Gives browser enough time to populate sheet

# Confirms successful run of the script and prints datetime for cronlog
print("Google Sheet successfully generated ",current_datetime)
driver.quit()

