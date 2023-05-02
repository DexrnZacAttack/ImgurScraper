import requests
import os
import re
from bs4 import BeautifulSoup

imgur_regex = r'http[s]?://(?:.*\.)?imgur\.com/[^\s]+'

# Print GitHub link so people can report issues or visit the repo.
print('https://github.com/DexrnZacAttack/ImgurScraper' )

# Set the base URL of the Minecraft Forge Forums search page
base_url = 'https://forums.minecraftforge.net/search/?&q=imgur.com&page={}&quick=1&search_and_or=or&sortby=relevancy'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Open a file in append mode to store the links
with open('links.txt', 'a') as file:

    # Loop through the pages of search results
    for page_num in range(1, 42):

        print(f"Page num: {page_num}")
        # Construct the URL of the search results page to scrape
        url = base_url.format(page_num)

        # Send a GET request to the URL and store the HTML response
        response = requests.get(url, headers=headers)
        html = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find all instances of data <div data-searchable="" data-findterm=""> and print their contents
        for div in soup.find_all('div', {'data-searchable': True, 'data-findterm': True}):
            links = re.findall(imgur_regex, div.text)

            with open("links.txt", "a") as file:
                for link in links:
                    if link:  # only write non-empty items to the file
                        file.write(link + "\n")
                        print(f"Link found on page {page_num}: {link}")
