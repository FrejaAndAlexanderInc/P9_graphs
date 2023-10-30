from typing import Callable
from graph_builder.config.Config import Config
import pandas_gbq
import pandas as pd
from pathlib import Path

QueryFunc = Callable[..., str]

class DataExctractor:
    def extract_entities(self):
        """Extract entities specified in extractor_config.json.
        Save as partquet to folder specified in same file. 
        """
        for entity in Config.entities:
            entity_extract_func = getattr(self, entity)
            df = self.extract(entity_extract_func)
            output_file = Path(Config.output_folder) / f'{entity_extract_func.__name__}.parquet'
            df.to_parquet(output_file)

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