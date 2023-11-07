from graph_builder.config.Config import Config

PROJECT_NAME = Config.project_id


class MimicivHosp:

    admissions = f"`{PROJECT_NAME}.mimiciv_hosp.admissions`"
    d_hcpcs = f"`{PROJECT_NAME}.mimiciv_hosp.d_hcpcs`"
    d_icd_diagnoses = f"`{PROJECT_NAME}.mimiciv_hosp.d_icd_diagnoses`"
    d_icd_procedures = f"`{PROJECT_NAME}.mimiciv_hosp.d_icd_procedures`"
    d_labitems = f"`{PROJECT_NAME}.mimiciv_hosp.d_labitems`"
    diagnoses_icd = f"`{PROJECT_NAME}.mimiciv_hosp.diagnoses_icd`"
    drgcodes = f"`{PROJECT_NAME}.mimiciv_hosp.drgcodes`"
    emar = f"`{PROJECT_NAME}.mimiciv_hosp.emar`"
    emar_detail = f"`{PROJECT_NAME}.mimiciv_hosp.emar_detail`"
    hcpcsevents = f"`{PROJECT_NAME}.mimiciv_hosp.hcpcsevents`"
    labevents = f"`{PROJECT_NAME}.mimiciv_hosp.labevents`"
    microbiologyevents = f"`{PROJECT_NAME}.mimiciv_hosp.microbiologyevents`"
    omr = f"`{PROJECT_NAME}.mimiciv_hosp.omr`"
    patients = f"`{PROJECT_NAME}.mimiciv_hosp.patients`"
    pharmacy = f"`{PROJECT_NAME}.mimiciv_hosp.pharmacy`"
    poe = f"`{PROJECT_NAME}.mimiciv_hosp.poe`"
    poe_detail = f"`{PROJECT_NAME}.mimiciv_hosp.poe_detail`"
    prescriptions = f"`{PROJECT_NAME}.mimiciv_hosp.prescriptions`"
    procedures_icd = f"`{PROJECT_NAME}.mimiciv_hosp.procedures_icd`"
    provider = f"`{PROJECT_NAME}.mimiciv_hosp.provider`"
    services = f"`{PROJECT_NAME}.mimiciv_hosp.services`"
    transfers = f"`{PROJECT_NAME}.mimiciv_hosp.transfers`"


class MimicivIcu:

    caregiver = f"`{PROJECT_NAME}.mimiciv_icu.caregiver`"
    chartevents = f"`{PROJECT_NAME}.mimiciv_icu.chartevents`"
    d_items = f"`{PROJECT_NAME}.mimiciv_icu.d_items`"
    datetimeevents = f"`{PROJECT_NAME}.mimiciv_icu.datetimeevents`"
    icustays = f"`{PROJECT_NAME}.mimiciv_icu.icustays`"
    ingredientevents = f"`{PROJECT_NAME}.mimiciv_icu.ingredientevents`"
    inputevents = f"`{PROJECT_NAME}.mimiciv_icu.inputevents`"
    outputevents = f"`{PROJECT_NAME}.mimiciv_icu.outputevents`"
    procedureevents = f"`{PROJECT_NAME}.mimiciv_icu.procedureevents`"


class MimicIvEd:
    pass


class MimicIvDerived:
    sepsis3 = f"`{PROJECT_NAME}.mimiciv_derived.sepsis3`"


class MimicIvSepsis:
    sepsis_cohort = f"`{PROJECT_NAME}.mimiciv_sepsis.sepsis_cohort`"
    patient_samples = f"`{PROJECT_NAME}.mimiciv_sepsis.patient_samples`"
    used_subject_ids = f"`{PROJECT_NAME}.mimiciv_sepsis.used_subject_ids`"


class Tables:
    """Enum type class that represent all the datasets and tables available
    in the GBQ database. Useful for intellisense when writing sql queries.

    Example use:
    Tables.mimiciv_hosp.admissions -> "project_name.mimiciv_hosp.admissions"
    """

    mimiciv_hosp = MimicivHosp
    mimiciv_icu = MimicivIcu
    mimiciv_ed = MimicIvEd
    mimiciv_derived = MimicIvDerived
    mimiciv_sepsis = MimicIvSepsis
