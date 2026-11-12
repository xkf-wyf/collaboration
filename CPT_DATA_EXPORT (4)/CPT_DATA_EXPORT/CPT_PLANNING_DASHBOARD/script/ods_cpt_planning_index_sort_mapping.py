# Databricks notebook source
pip install openpyxl

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_i = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cpt_pbi/dim_cpt_planning_index_sort_mapping.xlsx"

df_pd_i = pd.read_excel(file_i, header=0, sheet_name=0)

df_i = spark.createDataFrame(df_pd_i)

df_i.createOrReplaceTempView("v_dim_cpt_planning_index_sort_mapping")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_index_sort_mapping(
# MAGIC index_level1_name,
# MAGIC index_level2_name,
# MAGIC index_level3_name,
# MAGIC index_level3_code,
# MAGIC unit,
# MAGIC level1_sort,
# MAGIC level2_sort,
# MAGIC sort,
# MAGIC index_union_key,
# MAGIC index_type_level1_code,
# MAGIC index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC index_level1_name,
# MAGIC index_level2_name,
# MAGIC index_level3_name,
# MAGIC index_level3_code,
# MAGIC unit,
# MAGIC level1_sort,
# MAGIC level2_sort,
# MAGIC sort,
# MAGIC index_union_key,
# MAGIC index_type_level1_code,
# MAGIC index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from v_dim_cpt_planning_index_sort_mapping
# MAGIC ;