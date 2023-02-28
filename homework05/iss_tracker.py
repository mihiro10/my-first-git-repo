from flask import Flask, request
import xmltodict
import requests
import math

app = Flask(__name__)
data = {}

def get_data():
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data['ndm']['oem']['body']['segment']['data']['stateVector']

data = get_data() #define data as global variable

@app.route('/', methods = ['GET']) # default curl method
def location():
    """
    This function returns the state vectors in the xml file

    Args:

    Returns:
        data['ndm']['oem']['body']['segment']['data']['stateVector'] = Information within State Vectors as a list of dictionaries

    """
    try:
        global data
        return data
    except NameError:
        return "Data does not exist. \n"



@app.route('/epochs', methods = ['GET'])
def epochs_data():
    """
    This function returns a list of epochs

    Args:

    Returns:
        epoch_list = list of epochs

    """
    global data
    epoch_list = []
    total_results = 0
    index = 0
    
    # check offset
    try:
       offset = int(request.args.get('offset',0))
    except ValueError:
       return "Bad Input",400

    #check limit
    try:
       limit = int(request.args.get('limit',len(data)))
    except ValueError:
       return "Bad Input",400
    except NameError:
        return "Data does not exist. \n"


    for epoch_values in data:
        if (total_results == limit):
            break
        if (index >= offset):
            epoch_list.append(epoch_values['EPOCH'])
            total_results += 1
        index += 1
        
    return epoch_list




@app.route('/epochs/<epoch>', methods = ['GET'])
def epochs_data_specific(epoch: str):
    """
    This function returns a specific epoch value taken from the curl

    Args:
    epoch = value of a specific epoch as a string

    Returns:
    epoch_values = a specific epoch value
    string = when a match is not found

    """
    try:
        global data
        for epoch_values in data:
            if (epoch_values['EPOCH'] == epoch):
                return epoch_values  
        return "did not find matching epoch"
    except NameError:
        return "Data does not exist. \n"





@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def epochs_data_specific_speed(epoch: str):
    """
    This function returns a specific epoch value taken from the curl

    Args:
    epoch = value of a specific epoch as a string

    Returns:
    {"speed": speed} = dictionary of the speed value for the specific data

    """
    try:
        global data
        for epoch_values in data:
            if (epoch_values['EPOCH'] == epoch):
                x_dot = float(epoch_values['X_DOT']['#text'])
                y_dot = float(epoch_values['Y_DOT']['#text'])
                z_dot = float(epoch_values['Z_DOT']['#text'])
                speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
                return {"speed": speed}
        return "did not find matching epoch"
    except NameError: 
        return "Data does not exist. \n"

@app.route('/delete-data', methods=['DELETE'])
def delete_data():
    try:
        global data
        del data
        return 'All data has been deleted successfully.\n'
    except NameError:
        return "Data was already deleted. \n"

@app.route('/get-data', methods=['POST'])
def recover_data():
    global data
    data = get_data()
    return 'All data has been updated successfully.\n'

@app.route('/help', methods = ['GET'])
def help():
    """
    This function returns a human-readable description of all available routes and their methods for the API

    Args:

    Returns:
        Help string
    """
    return """
    Available routes:
    
    GET /
        - Returns the state vectors in the XML file
        
    GET /epochs?limit=int&offset=int
        - Returns a list of epoch values
        - Optional query parameters:
            - offset: number of results to skip
            - limit: maximum number of results to return
    
            
    GET /epochs/<epoch>
        - Returns a specific epoch value based on the provided epoch string
        
    GET /epochs/<epoch>/speed
        - Returns the speed value for a specific epoch
        
    DELETE /delete-data
        - Deletes the global data variable
        
    POST /get-data
        - Retrieves the XML data again and updates the global data variable
    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
