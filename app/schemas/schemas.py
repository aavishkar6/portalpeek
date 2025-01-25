from pydantic import BaseModel


class Announcements:
  identifier: str
  date: str
  title: str
  description: str
  topic: str
  postedBy: str
