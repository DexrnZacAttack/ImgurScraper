import os
import re
import requests

jira_url = "https://bugs.mojang.com/"
search_url = f"{jira_url}rest/api/2/search"
headers = {
    "Accept": "application/json"
}

# create a file to store the links (if it doesn't exist)
links_file = "links.txt"
if not os.path.exists(links_file):
    with open(links_file, "w") as f:
        f.write("")

# search for issues containing "imgur" in the summary or description using the JIRA REST API
params = {
    "jql": 'summary ~ "imgur" OR description ~ "imgur"',
    "fields": "key"
}
response = requests.get(search_url, headers=headers, params=params)
data = response.json()
issues = data.get("issues", [])

# loop through each issue and search for imgur links in the comments
for issue in issues:
    issue_key = issue["key"]
    issue_url = f"{jira_url}browse/{issue_key}"
    # get the comments for the issue using the JIRA REST API
    comments_url = f"{jira_url}rest/api/2/issue/{issue_key}/comment"
    response = requests.get(comments_url, headers=headers)
    data = response.json()
    comments = data.get("comments", [])
    for comment in comments:
        for link in comment.get("body", "").split():
            if "imgur.com" in link:
                # strip out all characters that are not in URLs and square brackets
                link = re.sub(r"[^a-zA-Z0-9:/\.\[\]]", "", link)
                # cut off anything before the first occurrence of "http"
                imgur_url = re.sub(r".*?(http.*)", r"\1", link)
                # cut off anything after .png, .jpg, or .gif
                imgur_url = re.sub(r"(?<=\.(png|jpg|gif)).*", "", imgur_url)
                print(f"Found imgur.com in {imgur_url} in issue {issue_url}")
                with open(links_file, "a") as f:
                    f.write(f"{imgur_url}\n")
