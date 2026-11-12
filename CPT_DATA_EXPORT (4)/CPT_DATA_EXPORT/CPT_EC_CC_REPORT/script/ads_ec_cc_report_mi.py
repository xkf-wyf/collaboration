# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC with tmp_store as (
# MAGIC select distinct store_name
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping
# MAGIC where 1 = 1
# MAGIC and cpt_scope = 'Y'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_index as (
# MAGIC select distinct cpt_index_mapping
# MAGIC from (
# MAGIC select cpt_index_mapping
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_index_mapping
# MAGIC where 1 = 1
# MAGIC and cpt_scope = 'Y'
# MAGIC union all
# MAGIC select cpt_index_mapping
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc
# MAGIC where 1 = 1
# MAGIC and cpt_scope = 'Y'
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_ads as (
# MAGIC select 
# MAGIC  t1.month
# MAGIC ,t1.bu_code
# MAGIC ,t1.bu_name
# MAGIC ,t1.category_code
# MAGIC ,t1.category_name
# MAGIC ,t1.brand_code
# MAGIC ,t1.brand_name
# MAGIC ,t1.product_line_group_code
# MAGIC ,t1.product_line_group_name
# MAGIC ,t1.site_code
# MAGIC ,t1.site_name
# MAGIC ,t1.store_code
# MAGIC ,t1.store_name
# MAGIC ,t1.index_type
# MAGIC ,t1.value_untaxed
# MAGIC from ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi t1
# MAGIC inner join tmp_store t2 
# MAGIC on upper(t1.store_name) = upper(t2.store_name) 
# MAGIC inner join tmp_index t3 
# MAGIC on upper(t1.index_type) = upper(t3.cpt_index_mapping)
# MAGIC where 1 = 1
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_ec_cc_report_mi(
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
# MAGIC create_by,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
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
# MAGIC 'Automatic' as create_by,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from tmp_ads
# MAGIC ;