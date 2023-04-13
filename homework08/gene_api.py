from flask import Flask, request, send_file
import redis
import requests
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, date
import io



app = Flask(__name__)
data = {}


def get_redis_client():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=0)


def get_redis_image_db():
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=1)



#redis client call
rd = get_redis_client()
#redis image db function call
rd_image = get_redis_image_db()

@app.route('/image', methods = ['POST', 'GET', 'DELETE'])
def ret_image():
    '''
    Manipulates image data with GET, POST, and DELETE methods
    
    Args:
    - None

    Methods:
        - "DELETE": deletes all data in redis db
        - "POST": method: posts plot into redis db
        "GET" method: returns plot from redis db
    Returns:
        - "DELETE": String confirming data deletion
        - "POST: String confirming data posted
        - "GET": returns plot from redis db in a file type specified by user
        
    '''


    if request.method == 'GET':
        if(len(rd_image.keys())== 0):
            return "There is no image in DB use /image -X POST first.\n"
        else:
            plot_bytes = rd_image.get("Plot")

            # Load the bytes as an image
            buf = io.BytesIO(plot_bytes)
            buf.seek(0)
            # Return the image as a file to the user
            return send_file(buf, mimetype='image/png')
        
            
    # Make plot of Date vs ID number
    elif request.method == 'POST':
        if(len(rd.keys()) == 0):
            return "No data that can be used to create image. run use /data -X POST first.\n"
        else:
            days_since_2000_list = []
            HGNC_list = []
            for item in rd.keys():
                #loading key value
                value = rd.get(item).decode('utf-8')
                value = json.loads(value)

                #date values 
                date_str = value["date_approved_reserved"]
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                reference_date = date(2000, 1, 1)

                #determining the delta
                delta = parsed_date - reference_date
                days_since_2000 = delta.days
                days_since_2000_list.append(days_since_2000)
                HGNC_list.append(int(value["hgnc_id"][5:]))

            fig, ax = plt.subplots()
            ax.scatter(days_since_2000_list, HGNC_list,s=8,alpha=0.5)
            ax.set_title('ID # vs Approved Date')
            ax.set_xlabel('Days since approval. January 1, 2000')
            ax.set_ylabel('HGNC ID #')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            rd_image.set("Plot", buf.getvalue())

            return 'Plot has been posted\n'

    elif request.method == 'DELETE':
        rd_image.flushdb()
        return f'Plot has ben deleted. There are {len(rd_image.keys())} plots in the db\n'

    
    
    else:
        return 'the method you tried does not work\n'



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
