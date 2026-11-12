# Databricks notebook source

import pandas as pd 
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

cl_ads = spark.conf.get('spark.var.catalog.ads')
# dt = dbutils.widgets.get("dt")
# current_date = datetime.strptime(dt, '%Y-%m-%d')
current_date = datetime.now()
last_month_date = current_date - relativedelta(months = 1)
mth = last_month_date.strftime("%Y%m") 
# mth = '202512'

# table_name = f'{cl_ads}.fin_cpt.ads_bmi_spending_mf'
out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt_ec_pnl/'
file_name = f'ads_cpt_ec_pnl_mi_{mth}.csv'

# 如果目录不存在，则创建目录
if not os.path.exists(out_path): 
    os.makedirs(out_path)

spark_sql = f'''
select 
   month
  ,bu_code
  ,bu_name
  ,category_code
  ,category_name
  ,brand_code
  ,brand_name
  ,product_line_group_code
  ,product_line_group_name
  ,business_type
  ,sold_to_code
  ,sold_to_name
  ,CASE   WHEN UPPER(site_code) LIKE '%TMALL%'  THEN 'TMALL'
          WHEN UPPER(site_code) LIKE '%JD%'     THEN 'JD'
          WHEN UPPER(site_code) LIKE '%VIP%'    THEN 'VIP'
          WHEN UPPER(site_code) LIKE '%PDD%'    THEN 'PDD'
          WHEN UPPER(site_code) LIKE '%DOUYIN%'    THEN 'DOUYIN'
          ELSE site_code
          END AS site_code
  ,CASE   WHEN UPPER(site_name) LIKE '%TMALL%' THEN 'TMALL'
          WHEN UPPER(site_name) LIKE '%JD%'    THEN 'JD'
          WHEN UPPER(site_name) LIKE '%VIP%'    THEN 'VIP'
          WHEN UPPER(site_name) LIKE '%PDD%'    THEN 'PDD'
          WHEN UPPER(site_name) LIKE '%DOUYIN%'    THEN 'DOUYIN'
          ELSE site_name
          END AS site_name
  ,store_code
  ,store_name
  ,index_type
  ,amount
  ,create_by
  ,dw_create_time
  ,dw_last_update_time
  ,etl_time
  ,etl_flag
from {cl_ads}.fin_cpt.ads_cpt_ec_pnl_mi
where 1 = 1
and etl_flag = date_format(current_date(), 'yyyyMM')
;
'''

pf = spark.sql(spark_sql).toPandas()

# 导出数据到CSV文件
pf.to_csv(out_path + file_name, index = False, header = True, mode='w+')