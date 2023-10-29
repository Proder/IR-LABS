from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import random

# Initialize Elasticsearch client
es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "DGwhdf6JaNY8eCtpF5OS"))
index_name = "email_index"  # Customize the index name

# Specify the email address of the user you're interested in
user_email = "director@iiitvadodara.ac.in"

# Modify the Elasticsearch query to filter by the 'from' field
query = {"query": {"match": {"from": user_email}}}

# Extract the text from Elasticsearch
body_texts = []
res = es.search(index=index_name, body=query, scroll='1m', size=1000)
while len(res['hits']['hits']):
    body_texts.extend([doc['_source']['body'] for doc in res['hits']['hits']])
    res = es.scroll(scroll_id=res['_scroll_id'], scroll='1m')

# Initialize the language models
bigram_model = {}
trigram_model = {}

# Preprocess the text data
for text in body_texts:
    tokens = word_tokenize(text)
    bigrams = list(ngrams(tokens, 2))
    trigrams = list(ngrams(tokens, 3))

    # Update the language models with bigrams and trigrams
    for bigram in bigrams:
        prefix, suffix = bigram
        if prefix not in bigram_model:
            bigram_model[prefix] = []
        bigram_model[prefix].append(suffix)

    for trigram in trigrams:
        prefix, suffix = trigram[:2], trigram[2]
        if prefix not in trigram_model:
            trigram_model[prefix] = []
        trigram_model[prefix].append(suffix)

# Function to generate text using bigram model
def generate_bigram_text(bigram_model, seed_word, max_length=50):
    text = [seed_word]
    current_word = seed_word
    for _ in range(max_length - 1):
        if current_word not in bigram_model:
            break
        next_word = random.choice(bigram_model[current_word])
        text.append(next_word)
        current_word = next_word
    # Truncate the text if it exceeds the word limit
    if len(text) > max_length:
        text = text[:max_length]
    return " ".join(text)

# Function to generate text using trigram model
def generate_trigram_text(trigram_model, seed_words, max_length=50):
    text = list(seed_words)
    current_words = seed_words
    for _ in range(max_length - len(seed_words)):
        if current_words not in trigram_model:
            break
        next_word = random.choice(trigram_model[current_words])
        text.append(next_word)
        current_words = (current_words[1], next_word)
    # Truncate the text if it exceeds the word limit
    if len(text) > max_length:
        text = text[:max_length]
    return " ".join(text)

# Generate random text for a seed word
seed_word = "Dear"  # Change to your desired seed word
print("Generated Bigram Text:")
print(generate_bigram_text(bigram_model, seed_word, max_length=10))

# Generate random text for a seed prefix
seed_words = ("Sarat", "Kumar")  # Change to your desired seed prefix
print("\nGenerated Trigram Text:")
print(generate_trigram_text(trigram_model, seed_words, max_length=10))