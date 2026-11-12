# Databricks notebook source
import pandas as pd 
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

cl_ads = spark.conf.get('spark.var.catalog.ads')
current_date = datetime.now()
dth = current_date.strftime("%Y%m%d") 
# dth = '20260129'

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_path = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/finbit/dm_tf_ddm_cc_output/{dth}"

df = spark.read.parquet(file_path)

# display(df)

# 123432
# df.count()

df.createOrReplaceTempView("v_cc_report")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf(
# MAGIC period,
# MAGIC ll1,
# MAGIC cc_report_fcst,
# MAGIC customer_group,
# MAGIC ph8,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC item_code,
# MAGIC item_name,
# MAGIC amount,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC period,
# MAGIC ll1,
# MAGIC cc_report_fcst,
# MAGIC customer_group,
# MAGIC ph8,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC item_code,
# MAGIC item_name,
# MAGIC amount,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_cc_report
# MAGIC ;

# COMMAND ----------

pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/cc_report_dim/B&W EC 12YTD  CC output.xlsx"

df_pd = pd.read_excel(file, header=0, sheet_name=0)

df = spark.createDataFrame(df_pd)

df.createOrReplaceTempView("v_cc_report_2025")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf(
# MAGIC period,
# MAGIC ll1,
# MAGIC cc_report_fcst,
# MAGIC customer_group,
# MAGIC ph8,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC item_code,
# MAGIC item_name,
# MAGIC amount,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC period,
# MAGIC ll1,
# MAGIC cc_report_fcst,
# MAGIC customer_group,
# MAGIC ph8,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC item_code,
# MAGIC item_name,
# MAGIC amount,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_cc_report_2025
# MAGIC ;