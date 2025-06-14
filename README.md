# Logs of my development process

## Day 1 - Jan 22, Wednesday

  1. Defined the directory structure and seperated folders into different modules. I knew what schemas were but now I understand that they are. **Schemas** are predefined data models that define the type, structure, and validity of the data. Whether it is a API request or a response, we can define a schema to ensure data consistency, data validity, and data predictability across our code.
  2. I migrated the scraper from another repo to this repo. Cleaned it and refactored it a bit.
  
## Day 2 - Jan 25, Saturday
  
  1. Used Mongodb for storing announcements.
  2. Integrated LLM for classfying announcements into one of several types.
  3. Integrated Scheduler to schedule the scraping task.

## To be completed

    - Preprocess the announcements to reduce the number of llm calls and reduce cost. Right now, every scraped announcement is going to the llm for categorization even though it has already been categorized.
    - Add a email service and define a email template to send to the users for sending out the announcements.
    - Define database for handling user info and a backend for API to interact with the front-end.
    - 