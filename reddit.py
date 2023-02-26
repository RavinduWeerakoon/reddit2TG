import praw
import telegram
import re
from const import *
from language_processing import is_question

reddit = praw.Reddit(
    client_id= reddit_client_id,  
    client_secret=reddit_client_secret,
    user_agent="Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
)




class RedditScraper():
    def __init__(self):
        self.reddit = reddit



    def get_hot(self,subreddit='GPT3', num=10):
        sub = self.reddit.subreddit(subreddit)
        return sub.hot(limit=num)



def parse_img_from_text(text):

    regex = r"https?://\S*"
    t = re.findall(regex, text)
    images = [url for url in t if "preview.redd.it" in url]
    for image in images:
        text = text.replace(image, "")
    images = [telegram.InputMediaPhoto(url) for url in images]
    return text, images

# def get_gallery_imgs(id):
#     r = requests.get(f"https://www.reddit.com/comments/{id}.json")
#     data = r.json()
#     print(type(data))

def markdown_to_html(text):

    #removing unnecassry tags

    text = re.sub(r'<(.*?)>', r'\1', text)
    text = re.sub(r'[<<`*_>>]', r'', text)
    #converting Hyperlinks
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    #convert codes
    text = re.sub(r'`(.)`', r'<code>\1</code>', text)

    #transform headlines
    text = re.sub(r'\*\*(.*)\*\*', r'<b>\1</b>', text)
    #converting points

    text = text.replace("*", '•')
    # #extra white spaces
    # text = text.replace("\n\n", '\n')
    return text




def check_question(submission):
    if not submission.is_self:
        return False 
    elif 'http' in submission.selftext:
        return False 
    flair = submission.author_flair_text
    if flair:
        if submission.author_flair_text.lower() == "help":
            print(f"{submission.id} removed")
            return True 

    if is_question(submission.title):
        if is_question(submission.selftext):
            return True 
        elif len(submission.selftext)<500:
            return True

    return False
    