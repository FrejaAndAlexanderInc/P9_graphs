import pandas as pd 
from models.entity import Entity

class Feature:
    def __init__(
        self,
        sub: Entity,
        mapping: pd.DataFrame,
    ):
        self.sub = sub
        self.mapping = self.construct_mapping(mapping)
        self.features_names = self.get_feature_names(mapping)

    def construct_mapping(self, mapping: pd.DataFrame) -> pd.DataFrame:
        """Removes duplicates from mapping.

        Args:
            mapping (pd.DataFrame): dataframe that maps entity to its features.
            each row has an id equal to the entity, rest of the columns are features. 
            ex. columns of mapping: ["patient", "patient_feature1", "patient_feature2", ...]

        Returns:
            pd.DataFrame: mapping without duplicates
        """

        # Filter mappings with non-existing entity ids
        mapping = mapping[mapping[self.sub.name].isin(self.sub.ids)]

        return mapping.drop_duplicates()

    def get_feature_names(self, mapping: pd.DataFrame) -> list[str]:
        """Returns a list of names for the features in the mapping. 

        Args:
            mapping (pd.DataFrame): mapping df

        Returns:
            list[str]: list of feature names, ie. ["feature1", "feature2", ...]
        """
        cols = list(mapping.columns)
        cols.remove(self.sub.name)
        return cols 
