# Databricks notebook source
pip install openpyxl

# COMMAND ----------

import pandas as pd
catalog_ods = spark.conf.get("spark.var.catalog.ods")
file_path = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/fin_mapping/finance_spending_type_mapping.xlsx"
df_pd = pd.read_excel(file_path, header=0, sheet_name=0)
df = spark.createDataFrame(df_pd)
df.createOrReplaceTempView("result")

# COMMAND ----------

# MAGIC %sql
# MAGIC truncate table ${spark.var.catalog.dim}.fin.dim_platform_finance_spending_mapping;

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into ${spark.var.catalog.dim}.fin.dim_platform_finance_spending_mapping
# MAGIC select 
# MAGIC a.platform_name
# MAGIC ,a.fee_type_platform
# MAGIC ,a.spending_type_fin
# MAGIC ,CURRENT_TIMESTAMP() + INTERVAL 8 HOUR AS dw_create_time
# MAGIC ,CURRENT_TIMESTAMP() + INTERVAL 8 HOUR AS dw_last_update_time
# MAGIC ,CURRENT_TIMESTAMP() + INTERVAL 8 HOUR AS etl_time
# MAGIC from result a 