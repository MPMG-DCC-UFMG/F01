# Indexing Environment

## Tools nedded:
* [Current Version of JDK](https://www.oracle.com/br/java/technologies/javase/javase-jdk8-downloads.html) 
* [Fscrawler](https://oss.sonatype.org/content/repositories/snapshots/fr/pilato/elasticsearch/crawler/fscrawler-es7/2.7-SNAPSHOT/)
* [Kibana](https://www.elastic.co/guide/en/kibana/current/install.html)
* [Elastic Search](https://www.elastic.co/pt/downloads/elasticsearch)

## Executing Elastic Search:

Go to **elasticsearch-7.13.2\config\elasticsearch.yml** and uncomment *cluster.name* and *node.name*. Name your node with a meaningful name, *job_name*. The cluster name is up to your imagination, I named mine givanildo_hulk_paraiba. 

Inside the ElasticSearch folder run 
````bash
bin\elasticsearch.bat
````
To verify if Elastic Search is running, navigate to http://localhost:9200 
<!--  -->
## Executing Kibana
Inside the Kibana folder run 
````bash
bin\kibana.bat
````
To verify if Kibana is running, navigate to http://localhost:5601/app/home

## Executing Fscrawler
Inside the Fscrawler folder run 
````bash
bin\fscrawler job_name
````
````bash
job [job_name] does not exist
Do you want to create it (Y/N)? Y
````
Go to **C:\Users\user\.fscrawler\job_name\_settings.yaml** and change the *url* attribute to the path where the dump is. Then run Fscrawler again.

````bash
bin\fscrawler job_name
````

## Indexing Files
While ElasticSearch, Kibana and Fscrawler are running, execute *indexing.py* in another cmd tab. Remember to change the *job_name* variable to your job name and the *PATH* variable in *indexing.py* to the dir that contains the ElasticSearch folder, for instance mine was:

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