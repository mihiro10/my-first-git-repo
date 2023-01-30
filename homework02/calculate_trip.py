import json
import math

mars_radius = 3389.5 #km

with open('meteorite_sites.json', 'r') as f:
    ml_data = json.load(f)

def calc_gcd(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    """
    This function takes in two points and returns the distance between the two.

    Args:
        latitude_1: Latitude of starting point
        longitude_1: longitude of starting point
        latitude_2: latitude of ending point
        longitude_2: longitude of ending point 

    Returns:
        mars_radius*d_sigma = distance between 2 points
    """
    lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
    return ( mars_radius * d_sigma )

def calc_time_to_sample(composition_type):
    """
    This function calculates the time required sample depending on the composition

    Args:
        composition_type: type of composition

    Returns:
        time_to_sample: time required to sample depending on composition

    """
    if composition_type == "stony":
        time_to_sample = 1
    elif composition_type == "iron":
        time_to_sample = 2
    elif composition_type == "stony-iron":
        time_to_sample = 3
    else:
        time_to_sample = 0
    
    return (time_to_sample)


#initial variables
init_latitude = 16.0
init_longitude = 82.0
leg = 1

for site in ml_data['sites']:
    
    # Set variables to calculate distance and determine time to travel
    prev_lat = init_latitude 
    prev_lon = init_longitude
    current_lat = site['latitude']
    current_long = site['longitude']
    distance = calc_gcd(latitude_1 = prev_lat, longitude_1= prev_lon, latitude_2 = current_lat, longitude_2 = current_long)
    time_to_travel = distance/10

    # Set variables to calculate time to sample
    current_composition = site['composition']
    time_to_sample = calc_time_to_sample(current_composition)

    #Print information
    print(f'leg = {leg}, time to travel = {time_to_travel} hr, time to sample = {time_to_sample} hr')

    
    # Reassign variables for next iteration
    init_latitude = current_lat
    init_longitude = current_long
    leg += 1




