from analyze_water import calculate_turbidity, safety_check, time_to_safe
import pytest

def test_calculate_turbidity():
    a0 = 1.2
    I90 = 3.0
    assert calculate_turbidity(a0,I90) == pytest.approx(3.6)
    #pytest.approx used for floating point impercision

def test_safety_check():
    turb_val = 1.5
    turb_threshold = 1.0
    assert safety_check(turb_val, turb_threshold) == False

def test_time_to_safe():
    turb_val = 2.0
    turb_threshold = 1.0
    decay_factor = 0.5
    assert time_to_safe(turb_val,turb_threshold,decay_factor) == pytest.approx(1.0)
