from flask import Flask, request
import redis
import requests
import json

app = Flask(__name__)
data = {}


def get_redis_client():
    return redis.Redis(host='127.0.0.1', port=6379, db=0)
rd = get_redis_client()

@app.route('/data', methods = ['POST', 'GET', 'DELETE'])
def handle_data():
    
    if request.method == 'GET':
        output_list = []
        for item in rd.keys():
            output_list.append(rd.hgetall(item))
        return output_list
    
    elif request.method == 'POST':
        response = requests.get(url= 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']:
            key = f'{item["numFound"]}'
            rd.hset(key, mapping=item)
        return 'data loaded\n'

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted there are {rd.keys()} keys in the db'
    
    else:
        return 'the method you tried does not work\n'
    


    # response = requests.get(url)
    # response_json = response.json()
    # with open('data.json', 'w') as f:
    #     json.dump(response_json, f) 
    # return()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')