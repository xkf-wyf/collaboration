# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_planning_formula_mapping(
# MAGIC period_code,
# MAGIC formula_type,
# MAGIC index_type_code,
# MAGIC index_type,
# MAGIC package_item_sub_type_code,
# MAGIC package_item_sub_type,
# MAGIC formula_code,
# MAGIC formula_name,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC period_code,
# MAGIC formula_type,
# MAGIC index_type_code,
# MAGIC index_type,
# MAGIC package_item_sub_type_code,
# MAGIC package_item_sub_type,
# MAGIC formula_code,
# MAGIC formula_name,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_golden_formula_configuration_mf
# MAGIC ;