<h2>In the Kubernetes</h2>
This project uses data from a gene api and performs different manipulations to it. It combines the use of Docker, docker-compose, redis and kubernetes to efficiently and reliably run simulations.

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
Once the github repository is pulled and cd into the homework07 directory. Then run the following command
```
mkdir data
```
This makes sure that the data is stored correctly in redis

To test the method 1 and 2, exec into the python debug deployment. Here is the example yaml file used for debug deployment.

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: py-debug-deployment
  labels:
    app: py-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: py-app
  template:
    metadata:
      labels:
        app: py-app
    spec:
      containers:
        - name: py39
          image: python:3.9
          command: ['sleep', '999999999']
```


<h4>Method 1: Using the Kubernetes Deployment of the App</h4>
Begin by pulling this git repository

The kubectl apply -f all the yaml files (except docker-compose.yml) Run the following command for all 5 of the flask and redis yml files.

```
kubectl apply -f mihiro10-flask-deployment.yml
kubectl apply -f mihiro10-flask-service.yml
kubectl apply -f mihiro10-test-redis-deployment.yml
kubectl apply -f mihiro10-test-redis-pvc.yml
kubectl apply -f mihiro10-test-redis-service.yml
```
Use the following command to exec into the debug deployment to run curl commands

```
kubectl exec -it <python-debug-deployment-name> -- /bin/bash
```

<h4>Method 2: Using a Kubernetes Deployment of your Own Image</h4>

Using the gene_api.py file and dockerfile, users may build their own image.

```
docker build -t <username>/<image-name>:<tag> .
```

To run this in the user's application, change the image name in the image section below.



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mihiro10-test-flask-deployment
  labels:
    username: mihiro10
    env: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mihiro10-test-flask
  template:
    metadata:
      labels:
        app: mihiro10-test-flask
        username: mihiro10
        env: test
    spec:
      containers:
        - name: flask
          image: NEW_IMAGE_NAME
          imagePullPolicy: Always
          env:
            - name: mihiro10-test-redis-service
              value: mihiro10-test-redis-service
          ports:
            - containerPort: 5000
```

Then follow the steps in method 1 to test app.



<h4>Method 3: Pulling the prebuilt image</h4>

```
docker pull mihiro10/gene_api:2.0
```

Then, in the terminal type

```
docker-compose up
```

Open a separate terminal to run curl commands such as
```
curl localhost:5000/data -X POST
```

<h4>Method 4: Builidng the image from dockerfile</h4>


To build the image using the dockerfile, run
```
docker build -t <username>/gene_api:<tag> .
```

The push to docker
```
docker push <username>/genes:<tag>
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
        image: <username>/gene_api:<tag>
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

*Make sure the data is loaded into the redis database for the routes to properly work. If the mkdir is not completed before, it will return an error*

For method 1 and 2 the localhost must be changed with the specific IP address for the flask service to run

```
kubectl get services -o wide
```

Which will return something like this if your services are up.

```
mihiro10@kube-access:~/my-first-git-repo/homework07$ kubectl get services -o wide
NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE   SELECTOR
hello-service                 ClusterIP   10.233.36.172   <none>        5000/TCP   8d    app=helloflask
mihiro10-test-flask-service   ClusterIP   10.233.21.155   <none>        5000/TCP   21h   app=mihiro10-test-flask,env=test,username=mihiro10
mihiro10-test-redis-service   ClusterIP   10.233.17.101   <none>        6379/TCP   18h   app=mihiro10-test-redis
```

The CLUSTER-IP of test-flask-service will be used after exec into the debug deployment.

Here is an example
```
mihiro10@kube-access:~/my-first-git-repo/homework07$ kubectl exec -it py-debug-deployment-f484b4b99-269cz -- /bin/bash

root@py-debug-deployment-f484b4b99-269cz:/# 
root@py-debug-deployment-f484b4b99-269cz:/# curl 10.233.21.155:5000/data -X POST
```


---
```
curl localhost:5000/data -X POST
```
Returns

```
data loaded
```
----
```
curl localhost:5000/data -X GET
```
Returns

```
[...
  {
    "_version_": 1761599372646154240,
    "agr": "HGNC:5383",
    "alias_symbol": [
      "IDH-2"
    ],
    "ccds_id": [
      "CCDS10359",
      "CCDS76792"
    ],
    "cosmic": "IDH2",
    "date_approved_reserved": "1986-01-01",
    "date_modified": "2023-01-20",
    "date_name_changed": "2019-07-08",
    "ensembl_gene_id": "ENSG00000182054",
    "entrez_id": "3418",
    "enzyme_id": [
      "1.1.1.42"
    ],
    "gencc": "HGNC:5383",
    "gene_group": [
      "Isocitrate dehydrogenases"
    ],
    "gene_group_id": [
      1926
    ],
    "hgnc_id": "HGNC:5383",
    "iuphar": "objectId:2885",
    "location": "15q26.1",
    "location_sortable": "15q26.1",
    "locus_group": "protein-coding gene",
    "locus_type": "gene with protein product",
    "lsdb": [
      "LRG_611|http://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_611.xml"
    ],
    "mane_select": [
      "ENST00000330062.8",
      "NM_002168.4"
    ],
    "mgd_id": [
      "MGI:96414"
    ],
    "name": "isocitrate dehydrogenase (NADP(+)) 2",
    "omim_id": [
      "147650"
    ],
    "orphanet": 247145,
    "prev_name": [
      "isocitrate dehydrogenase 2 (NADP+), mitochondrial",
      "isocitrate dehydrogenase (NADP(+)) 2, mitochondrial"
    ],
    "refseq_accession": [
      "NM_001289910"
    ],
    "rgd_id": [
      "RGD:1597139"
    ],
    "status": "Approved",
    "symbol": "IDH2",
    "symbol_report_tag": [
      "Stable symbol"
    ],
    "ucsc_id": "uc002box.4",
    "uniprot_ids": [
      "P48735"
    ],
    "uuid": "2e7c51ab-9907-4b47-90c7-697b2cb0b7c6",
    "vega_id": "OTTHUMG00000149815"
  }
]
```
---

```
curl localhost:5000/data -X DELETE
```
Returns
```
data deleted there are [] keys in the db
```

---

```
curl localhost:5000/genes -X GET
```
Returns


```
[...
  "HGNC:50395",
  "HGNC:37920",
  "HGNC:39828",
  "HGNC:14943",
  "HGNC:27747",
  "HGNC:39434",
  "HGNC:17346",
  "HGNC:41933",
  "HGNC:35476",
  "HGNC:46986",
  "HGNC:56695",
  "HGNC:5383"
]
```
---

```
curl localhost:5000/genes/"HGNC:56695" -X GET
```
returns
```
{
  "_version_": 1761599398581633025,
  "alias_name": [
    "Twist1 Associated Long Noncoding RNA regulated by AR"
  ],
  "date_approved_reserved": "2023-01-13",
  "date_modified": "2023-01-13",
  "ensembl_gene_id": "ENSG00000223991",
  "entrez_id": "128266846",
  "gene_group": [
    "Long non-coding RNAs with non-systematic symbols"
  ],
  "gene_group_id": [
    1992
  ],
  "hgnc_id": "HGNC:56695",
  "location": "2q37.3",
  "location_sortable": "02q37.3",
  "locus_group": "non-coding RNA",
  "locus_type": "RNA, long non-coding",
  "name": "TWIST1 associated long noncoding RNA regulated by androgen receptor",
  "pubmed_id": [
    33510354
  ],
  "rna_central_id": [
    "URS000060F02B"
  ],
  "status": "Approved",
  "symbol": "TANAR",
  "uuid": "ab4d841b-2d71-4030-9ad4-1096cbc3c81e"
}
```