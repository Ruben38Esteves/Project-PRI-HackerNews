import json
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk
import os
import regex

nltk.download('stopwords')
nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))

stop_words.update(string.punctuation)

def process_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        titles = [article['title'] for article in data]
    return titles

json_files = ['scrape.json']

all_titles = []
for file in json_files:
    all_titles.extend(process_file(file))

words = []
for title in all_titles:
    tokens = word_tokenize(title.lower())
    tokens = [regex.sub(r"'s\b", "", word) for word in tokens]
    filtered_tokens = [word for word in tokens if word not in stop_words and word]
    words.extend(filtered_tokens)

word_counts = Counter(words)

most_common_words = word_counts.most_common(10)

words, counts = zip(*most_common_words)

plt.figure(figsize=(10, 5))
plt.bar(words, counts, color='blue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Most Used Words in Titles')
plt.show()