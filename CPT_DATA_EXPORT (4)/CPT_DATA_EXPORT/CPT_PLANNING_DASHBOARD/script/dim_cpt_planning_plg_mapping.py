# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_planning_plg_mapping(
# MAGIC bu_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC plg_union_key,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select distinct  
# MAGIC bu_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC bu_name||site_name||store_name||category_name||brand_name||product_line_group_name as plg_union_key,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num 
# MAGIC from ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf 
# MAGIC ; 