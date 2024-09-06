import elasticsearch


es = elasticsearch.Elasticsearch('http://127.0.0.1:9200')


query = 'Nick'
statement = {
        "match": {
            "full_name": {
                "query": query, 
                "fuzziness": "auto",

            }
        }
    }
from_=1
size = 3

d = es.search(index='persons', query=statement, from_=from_, size=size)
print(d['hits'])