# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_sort_mapping(
# MAGIC index_level1_name,
# MAGIC index_level2_name,
# MAGIC index_level3_name,
# MAGIC index_level3_code,
# MAGIC unit,
# MAGIC level1_sort,
# MAGIC level2_sort,
# MAGIC sort,
# MAGIC index_union_key,
# MAGIC index_type_level1_code,
# MAGIC index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC index_level1_name,
# MAGIC index_level2_name,
# MAGIC index_level3_name,
# MAGIC index_level3_code,
# MAGIC unit,
# MAGIC level1_sort,
# MAGIC level2_sort,
# MAGIC sort,
# MAGIC index_union_key,
# MAGIC index_type_level1_code,
# MAGIC index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_index_sort_mapping
# MAGIC ;