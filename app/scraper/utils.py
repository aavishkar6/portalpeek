from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import json
import re
from bs4 import BeautifulSoup

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

def remove_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def scrape_student_portal(driver, count_max = 5):
    html_content = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the container that holds the announcements
    announce_container = soup.find(id="announceContainer")

    # Initialize the result dictionary
    result = {}

    count = 1

    for section in announce_container.find_all('section'):
        announcements = []
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

                # Construct the JSON object for the announcement
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
    
        result[date] = announcements

        if count >= count_max:
            break
        count += 1

    # Convert the list to JSON format
    json_data = json.dumps(result, indent=4)

    # Optionally, write the JSON data to a file
    with open('announcements.json', 'w') as f:
        f.write(json_data)

    return json_data