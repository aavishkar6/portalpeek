# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

# Other imports
import time
import os

from ..config import Config
from .utils import setup_driver, scrape_student_portal

# Setup the driver module. Production runs in headless mode
driver = setup_driver(production = False)

print("opening the URL")
# Go to the site
driver.get(Config.PORTAL_WEBSITE)

# Add username and password to the site
username_input = driver.find_element(By.ID, 'username')
username_input.send_keys(Config.NYU_USERNAME)

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys(Config.NYU_PASSWORD)

# Locate the button by name or other attributes as needed and click it
button = driver.find_element(By.NAME, "_eventId_proceed")
button.click()

print("Logging in")

time.sleep(20)

trust_button = driver.find_element(By.ID, "trust-browser-button")
trust_button.click()
print("Clicked duo trust the device button")

print("Scraping the website now")

wait = WebDriverWait(driver, 30)
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

element = wait.until(EC.presence_of_element_located((By.ID, "announceContainer")))

load_more_button = element.find_element(By.CLASS_NAME, "load-more-btn")

load_more_button.click()

time.sleep(5)
# Click on load more button 
# scrape the information
information = scrape_student_portal(driver, count_max=100)

# print(information)

print("scraping completed")

driver.quit()