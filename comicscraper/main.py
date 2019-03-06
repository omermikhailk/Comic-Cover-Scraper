#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests

# Gets the source HTML for the 3rd Batman volume
source = requests.get("https://dc.fandom.com/wiki/Batman_Vol_3").text
soup = BeautifulSoup(source, "lxml")


# Finds the anchor tags of the unordered list elements
issue_list = soup.find("div", id="mw-content-text")
issue_list = issue_list.find("ul").find_all("a")


# Constructs a list of URLs from the list of issues and their
# anchor tags
issue_urls = [anchorlink["href"] for anchorlink in issue_list]
base_site_url = "https://dc.fandom.com"
# Adds the base url of DC fandom to the individual issue
# URLs so that the resulting URL is a valid one
for i in range(0, len(issue_urls)):
    issue_urls[i] = base_site_url + issue_urls[i]

# Loops through each URL and downloads the image from it
for indiv_url in issue_urls:
    indiv_url_source = requests.get(indiv_url).text
    indiv_soup = BeautifulSoup(indiv_url_source, "lxml")
    img_url = indiv_soup.find("img", class_="pi-image-thumbnail")["src"]

    requests_img_url = requests.get(img_url)

    issue_title = indiv_soup.title.string.split("|")[0].rstrip()
    file_name = "_".join(issue_title.split())

    with open(f"covers/{file_name}.jpg", "wb") as f:
        f.write(requests_img_url.content)
