#!/usr/bin/env python3
import json

from typing import List
def compute_average_mass(a_list_of_dicts: List[dict], a_key_string: str) -> float:
    """
    Iterates through a list of dictionaries, pulling out values associated with
    a given key. Returns the average of those values.

    Args:
        a_list_of_dicts (list): A list of dictionaries, each dict should have the
                                same set of keys.
        a_key_string (string): A key that appears in each dictionary associated
                               with the desired value (will enforce float type).

    Returns:
        result (float): Average value.
    """
    total_mass = 0.
    for item in a_list_of_dicts:
        total_mass += float(item[a_key_string])
    return(total_mass / len(a_list_of_dicts) )

def check_hemisphere(latitude, longitude):
    """
    Given latitude and longitude in decimal notation, returns which hemispheres
    those coordinates land in.

    Args:
        latitude (float): Latitude in decimal notation.
        longitude (float): Longitude in decimal notation.

    Returns:
        location (string): Short string listing two hemispheres.
    """
    location = 'Northern' if (latitude > 0) else 'Southern'
    location = f'{location} & Eastern' if (longitude > 0) else f'{location} & Western'
    return(location)

def count_classes(a_list_of_dicts, a_key_string):
    """
    Given a list of dictionaries it prints out the specified a keys 
    and how many of each there are

    Args:
        a_list_of_dicts (dict): A list of dicts with information about landings
        a_key_string (string): A string of what key to take
   
    Returns:
        classes_observed (dictionary): A dictionary of the key with the different types and how many of each there are

    """
    classes_observed = {}
    for item in a_list_of_dicts:
        if item[a_key_string] in classes_observed:
            classes_observed[item[a_key_string]] += 1
        else:
            classes_observed[item[a_key_string]] = 1
    return(classes_observed)

def main():
    with open('Meteorite_Landings.json', 'r') as f:
        ml_data = json.load(f)

    print(compute_average_mass(ml_data['meteorite_landings'], 'mass (g)'))

    for row in ml_data['meteorite_landings']:
        print(check_hemisphere(float(row['reclat']), float(row['reclong'])))

    print(count_classes(ml_data['meteorite_landings'], 'recclass'))

if __name__ == '__main__':
    main()

from typing import List
