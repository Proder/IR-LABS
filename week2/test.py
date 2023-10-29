from elasticsearch import Elasticsearch
import mailbox

# Connect to your local Elasticsearch instance
es = Elasticsearch(host='localhost', port=9200, scheme='http', timeout=30)
# es = Elasticsearch(hosts=['http://localhost:9200'], http_auth=('elasticsearch', 'fp0cWSQvIzUE2wgb+onv'))


# Specify the path to your mbox file
mbox_file_path = r'C:\Users\Dell\Downloads\takeout-20231025T134216Z-002\mail.mbox'

# Create an index for your emails
index_name = 'emails'

# Check if the index already exists, and if not, create it
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# Parse the mbox file
mbox = mailbox.mbox(mbox_file_path)

# Iterate through each email and index it
for idx, email in enumerate(mbox):
    # Extract email fields
    subject = email['subject']
    content = email.get_payload()

    # Create a document for indexing
    doc = {
        'subject': subject,
        'content': content
    }

    # Index the email
    es.index(index=index_name, id=idx + 1, body=doc)

# Confirm that indexing is complete
print(f"Indexed {idx + 1} emails in the '{index_name}' index.")


