from typing import Callable
from graph_builder.config.Config import Config
import pandas_gbq
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from more_itertools import grouper
from abc import ABC  # abstract class

QueryFunc = Callable[..., str]


class DataExctractor(ABC):
    def extract_from_config(self, members: list[str]):
        pass

    def extract_entities(self):
        """Extract entities specified in extractor_config.json.
        Save as partquet to folder specified in same file.
        """
        for m in Config.entities:
            entity_extract_func = getattr(self, m["file_name"])
            df = self.extract(entity_extract_func, m["sub"])
            output_file = (
                Path(Config.output_folder) / f"{entity_extract_func.__name__}.parquet"
            )
            df.to_parquet(output_file)

    def extract_relations(self):
        # Extract relations using feature specific functions
        for r in Config.relations:
            relation_extract_func = getattr(self, r["file_name"])
            df = self.extract(relation_extract_func, r["sub"], r["obj"])
            output_file = (
                Path(Config.output_folder) / f"{relation_extract_func.__name__}.parquet"
            )
            df.to_parquet(output_file)

    def extract_features(self):
        # Extract features using relation specific functions
        for f in Config.features:
            relation_extract_func = getattr(self, f["file_name"])
            df = self.extract(relation_extract_func, f["sub"])
            output_file = (
                Path(Config.output_folder) / f"{relation_extract_func.__name__}.parquet"
            )
            df.to_parquet(output_file)

    def extract_all(self) -> None:
        self.extract_entities()
        self.extract_relations()
        self.extract_features()

    def extract(self, query_func: QueryFunc, *args) -> pd.DataFrame:
        """Extract data using a query function and return result as
        dataframe.

        Args:
            query_func (QueryFunc): should return query string
            *args: arguments to query_func

        Raises:
            Exception: if query fails

        Returns:
            pd.DataFrame: dataframe with result
        """
        df = pandas_gbq.read_gbq(
            query_func(*args),
            project_id=Config.project_id,
            credentials=Config.connection,
        )

        if df is None:
            raise Exception(f"The following query failed: {query_func.__name__}")
        else:
            return df  # type: ignore
