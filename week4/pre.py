import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Download NLTK resources (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# Initialize the Porter stemmer
stemmer = PorterStemmer()

# Get the list of English stop words
stop_words = set(stopwords.words('english'))

def preprocess_documents(documents):
    preprocessed_documents = []

    for doc in documents:
        # Tokenize the document
        tokens = word_tokenize(doc)
        
        # Stem the tokens
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        
        # Remove stop words
        filtered_tokens = [token for token in stemmed_tokens if token.lower() not in stop_words]
        
        # Join the filtered tokens back into a single string
        preprocessed_doc = ' '.join(filtered_tokens)
        
        # Append the preprocessed document to the list
        preprocessed_documents.append(preprocessed_doc)

    return preprocessed_documents

