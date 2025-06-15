from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from ..config import Config
from ..db.db import get_identifiers, get_db, find_documents


from datetime import date

from hashlib import sha256

import warnings
warnings.filterwarnings("ignore")

# Initialize the chat model
llm = ChatOpenAI(
    model_name = "gpt-3.5-turbo",
    openai_api_key = Config.OPENAI_API_KEY
)

prompt = """
Classify the following announcement into one of these categories. Return only the category in your response.
On-Campus Job, Research program, Grad School Announcement, On-Campus Announcements, Research Participation,
Technical Issues, or Miscellaneous:
"""
def classify(announcement : object) -> str :
    # Format the announcement as text
    announcement_text = f"""
        Title: {announcement['title']}
        Category: {announcement['category']}
        Description: {announcement['description']}
        Topic: {announcement['topic']}
        Date: {announcement['date']}
        Posted By: {announcement['posted_by']}
    """

    # Construct the messages for the chat model
    messages = [
        SystemMessage(content="You are a helpful assistant for classifying announcements."),
        HumanMessage(content=prompt + announcement_text)
    ]

    # Get the response from the chat model
    response = llm(messages)

    return response.content

def categorize_using_llm(announcements: list) -> list:
    # print(f"announcements is {announcements}")

    identifiers = get_identifiers(get_db().announcements)
    for announcement in announcements:
        # Check if the announcement is already in the db.
        # 1. Get all the identifiers from the db.
        # 2. If the identifier of this announcements is in the db, skip, else classify

        identifier = sha256(f"{announcement['date']}{announcement['title']}".encode()).hexdigest()

        if identifier in identifiers:
            print(f"Announcement already in the db. Announcement has title {announcement['title']}")
            continue

        # returns a llm response
        category = classify(announcement)

        # Add another key to the announcement to the object
        announcement["announcement_type"] = category

    return announcements


def get_summary_announcements(announcements):
    prompt = """ You are given a list of announcements. You need to summarize them and 
    highlight important points so that a user would be able to read the summary 
    and get a sense of all the announcements. You can be creative in summarizing the text. 
    Make sure the summary covers all of the announcements.
    """

    # Construct the messages for the chat model
    messages = [
        SystemMessage(content="You are a helpful assistant for classifying announcements."),
        HumanMessage(content=prompt + announcements)
    ]

    # Get the response from the chat model
    response = llm(messages)

    return response.content



if __name__ == "__main__":
    
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

    print(announcements)

    announcements_list = "\n".join(str(a) for a in list(announcements))
    print(announcements_list)

    # Ask the LLM to get the summary of the announcements.
    summary = get_summary_announcements(announcements_list)


    print(summary)