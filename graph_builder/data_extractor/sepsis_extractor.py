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
            SELECT 
            p.subject_id, 
            p.gender, 
            p.anchor_age as age,
            s.suspected_infection_time, 
            s.suspected_infection_time - INTERVAL 1 day as prognosis_start,
            s.stay_id,
            s.sepsis3 as has_sepsis,
            los.hr as los_hours
            FROM (
            SELECT 
                subject_id, suspected_infection_time, stay_id, sepsis3
                FROM `masterthesis-401512.mimiciv_derived.sepsis3`
                QUALIFY ROW_NUMBER() OVER (PARTITION BY subject_id ORDER BY suspected_infection_time) = 1
            ) s
            JOIN `masterthesis-401512.mimiciv_hosp.patients` p
                ON s.subject_id = p.subject_id
            JOIN `masterthesis-401512.mimiciv_derived.icustay_hourly` los 
                ON s.stay_id = los.stay_id
                WHERE los.hr > 24
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

    

    