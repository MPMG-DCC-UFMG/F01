# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os

# !pip install elasticsearch_dsl

es = Elasticsearch('127.0.0.1', port=9200)

def request_search(search_term, must_words, should_words, job_name, verbose=False):

    response = es.search(
    index=job_name,
    body={
      "query": {
         "bool": {
           "must": [
              {
                "more_like_this" : {
                "fields" : ["content"],
                "like" : search_term,
                "min_term_freq" : 1,
                "max_query_terms" : 10,
                "min_doc_freq" : 4
                }
              },
              {
                "match": {
                   "content": must_words[0]
                 }
              },
                {
                 "match": {
                   "content": must_words[1]
                 }
              },
                {
                "match": {
                   "content": must_words[2] 
                 } 
              }
              
              ],
              "should":[
                 {
                "match": {
                    "content": should_words[0]
                 }
              },
              {
                "match": {
                    "content": should_words[1]
                 }
              },
              {
                "match": {
                    "content": should_words[2]
                  
                 }
              },
              {
                "match": {
                    "content":  should_words[3]
                  
                 }
              }
           ]
        }
      }
    })
    
    for hit in response['hits']['hits']:
        print(hit['_score'], hit['_source'])
        print("\n\n")



if __name__ == "__main__":

    #search_term="Licitações"
    #must_words = ["Modalidade", "Fundamentação legal", "Status"]
    #should_words = ["Pregão", "Inexigibilidade", "Homologada", "Resultado Final de Licitação" ]

    #search_term="Servidores"
    #must_words = ["Cargo/Função", "Unidade", "Valor"]
    #should_words = ["Matrícula", "Nome", "Competência", "Lotação" ]

    #search_term="Contas Públicas"
    #must_words = ["Prestação de Contas", "Convênios", "Repasses"]
    #should_words = ["Demonstrativos", "Balancete", "Gastos com Saúde", "Gastos com Educação" ]

    search_term="Concurso Público"
    must_words = ["Edital", "Concurso Público", "Publicado em"]
    should_words = ["Edital", "Relaçao de Aprovados", "Recursos", "Remanescentes" ]

    request_search(
      search_term=search_term, must_words=must_words, should_words=should_words, job_name="index_gv")




