# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dwd}.fin.dwd_cpt_planning_pl_target_mf(
# MAGIC section,
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC store_type,
# MAGIC brand,
# MAGIC period,
# MAGIC kpi_name,
# MAGIC target,
# MAGIC year,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC section,
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC 'LEC' as store_type,
# MAGIC brand,
# MAGIC period,
# MAGIC kpi_name,
# MAGIC target,
# MAGIC year,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_pl_target_mf
# MAGIC ;