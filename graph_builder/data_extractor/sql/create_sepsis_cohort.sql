create table `masterthesis-401512.mimiciv_sepsis.sepsis_cohort` as
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