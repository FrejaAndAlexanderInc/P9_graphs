from graph_builder.data_extractor.data_extractor import DataExctractor, QueryFunc
from graph_builder.Tables import Tables


class SepsisDataExtractor(DataExctractor):
    """Data extractor for 24 hour sepsis prognosis."""

    def __init__(
        self,
        sepsis_patients_limit: int = -1,
        patient_limit: int = -1,
        medication_limt: int = -1,
    ) -> None:
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

    def used_subject_ids(self):
        q = f"""
            select subject_id from `masterthesis-401512.mimiciv_sepsis.patient_samples`
            union all 
            SELECT subject_id FROM `masterthesis-401512.mimiciv_sepsis.sepsis_cohort`
        """

        return self.create_table_wrapper("used_subject_ids", q)

    def sepsis_cohort(self) -> str:
        limit = f"limit {self.sepsis_limit}" if self.sepsis_limit != -1 else ""

        query = f"""
            SELECT *
            from {Tables.mimiciv_sepsis.sepsis_cohort}
            {limit}
        """

        return query

    def patients(self) -> str:
        limit = f"limit {self.patient_limit}" if self.patient_limit != -1 else ""

        query = f"""
            SELECT subject_id, gender, anchor_age
            FROM {Tables.mimiciv_hosp.patients} as P
            WHERE P.subject_id NOT IN
                (SELECT S.subject_id 
                FROM {Tables.mimiciv_derived.sepsis3} S)
            {limit}
        """
        return self.create_table_wrapper("patient_samples", query)

    def diagnosis(self) -> str:
        query = f"""
            select 
                distinct 
                icd_code, 
                icd_version, 
                row_number() over () as id
            from {Tables.mimiciv_hosp.diagnoses_icd} d
            where d.subject_id in     
                (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """
        return self.create_table_wrapper("diagnosis", query)

    def labevents(self) -> str:
        # should not have subject_id
        query = f""" 
            select 
                lab.subject_id, 
                lab.valuenum, 
                lab.valueuom, 
                lab.ref_range_lower, 
                lab.ref_range_upper, 
                lab.flag,
                row_number() over () as id
            from {Tables.mimiciv_hosp.labevents} lab
            inner join `.mimiciv_hosp.d_labitems` item on
            lab.itemid = item.itemid
            where lab.subject_id in     
                (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """
        return self.create_table_wrapper("labevents", query)

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

    def procedure(self) -> str:
        query = f"""
            select distinct 
                icd_code, 
                icd_version,
                row_number() over () as id
            from {Tables.mimiciv_hosp.procedures_icd} pr
            where 
                icd_code is not null and 
                icd_version is not null and 
                pr.subject_id in     
                    (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """
        return self.create_table_wrapper("procedure", query)

    def medication(self) -> str:
        """Medication
        Select top n most popular medication prescribed, based on medication_limit.

        Returns:
            str: query string
        """

        limit = f"limit {self.medication_limit}" if self.medication_limit != -1 else ""

        query = f"""
            select 
                ph.medication,
                row_number() over () as id
            from `masterthesis-401512.mimiciv_hosp.pharmacy` ph
            join `masterthesis-401512.mimiciv_hosp.patients` pa
                on ph.subject_id = pa.subject_id
            where medication is not null
            group by medication
            order by count(pa.subject_id) desc 
            {limit};
        """

        return self.create_table_wrapper("medication", query)

    def admissions(self) -> str:
        query = f"""
            select hadm_id from {Tables.mimiciv_hosp.admissions} a,
            where a.subject_id in
            (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """

        return self.create_table_wrapper("admissions", query)

    # relations

    def patient_labevents(self) -> str:
        query = f"""
            select distinct labevent_id, subject_id
            from {Tables.mimiciv_hosp.labevents} l
            where l.subject_id in
            (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """

        return self.create_table_wrapper("patient_labevents", query)

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

    def patient_diagnosis(self) -> str:
        query = f"""
            select distinct subject_id, icd_code, icd_version
            from {Tables.mimiciv_hosp.diagnoses_icd} d
            where d.subject_id in
            (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """
        return self.create_table_wrapper("patient_diagnosis", query)

    def patient_medication(self) -> str:
        query = f"""
            select subject_id, medication
            from {Tables.mimiciv_hosp.pharmacy} p
            where p.subject_id in
            (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """
        return self.create_table_wrapper("patient_medication", query)

    def patient_procedure(self) -> str:
        query = f"""
            select subject_id, icd_code, icd_version
            from {Tables.mimiciv_hosp.procedures_icd} pr
            where 
                icd_code is not null and 
                icd_version is not null and 
                pr.subject_id in     
                    (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """

        return self.create_table_wrapper("patient_procedure", query)

    def patient_admissions(self) -> str:
        query = f"""
            select subject_id, hadm_id from {Tables.mimiciv_hosp.admissions} a
            where a.subject_id in     
                (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
        """
        return self.create_table_wrapper("patient_admissions", query)

    def patient_labevent(self) -> str:
        ...

    # features

    def patients_features(self):
        pass
        # gender, anchor_age...

    def create_table_wrapper(self, table_name: str, query: str) -> str:
        return f"""
            DROP TABLE IF EXISTS `masterthesis-401512.mimiciv_sepsis.{table_name}`;
            create table `masterthesis-401512.mimiciv_sepsis.{table_name}` as
            {query};
            select * from `masterthesis-401512.mimiciv_sepsis.{table_name}`;
        """
