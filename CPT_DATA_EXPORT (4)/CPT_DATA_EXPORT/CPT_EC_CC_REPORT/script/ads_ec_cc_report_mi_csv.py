# Databricks notebook source

import pandas as pd 
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

cl_ads = spark.conf.get('spark.var.catalog.ads')
current_date = datetime.now()
last_month_date = current_date - relativedelta(months=1)
mth = last_month_date.strftime("%Y%m")
# mth = '202601'

# table_name = f'{cl_ads}.fin_cpt.ads_ec_cc_report_mi'
out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt_ec_cc_report/'
file_name = f'ads_ec_cc_report_mi_{mth}.csv'

# 如果目录不存在，则创建目录
if not os.path.exists(out_path): 
    os.makedirs(out_path)

c_mth = current_date.strftime("%m")
f_mth = current_date.strftime("%Y")+'01'
l_mth = last_month_date.strftime("%Y")+'01'

if c_mth == '01':
    
    spark_sql = f'''
select 
MONTH,
BU_CODE,
BU_NAME,
CATEGORY_CODE,
CATEGORY_NAME,
BRAND_CODE,
BRAND_NAME,
 translate(PRODUCT_LINE_GROUP_CODE,
          concat(chr(160),chr(12288),chr(8199),chr(8202),chr(8232),chr(8233),chr(8203),chr(8239),chr(8287),chr(65279),chr(5760)),
          repeat(' ', 11)) AS PRODUCT_LINE_GROUP_CODE,
 translate(PRODUCT_LINE_GROUP_NAME,
          concat(chr(160),chr(12288),chr(8199),chr(8202),chr(8232),chr(8233),chr(8203),chr(8239),chr(8287),chr(65279),chr(5760)),
          repeat(' ', 11)) AS PRODUCT_LINE_GROUP_NAME,
CASE   WHEN UPPER(SITE_CODE) LIKE '%TMALL%'  THEN 'TMALL'
    WHEN UPPER(SITE_CODE) LIKE '%JD%'     THEN 'JD'
    WHEN UPPER(SITE_CODE) LIKE '%VIP%'    THEN 'VIP'
    WHEN UPPER(SITE_CODE) LIKE '%PDD%'    THEN 'PDD'
    WHEN UPPER(SITE_CODE) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    WHEN UPPER(STORE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    ELSE SITE_CODE
    END AS SITE_CODE,
CASE   WHEN UPPER(SITE_NAME) LIKE '%TMALL%' THEN 'TMALL'
    WHEN UPPER(SITE_NAME) LIKE '%JD%'    THEN 'JD'
    WHEN UPPER(SITE_NAME) LIKE '%VIP%'    THEN 'VIP'
    WHEN UPPER(SITE_NAME) LIKE '%PDD%'    THEN 'PDD'
    WHEN UPPER(SITE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    WHEN UPPER(STORE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    ELSE SITE_NAME
    END AS SITE_NAME,
STORE_CODE,
STORE_NAME,
INDEX_TYPE,
VALUE_UNTAXED/1000 as VALUE_UNTAXED,
CREATE_BY,
DW_CREATE_TIME,
DW_LAST_UPDATE_TIME,
ETL_TIME
from {cl_ads}.fin_cpt.ads_ec_cc_report_mi
where month >= '{l_mth}'
and month < '{f_mth}'
;
'''

else:

  spark_sql = f'''
select 
MONTH,
BU_CODE,
BU_NAME,
CATEGORY_CODE,
CATEGORY_NAME,
BRAND_CODE,
BRAND_NAME,
 translate(PRODUCT_LINE_GROUP_CODE,
          concat(chr(160),chr(12288),chr(8199),chr(8202),chr(8232),chr(8233),chr(8203),chr(8239),chr(8287),chr(65279),chr(5760)),
          repeat(' ', 11)) AS PRODUCT_LINE_GROUP_CODE,
 translate(PRODUCT_LINE_GROUP_NAME,
          concat(chr(160),chr(12288),chr(8199),chr(8202),chr(8232),chr(8233),chr(8203),chr(8239),chr(8287),chr(65279),chr(5760)),
          repeat(' ', 11)) AS PRODUCT_LINE_GROUP_NAME,
CASE   WHEN UPPER(SITE_CODE) LIKE '%TMALL%'  THEN 'TMALL'
    WHEN UPPER(SITE_CODE) LIKE '%JD%'     THEN 'JD'
    WHEN UPPER(SITE_CODE) LIKE '%VIP%'    THEN 'VIP'
    WHEN UPPER(SITE_CODE) LIKE '%PDD%'    THEN 'PDD'
    WHEN UPPER(SITE_CODE) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    WHEN UPPER(STORE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    ELSE SITE_CODE
    END AS SITE_CODE,
CASE   WHEN UPPER(SITE_NAME) LIKE '%TMALL%' THEN 'TMALL'
    WHEN UPPER(SITE_NAME) LIKE '%JD%'    THEN 'JD'
    WHEN UPPER(SITE_NAME) LIKE '%VIP%'    THEN 'VIP'
    WHEN UPPER(SITE_NAME) LIKE '%PDD%'    THEN 'PDD'
    WHEN UPPER(SITE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    WHEN UPPER(STORE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
    ELSE SITE_NAME
    END AS SITE_NAME,
STORE_CODE,
STORE_NAME,
INDEX_TYPE,
VALUE_UNTAXED/1000 as VALUE_UNTAXED,
CREATE_BY,
DW_CREATE_TIME,
DW_LAST_UPDATE_TIME,
ETL_TIME
from {cl_ads}.fin_cpt.ads_ec_cc_report_mi
where 1 = 1
and month >= '{f_mth}'
;
'''

pf = spark.sql(spark_sql).toPandas()

# 导出数据到CSV文件
pf.to_csv(out_path + file_name, index = False, header = True, mode='w+')