# Databricks notebook source
# MAGIC %py
# MAGIC import pandas as pd 
# MAGIC import os
# MAGIC from datetime import datetime
# MAGIC from dateutil.relativedelta import relativedelta
# MAGIC
# MAGIC cl_ads = spark.conf.get('spark.var.catalog.ads')
# MAGIC current_date = datetime.now()
# MAGIC last_month_date = current_date - relativedelta(months = 1)
# MAGIC mth = last_month_date.strftime("%Y%m") 
# MAGIC # mth = '202602'
# MAGIC # bill_month = last_month_date.strftime("%Y-%m")  
# MAGIC # bill_month = '2025-11'
# MAGIC
# MAGIC
# MAGIC # 路径设置
# MAGIC table_name = f'{cl_ads}.fin_cpt.ads_ec_platform_bill_mi'
# MAGIC out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt_ec_platform_bill/ec_platform_bill/'
# MAGIC file_name = f'ads_ec_platform_bill_mi_{mth}.csv'
# MAGIC
# MAGIC # 如果目录不存在，则创建目录
# MAGIC if not os.path.exists(out_path): 
# MAGIC     os.makedirs(out_path)
# MAGIC
# MAGIC spark_sql = f'''
# MAGIC select 
# MAGIC 	month,
# MAGIC     bu_code,
# MAGIC     bu_name,
# MAGIC     category_code,
# MAGIC     category_name,
# MAGIC     brand_code,
# MAGIC     brand_name,
# MAGIC     product_line_group_code,
# MAGIC     product_line_group_name,
# MAGIC     business_type,
# MAGIC    CASE   WHEN UPPER(site_code) LIKE '%TMALL%'  THEN 'TMALL'
# MAGIC     WHEN UPPER(site_code) LIKE '%JD%'     THEN 'JD'
# MAGIC     WHEN UPPER(site_code) LIKE '%VIP%'    THEN 'VIP'
# MAGIC     WHEN UPPER(site_code) LIKE '%PDD%'    THEN 'PDD'
# MAGIC     WHEN UPPER(site_code) LIKE '%DOUYIN%'    THEN 'DOUYIN'
# MAGIC     ELSE site_code
# MAGIC     END AS site_code,
# MAGIC    CASE   WHEN UPPER(site_name) LIKE '%TMALL%' THEN 'TMALL'
# MAGIC     WHEN UPPER(site_name) LIKE '%JD%'    THEN 'JD'
# MAGIC     WHEN UPPER(site_name) LIKE '%VIP%'    THEN 'VIP'
# MAGIC     WHEN UPPER(site_name) LIKE '%PDD%'    THEN 'PDD'
# MAGIC     WHEN UPPER(site_name) LIKE '%DOUYIN%'    THEN 'DOUYIN'
# MAGIC     ELSE site_name
# MAGIC     END AS site_name,
# MAGIC     store_code,
# MAGIC     store_name,
# MAGIC     spending_type_fin,
# MAGIC     amount_taxed,
# MAGIC     amount_untaxed,
# MAGIC     create_by,
# MAGIC     dw_create_time,
# MAGIC     dw_last_update_time,
# MAGIC     etl_time
# MAGIC     from {table_name} where month = '{mth}' 
# MAGIC     ;
# MAGIC '''
# MAGIC
# MAGIC
# MAGIC pf = spark.sql(spark_sql).toPandas()
# MAGIC
# MAGIC # 导出数据到CSV文件
# MAGIC pf.to_csv(out_path + file_name, index=False, header=True, mode='w+')
# MAGIC