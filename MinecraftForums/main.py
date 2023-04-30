import requests
from bs4 import BeautifulSoup

# Print GitHub link so people can report issues or visit the repo.
print('https://github.com/DexrnZacAttack/ImgurScraper')

# Set the base URL of the Minecraft Forum search page
base_url = 'https://www.minecraftforum.net/forums/search?display-type=0&forum-scope=f&page={}&search=imgur&search-type=2&submit=y'

# Open a text file called "links.txt" in write mode
with open('links.txt', 'w') as f:

    # Loop through the first 5 pages of search results
    for page_num in range(1, 35):

        # Construct the URL of the search results page to scrape
        url = base_url.format(page_num)
        print(url)

        # Send a GET request to the URL and store the HTML response
        response = requests.get(url)
        html = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find all <img> tags with a "src" attribute containing "imgur.com"
        img_tags = soup.find_all('img', {'src': lambda x: 'imgur.com' in x})

        # Extract the "src" attribute from each <img> tag and store it in a list
        img_urls = [tag['src'] for tag in img_tags]

        # Write each image URL to the text file, one per line
        for url in img_urls:
            f.write(url + '\n')
