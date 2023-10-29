import os
from pre import preprocess_documents

# Replace 'path_to_documents' with the actual path to your extracted documents
path_to_documents = 'data/20_newsgroups/'

# Initialize an empty list to store the documents
documents = []

# Iterate through the directories and files in the corpus
for root, dirs, files in os.walk(path_to_documents):
    for file_name in files:
        # Create the full path to the file
        file_path = os.path.join(root, file_name)
        
        # Read the content of the file
        with open(file_path, 'r', encoding='latin-1') as file:
            document_content = file.read()
            documents.append(document_content)

# Preprocess the documents
preprocessed_documents = preprocess_documents(documents)

# Now, 'preprocessed_documents' contains the preprocessed text of the 20 Newsgroups corpus
