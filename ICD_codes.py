import pandas as pd # type: ignore



def diagnosis_dict(path: str) -> dict[str, str]:
    result = dict()
    df = pd.read_csv(path)
    df = df.drop(["icd_version"], axis=1)

    add_row_to_dict = lambda row: result.update({row['icd_code']: row['long_title']})
    df.apply(add_row_to_dict, axis=1)

    return result

icd_d_path = "datasets/mimic_iv_demo/hosp/d_icd_diagnoses.csv"
icd_p_path = "datasets/mimic_iv_demo/hosp/d_icd_procedures.csv"

ICD_DIAGNOSIS_CODES = diagnosis_dict(icd_d_path)
ICD_PROCEDURE_CODES = diagnosis_dict(icd_p_path)