from typing import Callable
from graph_builder.config.Config import Config
import pandas_gbq
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from more_itertools import grouper
from abc import ABC # abstract class

QueryFunc = Callable[..., str]

class DataExctractor(ABC):

    def extract_from_config(self, members: list[str]):
        for entity in members:
            entity_extract_func = getattr(self, entity)
            df = self.extract(entity_extract_func)
            output_file = Path(Config.output_folder) / f'{entity_extract_func.__name__}.parquet'
            df.to_parquet(output_file)

    def extract_from_config_multithreaded(self, members: list[str]):
        executor = concurrent.futures.ProcessPoolExecutor(10)
        futures = [executor.submit(self.extract_from_config, group) for group in grouper(members, len(members))]
        concurrent.futures.wait(futures)

    def extract_entities(self):
        """Extract entities specified in extractor_config.json.
        Save as partquet to folder specified in same file. 
        """
        self.extract_from_config(Config.entities)

    def extract_relations(self):
        self.extract_from_config(Config.relations)

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