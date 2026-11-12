# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC delete from ${spark.var.catalog.ads}.fin_cpt.ads_cpt_ec_pnl_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;
# MAGIC
# MAGIC insert into ${spark.var.catalog.ads}.fin_cpt.ads_cpt_ec_pnl_mi
# MAGIC select 
# MAGIC    month
# MAGIC   ,bu_name as bu_code
# MAGIC   ,bu_name
# MAGIC   ,category_name as category_code
# MAGIC   ,category_name
# MAGIC   ,brand_name as brand_code
# MAGIC   ,brand_name
# MAGIC   ,product_line_group_name as product_line_group_code
# MAGIC   ,product_line_group_name
# MAGIC   ,business_type
# MAGIC   ,sold_to_code
# MAGIC   ,sold_to_name
# MAGIC   ,site_name as site_code
# MAGIC   ,site_name
# MAGIC   ,store_name as store_code
# MAGIC   ,store_name
# MAGIC   ,spending_type_fin as index_type
# MAGIC   ,amount
# MAGIC   ,'Automatic' create_by
# MAGIC   ,NOW() + INTERVAL 8 HOUR dw_create_time
# MAGIC   ,NOW() + INTERVAL 8 HOUR dw_last_update_time
# MAGIC   ,NOW() + INTERVAL 8 HOUR etl_time
# MAGIC   ,etl_flag
# MAGIC from ${spark.var.catalog.dws}.fin.dws_ec_pnl_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;