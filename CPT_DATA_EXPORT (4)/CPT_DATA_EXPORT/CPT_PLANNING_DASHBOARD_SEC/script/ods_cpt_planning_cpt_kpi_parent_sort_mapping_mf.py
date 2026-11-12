# Databricks notebook source
pip install openpyxl

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_i = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cpt_pbi_sec/kpi_order_cpt_parent.xlsx"

df_pd_i = pd.read_excel(file_i, header=0, sheet_name=0)

df_i = spark.createDataFrame(df_pd_i)

df_i.createOrReplaceTempView("v_kpi_order_cpt_parent")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_parent_sort_mapping_mf(
# MAGIC kpi_parent_sort_no,
# MAGIC kpi_parent_name,
# MAGIC kpi_list,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num,
# MAGIC data_source
# MAGIC )
# MAGIC select 
# MAGIC kpi_parent_order,
# MAGIC kpi_parent,
# MAGIC kpi_content,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num,
# MAGIC 'manual' as data_source
# MAGIC from v_kpi_order_cpt_parent
# MAGIC ;