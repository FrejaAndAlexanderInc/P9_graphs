DROP TABLE IF EXISTS `masterthesis-401512.mimiciv_sepsis.sepsis_cohort_samples`;
create table `masterthesis-401512.mimiciv_sepsis.sepsis_cohort_samples` as
select * from `masterthesis-401512.mimiciv_sepsis.sepsis_cohort`
limit 200;

DROP TABLE IF EXISTS `masterthesis-401512.mimiciv_sepsis.used_subject_ids`;
create table `masterthesis-401512.mimiciv_sepsis.used_subject_ids` as
select distinct subject_id from `masterthesis-401512.mimiciv_sepsis.patient_samples`
union all 
SELECT distinct subject_id FROM `masterthesis-401512.mimiciv_sepsis.sepsis_cohort_samples`;

-- missing sepsis chort...

-- entities
drop table if exists `masterthesis-401512.mimiciv_sepsis.diagnosis`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.diagnosis` AS
SELECT
  GENERATE_UUID() AS id,
  d.subject_id,
  d.icd_code,
  d.icd_version
FROM (
  SELECT DISTINCT
    d.subject_id,
    d.icd_code,
    d.icd_version
  FROM `physionet-data.mimiciv_ed.diagnosis` d
  WHERE d.subject_id IN     
    (SELECT subject_id FROM `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
) d;

drop table if exists `masterthesis-401512.mimiciv_sepsis.medication`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.medication` as 
select p.subject_id, p.medication, top.id
from
(
    select  
        ph.medication,
        GENERATE_UUID() AS id
    from `masterthesis-401512.mimiciv_hosp.pharmacy` ph
    join `masterthesis-401512.mimiciv_hosp.patients` pa
        on ph.subject_id = pa.subject_id
    where medication is not null
    group by medication
    order by count(pa.subject_id) desc 
    limit 50
) top
join `masterthesis-401512.mimiciv_hosp.pharmacy` p
on top.medication = p.medication;

drop table if exists `masterthesis-401512.mimiciv_sepsis.admissions`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.admissions` as 
select distinct 
    subject_id, 
    hadm_id 
from `masterthesis-401512.mimiciv_hosp.admissions` a
where a.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

drop table if exists `masterthesis-401512.mimiciv_sepsis.procedures`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.procedures` as 
select 
    icd_code, 
    icd_version,
    subject_id,
    GENERATE_UUID() AS id
from `masterthesis-401512.mimiciv_hosp.procedures_icd` pr
where 
    icd_code is not null and 
    icd_version is not null and 
    pr.subject_id in     
        (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

-- labevents, max 10 latest labevents per subject_id
drop table if exists `masterthesis-401512.mimiciv_sepsis.labevents`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.labevents` as 
WITH RankedData AS (
  SELECT
    subject_id,
    valuenum,
    valueuom,
    ref_range_lower,
    ref_range_upper,
    flag,
    labevent_id AS id,
    ROW_NUMBER() OVER (PARTITION BY subject_id ORDER BY charttime DESC) AS row_num
  FROM `masterthesis-401512.mimiciv_hosp.labevents` lab
  WHERE subject_id IN (SELECT subject_id FROM `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)
)
SELECT
  subject_id,
  valuenum,
  valueuom,
  ref_range_lower,
  ref_range_upper,
  flag,
  id
FROM RankedData
WHERE row_num <= 10;

-- relations
-- patient_diagnosis
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_diagnosis`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_diagnosis` as 
select distinct subject_id, id
from `masterthesis-401512.mimiciv_sepsis.diagnosis` d
where d.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

-- patient_medication
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_medication`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_medication` as 
select distinct subject_id, id
from `masterthesis-401512.mimiciv_sepsis.medication` m
where m.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

-- patient_procedure
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_procedure`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_procedure` as 
select subject_id, id
from `masterthesis-401512.mimiciv_sepsis.procedures` pr
where 
    icd_code is not null and 
    icd_version is not null and 
    pr.subject_id in     
        (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

-- patient_labevents
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_labevents`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_labevents` as 
select distinct subject_id, id
from `masterthesis-401512.mimiciv_sepsis.labevents` l
where l.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);