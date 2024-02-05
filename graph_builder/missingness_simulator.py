from enum import Enum, auto
import numpy as np
import pandas as pd

class MissingSimulator:
    """Class for simulating missingness in data.
    """
        
    def simulate_attribute_mcar(self, attributes: pd.DataFrame, missingness_rate: float) -> pd.DataFrame:
        """Simulate MCAR missingness of node attributes.

        Args:
            attributes (pd.DataFrame): Attributes to simulate missingness on.
            missingness_rate (float): The rate of missingness to simulate.
                0.01 is 1% missingness, 0.1 is 10% missingness, etc.

        Returns:
            pd.DataFrame: A new dataframe with missingness simulated.
        """
        attributes = attributes.copy(deep=True)
        mask = np.random.uniform(0, 1, size=attributes.shape) <= missingness_rate
        attributes[mask] = np.nan
        return attributes