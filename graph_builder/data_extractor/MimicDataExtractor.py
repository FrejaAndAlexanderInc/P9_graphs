import pandas as pd
import pandas_gbq
from typing import Callable
from graph_builder.config.Config import Config 
from graph_builder.Tables import Tables
from pathlib import Path
from graph_builder.data_extractor.data_extractor import DataExctractor

QueryFunc = Callable[..., str]

# TODO: Joins cause duplicate cols
class MimicDataExtractor(DataExctractor):
    """Extractor for entities, relations ... from GBQ dataset.
    """
    
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

