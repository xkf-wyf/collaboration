# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_ph8 = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/CPT ph8 Mapping.xlsx"

df_pd_ph8 = pd.read_excel(file_ph8, header=0, sheet_name=0)

df_ph8 = spark.createDataFrame(df_pd_ph8)

df_ph8.createOrReplaceTempView("v_ph8")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc(
# MAGIC ph8,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line_group,
# MAGIC remark,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC ph8,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line_group,
# MAGIC remark,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_ph8
# MAGIC ;