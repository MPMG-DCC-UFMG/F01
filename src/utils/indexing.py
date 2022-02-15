# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from utils import path_functions
import os

# !pip install elasticsearch_dsl

es = Elasticsearch('127.0.0.1', port=8055)

def remove_index (job_name):
   es.indices.delete(index=job_name, ignore=[400, 404])

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
                  { "match" : { "content": search_term }},
               ]
            },
         }
      }
   )
   
   result = [ (hit['_source'].get('file').get('filesize'), hit['_score'], hit['_source'].get('path').get('real')) for hit in response['hits']['hits']]

   return result

def get_files_to_valid(
    search_term, index_keywords, num_matches,
    job_name, path_base, types=None): 
        
   #Search
   result = request_search(
   search_term=search_term, keywords=index_keywords, num_matches=num_matches, job_name=job_name)
      
   files = [i[2] for i in result]

   #Aggregate file by type
   agg_files = path_functions.agg_paths_by_type2(files)

   #Return files in specific type
   if types:
      filter_files = []
      for ty in types:
         filter_files.extend(agg_files.get(ty))
      return filter_files
   return files

def get_files(
    search_term, index_keywords, num_matches,
    job_name, path_base): 
        
   #Search
   result = request_search(
   search_term=search_term, keywords=index_keywords, num_matches=num_matches, job_name=job_name)
      
   files = [i[2] for i in result]

   return files






