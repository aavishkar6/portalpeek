from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

def setup_driver(production : bool = False) -> webdriver.Chrome:
    # Set up ChromeOptions for headless mode and other arguments
    chrome_options = webdriver.ChromeOptions()

    if production:
        # Run headless (no browser UI)
        chrome_options.add_argument("--headless")

        # Disable GPU acceleration (recommended for headless)
        chrome_options.add_argument("--disable-gpu")

        # Disable browser sandboxing (useful for some server environments)
        chrome_options.add_argument("--no-sandbox")

        # Disable dev-shm-usage for limited shared memory environments
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Optionally, add user-agent string to avoid detection (optional but useful)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        chrome_options.add_argument("--enable-javascript")

    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return driver

def remove_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def scrape_student_portal(driver : webdriver.Chrome, num_of_days: int, save_to_file : bool) -> list:
    """ count_max limits the number of days to scrape."""

    html_content = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the container that holds the announcements
    announce_container = soup.find(id="announceContainer")

    announcements = []

    count = 1
    for section in announce_container.find_all('section'):
        date = section['data-date']
        ul = section.find('ul')

        try:
            for li in ul.find_all('li', class_='announcement'):
                # Extract the title
                title_tag = li.find('a')
                title = title_tag.get_text(strip = True)

                # Extract the description
                description_tag = li.find('div', class_='details')
                description = description_tag.get_text(strip=True) if description_tag else ""

                # Remove the last few words from the description.
                desc = description.split("Category")[0].strip()

                # This is a way to get the name of the person who posted the announcement from the desciption.
                posted_by = description.split('Posted by:')[1].split('Permalink')[0]

                # Extract the topic (inside <li class="topic">)
                topic_tag = li.find('li', class_='topic')
                topic = topic_tag.get_text(strip=True).replace('Topic:', '') if topic_tag else ""
                
                # Extract the category (inside <li class="category">)
                category_tag = li.find('li', class_='category')
                category = category_tag.get_text(strip=True).replace('Category:', '') if category_tag else ""

                announcement = {
                    "title": remove_whitespace(title),
                    "category": remove_whitespace(category),
                    "description": remove_whitespace(desc),
                    "topic": remove_whitespace(topic),
                    "date": remove_whitespace(date),
                    "posted_by": remove_whitespace(posted_by)
                }

                # Append the announcement to the list
                announcements.append(announcement)
        except Exception as e:
            print("Error occured ", e )
    
        if count >= num_of_days:
            break
        count += 1

    # Write to file if True
    if save_to_file:
        json_data = json.dumps(announcements, indent=4)

        # Define unique filename based on current time of scraping.
        file_name = f"announcements_{str(datetime.now())}.json"
        file_path = f"./announcements_json/{file_name}"

        with open(file_path, 'w') as f:
            f.write(json_data)

    return announcements