import requests
import os
from bs4 import BeautifulSoup
import sys
sys.path.append('../common')
from cleanup import cleanup

# Print GitHub link so people can report issues or visit the repo.
print('https://github.com/DexrnZacAttack/ImgurScraper')

# Set the base URL of the FeedTheBeast search page
base_url = 'https://forum.feed-the-beast.com/search/2709865/?page={}&q=imgur&o=date'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Loop through the pages of search results
for page_num in range(1, 10):
    
    print("Page num: " + str(page_num))
    # Construct the URL of the search results page to scrape
    url = base_url.format(page_num)

    # Send a GET request to the URL and store the HTML response
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all links with the class of "title"
    # Find all h3 elements with the class of "contentRow-title"
    h3s = soup.find_all('h3', class_='contentRow-title')

    # Loop through the h3 elements and visit each one to scrape for Imgur links
    for h3 in h3s:
        link = h3.find('a')
        link_url = link.get('href')
        link_response = requests.get("https://forum.feed-the-beast.com" + link_url, headers=headers)
        link_html = link_response.text
        link_soup = BeautifulSoup(link_html, 'html.parser')
        imgur_links = link_soup.find_all('a', href=lambda href: href and 'i.imgur' in href)
        for imgur_link in imgur_links:
            # Extract only the URL from the full link and cut off anything before "http"
            url = imgur_link.get('href')
            if url.endswith(('.png', '.jpg', '.gif')):
                url = url[url.find('http'):]
                url = url[:url.find('.')] + url[url.find('.'):]
                with open('links.txt', 'a') as f:
                    f.write(url + '\n')
                    print(url)

cleanup(os.path.abspath('.') + 
"links.txt")