# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf(
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
# MAGIC value_taxed,
# MAGIC source,
# MAGIC create_by,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC month,
# MAGIC upper(bu_code) as bu_code,
# MAGIC upper(bu_name) as bu_name,
# MAGIC upper(category_code) as category_code,
# MAGIC upper(category_name) as category_name,
# MAGIC upper(brand_code) as brand_code,
# MAGIC upper(brand_name) as brand_name,
# MAGIC upper(product_line_group_code) as product_line_group_code,
# MAGIC upper(product_line_group_name) as product_line_group_name,
# MAGIC upper(site_code) as site_code,
# MAGIC upper(site_name) as site_name,
# MAGIC upper(store_code) as store_code,
# MAGIC upper(store_name) as store_name,
# MAGIC bmi_spend_type as index_type,
# MAGIC CASE 
# MAGIC     WHEN SOURCE = 'cc_report' 
# MAGIC     THEN value_untaxed * -1 
# MAGIC     ELSE value_untaxed 
# MAGIC END AS value_untaxed,   --2026/08/31 PFM三合一-cc_report逻辑value_untaxed * -1
# MAGIC value_taxed,
# MAGIC source,
# MAGIC 'Automatic' as create_by,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from ${spark.var.catalog.dws}.fin.dws_pfm_spending_mf
# MAGIC ;