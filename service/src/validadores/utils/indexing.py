# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from src.validadores.utils import path_functions

es = Elasticsearch('127.0.0.1', port=8055)

def remove_index (job_name):
   es.indices.delete(index=job_name, ignore=[400, 404])

def request_search(search_term, keywords_search, job_name):
   num_matches = 10000
   response = es.search(
   index=job_name, 
   body={
      "size" : num_matches,
      "query": 
         {
            "bool":{
               "should":[
                  { "terms": { "array": keywords_search }},
                  { "match" : { "content": search_term }},
               ]
            },
         }
      }
   )
   # print(response)
   result = [ (hit['_source'].get('file').get('filesize'), hit['_score'], hit['_source'].get('path').get('real')) for hit in response['hits']['hits']]
   return result

def get_files(search_term,
      job_name, keywords_search): 
        
   #Search
   result = request_search(
   search_term=search_term, keywords_search=keywords_search, job_name=job_name)
      
   files = [i[2] for i in result]

   return files

def get_files_html(search_term, 
      job_name, keywords_search, filter_in_path): 
   
   """
    Busca arquivos através da função "get_files", opcionalmente filtra os que contém alguma palavra especificada
    no caminho (path), e retorna as páginas html.

    Parameters
    ----------
    search_term: string
        Parâmetro para o elasticseach. Termo principal pesquisado no elasticsearch.
    job_name: string
         Parâmetro para o elasticseach. Job elasticsearch que será pesquisado.
    keywords_search: string
         Parâmetro para o elasticseach. Termos que auxiliam a classificação das páginas mais semelhantes.
    filter_in_path: list of string
         Opcional, filtra os arquivos que o caminho contém alguma palavra nessa lista.
        
    Returns
    -------
    html_files: list of string
       Lista dos caminhos para os arquivos.
    """

   files = get_files(search_term, job_name, keywords_search)
   if filter_in_path:
      files = path_functions.filter_paths(files, words=filter_in_path)
   agg_files = path_functions.agg_paths_by_type(files)

   html_files = agg_files.get('html')
   return html_files