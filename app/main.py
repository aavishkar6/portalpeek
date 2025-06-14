# Import Libraries
from apscheduler.schedulers.background import BackgroundScheduler
import json


# Import required modules
from .scraper.scraper import scrape_portal
from .llm.llm import categorize_using_llm
from .db.db import save_announcements_to_database


def scrape_job():

  # Notify Admin about the scraping.
  # Import email service and send appropriate email to the user.

  # Scrape the portal.
  announcements = scrape_portal(production = True, save_to_file = True, num_of_days = 50)

  # categorize data using a llm.
  # Needs to filter previous announcements since they have already been categorized.
  categorized_data = categorize_using_llm(announcements)

  # save data into database.
  save_announcements_to_database(categorized_data)


# Pass the data onto the llm to get the category for the announcements.

# Save the data in the database along with the categories returned by the llm.

# Trigger email service module to make sure it is scheduled and is sent.


if __name__ == "__main__":

    # scheduler = BackgroundScheduler()

    # # Schedule scraper every 5 minutes.
    # scheduler.add_job(scrape_job, "interval", minutes=5)

    # # Add another job to the background that sends email
    # # scheduler.add_job(send_email, "interval", minutes=1)

    # scheduler.start()

    # print("Scheduler started...")
    # try:
    #     while True:
    #         pass
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()

    scrape_job()