# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_plg_mapping(
# MAGIC cc_bu,
# MAGIC cc_category,
# MAGIC cc_brand,
# MAGIC cc_product_line,
# MAGIC cpt_category,
# MAGIC cpt_brand,
# MAGIC cpt_plg,
# MAGIC remark,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC cc_bu,
# MAGIC cc_category,
# MAGIC cc_brand,
# MAGIC cc_product_line,
# MAGIC cpt_category,
# MAGIC cpt_brand,
# MAGIC cpt_plg,
# MAGIC remark,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc
# MAGIC ;