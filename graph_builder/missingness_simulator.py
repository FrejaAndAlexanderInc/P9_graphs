from enum import Enum, auto
import numpy as np
import pandas as pd

class MissingSimulator:
        
    def simulate_attribute_mcar(self, attributes: pd.DataFrame, missingness_rate: float) -> pd.DataFrame:
        attributes = attributes.copy(deep=True)
        mask = np.random.uniform(0, 1, size=attributes.shape) <= missingness_rate
        attributes[mask] = np.nan
        return attributes