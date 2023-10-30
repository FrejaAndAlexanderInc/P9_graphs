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
torch_geometric for graphs and nn 

https://www.youtube.com/watch?v=-UjytpbqX4A

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