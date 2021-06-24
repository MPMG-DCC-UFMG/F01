from elasticsearch import Elasticsearch
import os

PATH = 'C:\\Users\\ritar\\Desktop\\SearchEngine\\'
os.chdir(PATH)
es = Elasticsearch('127.0.0.1', port=9200)

def request_search(search_term):
    res = es.search(
        index='dump',
        body={
            "query" : {"match": {"content": search_term}},
            "highlight" : {"pre_tags" : ["<b>"] , "post_tags" : ["</b>"], "fields" : {"content":{}}}
        })

    res["ST"]= search_term
    for hit in res["hits"]["hits"]:
        hit["good_summary"]="….".join(hit["highlight"]["content"][1:])
 
    print(res)


if __name__ == "__main__":
    request_search("despesas")