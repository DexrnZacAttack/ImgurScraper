import praw
import os

# Set up the Reddit instance and the subreddit to scrape
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID_HERE',
                     client_secret='YOUR_CLIENT_SECRET_HERE',
                     user_agent='imgurscraper by v1.0 by /u/ZacAttackedYou)')
subreddit = reddit.subreddit('minecraft')
posts = subreddit.new(params={'sort': 'old'})


os.system('cls')
print('r/Minecraft')
os.system('echo.')
print('[--------------------]')


with open('links-rMinecraft.txt', 'a') as f:
    for post in posts:
        if 'imgur.com' in post.url:
            f.write(post.url + '\n')



os.system('cls')
print('r/GoldenAgeMinecraft')
os.system('echo.')
print('[==========----------]')

# Set up the Reddit instance and the subreddit to scrape
subreddit = reddit.subreddit('GoldenAgeMinecraft')
posts = subreddit.new(params={'sort': 'old'})

# Open the file for writing
with open('links-rGoldenAgeMinecraft.txt', 'a') as f:
    for post in posts:
        if 'imgur.com' in post.url:
            f.write(post.url + '\n')


os.system('cls')
print('Complete')
os.system('echo.')
print('[====================]')