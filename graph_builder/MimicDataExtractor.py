import pandas as pd
import pandas_gbq
from typing import Callable
from graph_builder.config.Config import Config 
from graph_builder.Tables import Tables
from pathlib import Path

QueryFunc = Callable[..., str]

class MimicDataExtractor:
    """Extractor for entities, relations ... from GBQ dataset.
    """

    def __init__(self) -> None:
        pass

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

    def patients(self) -> str:
        return f"select * from {Tables.mimiciv_hosp.patients}"

    def admissions(self) -> str:
        return f"select * from {Tables.mimiciv_hosp.admissions}"

    def diagnosis(self) -> str:
        return f'''
            select * 
            from {Tables.mimiciv_hosp.diagnoses_icd}
            inner join {Tables.mimiciv_hosp.d_icd_diagnoses} on 
                {Tables.mimiciv_hosp.diagnoses_icd}.icd_code={Tables.mimiciv_hosp.d_icd_diagnoses}.icd_code
                and
                {Tables.mimiciv_hosp.diagnoses_icd}.icd_version={Tables.mimiciv_hosp.d_icd_diagnoses}.icd_version
        '''

    def labevents(self) -> str:
        return f'''
            select * 
            from {Tables.mimiciv_hosp.labevents}
            inner join {Tables.mimiciv_hosp.d_labitems} on
                {Tables.mimiciv_hosp.labevents}.itemid = {Tables.mimiciv_hosp.d_labitems}.itemid
        '''

    def medications(self) -> str:
        return f'''
            select * from {Tables.mimiciv_hosp.pharmacy}
            inner join {Tables.mimiciv_hosp.prescriptions} on 
                {Tables.mimiciv_hosp.prescriptions}.pharmacy_id = {Tables.mimiciv_hosp.pharmacy}.pharmacy_id
        '''

    # mabye procedure...

