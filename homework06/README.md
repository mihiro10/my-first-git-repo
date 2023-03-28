<h2>Say It Ain’t Genes</h2>
This project uses data from a gene api and performs different manipulations to it. It combines the use of Docker, docker-compose, and redis to efficiently and reliably run simulations.

<h3>Data Used</h3>
The HGNC data can be found on this page: https://www.genenames.org/download/archive/ . The specific link that was used to access the json dataset is here https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json . This json file contains different infomation about genes. The source describes it as "The hgnc_complete_set is a set of all approved gene symbol reports found on the GRCh38 reference and the alternative reference loci"

Here is how you can view the json.

```
import json
import requests

url = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json'
response = requests.get(url)
```

<h2>Scripts</h2>

`gene_api.py` - This Flask app is designed to retrieve information from genome data. Once the data is loaded, the app offers Flask routes that allow users to browse through the data and locate particular data points with their corresponding values. Here are the routes and their corresponding outputs.

| Route  | Method   | What it does     |
| ----------- | -------- | ----------- |
| `/data`      | GET |Returns all data from Redis |
| `/data`      | POST |Puts data into Redis |
| `/data`      | DELETE |Deletes data in Redis|
| `/genes`      | GET |Returns json-formatted list of all hgnc_ids |
| `/genes/<hgnc_id>`      | GET |Returns all data associated with <hgnc_id>|

`Dockerfile` - Document that consists of instructions for creating the gene_api Docker image. This image is utilized to generate a Docker container when executed.

`docker-compose.yml` - YAML script that ochestrates the containerization process and port mapping between the Flask application and Redis database.



<h3>How to Run the Scripts</h3>

<h4>First step</h4> 
Once the github repository is pulled and cd into the homework06 directory. Then run the following command
```
mkdir data
```
This makes sure that the data is stored correctly in redis

<h4>Method 1: Pulling the prebuilt image</h4>

```
docker pull mihiro10/gene_api:1.0
```

Then, in the terminal type

```
docker-compose up
```

Open a separate terminal to run curl commands such as
```
curl localhost:5000/data -X POST
```

<h4>Method 2: Builidng the image from dockerfile</h4>


To build the image using the dockerfile, run
```
docker build -t <username>/genes:<tag> .
```

To launch the Flask app using the newly built image, change the image name in yaml file 
```
version: "3"

services:
    redis-db:
        image: redis:7
        ports:
            - 6379:6379
        volumes:
            - ./data:/data
        user: "1000:1000"
    flask-app:
        build:
            context: ./
            dockerfile: ./Dockerfile
        depends_on:
            - redis-db
        image: <username>/genes:<tag>
        ports:
            - 5000:5000
        volumes:
            - ./config.yaml:/config.yaml
```
Then, in your terminal run
```
docker-compose up
```

Open a separate terminal to run curl commands such as
```
curl localhost:5000/data -X POST
```

<h3>Flask app example responses</h3>

*Make sure the data is loaded into the redis database for the routes to properly work*





