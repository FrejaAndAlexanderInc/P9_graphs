from graph_builder.data_extractor.data_extractor import DataExctractor
from graph_builder.Tables import Tables

class SepsisDataExtractor(DataExctractor):

    def __init__(self, sepsis_patients_limit: int = -1, patient_limit: int = -1) -> None:
        super().__init__()
        self.sepsis_limit = sepsis_patients_limit
        self.patient_limit = patient_limit

        # If no limits, use full dataset
        self.full_dataset = True if sepsis_patients_limit == -1 and patient_limit == -1 else False

    def sepsis_cohort_patients(self):
        limit = f"limit {self.sepsis_limit}" if not self.full_dataset else ""

        return f"""
            SELECT *
            from {Tables.mimiciv_sepsis.sepsis_cohort}
            {limit}
        """

    def patients(self):
        limit = f"limit {self.patient_limit}" if not self.full_dataset else ""

        return f"""
            SELECT subject_id, gender, anchor_age
            FROM {Tables.mimiciv_hosp.patients} as P
            WHERE P.subject_id NOT IN
                (SELECT S.subject_id 
                FROM {Tables.mimiciv_derived.sepsis3} S)
            {limit}
        """

    

    