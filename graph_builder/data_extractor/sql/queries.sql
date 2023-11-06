-- entities
drop table if exists `masterthesis-401512.mimiciv_sepsis.diagnosis`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.diagnosis` AS
SELECT
  DENSE_RANK() OVER (ORDER BY d.icd_code, d.icd_version) AS id,
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
        row_number() over () as id
    from `masterthesis-401512.mimiciv_hosp.pharmacy` ph
    join `masterthesis-401512.mimiciv_hosp.patients` pa
        on ph.subject_id = pa.subject_id
    where medication is not null
    group by medication
    order by count(pa.subject_id) desc 
    limit 50
) top
join `masterthesis-401512.mimiciv_hosp.pharmacy` p
on top.medication = p.medication

drop table if exists `masterthesis-401512.mimiciv_sepsis.admissions`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.admissions` as 
select distinct subject_id, hadm_id from `masterthesis-401512.mimiciv_hosp.admissions` a
where a.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

drop table if exists `masterthesis-401512.mimiciv_sepsis.procedures`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.procedures` as 
select 
    icd_code, 
    icd_version,
    subject_id,
    DENSE_RANK() OVER (ORDER BY icd_code, icd_version) AS id
from `masterthesis-401512.mimiciv_hosp.procedures_icd` pr
where 
    icd_code is not null and 
    icd_version is not null and 
    pr.subject_id in     
        (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

drop table if exists `masterthesis-401512.mimiciv_sepsis.labevents`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.labevents` as 
select 
    lab.subject_id, 
    lab.valuenum, 
    lab.valueuom, 
    lab.ref_range_lower, 
    lab.ref_range_upper, 
    lab.flag,
    lab.labevent_id as id
from `masterthesis-401512.mimiciv_hosp.labevents` lab
inner join `masterthesis-401512.mimiciv_hosp.d_labitems` item on
lab.itemid = item.itemid
where lab.subject_id in     
    (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`);

-- relations
-- patient_diagnosis
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_diagnosis`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_diagnosis` as 
select distinct subject_id, id
from `masterthesis-401512.mimiciv_sepsis.diagnosis` d
where d.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)

-- patient_medication
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_medication`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_medication` as 
select distinct subject_id, id
from `masterthesis-401512.mimiciv_sepsis.medication` m
where m.subject_id in
(select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)

-- patient_procedure
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_procedure`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_procedure` as 
select subject_id, id
from `masterthesis-401512.mimiciv_sepsis.procedures` pr
where 
    icd_code is not null and 
    icd_version is not null and 
    pr.subject_id in     
        (select subject_id from `masterthesis-401512.mimiciv_sepsis.used_subject_ids`)

-- patient_labevents
drop table if exists `masterthesis-401512.mimiciv_sepsis.patient_labevents`;
CREATE TABLE `masterthesis-401512.mimiciv_sepsis.patient_labevents` as 
select distinct subject_id, id
from `masterthesis-401512.mimiciv_sepsis.labevents`