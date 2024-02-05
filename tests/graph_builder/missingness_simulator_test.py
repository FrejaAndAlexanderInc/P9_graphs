import pytest
import pandas as pd
import numpy as np
from graph_builder.missingness_simulator import MissingSimulator

@pytest.mark.parametrize(
    "missing_rate, expected",
    [
        (1,1), (3,3), (5,5), (7,7), (10,10), (15,15), (20,20), (25,25), (30,30), (40,40), (50,50), (60,60), (70,70), (80,80), (90,90), (100,100)
    ],
)
def test_simulate_attribute_mcar_correct_missing_rate(missing_rate, expected):    
    np.random.seed(42)
    df = pd.DataFrame({
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10),
        'D': np.random.rand(10),
        'E': np.random.rand(10),
        'F': np.random.rand(10),
        'G': np.random.rand(10),
        'H': np.random.rand(10),
        'I': np.random.rand(10),
        'J': np.random.rand(10),
    })

    df = MissingSimulator().simulate_attribute_mcar(df, missing_rate / 100, np.nan)
    actual_missing_rate = df.isnull().sum().sum() / 100
    expected_rate = expected / 100

    tolerance = 0.041 # tolerance of 4.1% for the missing rate
    assert pytest.approx(actual_missing_rate, abs=tolerance) == expected_rate
