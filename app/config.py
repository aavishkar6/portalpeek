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