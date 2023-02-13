import requests
import json
import math

response = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
turb_data = response.json()




def calculate_turbidity(a0: float, I90: float) -> float:
    """
    This function takes in the calibration constant and the detector constant and returns the turbidity in NTU Units

    Args:
        a0: Calibration Constant
        I90: Ninety degreee detector current
    
    Returns:
        tubidity = Turbidity in NTU Units
    
    """
    turb = a0*I90

    return (turb)

def safety_check (turb_val:float, turb_threshold:float) -> bool:
    """
    This function hecks if the turbidity is within the safe threshold

    Args:
        turb_val = turbidity value
        turb_threshold = turbidity threshold for safe water

    Returns:
        true or false. If the water is safe, true, if not false
    """
    if turb_val > turb_threshold: #figure out if need to add threshold as arg
        print("Warning: Turbidity is above threshold for safe use")
        return False
    else:
        print("Info: Turbidity is below threshold for safe use")

def time_to_safe(turb_val: float, turb_threshold:float, decay_factor:float) -> float:
    """
    This function takes in turbidity and returns the time it takes to return to a safe level.
    It uses the equation Ts > T0(1-d)**b as a governing equation. 
    Args:
        turb_val = turbidity value = T0
        turb_threshold = value at which water is safe = Ts
        decay_factor = decay factor per hour. Percentage represented as a decimal = d

    Returns:
        hours_elapsed = time it takes to return to safe threshold = b

    """
    if turb_val < turb_threshold:
        hours_elapsed = 0
    else:
        hours_elapsed = abs(math.log((turb_val/turb_threshold), (1-decay_factor)))
  
    print("Minimum time required to return below a safe threshold =", hours_elapsed, "hours")
    return(hours_elapsed)


    


    

turb_threshold = 1.0
decay_factor = 0.02

def main():


    counter = 0
    T_sum = 0
    number_of_samples = 5

    #pulls in data from api and computes average of number of samples
    for sample in turb_data['turbidity_data']:
        current_calibration_constant = sample['calibration_constant']
        current_detector_current = sample['detector_current']

        T = calculate_turbidity(current_calibration_constant, current_detector_current)
        T_sum = T_sum + T
        counter += 1
        if counter == number_of_samples:
            break
    turb_average =  0.2 #T_sum/number_of_samples

    print("Average turbidity based on most recent five measurements = ", turb_average, "NTU")


    safety_check(turb_average, turb_threshold)
    time_to_safe(turb_average, turb_threshold, decay_factor)



if __name__ == '__main__':
    main()



