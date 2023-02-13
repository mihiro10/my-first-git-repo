# Mars Mission 
<h2>Project Objective</h2>
This project simulates a robotic mission to Mars to collect samples of meteorites at different locations. The project consists of two python scripts: generate_sites.py and calculate_trip.py.


<h2>Folder Contents</h2>
<h3>generate_sites.py:</h3>
a script that generates a JSON file of randomly generated meteorite sites with latitude, longitude, and composition information
<h3>calculate_trip.py:</h3> a script that calculates the time required to travel to each site and the time required to sample each meteorite, based on the information in the JSON file generated by generate_sites.py
<h2>Specific Description of Python Scripts</h2>
<h3>generate_sites.py:</h3> This script creates a dictionary of meteorite sites, with randomly generated latitude, longitude, and composition values. The dictionary is then saved as a JSON file.

<h3>calculate_trip.py:</h3> This script opens the JSON file generated by generate_sites.py, and uses the latitude and longitude information to calculate the distance between each site and the starting point. It also uses the composition information to determine the time required to sample each meteorite. The script then prints the time required to travel to each site and the time required to sample each meteorite.

<h2>Instructions to Run the Code</h2>

<h3>Step 1</h3>
Download the git repository and cd into homework02
```cd coe-332/homework02 ```

<h3>Step 2</h3>
Run generate_sites.py to generate the JSON file of meteorite sites. The created JSON file will be called ```meteorite_sites.json```:

``` $ python3 generate_sites.py   ```
The meteorite_sites.json should look like this:
 ``` 
 {
  "sites": [
    {
      "site_id": 1,
      "latitude": 16.258737458778725,
      "longitude": 82.31870942308117,
      "composition": "iron"
    },
    {
      "site_id": 2,
      "latitude": 17.500410056251926,
      "longitude": 82.80421653062976,
      "composition": "stony-iron"
    },
    {
      "site_id": 3,
      "latitude": 17.920823117650347,
      "longitude": 82.4809118723955,
      "composition": "stony-iron"
    },
    {
      "site_id": 4,
      "latitude": 16.437364667926488,
      "longitude": 83.67730836347022,
      "composition": "stony"
    },
    {
      "site_id": 5,
      "latitude": 16.628492328703366,
      "longitude": 83.57611661503267,
      "composition": "stony-iron"
    }
  ]
}
 ```
<h3>Step 3</h3>
Run:
```calculate_trip.py```   to calculate the time required to travel to each site and the time required to sample each meteorite

```$ python3 calculate_trip.py```

The result should look something like this:

```
leg = 1, time to travel = 2.371349832634944 hr, time to sample = 2 hr
leg = 2, time to travel = 7.842798154226783 hr, time to sample = 3 hr
leg = 3, time to travel = 3.083026868256632 hr, time to sample = 3 hr
leg = 4, time to travel = 11.078572716749822 hr, time to sample = 1 hr
leg = 5, time to travel = 1.2679733726041362 hr, time to sample = 3 hr
```

The script will print the time required to travel to each site and the time required to sample each meteorite for each leg of the trip.



<h3>Interpreting the Results</h3>
The script will print the time required to travel to each site and the time required to sample each meteorite for each leg of the trip.
The generate_sites.py script will also save the meteorite_sites.json file that is used as input for the next script.
The script is set to 5 meteorite sites, you can change the range of the loop to generate more meteorite sites.
The time to sample is based on the type of composition, stony = 1 hr, iron = 2 hr and stony-iron = 3 hr.
<h3>Note</h3>
Make sure to change the path of the file to the correct directory before running the script
The script uses the Haversine formula to calculate the distance between the two points.
The script assumes that the initial point is at latitude 16.0 and longitude 82.0
The script assumes that the vehicle travels at a speed of 10 km/hr