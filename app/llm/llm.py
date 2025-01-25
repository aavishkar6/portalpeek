from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from ..config import Config

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
    
    for announcement in announcements:
        # returns a llm response
        category = classify(announcement)

        # Add another key to the announcement to the object
        announcement["announcement_type"] = category

    return announcements









if __name__ == "__main__":
    duplicate = {
        "title": "Study Away Course Alternate Proposals",
        "category": "News & Information",
        "description": "If you submitted a proposal that is pending a final decision, please be sure to have a backup enrollment plan in place in case the course is not approved as proposed or a decision is not made before the end of add/drop. Although every effort is made to review courses timely, the review process can take several weeks. You will be notified by email when a decision is made. Proposals should be submitted at least three weeks before the start of registration to allow time for schedule adjustments and/or further proposals. Course alternates are reviewed and updated regularly. Please check frequently as you plan your study away.",
        "topic": "Registrar",
        "date": "2025-01-24",
        "posted_by": "Monique Hassan"
    }

    # Pass the announcement to the function
    response = classify(duplicate)

    # Print the classification response
    print(response)
