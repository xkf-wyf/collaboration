# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_index_mapping(
# MAGIC item_code,
# MAGIC item_name,
# MAGIC cpt_index_mapping,
# MAGIC cpt_scope,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC item_code,
# MAGIC item_name,
# MAGIC cpt_index_mapping,
# MAGIC cpt_scope,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc
# MAGIC ;