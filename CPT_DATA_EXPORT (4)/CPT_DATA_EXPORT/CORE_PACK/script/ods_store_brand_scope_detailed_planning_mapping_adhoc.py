# Databricks notebook source
pip install openpyxl

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

# file_store = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/CPT Store Mapping.xlsx"

file_store = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/core_pack_check_mapping/store_brand_scope_detailed_planning_mapping.xlsx"

df_pd_store = pd.read_excel(file_store, header=0, sheet_name=0)

df_store = spark.createDataFrame(df_pd_store)

df_store.createOrReplaceTempView("v_result")

# COMMAND ----------

# MAGIC %sql
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_store_brand_scope_detailed_planning_mapping_adhoc
# MAGIC select 
# MAGIC bu	
# MAGIC ,store	
# MAGIC ,category	
# MAGIC ,brand	
# MAGIC ,detailed_planning	
# MAGIC ,date_format(current_timestamp + interval 8 hour, 'yyyy-MM-dd HH:mm:ss') as dw_create_time
# MAGIC ,date_format(current_timestamp + interval 8 hour, 'yyyy-MM-dd HH:mm:ss') as dw_last_update_time
# MAGIC ,date_format(current_timestamp + interval 8 hour, 'yyyy-MM-dd HH:mm:ss') as etl_date
# MAGIC from v_result a 