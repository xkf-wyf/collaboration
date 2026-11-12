# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd
from pyspark.sql.functions import lit,col,replace,when

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_store = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/pfm_dim/store_finance_spending_source_mapping_data.xlsx"

df_pd_store = pd.read_excel(file_store, header=0, sheet_name=0)

df_store = spark.createDataFrame(df_pd_store)

df_store_new = df_store \
    .withColumn("is_current", lit("1")) \
    .withColumn("source",when(col("source") == "账单", "platform_bill").otherwise(col("source")))

df_store_new.createOrReplaceTempView("v_store")

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_store_finance_spending_source_mapping_adhoc(
# MAGIC bu_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC bmi_spend_type,
# MAGIC start_month,
# MAGIC end_month,
# MAGIC source,
# MAGIC is_current,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select
# MAGIC src.bu_name,
# MAGIC src.site_name,
# MAGIC src.store_name,
# MAGIC src.bmi_spend_type,
# MAGIC src.start_month,
# MAGIC src.end_month,
# MAGIC src.source,
# MAGIC src.is_current,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from v_store src
# MAGIC ;