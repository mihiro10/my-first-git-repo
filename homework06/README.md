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

+-------------------------+------------+--------------------------------------------+
| **Route**               | **Method** | **What it does**                      |
+-------------------------+------------+--------------------------------------------+
| ``/data``               | POST       | Puts data into Redis                        |
+-------------------------+------------+--------------------------------------------+
| ``/data``               | GET        | Returns all data from Redis                 |
+-------------------------+------------+--------------------------------------------+
| ``/data``               | DELETE     | Deletes data in Redis                       |
+-------------------------+------------+--------------------------------------------+
| ``/genes``              | GET        | Returns json-formatted list of all hgnc_ids |
+-------------------------+------------+--------------------------------------------+
| ``/genes/<hgnc_id>``    | GET        | Returns all data associated with <hgnc_id>  |
+-------------------------+------------+--------------------------------------------+
