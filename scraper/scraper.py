#!/usr/bin/python3

"""
Parser makes use of lxml to parse the HTML for faster results:

    pip install lxml


Output is a JSON file, as an array of the following objects:
{
    url: URL of the news article
    title: Article title
    date: Date of the article
    author: Article author's name
    tags: Array of the tags indicated in the article
    contents: Raw HTML of the article body's text elements
}
"""

import json
import requests
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

current_url = "https://thehackernews.com/search/label/Cyber%20Attack"
scrape = []


def parse_article(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    title_tag = soup.find("h1", class_="story-title").a
    title = title_tag.get_text()

    blog_body = soup.find("div", id="Blog1")

    author_text = blog_body.find("span", class_="p-author").find_all("span", class_="author")
    date    = author_text[0].get_text() # Don't know if any special formatting is expected, so we store the undoctored text for now
    author  = author_text[1].get_text()

    tags = []
    tags_span = blog_body.find("span", class_="p-tags")
    if tags_span != None:
        tags_text = tags_span.get_text()
        tags = tags_text.split(" / ")
    else:
        print("WARNING: Tags not found.")

    contents = ""
    contents_body = blog_body.find("div", id="articlebody")
    for child in contents_body.children:
        if child.name != "div" and child.name != "meta" and child.name != "script":
            contents += str(child)

    scrape.append({
        'url': url, 
        'title': title, 
        'date': date, 
        'author': author, 
        'tags': tags, 
        'contents': contents
    })


if len(sys.argv) < 3:
    print("Usage: scraper.py [url] [output_filename]")
    quit(2)

#current_url = sys.argv[1]

while True:
    page = requests.get(current_url)
    soup = BeautifulSoup(page.content, "lxml")
    
    base_div = soup.find("div", id="Blog1")
    base_div = base_div.find("div", class_="blog-posts")
    articles = base_div.find_all("div", class_="body-post")

    if len(articles) == 0:
        break

    for article in articles:
        link = article.find("a", class_="story-link")
        url = urlparse(link["href"])

        if url.hostname != "thehackernews.com":
            continue

        parse_article(link["href"])
        print(link["href"])

    next_page = soup.find("a", id="Blog1_blog-pager-older-link")
    current_url = next_page["href"]


with open(sys.argv[2], "w") as file:
    file.write(json.dumps(scrape, indent=4))
