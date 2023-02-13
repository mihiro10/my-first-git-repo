<h1>The World Has Turned and Left Me Turbid</h1>


<h2>Project Description</h2>

This project uses different samples of water and analyzes their turbidity levels to determine the safety of the water. The analyzes_water.py file pulls information from an API that returns information about different samples including their turbidity levels. Then using the information, it returns the average turbidity based on the most recent five measurements, if the turbidity is below threshold for safe use and the minimum time required to return below a safe threshold. The test_analyze_turbidity.py is a tester function that unit tests the functions of analyze_turbidity.py with sample data.


<h3>Installations</h3>

To run the following scripts, the 2 folowing lines must be run

```
pip3 install --user requests
```
For the get requests.
and...

```
pip3 install --user pytest
```
For unit testing.


<h3>Data</h3>
The data is accesed from the following link
https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json .
The code snippet below stores the json into turb_data

```
import requests
import json

response = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
turb_data = response.json()

```

Here is a sample of the data about the different samples.


```
{
  "turbidity_data": [
    {
      "datetime": "2023-02-01 00:00",
      "sample_volume": 1.19,
      "calibration_constant": 1.022,
      "detector_current": 1.137,
      "analyzed_by": "C. Milligan"
    },
    {
      "datetime": "2023-02-01 01:00",
      "sample_volume": 1.15,
      "calibration_constant": 0.975,
      "detector_current": 1.141,
      "analyzed_by": "C. Milligan"
    },
    ... etc
```

<h3>Instructions to Run Code</h3>

After cloning the repository, run
```cd coe-332/homework03```

Then, to ensure all functions are working correctly, run the test_analyze_water.py by running 
```pytest -q test_analyze_water.py```
This should return something like this

```
...                                                                                                                  [100%]
3 passed in 0.25s
```

Now, run the water analyzing script with

```
python3 analyze_water.py 
```
The output should be something like this
```
Average turbidity based on most recent five measurements =  1.1538822 NTU
Warning: Turbidity is above threshold for safe use
Minimum time required to return below a safe threshold = 7.084797146399919 hours
```

This means that the water level is not safe and takes approximately 7 hours to return to a safe level.

On the other hand, if the average turbidity is already below the safety threshold it will return something like this.

```
Average turbidity based on most recent five measurements =  0.2 NTU
Info: Turbidity is below threshold for safe use
Minimum time required to return below a safe threshold = 0 hours
```

Meaning that the tubidity is already below 1 NTU. 
