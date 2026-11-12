# Databricks notebook source
pip install openpyxl

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_i = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cpt_pbi_sec/pl_target.xlsx"

df_pd_i = pd.read_excel(file_i, header=0, sheet_name=0)

df_i = spark.createDataFrame(df_pd_i)

df_i.createOrReplaceTempView("v_pl_target")

# COMMAND ----------

# MAGIC %sql
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_pl_target_mf(
# MAGIC section,
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC period,
# MAGIC kpi_name,
# MAGIC target,
# MAGIC year,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num,
# MAGIC data_source
# MAGIC )
# MAGIC select 
# MAGIC 'P&L' as section,
# MAGIC 'BEAUTY&WELLBEING' as bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC quarter as period,
# MAGIC 'Channel PBO' as kpi,
# MAGIC channel_pbo_target as target,
# MAGIC 2026 as year,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num,
# MAGIC 'manual' as data_source
# MAGIC from v_pl_target
# MAGIC ;