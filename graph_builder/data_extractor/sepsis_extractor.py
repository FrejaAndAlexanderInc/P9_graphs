from graph_builder.data_extractor.data_extractor import DataExctractor, QueryFunc
from graph_builder.Tables import Tables

class SepsisDataExtractor(DataExctractor):
    """Data extractor for 24 hour sepsis prognosis. 
    """

    def __init__(self, sepsis_patients_limit: int = -1, patient_limit: int = -1, medication_limt: int = -1) -> None:
        """_summary_

        Args:
            sepsis_patients_limit (int, optional): Limited number of sepsis cohort patients to use.
                If no limit is set, all patients will be extracted. Defaults to -1.
            patient_limit (int, optional): Limited number of patients to use.
                If no limit is set, all patients will be extracted.. Defaults to -1.
        """
        super().__init__()
        self.sepsis_limit = sepsis_patients_limit
        self.patient_limit = patient_limit
        self.medication_limit = medication_limt

    ### entities

    def sepsis_cohort(self, obj: str) -> str:
        return f"select distinct subject_id as {obj} from masterthesis-401512.mimiciv_sepsis.sepsis_cohort_samples"

    def patient(self, obj: str) -> str:
        return f"select distinct subject_id as {obj} from masterthesis-401512.mimiciv_sepsis.patient_samples"

    def admissions(self, obj: str) -> str:
        return f'select distinct hadm_id as {obj} from masterthesis-401512.mimiciv_sepsis.admissions'

    def diagnosis(self, obj: str) -> str:
        return f'select distinct id as {obj} from `masterthesis-401512.mimiciv_sepsis.diagnosis`'

    def procedures(self, obj: str) -> str:
        return f'select distinct id as {obj} from `masterthesis-401512.mimiciv_sepsis.procedures`'

    def labevents(self, obj: str) -> str:
        return f'select distinct id as {obj} from `masterthesis-401512.mimiciv_sepsis.labevents`'

    def medication(self, obj: str) -> str:
        return f'select distinct id as {obj} from `masterthesis-401512.mimiciv_sepsis.medication`'

    ### relations

    def patient_diagnosis(self, sub: str, obj: str) -> str:
        return f'select distinct subject_id {sub}, id as {obj} from `masterthesis-401512.mimiciv_sepsis.patient_diagnosis`'

    def patient_medication(self, sub: str, obj: str) -> str:
        return f'select distinct subject_id {sub}, id as {obj} from `masterthesis-401512.mimiciv_sepsis.patient_medication`'

    def patient_procedure(self, sub: str, obj: str) -> str:
        return f'select distinct subject_id {sub}, id as {obj} from `masterthesis-401512.mimiciv_sepsis.patient_procedure`'
 
    def patient_admissions(self, sub: str, obj: str) -> str:
        return f'select distinct subject_id {sub}, hadm_id as {obj} from `masterthesis-401512.mimiciv_sepsis.patient_admissions`'

    def patient_labevents(self, sub: str, obj: str) -> str:
        return f'select distinct subject_id {sub}, id as {obj} from `masterthesis-401512.mimiciv_sepsis.patient_labevents`'

    ### features 

    def patient_features(self, sub: str) -> str:
        return f'''
            select 
                subject_id {sub}, 
                gender, 
                anchor_age as age, 0 as has_sepsis, 
            from `masterthesis-401512.mimiciv_sepsis.patient_samples`'''
    
    def sepsis_cohort_features(self, sub: str) -> str:
        return f'''
            select 
                subject_id {sub}, 
                gender, 
                age, 
                1 as has_sepsis, 
            from `masterthesis-401512.mimiciv_sepsis.sepsis_cohort_samples`'''

    def labevents_features(self, sub: str) -> str:
        return f'select subject_id {sub}, flag, from `masterthesis-401512.mimiciv_sepsis.labevents`'    

    # def create_table_wrapper(self, table_obj: str, query: str) -> str:
    #     return f'''
    #         DROP TABLE IF EXISTS `masterthesis-401512.mimiciv_sepsis.{table_obj}`;
    #         create table `masterthesis-401512.mimiciv_sepsis.{table_obj}` as
    #         {query};
    #         select * from `masterthesis-401512.mimiciv_sepsis.{table_obj}`;
    #     '''

    # def lab_items(self) -> str:
    #     query = f'''
    #         select distinct 
    #             distinct fluid, 
    #             category,
    #             row_number() over () as id
    #         from {Tables.mimiciv_hosp.d_labitems} l
    #         where l.subject_id in     
    #             (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
    #     '''
    #     return self.create_table_wrapper('lab_items', query)
        

    # def labevents_lab_items(self) -> str:
    #     query = f'''
    #         select distinct lab.subject_id, lab.itemid
    #         from {Tables.mimiciv_hosp.labevents} lab
    #         inner join {Tables.mimiciv_hosp.d_labitems} item on
    #         lab.itemid = item.itemid
    #         where lab.subject_id in
    #         (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
    #     '''

    #     return self.create_table_wrapper('labevents_lab_items', query)

    # def sepsis_cohort(self) -> str:
    #     limit = f'limit {self.sepsis_limit}' if self.sepsis_limit != -1 else ''

    #     query = f'''
    #         SELECT *
    #         from {Tables.mimiciv_sepsis.sepsis_cohort}
    #         {limit}
    #     '''

    #     return query

    # def patients(self) -> str:
    #     limit = f'limit {self.patient_limit}' if self.patient_limit != -1 else ''

    #     query = f'''
    #         SELECT subject_id, gender, anchor_age
    #         FROM {Tables.mimiciv_hosp.patients} as P
    #         WHERE P.subject_id NOT IN
    #             (SELECT S.subject_id 
    #             FROM {Tables.mimiciv_derived.sepsis3} S)
    #         {limit}
    #     '''
    #     return self.create_table_wrapper('patient_samples', query)