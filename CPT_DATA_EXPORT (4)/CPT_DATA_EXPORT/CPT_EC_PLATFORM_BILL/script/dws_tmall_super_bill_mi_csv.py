# Databricks notebook source
# MAGIC %py
# MAGIC import pandas as pd 
# MAGIC import os
# MAGIC from datetime import datetime
# MAGIC from dateutil.relativedelta import relativedelta
# MAGIC
# MAGIC cl_dws = spark.conf.get('spark.var.catalog.dws')
# MAGIC cl_ads = spark.conf.get('spark.var.catalog.ads')
# MAGIC current_date = datetime.now()
# MAGIC last_month_date = current_date - relativedelta(months = 1)
# MAGIC mth = last_month_date.strftime("%Y%m") 
# MAGIC # mth = '202511'
# MAGIC bill_month = last_month_date.strftime("%Y-%m")  
# MAGIC # bill_month = '2025-11'
# MAGIC
# MAGIC # 路径设置
# MAGIC table_name = f'{cl_dws}.ddm.dws_tmall_super_bill_mi'
# MAGIC out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt_ec_platform_bill/raw_data_tmall_super/'
# MAGIC file_name = f'dws_tmall_super_bill_mi_{mth}.csv'
# MAGIC
# MAGIC # 如果目录不存在，则创建目录
# MAGIC if not os.path.exists(out_path): 
# MAGIC     os.makedirs(out_path)
# MAGIC
# MAGIC spark_sql = f'''
# MAGIC select 
# MAGIC 	backend_product_code
# MAGIC 	,backend_product_name
# MAGIC 	,CASE WHEN bu='B&W' THEN 'BEAUTY&WELLBEING'
# MAGIC 			WHEN bu='PC' THEN 'PERSONAL CARE'
# MAGIC 			WHEN bu='HC' THEN 'HOME CARE'
# MAGIC 			ELSE bu END AS bu
# MAGIC 	,UPPER(category) AS category
# MAGIC 	,UPPER(brand) AS brand
# MAGIC 	,UPPER(product_line_group) AS product_line_group
# MAGIC 	,fee_type
# MAGIC 	,fee_type_sort
# MAGIC 	,untaxed_amount
# MAGIC 	,dw_last_update_time
# MAGIC 	,data_source
# MAGIC 	,REPLACE(mth,'-','') AS mth
# MAGIC 	,CASE WHEN fee_type IN ('供应商承担优惠金额','收入金额') THEN 'GMV'
# MAGIC 			WHEN fee_type IN ('商品成本') THEN 'Secondary GSV'
# MAGIC 			WHEN fee_type IN ('Total CPP') THEN 'CPP'
# MAGIC 			WHEN fee_type IN ('平台费') THEN '平台费'
# MAGIC 			WHEN fee_type IN ('百亿补贴佣金','淘客U选返佣','营销活动-淘客','营销活动-淘客团长服务费') THEN 'CPS'
# MAGIC 			WHEN fee_type IN ('达播佣金','店播佣金') THEN 'Livestream'
# MAGIC 			WHEN fee_type IN ('品牌新享') THEN '品牌新享'
# MAGIC 			ELSE NULL END AS  spending_type_fin
# MAGIC 	,'TMALL' as site_name
# MAGIC 	,'TMALL SUPER - UL' as store_name
# MAGIC     from {table_name} where mth = '{bill_month}' 
# MAGIC     ;
# MAGIC '''
# MAGIC
# MAGIC
# MAGIC pf = spark.sql(spark_sql).toPandas()
# MAGIC
# MAGIC # 导出数据到CSV文件
# MAGIC pf.to_csv(out_path + file_name, index=False, header=True, mode='w+')
# MAGIC