# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_plg = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/CC PLG Mapping.xlsx"

df_pd_plg = pd.read_excel(file_plg, header=0, sheet_name=0)

df_plg = spark.createDataFrame(df_pd_plg)

df_plg.createOrReplaceTempView("v_plg")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc(
# MAGIC cc_bu,
# MAGIC cc_category,
# MAGIC cc_brand,
# MAGIC cc_product_line,
# MAGIC cpt_category,
# MAGIC cpt_brand,
# MAGIC cpt_plg,
# MAGIC remark,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC cc_bu,
# MAGIC cc_category,
# MAGIC cc_brand,
# MAGIC cc_product_line,
# MAGIC cpt_category,
# MAGIC cpt_brand,
# MAGIC cpt_plg,
# MAGIC remark,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from v_plg
# MAGIC ;