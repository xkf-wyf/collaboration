# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping(
# MAGIC period_code,
# MAGIC indicator_type,
# MAGIC index_type_code,
# MAGIC index_type,
# MAGIC package_item_sub_type_code,
# MAGIC package_item_sub_type,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select  
# MAGIC period_code,
# MAGIC indicator_type,
# MAGIC index_type_code,
# MAGIC index_type,
# MAGIC package_item_sub_type_code,
# MAGIC package_item_sub_type,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf
# MAGIC ;