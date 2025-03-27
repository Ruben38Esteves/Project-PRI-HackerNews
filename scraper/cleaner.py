#!/usr/bin/python3

import datetime
import json
import sys
from scraper.text_optimizer import clean_string
from scraper.NER import process_articles

from bs4 import BeautifulSoup

data = None

named_entities = None



if len(sys.argv) < 3:
    print("Usage: cleaner.py [input_filename] [output_filename]")
    quit(2)

with open(sys.argv[1], "r") as file:
    data = json.load(file)

# Extra: check for which tags are used in the article body
print("Getting tags used in content...")
tags = set()
for obj in data:
    soup = BeautifulSoup(obj["contents"], "lxml")
    for element in soup.find("body").children:
        tags.add(element.name)
print(tags)

# Parse contents into actual text
print("Turning contents HTML into plain text...")
for obj in data:
    content_text = ""
    soup = BeautifulSoup(obj["contents"], "lxml")
    for element in soup.find("body").children:
        match element.name:
            case "a":
                content_text += element.get_text() + '\n'
            case "b":
                content_text += element.get_text()
            case "blockquote":                      # Contains a quote, so denote them with ""s. No cite attributes were found.
                content_text += '"' + element.get_text() + '"\n'
            case "br":
                content_text += '\n'
            case "center":                          # Used once to embed a Flash file, scrap it.
                pass
            case "h2":
                content_text += element.get_text() + '\n'
            case "h3":
                content_text += element.get_text() + '\n'
            case "h4":
                content_text += element.get_text() + '\n'
            case "noscript":
                pass
            case "ol":                              # Ordered list, so get all those elements:
                items = element.find_all("li")
                content_text += '\n'
                for i in range(0, len(items)):
                    content_text = str(i) + '- ' + items[i].get_text() + '\n'
            case "p":
                content_text += element.get_text() + '\n'
            case "pre":
                content_text += element.get_text() + '\n'
            case "section":                         # Only one section spotted and it was an ad, so scrap it.
                pass
            case "span":                            # Used for superscript links, scrap it.
                pass
            case "strong":                          # Plain text, so just use the unedited text.
                content_text += element.get_text()
            case "style":
                pass
            case "table":                           # Tables are used for images with captions. We don't scrape images, so scrap it.
                pass
            case "ul":
                items = element.find_all("li")
                content_text += '\n'
                for i in range(0, len(items)):
                    content_text += '- ' + items[i].get_text() + '\n'
    named_entities = process_articles(content_text, named_entities)
    content_text = clean_string(content_text,'NER.json')
    obj["contents"] = content_text
    obj["word_counts"] = named_entities

# Convert dates into a proper format
print(named_entities)
print("Converting dates to SQL friendly format...")
for obj in data:
    date_string = obj["date"]
    date = datetime.datetime.strptime(date_string, "%b %d, %Y")
    new_date_string = datetime.datetime.strftime(date, "%Y-%m-%d")
    obj["date"] = new_date_string

with open(sys.argv[2], "w") as file:
    file.write(json.dumps(data, indent=4))