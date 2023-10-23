import pandas as pd
import pandas_gbq
from typing import Callable
from graph_builder.config.Config import Config 
from graph_builder.Tables import Tables

QueryFunc = Callable[..., str]

class MimicDataExtractor:

    def __init__(self) -> None:
        pass

    def extract_entities(self) -> pd.DataFrame:
        return self.extract(self.patient)

    def extract(self, query_func: QueryFunc, *args) -> pd.DataFrame:
        df = pandas_gbq.read_gbq(
            query_func(*args),
            project_id=Config.project_id,
            credentials=Config.connection
        )

        if df is None:
            raise Exception(f"The following query failed: {query_func.__name__}")
        else:
            return df # type: ignore 

    def patient(self):
        return f"select * from {Tables.mimiciv_hosp.patients} where anchor_age > 18"