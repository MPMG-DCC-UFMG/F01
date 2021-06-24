# Indexing Enviroment

## Tools nedded:
* [Current Version of JDK](https://www.oracle.com/br/java/technologies/javase/javase-jdk8-downloads.html) 
* [Fscrawler](https://oss.sonatype.org/content/repositories/snapshots/fr/pilato/elasticsearch/crawler/fscrawler-es7/2.7-SNAPSHOT/)
* [Kibana](https://www.elastic.co/guide/en/kibana/current/install.html)
* [Elastic Search](https://www.elastic.co/pt/downloads/elasticsearch)

## Running Elastic Search:

Go to elasticsearch-7.13.2\config\elasticsearch.yml and uncomment cluster.name and node.name. Name it something meaninful, i named mine givanildo_hulk_paraiba. 

Inside the ElasticSearch folder run 
````bash
bin\elasticsearch.bat
````
To verify if elastic search is running, navigate to http://localhost:9200 
<!--  -->
## Running Kibana
Inside the Kibana folder run 
````bash
bin\kibana.bat
````
To verify if kibana is running, navigate to http://localhost:5601/app/home

## Running Fscrawler
Inside the Fscrawler folder run 
````bash
bin\fscrawler job_name
````
````bash
job [job_name] does not exist
Do you want to create it (Y/N)? Y
````
Go to C:\Users\user\.fscrawler\job_name\_settings.yaml and change url attribute to folder where the dump is.

## Indexing Files
While running ElasticSearch, Kibana and Fscrawler run indexing.py, remember to change PATH in indexing.py so that the dir contains the ElasticSearch folder, for instance mine was:

````bash
PATH = 'C:\\Users\\ritar\\Desktop\\SearchEngine\\'
````

my directory organization was:

````bash
SearchEngine
├── elasticsearch-7.13.2
├── fscrawler-es7-2.7-SNAPSHOT
├── skibana-7.13.2-windows-x86_64
````