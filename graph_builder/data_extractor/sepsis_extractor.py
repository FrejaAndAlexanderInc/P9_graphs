from graph_builder.data_extractor.data_extractor import DataExctractor
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

    def sepsis_cohort_patients(self) -> str:
        limit = f'limit {self.sepsis_limit}' if self.sepsis_limit != -1 else ''

        return f'''
            SELECT *
            from {Tables.mimiciv_sepsis.sepsis_cohort}
            {limit}
        '''

    def patients(self) -> str:
        limit = f'limit {self.patient_limit}' if self.patient_limit != -1 else ''

        return f'''
            SELECT subject_id, gender, anchor_age
            FROM {Tables.mimiciv_hosp.patients} as P
            WHERE P.subject_id NOT IN
                (SELECT S.subject_id 
                FROM {Tables.mimiciv_derived.sepsis3} S)
            {limit}
        '''

    def diagnosis(self) -> str:
        return f'''
            select distinct icd_code, icd_version
            from {Tables.mimiciv_hosp.diagnoses_icd}
        '''

    def labevents(self) -> str:
        return f'''
            select lab.subject_id, lab.valuenum, lab.valueuom, lab.ref_range_lower, lab.ref_range_upper, lab.flag
            from `.mimiciv_hosp.labevents` lab
            inner join `.mimiciv_hosp.d_labitems` item on
            lab.itemid = item.itemid
        '''

    def lab_items(self) -> str:
        return f'''
            select distinct distinct fluid, category
            from {Tables.mimiciv_hosp.d_labitems}
        '''

    def procedure(self) -> str:
        return f'''
            
        '''

    def medication(self) -> str:
        """Medication
        Select top n most popular medication prescribed, base on medication_limit. 

        Returns:
            str: query string
        """

        limit = "limit {self.medication_limit}" if self.medication_limit != -1 else ''

        return f'''
            select ph.medication 
            from `masterthesis-401512.mimiciv_hosp.pharmacy` ph
            join `masterthesis-401512.mimiciv_hosp.patients` pa
                on ph.subject_id = pa.subject_id
            where medication is not null
            group by medication
            order by count(pa.subject_id) desc 
            {limit}
        '''

    # relations

    def patient_labevents(self) -> str:
        return f'''
            select distinct labevent_id, subject_id
            from {Tables.mimiciv_hosp.labevents}
        '''

    def labevents_lab_items(self) -> str:
        return f'''
            select distinct lab.subject_id, lab.itemid
            from {Tables.mimiciv_hosp.labevents} lab
            inner join {Tables.mimiciv_hosp.d_labitems} item on
            lab.itemid = item.itemid
        '''

    def patient_diagnosis(self) -> str:
        return f'''
            select distinct subject_id, icd_code, icd_version
            from {Tables.mimiciv_hosp.diagnoses_icd}
        '''

    def patient_medication(self) -> str:
        return f'''
            select subject_id
        '''

    # features 

    def patients_features(self):
        pass 
        # gender, anchor_age...
    

    