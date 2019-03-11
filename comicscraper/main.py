#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import requests


def main():
    url = desired_user_url()

    # Gets the source HTML for the user-inputted DC wiki url
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")

    list_of_issue_urls = get_issue_list_links(soup)
    image_downloader(list_of_issue_urls)


def desired_user_url():
    """
    Gets the user input for what URL they would like to visit
    and get the comic cover images from.

    It will then also validate the URL.

    It then returns this URL as a string if it is valid, otherwise
    it will repeat until it receives a valid URL.
    """
    while True:
        input_msg = ("Please enter the URL for your comic page, it must be a"
                     " DC Wiki page.\nURL: ")
        url = input(input_msg)

        request = requests.get(url)
        if request.status_code == 200:
            # Means that the URL exists
            return url
        # Otherwise the loop will keep on repeating until
        # it receives a valid URL
        print("\nYou did not enter a valid URL, please try again.\n\n")
        continue


def get_issue_list_links(soup_object):
    """
    Takes in the predefined soup_object as input and then uses that
    to do the tasks below

    Finds the anchor tags of the unordered list elements.
    Then construcsts a list of URLs from the list of issues and their
    anchor tags.

    Then it adds the base URL of DC Wikia to the list of issue URLs.

    It then returns these URLs as a list.
    """
    issue_list = soup_object.find("div", id="mw-content-text")
    issue_list = issue_list.find("ul").find_all("a")

    # Makes a list of the issue_urls
    issue_urls = [anchorlink["href"] for anchorlink in issue_list]
    # Adds the base URL to each element in the list of issue URLs
    base_site_url = "https://dc.fandom.com"

    for i in range(0, len(issue_urls)):
        issue_urls[i] = base_site_url + issue_urls[i]

    return issue_urls


def image_downloader(issue_urls):
    """
    Loops through each URL in the list of article URLs,
    then it downloads the image from each URLself.

    The images are then saved in the covers/ directory.
    """
    for indiv_url in issue_urls:
        indiv_url_source = requests.get(indiv_url).text
        indiv_soup = BeautifulSoup(indiv_url_source, "lxml")
        img_url = indiv_soup.find("a", class_="image image-thumbnail")["href"]

        requests_img_url = requests.get(img_url)

        issue_title = indiv_soup.title.string.split("|")[0].rstrip()
        file_name = "_".join(issue_title.split())

        with open(f"covers/{file_name}.jpg", "wb") as f:
            f.write(requests_img_url.content)


if __name__ == "__main__":
    main()
