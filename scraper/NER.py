import json
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def count_words(text):
    doc = nlp(text)
    words = [ent.text for ent in doc.ents]
    return dict(Counter(words))

def process_articles(content_text, output_file):

    data = content_text

    # for article in data:
    #     contents = article.get('contents','')
    #     word_counts = count_words(contents)  #count_words(contents)
    #     article['word_counts'] = word_counts
    
    word_counts = count_words(data)

    #print(word_counts)
    return word_counts
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(word_counts, f, indent=4)






