<h2>Undone (The Sweater Container)</h2>
This project aims to develop a Flask web application that provides information on the current location of the International Space Station (ISS). The application retrieves the current location data from an XML file published by NASA and provides a RESTful API to query specific information. This project is then packaged and uploaded onto dockerhub where this information can be pulled from.

<h3>Data Set</h3>
The data set used in this project is the ISS OEM data set published by NASA. The data set is available as an XML file and can be accessed using the following link: https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml.


<h3>Flask App/Scripts</h3>

`iss_tracker.py:` contains three endpoints that provide information on the ISS's location and speed:

| Route | Method    | What it does   |
| :---:   | :---: | :---: |
| <code>/</code> | GET   |  Returns the entire state vector information as a list of dictionaries  |
| <code>/epochs</code> | GET   |  Returns a list of all Epochs in the data set |
| <code>/epochs?limit=int&offset=int</code> | GET   |  Returns a list of Epochs given query parameters |
| `/epochs/<epoch>` </code> | GET   |  Returns a specific epoch value as a dictionary. |
| `/epochs/<epoch>/speed` </code> | GET   |  Returns the speed of the ISS at a specific epoch as a dictionary. |
| `/delete-data` </code> | DELETE   | Deletes the global data variable. |
| `/get-data` </code> | POST | Retrieves the XML data again and updates the global data variable |
| `/help` </code> | POST | Returns help text as a string. Gives info on all methods|

`Dockerfile:` Is a document that contains the commands neccesary to containerize the iss_tracker docker image.

<h3>Installation Methods:</h3>

<h4>Method 1: Using the existing Docker Image</h4>
Step 1: 
Run the following in the terminal to pull the docker container.

<code>docker pull mihiro10/iss_tracker:hw05</code>

Run,

` docker run -it --rm -p 5000:5000 mihiro10/iss_tracker:hw05 `

Finally, in a seperate terminal, run the different desired methods.

`curl localhost:5000/`

<h4>Method 2: Building the image from Dockerfile</h4>

Check that you are in the directory with the contents of homework05

Here is a way to check.

Run

```
ls
```

and make sure the output looks like

```
Dockerfile  README.md  iss_tracker.py
```

Now, to build the image using the Dockerfile, use

```
docker build -t <username>/iss_tracker:<tag> .
```

To check that it was built, run 
```
$ docker images
REPOSITORY                  TAG       IMAGE ID       CREATED         SIZE
mihiro10/iss_tracker        hw05      ff34eab7ec29   22 hours ago    897MB
``` 


Then to run the flask app, run

```
docker run -it --rm -p 5000:5000 <username>/iss_tracker:<tag>
```

Finally, open up another terminal and run the different methods

```
curl 'localhost:5000/' 
```


<h3>Example Queries</h3>

Once the Flask app is up and running, the following methods are available.



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

To specify the range of these epochs, a query parameters can be added. 
```
curl localhost:5000/epochs?limit=int&offset=int
```
Here is an example using ?limit=20&offset=50
```
[
  "2023-058T12:00:00.000Z",
  "2023-058T12:04:00.000Z",
  "2023-058T12:08:00.000Z",
  "2023-058T12:12:00.000Z",
  "2023-058T12:16:00.000Z",
  "2023-058T12:20:00.000Z",
  "2023-058T12:24:00.000Z",
  "2023-058T12:28:00.000Z",
  "2023-058T12:32:00.000Z",
  "2023-058T12:36:00.000Z",
  "2023-058T12:40:00.000Z",
  "2023-058T12:44:00.000Z",
  "2023-058T12:48:00.000Z",
  "2023-058T12:52:00.000Z",
  "2023-058T12:56:00.000Z",
  "2023-058T13:00:00.000Z",
  "2023-058T13:04:00.000Z",
  "2023-058T13:08:00.000Z",
  "2023-058T13:12:00.000Z",
  "2023-058T13:16:00.000Z"
]
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

To find the speed at that location, add /speed to the end. Here is an example continuing the one from before.

```
curl localhost:5000/epochs/2023-063T11:55:00.000Z/speed
```
Output 

```
{
  "speed": 7.663985096533364
}
```

To get help on different methods, run

```
curl localhost:5000/help
```
This will return
```
[1]+  Done                    curl localhost:5000/epochs?limit=20

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
```

To delete the data,run

```
curl -X DELETE localhost:5000/delete-data
```
This will return

```
All data has been deleted successfully.
```
confirming that the data was deleted.


To recover that data, run
```
curl -X POST localhost:5000/get-data
```
This wil return
```
All data has been updated successfully.
```