# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_store_finance_spending_source_mapping(
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
# MAGIC bu_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC bmi_spend_type,
# MAGIC start_month,
# MAGIC end_month,
# MAGIC source,
# MAGIC is_current,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_store_finance_spending_source_mapping_adhoc
# MAGIC ;