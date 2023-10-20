import pandas as pd
import pandas_gbq
from typing import Callable
from graph_builder.config.Config import Config 

QueryFunc = Callable[..., str]

class MimicDataExtractor:

    def __init__(self, config: Config) -> None:
        self.config = config

    def extract_entities(self) -> pd.DataFrame:
        return self.extract(self.patient, None)

    def extract(self, query_func: QueryFunc, *args) -> pd.DataFrame:
        df = pandas_gbq.read_gbq(
            query_func(*args),
            project_id=self.config.project_id,
            credentials=self.config.credentials
        )

        if df is None:
            raise Exception(f"The following query failed: {query_func.__name__}")
        else:
            return df

    def patient(self):
        return f"select * from `masterthesis-401512.mimiciv_hosp.patient`"