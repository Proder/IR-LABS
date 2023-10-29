from elasticsearch import Elasticsearch

es = Elasticsearch("https://localhost:9200/", ca_certs="C:\elastic stack\elasticsearch-8.10.4-windows-x86_64\elasticsearch-8.10.4\config\certs\http_ca.crt", basic_auth=("elastic", "DGwhdf6JaNY8eCtpF5OS"))
# print(es.info())
print(es.ping())
