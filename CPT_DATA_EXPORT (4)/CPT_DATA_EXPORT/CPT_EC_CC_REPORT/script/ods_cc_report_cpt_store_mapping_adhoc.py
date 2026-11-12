# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_store = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/CPT Store Mapping.xlsx"

df_pd_store = pd.read_excel(file_store, header=0, sheet_name=0)

df_store = spark.createDataFrame(df_pd_store)

df_store.createOrReplaceTempView("v_store")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC with tmp_store as (
# MAGIC select distinct customer_group,store_name,cpt_scope
# MAGIC from (
# MAGIC select distinct customer_group, upper(`B&W`) as store_name, 'Y' as cpt_scope
# MAGIC from v_store 
# MAGIC where `B&W` is not null
# MAGIC union all 
# MAGIC select distinct customer_group, upper(HC) as store_name, 'Y' as cpt_scope
# MAGIC from v_store 
# MAGIC where HC is not null
# MAGIC union all 
# MAGIC select distinct customer_group, upper(PC) as store_name, 'Y' as cpt_scope
# MAGIC from v_store 
# MAGIC where PC is not null
# MAGIC union all 
# MAGIC select distinct customer_group, upper(PFM) as store_name, null as cpt_scope
# MAGIC from v_store 
# MAGIC where PFM is not null
# MAGIC ) a
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_store_mapping_adhoc(
# MAGIC customer_group,
# MAGIC store_name,
# MAGIC cpt_scope,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC customer_group,
# MAGIC store_name,
# MAGIC cpt_scope,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from tmp_store
# MAGIC ;