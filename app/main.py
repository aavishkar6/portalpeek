# Import Libraries
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import timedelta, datetime, date
import time

# Import required modules
from .scraper.scraper import scrape_portal
from .llm.llm import categorize_using_llm, get_summary_announcements
from .db.db import save_announcements_to_database, get_db, find_documents, get_all
from .email_service.email_service import send_reminder_email, send_dynamic_email
from .config import Config

def scrape_job():
  # Scrape the portal.
  announcements = scrape_portal(production = True, save_to_file = True, num_of_days = 50)

  # categorize data using llm.
  categorized_data = categorize_using_llm(announcements)

  # save data into database.
  save_announcements_to_database(categorized_data)


def send_email_reminder():
    """Sends email reminder to the admin to let them know about an upcoming scrape job.
      Requires Admin's attention for 2FA.
    """
    response_code = send_reminder_email(
        receipient_email=Config.receipient_email,
        subject = Config.reminder_email_subject,
        content = Config.reminder_email_content
    )
    
    print(f"Response code of the reminder email : {response_code}")

def send_email():
    """Sends the actual email to the subscribed users about their daily student portal
    Updates."""

    try:
      # Get date.
      date_today = date.today().strftime('%Y-%m-%d')
      print("Today's date is ", date_today)

      # Get all the documents where data is equal to date.
      announcements = find_documents(
          collection = get_db().announcements,
          query = {
              "date":"2025-06-13"
          }
      )

      announcements_list = "\n".join(str(a) for a in list(announcements))

      # Ask the LLM to get the summary of the announcements.
      summary = get_summary_announcements(announcements_list)

      # send email to users.
      users = get_all(
          collection = get_db().users
      )

      for user in users:
          # define a dynamic email.
          dynamic_template = {
              "receipient_name":user['name'],
              "portal_url": Config.PORTAL_WEBSITE,
              "date": date.today().strftime("%B %d, %Y"),
              "summary" : summary
          }

          send_dynamic_email(
            receipient_email=user['email'],
            subject = "Testing the first PortalPeek Updates: More such to come",
            dynamic_template=dynamic_template,
            template_id=Config.template_id
          )

          print(f"Email sent to {user['name']} with email {user['email']}")

          break


    except ValueError:
        print("Unable to send emails to users due to db issues.")


# Pass the data onto the llm to get the category for the announcements.

# Save the data in the database along with the categories returned by the llm.

# Trigger email service module to make sure it is scheduled and is sent.


if __name__ == "__main__":

    # Initialize scheduler.
    scheduler = BackgroundScheduler()

    # # Initialize multiple jobs.

    # # Scraping the portal.
    # scheduler.add_job(scrape_job, trigger=IntervalTrigger(hours=6), id="portal_scraper")

    # # Email reminder to let the admin know about scraping job.
    # reminder_time = datetime.now() + timedelta(hours=6) - timedelta(minutes=5)
    # scheduler.add_job(send_email_reminder, trigger=DateTrigger(run_date=reminder_time))

    # # Sending email updates each day.
    # scheduler.add_job(send_email, trigger=CronTrigger(hour=9, minute=0), id="job_daily")

    # scheduler.start()


    # Start now for reproducibility
    start_time = datetime.now()
    scrape_interval = timedelta(minutes=5)
    reminder_offset = timedelta(minutes=2)

    # 1. Initialize scheduler
    scheduler = BackgroundScheduler()

    # 2. Scraping job every 5 minutes
    scheduler.add_job(
        scrape_job,
        trigger=IntervalTrigger(minutes=4, start_date=start_time),
        id="portal_scraper"
    )

    # 3. Email reminder 1 minute BEFORE the first scrape
    scheduler.add_job(
        send_email_reminder,
        trigger=DateTrigger(run_date=start_time + scrape_interval - reminder_offset),
        id="scrape_reminder"
    )

    # 4. Send email update IMMEDIATELY after first scrape (i.e., 5 mins from now)
    scheduler.add_job(
        send_email,
        trigger=DateTrigger(run_date=start_time + scrape_interval),
        id="send_email"
    )

    # 5. Start scheduler
    scheduler.start()

    # Log all jobs for confirmation
    for job in scheduler.get_jobs():
      print(f"{job.id} scheduled at {job.next_run_time}")


    print("Scheduler started...")
    try:
        while True:
            # simulate some work being done.
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

    scrape_job()

    send_email()