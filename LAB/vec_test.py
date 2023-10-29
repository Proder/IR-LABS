import gensim
from elasticsearch import Elasticsearch
from gensim.models import KeyedVectors
from sklearn.datasets import fetch_20newsgroups

# Load the dataset
newsgroups = fetch_20newsgroups(subset='all')

# Preprocess the documents
preprocessed_docs = []
for doc in newsgroups.data:
    # Tokenize the document
    tokens = gensim.utils.simple_preprocess(doc.lower())
    # Remove stop words and stem the tokens
    stemmed_tokens = [gensim.parsing.porter.PorterStemmer().stem(token) for token in tokens if token not in gensim.parsing.preprocessing.STOPWORDS]
    # Join the stemmed tokens back into a string
    preprocessed_doc = ' '.join(stemmed_tokens)
    preprocessed_docs.append(preprocessed_doc)

#  model
model = KeyedVectors.load_word2vec_format('C:/Users/Dell/Downloads/GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)


# Initialize Elasticsearch client with URL
es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "sTyuyUy3Usw7igqaIJ0j"))


# Delete the index if it already exists
index_name = 'vec'
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Create index with appropriate mappings
index_mappings = {
    'mappings': {
        'properties': {
            'text': {
                'type': 'text'
            },
            'vector': {
                'type': 'dense_vector',
                'dims': 300
            }
        }
    }
}
es.indices.create(index=index_name, body=index_mappings)

# Iterate over preprocessed documents and generate vectors
for i, doc in enumerate(preprocessed_docs):
    # Split the preprocessed document into tokens
    tokens = doc.split()
    # Generate the vector for the document by averaging the vectors of its tokens
    vector_sum = 0
    count = 0
    for token in tokens:
        if token in model.wv:
            vector_sum += model.wv[token]
            count += 1
    if count > 0:
        vector = vector_sum / count
        # Store the document and its vector in the Elasticsearch index
        es.index(index=index_name, id=i, body={'text': doc, 'vector': vector.tolist()})