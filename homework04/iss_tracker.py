from flask import Flask
import xmltodict
import requests
import math

app = Flask(__name__)

def get_data():
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data #['ndm']['oem']['header']

@app.route('/', methods = ['GET']) # default curl method
def location():
    """
    This function returns the state vectors in the xml file

    Args:

    Returns:
        data['ndm']['oem']['body']['segment']['data']['stateVector'] = Information within State Vectors as a list of dictionaries

    """

    data = get_data()
    return data['ndm']['oem']['body']['segment']['data']['stateVector']


@app.route('/epochs', methods = ['GET'])
def epochs_data():
    """
    This function returns a list of epochs

    Args:

    Returns:
        epoch_list = list of epochs

    """
    data = location()
    epoch_list = []
    for epoch_values in data:
        epoch_list.append(epoch_values['EPOCH'])

    return epoch_list


@app.route('/epochs/<epoch>', methods = ['GET'])
def epochs_data_specific(epoch):
    """
    This function returns a specific epoch value taken from the curl

    Args:
    epoch = value of a specific epoch

    Returns:
    epoch_values = a specific epoch value
    string = when a match is not found

    """
    data = location()
    for epoch_values in data:
        if (epoch_values['EPOCH'] == epoch):
            return epoch_values
    
    return "did not find matching epoch"


@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def epochs_data_specific_speed(epoch):
    """
    This function returns a specific epoch value taken from the curl

    Args:
    epoch = value of a specific epoch

    Returns:
    {"speed": speed} = dictionary of the speed value for the specific epoch

    """
    data = location()
    for epoch_values in data:
        if (epoch_values['EPOCH'] == epoch):
            x_dot = float(epoch_values['X_DOT']['#text'])
            y_dot = float(epoch_values['Y_DOT']['#text'])
            z_dot = float(epoch_values['Z_DOT']['#text'])
            speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
            return {"speed": speed}
    
    return "did not find matching epoch"




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
