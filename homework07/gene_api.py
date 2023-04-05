from flask import Flask, request
import redis
import requests
import json

app = Flask(__name__)
data = {}


def get_redis_client():
    return redis.Redis(host='mihiro10-test-redis-service', port=6379, db=0)
rd = get_redis_client()

@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def handle_data():

    '''
        Manipulates data with GET, POST, and DELETE methods
    
        Args: 
        - None

        Methods:

        - "POST" method: posts data into redis database
        - "GET" method: returns data from redis database
        - "DELETE" method: deletes all data in the redis database


        Returns:
        - "POST" method: String that confirms data was posted
        - "GET" method: returns data from redis databse as a list of dictionaries
        - "DELETE" method: String that confirms data deletion
            
    '''
    
    if request.method == 'GET':
        output_list = []
        for item in rd.keys():
            output_list.append(json.loads(rd.get(item)))
        return output_list
    
    elif request.method == 'POST':
        response = requests.get(url= 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            rd.set(key,json.dumps(item))
        return 'data loaded\n'


    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted there are {rd.keys()} keys in the db'
    
    else:
        return 'the method you tried does not work\n'
    
@app.route('/genes', methods = ['GET'])
def gene_return() -> list:
    '''
    Creates and returns a list of all hgnc_ids

    Args: 
    - NONE

    Returns:
    - hgnc_list: List of all the hgnc IDs
    '''
    hgnc_list = []  # Initialize an empty list to store the hgnc_ids

    # Iterate through all keys in the Redis database
    for key in rd.keys():
        key = key.decode('utf-8')  # Convert the key from bytes to a string
        hgnc_list.append(key)  # Append the string key to the hgnc_list

    return hgnc_list  # Return the list of all the hgnc_ids



@app.route('/genes/<hgnc_id>', methods = ['GET'])
def specific_gene(hgnc_id:str) -> dict:
    '''
    Return all data associated with <hgnc_id>
    ROUTE: /gene/<hgnc_id>
    Args:
    - hgnc_id:    The unique hgnc ID of the gene in the data set
    
    Returns:
    - all data associated with the given <hgnc_id>
    '''

    if len(rd.keys()) == 0:
        return "Database is empty, please post the data first\n"

    for key in rd.keys():
        if key.decode('utf-8') == hgnc_id: #finding the matching id
            return json.loads(rd.get(key))

    return "The given ID did not match any IDs in the database\n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')