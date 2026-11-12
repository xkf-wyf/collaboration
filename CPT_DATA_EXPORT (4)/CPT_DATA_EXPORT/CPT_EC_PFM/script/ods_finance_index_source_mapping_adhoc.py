# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_index = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/pfm_dim/finance_index_source_mapping.xlsx"

df_pd_index = pd.read_excel(file_index, header=0, sheet_name=0)

df_index = spark.createDataFrame(df_pd_index)

df_index.createOrReplaceTempView("v_index")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_finance_index_source_mapping_adhoc(
# MAGIC source,
# MAGIC bmi_spend_type,
# MAGIC source_index_type,
# MAGIC output_index_type,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC source,
# MAGIC bmi_spend_type,
# MAGIC source_index_type,
# MAGIC output_index_type,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_index
# MAGIC ;