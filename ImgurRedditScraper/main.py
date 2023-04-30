import praw
import os
import re
from bs4 import BeautifulSoup
import atexit

# Print GitHub link so people can report issues or visit the repo.
print('https://github.com/DexrnZacAttack/ImgurScraper')


# Set up the Reddit instance and the subreddit to scrape
reddit = praw.Reddit(client_id='vYeGNSLN1VqcxvRvolu4Bw',
                     client_secret='81SufJbzWWdFLg60cUiupfZegGpz3w',
                     user_agent='imgurscraper by v1.0 by /u/ZacAttackedYou)')
subreddit = reddit.subreddit('minecraft')

# Open file for writing
f = open('links.txt', 'a')

def write_to_file():
    f.close()

atexit.register(write_to_file)

# Iterate over the submissions in the subreddit
for submission in subreddit.new(limit=100000):
    # Check if the submission is a link post and if it links to Imgur
    if submission.is_self == False and 'imgur.com' in submission.url:
        # Write the Imgur link to the file
        f.write(submission.url + '\n')

# Define the query string
query = "imgur"

for submission in subreddit.search(query, sort="old", limit=1000):
    if submission.is_self == False and 'imgur.com' in submission.url:
        f.write(submission.url + '\n')
    if submission.is_self == True and submission.selftext_html is not None:
        soup = BeautifulSoup(submission.selftext_html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and 'imgur.com' in href:
                f.write(href + '\n')
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        soup = BeautifulSoup(comment.body_html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and 'imgur.com' in href:
                f.write(href + '\n')
