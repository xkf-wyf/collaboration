# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping(
# MAGIC kpi_parent_sort_no,
# MAGIC kpi_parent_name,
# MAGIC kpi_list,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC kpi_parent_sort_no,
# MAGIC kpi_parent_name,
# MAGIC kpi_list,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_parent_sort_mapping_mf
# MAGIC ;