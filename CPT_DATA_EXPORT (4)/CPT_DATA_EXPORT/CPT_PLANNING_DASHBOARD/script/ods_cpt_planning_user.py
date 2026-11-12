# Databricks notebook source
pip install openpyxl

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_i = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cpt_pbi/dim_cpt_planning_user.xlsx"

df_pd_i = pd.read_excel(file_i, header=0, sheet_name=0)

df_i = spark.createDataFrame(df_pd_i)

df_i.createOrReplaceTempView("v_dim_cpt_planning_user")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_user(
# MAGIC bu_name,
# MAGIC user_name,
# MAGIC email,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC bu_name,
# MAGIC user_name,
# MAGIC email,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from v_dim_cpt_planning_user
# MAGIC ;