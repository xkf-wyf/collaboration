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
# MAGIC
# MAGIC # 路径设置
# MAGIC table_name = f'{cl_dws}.ddm.dws_pdd_bill_mi'
# MAGIC out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt_ec_platform_bill/raw_data_pdd/'
# MAGIC file_name = f'dws_pdd_bill_mi_{mth}.csv'
# MAGIC
# MAGIC # 如果目录不存在，则创建目录
# MAGIC if not os.path.exists(out_path): 
# MAGIC     os.makedirs(out_path)
# MAGIC
# MAGIC spark_sql = f'''
# MAGIC select 
# MAGIC 	product_id
# MAGIC 	,product_name
# MAGIC 	,ul_sku_code
# MAGIC 	,lp_untax
# MAGIC 	,qty
# MAGIC 	,gsv
# MAGIC 	,gmv
# MAGIC 	,total_price
# MAGIC 	,store_discount
# MAGIC 	,trans_duoduo
# MAGIC 	,trans_technical_service_fee
# MAGIC 	,trans_deduction
# MAGIC 	,trans_other
# MAGIC 	,trans_other_service
# MAGIC 	,trans_account_split
# MAGIC 	,inbox_market_campaign_settlement
# MAGIC 	,inbox_market_campaign_recovery
# MAGIC 	,inbox_service_fee_settlement
# MAGIC 	,inbox_service_fee_recovery
# MAGIC 	,inbox_technical_service_fee_return
# MAGIC 	,trans_cannot_disassembled_fee
# MAGIC 	,positive_reward_fee
# MAGIC 	,CASE WHEN bu='B&W' THEN 'BEAUTY&WELLBEING'
# MAGIC 			WHEN bu='PC' THEN 'PERSONAL CARE'
# MAGIC 			WHEN bu='HC' THEN 'HOME CARE'
# MAGIC 			ELSE bu END AS bu
# MAGIC 	,UPPER(category) AS category
# MAGIC 	,UPPER(brand) AS brand
# MAGIC 	,UPPER(product_line_group) AS product_line_group
# MAGIC 	,write_off_cpp
# MAGIC 	,cpp_percent
# MAGIC 	,statistics_return_qty
# MAGIC 	,statistics_return_gsv
# MAGIC 	,statistics_return_gmv
# MAGIC 	,REPLACE(mth,'-','') AS mth
# MAGIC 	,'PDD' as site_name
# MAGIC 	,'PDD - UL' as store_name
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