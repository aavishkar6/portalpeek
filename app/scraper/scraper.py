# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Other imports
import time

from ..config import Config
from .utils import setup_driver, scrape_student_portal

def scrape_portal(production: bool = False, save_to_file: bool = True, num_of_days: int = 50) -> list:
  try:
    # Setup the driver module. Production runs in headless mode
    driver = setup_driver(production = production)

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

    # Give time to approve the 2FA button.
    time.sleep(20)

    trust_button = driver.find_element(By.ID, "trust-browser-button")
    trust_button.click()
    print("Clicked duo trust the device button")

    print("Scraping the website now")

    wait = WebDriverWait(driver, 50)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

    element = wait.until(EC.presence_of_element_located((By.ID, "announceContainer")))

    try :
      load_more_button = element.find_element(By.CLASS_NAME, "load-more-btn")

      # Click on load more button 
      load_more_button.click()
    except Exception as e:
      print("Unable to find load more button. Moving on with scraping.")

    time.sleep(5)
    # scrape the information
    information = scrape_student_portal(driver, num_of_days, save_to_file)

    # print(information)

    print("scraping completed")

    driver.quit()

    return information

  except Exception as e:

    driver.quit()
    print(f"Exception occured: {e}")
    return ValueError