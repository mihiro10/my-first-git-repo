<h1>Buddy Flask</h1>


<h2>Project Description</h2>
This project aims to develop a Flask web application that provides information on the current location of the International Space Station (ISS). The application retrieves the current location data from an XML file published by NASA and provides a RESTful API to query specific information.
<h3>Data Set</h3>
The data set used in this project is the ISS OEM data set published by NASA. The data set is available as an XML file and can be accessed using the following link: https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml.


<h3>Flask App</h3>

The Flask app has three endpoints that provide information on the ISS's location and speed:

/: Returns the entire state vector information as a list of dictionaries.
/epochs: Returns a list of epochs in the XML file.
/epochs/<epoch>: Returns a specific epoch value as a dictionary.
/epochs/<epoch>/speed: Returns the speed of the ISS at a specific epoch as a dictionary.

<h3>Install the required packages:</h3> 

```
pip3 install --user xmltodict
```

Running the app will require 2 terminals. Open two terminals and in the first one, run

```
flask --app iss_tracker --debug run
```
In the second terminal, run 

```
curl localhost:5000
```


<h3>Example Queries</h3>


```
curl localhost:5000
```
Returns the entire state vector information as a list of dictionaries.

Here is an example snippet

```
 {
    "EPOCH": "2023-063T11:51:00.000Z",
    "X": {
      "#text": "-242.12485388276099",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.9511600325922904",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5285.0073157200604",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-3.1998687127665399",
      "@units": "km/s"
    },
    "Z": {
      "#text": "4254.7035249005503",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-3.6194381039437298",
      "@units": "km/s"
    }
  },

  ... etc.
```



Next, running 

```
curl localhost:5000/epochs
```
Returns a list of epochs in the XML file.

Here is an example.

```
[
  "2023-063T11:23:00.000Z",
  "2023-063T11:27:00.000Z",
  "2023-063T11:31:00.000Z",
  "2023-063T11:35:00.000Z",
  "2023-063T11:39:00.000Z",
  "2023-063T11:43:00.000Z",
  "2023-063T11:47:00.000Z",
  "2023-063T11:51:00.000Z",
  "2023-063T11:55:00.000Z",
  "2023-063T11:59:00.000Z",
  "2023-063T12:00:00.000Z"
... etc.
```
Now to find information about a specific epoch, include the information after epoch. Here is an example using 2023-063T11:55:00.000Z

```
curl localhost:5000/epochs/2023-063T11:55:00.000Z
```
This returns

```
{
  "EPOCH": "2023-063T11:55:00.000Z",
  "X": {
    "#text": "1177.59304662879",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "5.8075028706235097",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-5851.2024874564004",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-1.4895857081331501",
    "@units": "km/s"
  },
  "Z": {
    "#text": "3241.2823555820801",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-4.7739619170779601",
    "@units": "km/s"
  }
}
```

Finally, to find the speed at that location, add /speed to the end. Here is an example continuing the one from before.

```
curl localhost:5000/epochs/2023-063T11:55:00.000Z/speed
```
Output 

```
{
  "speed": 7.663985096533364
}
```


