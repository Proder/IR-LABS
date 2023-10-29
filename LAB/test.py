from elasticsearch import Elasticsearch
import os

# Initialize Elasticsearch client
es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "DGwhdf6JaNY8eCtpF5OS"))

# Define the folder containing your email .txt files
email_folder = "C:\\INSTTUTE\\Languages\\Python\\IR\\LAB3\\email"

# Define the mapping for the index
mapping = {
    "mappings": {
        "properties": {
            "subject": {
                "type": "text",
            },
            "from": {
                "type": "text"
            },
            "to": {
                "type": "text"
            },
            "cc": {
                "type": "text"
            },
            "reply-to": {
                "type": "text"
            },
            "body": {
                "type": "text"
            }
        }
    }
}

# Check if the index exists, and delete it if it does
index_name = "email_index"  # Customize the index name
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Create the index with the specified mapping
es.indices.create(index=index_name, body=mapping)

# Iterate through the .txt files in the folder and index them
for root, dirs, files in os.walk(email_folder):
    for file in files:
        email_path = os.path.join(root, file)

        try:
            # Read the content of the .txt file
            with open(email_path, 'r', encoding='utf-8') as email_file:
                email_content = email_file.read()

                # Split the email content into lines
                lines = email_content.split('\n')
                subject = ""
                sender = ""
                recipient = ""
                cc = ""
                reply_to = ""
                body = []

                for line in lines:
                    if line.startswith('Subject:'):
                        subject = line[8:].strip()
                    elif line.startswith('From:'):
                        sender = line[5:].strip()
                    elif line.startswith('To:'):
                        recipient = line[3:].strip()
                    elif line.startswith('Cc:'):
                        cc = line[3:].strip()
                    elif line.startswith('Reply-to:'):
                        reply_to = line[9:].strip()
                    else:
                        body.append(line)

                # Join body lines into a single text
                body_text = '\n'.join(body)

                # Create the document
                document = {
                    "subject": subject,
                    "from": sender,
                    "to": recipient,
                    "cc": cc,
                    "reply-to": reply_to,
                    "body": body_text
                }

                # Index the document
                res = es.index(index=index_name, body=document)
                print(f"Indexed .txt file: {email_path}")
        except Exception as e:
            print(f"Error processing .txt file: {email_path} - {e}")

# Refresh the index to make the documents immediately available for search
es.indices.refresh(index=index_name)
