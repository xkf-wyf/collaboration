# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping(
# MAGIC customer_group,
# MAGIC store_name,
# MAGIC cpt_scope,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC customer_group,
# MAGIC store_name,
# MAGIC cpt_scope,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_store_mapping_adhoc
# MAGIC ;