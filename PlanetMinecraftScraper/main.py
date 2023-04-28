import requests
from bs4 import BeautifulSoup

# Set the base URL of the PlanetMinecraft search page
base_url = 'https://www.planetminecraft.com/forums/search/?keywords=imgur&p={}'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Open a file for writing
with open('links.txt', 'w') as f:

    # Loop through the first 5 pages of search results
    for page_num in range(1, 5000):

        # Construct the URL of the search results page to scrape
        url = base_url.format(page_num)

        # Send a GET request to the URL and store the HTML response
        response = requests.get(url, headers=headers)
        html = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find all links with the class of "title"
        links = soup.find_all('a', class_='title')

        # Loop through the links and visit each one to scrape for Imgur links
        for link in links:
            link_url = link.get('href')
            link_response = requests.get(("https://www.planetminecraft.com" + link_url), headers=headers)
            link_html = link_response.text
            link_soup = BeautifulSoup(link_html, 'html.parser')
            imgur_links = link_soup.find_all('a', href=lambda href: href and 'imgur.com' in href)
            for imgur_link in imgur_links:
                f.write(imgur_link.get('href') + '\n')
