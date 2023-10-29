from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "0VJJ*mkTwphmq3jk406d"))

# Index name
index_name = "emails"

# Search for documents in the index
search_body = {
    "query": {
        "match_all": {}  # Match all documents
    }
}

# Perform the search
response = es.search(index=index_name, body=search_body)

# Check if the search was successful
if response['hits']['total']['value'] > 0:
    print(f"Found {response['hits']['total']['value']} documents in the '{index_name}' index.")
    # You can also access the individual documents in response['hits']['hits']
else:
    print(f"No documents found in the '{index_name}' index.")



# CHECK WHETHER OR NOT INDEX EXISTS AND PERFORMING A SIMPLE QUERY ON IT 

# from elasticsearch import Elasticsearch

# # Initialize Elasticsearch client
# es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "0VJJ*mkTwphmq3jk406d"))

# # Define the index name
# index_name = "txt_emails"

# # Check if the index exists
# if es.indices.exists(index=index_name):
#     print(f"Index '{index_name}' exists.")

#     # Perform a match-all query to verify index content
#     query = {
#         "query": {
#             "match_all": {}
#         }
#     }
    
#     try:
#         search_results = es.search(index=index_name, body=query)
#         total_hits = search_results['hits']['total']['value']
#         print(f"Total documents in the index: {total_hits}")
#     except Exception as e:
#         print(f"Error searching index: {e}")
# else:
#     print(f"Index '{index_name}' does not exist.")
