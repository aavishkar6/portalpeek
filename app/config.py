import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  PORTAL_WEBSITE = "https://students.nyuad.nyu.edu"
  NYU_USERNAME = os.getenv("USERNAME")
  NYU_PASSWORD = os.getenv("PASSWORD")
  MONGO_URI = os.getenv("MONGODB_PASSWD")
  MONGO_PASSWORD = os.getenv("MONGO_URI")
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
  sender_email = "aavishkargautam@gmail.com"
  receipient_email = "ag8298@nyu.edu"


  # Configurations about the email service.
  reminder_email_subject = "Scraping job starts in 5 minutes."
  reminder_email_content = "Hey there. The scraping job is about to start in 5 minutes." \
  "Make sure you are there to authorize the 2FA."
  template_id = "d-160958b06b8d4812b18dbaf621882b2a"



  