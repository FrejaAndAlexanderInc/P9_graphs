# P9

# setup 
1. ```pip install -e .```
2. ```pip install -r requirements.txt```
3. get [service account](#service-account) json key, rename to service_account.json, and place in config folder. See service 

# install Pytorch Geometric
https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html
# install DGL
https://www.dgl.ai/pages/start.html

# packages explained 
networkx for visualizing graphs 

# Service account 
A service account is needed for ehr_graph module to extract data from GBQ.
create service account: 
https://console.cloud.google.com/iam-admin/serviceaccounts?project=masterthesis-401512
get service account json file:
https://www.youtube.com/watch?v=gb0bytUGDnQ

# Google cloud
bucket: gs://mimic-iv-dataset-master/  
project: masterthesis-401512  

# Create sepsis cohort table
run the query in create_sepsis_cohort.sql 
after creating sepsis_cohort and patient_samples, used_subject_ids must be created as a union of the two

# sepsis ICD codes
ICD-9-CM Codes for Sepsis:
995.91: Sepsis  
995.92: Severe sepsis  
785.52: Septic shock  
038.xx: Certain other septicemias (various subcodes may indicate sepsis)  

ICD-10-CM Codes for Sepsis:  
A40.xx: Streptococcal sepsis  
A41.xx: Other sepsis  
R65.20: Severe sepsis without septic shock  
R65.21: Severe sepsis with septic shock  
T81.12x: Postprocedural sepsis (various subcodes)  