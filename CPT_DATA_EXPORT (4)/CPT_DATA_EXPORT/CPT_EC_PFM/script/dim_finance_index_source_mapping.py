# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping(
# MAGIC source,
# MAGIC bmi_spend_type,
# MAGIC source_index_type,
# MAGIC output_index_type,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC source,
# MAGIC bmi_spend_type,
# MAGIC source_index_type,
# MAGIC output_index_type,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_finance_index_source_mapping_adhoc
# MAGIC ;