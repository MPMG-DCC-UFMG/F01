from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os

PATH = 'C:\\Users\\ritar\\Desktop\\SearchEngine\\'
job_name = "dump"
os.chdir(PATH)
es = Elasticsearch('127.0.0.1', port=9200)

def request_search(search_term):
    s = Search(using=es, index=job_name) \
    .query("match", content=search_term)   \
    .exclude("match", content="")
    
    response = s.execute()
    for hit in response:
        print("score: ", hit.meta.score, " path: ", hit.meta)


if __name__ == "__main__":
    request_search("despesa")

