# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_index = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/CPT Index Mapping.xlsx"

df_pd_index = pd.read_excel(file_index, header=0, sheet_name=0)

df_index = spark.createDataFrame(df_pd_index)

df_index.createOrReplaceTempView("v_index")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc(
# MAGIC item_code,
# MAGIC item_name,
# MAGIC cpt_index_mapping,
# MAGIC cpt_scope,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC item_code,
# MAGIC item_name,
# MAGIC cpt_index_mapping,
# MAGIC cpt_scope,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_index
# MAGIC ;

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_index = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/CPT Index Mapping_2025.xlsx"

df_pd_index = pd.read_excel(file_index, header=0, sheet_name=0)

df_index = spark.createDataFrame(df_pd_index)

df_index.createOrReplaceTempView("v_index_2025")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc(
# MAGIC item_code,
# MAGIC item_name,
# MAGIC cpt_index_mapping,
# MAGIC cpt_scope,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC item_code,
# MAGIC item_name,
# MAGIC cpt_index_mapping,
# MAGIC cpt_scope,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_index_2025
# MAGIC ;