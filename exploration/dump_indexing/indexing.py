# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os

# !pip install elasticsearch_dsl

es = Elasticsearch('127.0.0.1', port=9200)

def request_search(search_term, keywords=[], num_matches= 10, job_name='index_gv', verbose=False):

   response = es.search(
   index=job_name, 
   body={
      "size" : num_matches,
      "query": 
         {
            "bool":{
               "should":[
                  { "terms": { "array": keywords }},
                  { "fuzzy" : { "content": search_term }},
                  { "match" : { "content": search_term }},
               ]
            },
         }
      }
   )
   
   result = [ (hit['_source'].get('file').get('filesize'), hit['_score'], hit['_source'].get('path').get('real')) for hit in response['hits']['hits']]

   sorted_result = sorted(result, key=lambda tup: float(tup[0]), reverse=True)
   return result, sorted_result




