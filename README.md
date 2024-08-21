# reddit2TG


This bot requires 2 api keys

 1. Telegram API key
 2. Reddit Api Key


To have the Reddit API key  follow  [here](https://www.reddit.com/prefs/apps)
 A guide can be found on [here](https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/)

Then rename the `const.py.example` to `const.py` and update the API keys
Install dependencies:
```pip install -r requiremets.txt```
Then run bot.py


Features
--------

-   **Fetch Hot Posts:** Retrieves the latest hot posts from a specified subreddit.
-   **Filter Posts:** Ignores stickied posts and those formatted as questions.
-   **Post to Telegram:** Automatically posts images, text, and links to a Telegram channel.
-   **Error Handling:** Ensures smooth operation by updating the database in case of sudden failures.
-   **NLP-based Filtering:** Ensures the messages are filtered through the NLTK library and appropriate messages are forwarded.

Code Overview
-------------

-   **RedditScraper:** Handles fetching hot posts from Reddit.
-   **send_images:** Manages the sending of images to the Telegram channel.
-   **hot:** Main function to fetch and post new hot posts.
-   **error_handler:** Updates the database in case of errors
  
