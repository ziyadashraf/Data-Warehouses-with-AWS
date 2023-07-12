# Udacity Data Engineering Nanodegree - Project 

## **Data Warehouse**
---  
  
## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
As their data engineer, I am tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for the analytics team of Sparkify to continue finding insights in what songs their users are listening to.  

## Project Description
In this project, i will apply what i've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, i will load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.  

## Run Cluster
Create and run your cluster first by running IaC.ipynb and don't forget to add configurations inside /Run Cluster/dwh.cfg

## Project Datasets
Datasets that reside in S3 links:
- Song data: `s3://udacity-dend/song_data`
- Log data: `s3://udacity-dend/log_data`
Log data json path: `s3://udacity-dend/log_json_path.json`  

## Run scripts
 Jump to the correct folder path, then run:
```bash
python create_tables.py
python etl.py
```

## Explanation of the files in the project  

- `create_tables.py`
  - This drops and creates tables
- `etl.py`
  - Loads and Inserts data into fact and dim tables.
- `sql_queries.py`
  - Contains all necessary queries for create_tables.py and etl.py.
- `dwh.cfg`
  - Credentials File.

