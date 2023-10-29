# import os
# import numpy as np
# from gensim.models import KeyedVectors
# from elasticsearch import Elasticsearch

# # Specify the path to the root directory of the dataset
# dataset_path = "C:/INSTTUTE/Languages/Python/IR/LAB3/20news-19997/20_newsgroups"

# # List of category names (subdirectories in the dataset)
# categories = os.listdir(dataset_path)

# # Initialize lists to store documents and their corresponding labels
# documents = []
# labels = []

# # Iterate through each category
# for category_id, category in enumerate(categories):
#     category_path = os.path.join(dataset_path, category)

#     # Iterate through files in the category
#     for filename in os.listdir(category_path):
#         file_path = os.path.join(category_path, filename)
        
#         # Read the content of the file
#         with open(file_path, 'r', errors='ignore') as file:
#             content = file.read()

#         # Append the content to the documents list
#         documents.append(content)
#         labels.append(category_id)

# # Load the pre-trained word2vec model
# es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "DGwhdf6JaNY8eCtpF5OS"))

# # Define a function to generate a vector for a document
# def generate_vector(document):
#     # Split the document into words
#     words = document.split()

#     # Check if there are words in the document
#     if len(words) == 0:
#         # Return a zero vector or handle it as needed
#         return np.zeros(300)

#     # Initialize an empty vector
#     vector = np.zeros(300)

#     # Iterate through each word in the document
#     for word in words:
#         # Check if the word is in the word2vec model's vocabulary
#         if word in model.vocab:
#             # Add the word's vector to the document's vector
#             vector += model[word]

#     # Normalize the vector
#     vector /= len(words)

#     return vector


# # Generate a vector for each document
# vectors = [generate_vector(document) for document in documents]

# # Now, 'vectors' contains the vector for each document in the dataset.
# # You can store these vectors in Elasticsearch along with the documents and labels.
# # Here's an example of how to do that:

# # Create an Elasticsearch instance
# es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt",basic_auth=("elastic", " 0VJJ*mkTwphmq3jk406d"))

# # Define the index settings and mappings
# index_settings = {
#     "settings": {
#         "number_of_shards": 1,
#         "number_of_replicas": 0
#     },
#     "mappings": {
#         "properties": {
#             "content": {
#                 "type": "text"
#             },
#             "label": {
#                 "type": "keyword"
#             },
#             "vector": {
#                 "type": "dense_vector",
#                 "dims": 300
#             }
#         }
#     }
# }

# # Create the index with the defined settings and mappings
# es.indices.create(index="vec_index", body=index_settings)

# # Iterate through each document, label, and vector, and index them in Elasticsearch
# for document, label, vector in zip(documents, labels, vectors):
#     body = {
#         "content": document,
#         "label": categories[label],
#         "vector": vector.tolist()
#     }
#     es.index(index="vec_index",body=body)

import os
import numpy as np
import torch
from transformers import DistilBertModel, DistilBertTokenizer, Trainer, TrainingArguments
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor

# Specify the path to the root directory of the 20_newsgroups dataset
dataset_path = "C:/INSTTUTE/Languages/Python/IR/LAB3/20news-19997/20_newsgroups"

# List of category names (subdirectories in the dataset)
categories = os.listdir(dataset_path)

# Initialize lists to store documents and their corresponding labels
documents = []
labels = []

# Iterate through each category
for category_id, category in enumerate(categories):
    category_path = os.path.join(dataset_path, category)

    # Iterate through files in the category
    for filename in os.listdir(category_path):
        file_path = os.path.join(category_path, filename)

        # Read the content of the file
        with open(file_path, 'r', errors='ignore') as file:
            content = file.read()

        # Append the content to the documents list
        documents.append(content)
        labels.append(category_id)

# Load a pre-trained DistilBERT model
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertModel.from_pretrained(model_name)

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, documents):
        self.encodings = tokenizer(documents, return_tensors='pt', padding=True, truncation=True, max_length=512)

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

dataset = MyDataset(documents)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,  # new
    fp16=True,  # new
    evaluation_strategy="steps",
    save_steps=10_000,
    eval_steps=10_000,
    push_to_hub=False,
    report_to="none",
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Process documents and get BERT embeddings
document_embeddings = trainer.predict(dataset)

# Create an Elasticsearch instance
es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "DGwhdf6JaNY8eCtpF5OS"))

# Define the index settings and mappings
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text"
            },
            "label": {
                "type": "keyword"
            },
            "vector": {
                "type": "dense_vector",
                "dims": 768  # Dimensions of the BERT embeddings
            }
        }
    }
}

# Create the index with the defined settings and mappings
es.indices.create(index="vec_index", body=index_settings)

# Iterate through each document, label, and vector, and index them in Elasticsearch
for document, label, vector in zip(documents, labels, document_embeddings.predictions):
    body = {
        "content": document,
        "label": categories[label],
        "vector": vector.tolist()
    }
    es.index(index="vec_index", body=body)
