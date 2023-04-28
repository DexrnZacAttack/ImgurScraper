import os
import requests
import re
from bs4 import BeautifulSoup
import sys
sys.setrecursionlimit(999999)

# set the base URL of the forum
base_url = "https://sargunster.com/btwforum/viewtopic.php?t="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# set the starting topic ID to crawl
start_topic_id = 1000

# set the ending topic ID to crawl
end_topic_id = 10000

# create a file to store the links (if it doesn't exist)
links_file = "links.txt"
if not os.path.exists(links_file):
    with open(links_file, "w") as f:
        f.write("")

def crawl_topics(start_topic_id, end_topic_id):
    for topic_id in range(start_topic_id, end_topic_id + 1):
        # create a full URL by combining the base URL with the topic ID
        full_url = base_url + str(topic_id)
        
        # make a GET request to the topic page
        response = requests.get(full_url, headers=headers)

        # check if the topic exists
        if "The requested topic does not exist." in response.text:
            print(f"Topic {topic_id} does not exist.")
        else:
            # parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # find all img tags on the page
            img_tags = soup.find_all('img')

            # iterate over the img tags and save any direct image links to the file
            for img_tag in img_tags:
                src = img_tag.get('src')
                if src and 'imgur' in src and ('.jpg' in src or '.png' in src or '.gif' in src):
                    print("Found imgur link:", src)
                    # write the link to the file
                    with open(links_file, "a") as f:
                        f.write(src + "\n")

            # print the percentage of topics done
            percent_done = int((topic_id - start_topic_id + 1) / (end_topic_id - start_topic_id + 1) * 100)
            print(f"{percent_done}% done.", end="\r")

crawl_topics(start_topic_id, end_topic_id)
