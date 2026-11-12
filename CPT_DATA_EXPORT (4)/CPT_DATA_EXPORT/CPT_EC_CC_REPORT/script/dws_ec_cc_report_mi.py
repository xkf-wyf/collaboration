# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC with tmp_dws as (
# MAGIC select 
# MAGIC  month
# MAGIC ,bu_name
# MAGIC ,category_name
# MAGIC ,brand_name
# MAGIC ,product_line_group_name
# MAGIC ,site_name
# MAGIC ,store_name
# MAGIC ,index_type
# MAGIC ,sum(value_untaxed) as value_untaxed
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_ec_cc_report_mi
# MAGIC where 1 = 1
# MAGIC and COALESCE(month,'') <> ''
# MAGIC and COALESCE(bu_name,'') <> ''
# MAGIC and COALESCE(category_name,'') <> ''
# MAGIC and COALESCE(brand_name,'') <> ''
# MAGIC and COALESCE(product_line_group_name,'') <> ''
# MAGIC and COALESCE(site_name,'') <> ''
# MAGIC and COALESCE(store_name,'') <> ''
# MAGIC and COALESCE(index_type,'') <> ''
# MAGIC group by 
# MAGIC  month
# MAGIC ,bu_name
# MAGIC ,category_name
# MAGIC ,brand_name
# MAGIC ,product_line_group_name
# MAGIC ,site_name
# MAGIC ,store_name
# MAGIC ,index_type
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi(
# MAGIC month,
# MAGIC bu_code,
# MAGIC bu_name,
# MAGIC category_code,
# MAGIC category_name,
# MAGIC brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC site_code,
# MAGIC site_name,
# MAGIC store_code,
# MAGIC store_name,
# MAGIC index_type,
# MAGIC value_untaxed,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC month,
# MAGIC bu_name as bu_code,
# MAGIC bu_name,
# MAGIC category_name as category_code,
# MAGIC category_name,
# MAGIC brand_name as brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_name as product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC site_name as site_code,
# MAGIC site_name,
# MAGIC store_name as store_code,
# MAGIC store_name,
# MAGIC index_type,
# MAGIC value_untaxed,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from tmp_dws
# MAGIC ;