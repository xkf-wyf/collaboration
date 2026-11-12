# Databricks notebook source
dbutils.widgets.text("dt", '2026-03-31')
dbutils.widgets.text("current_date", '2026-03-31')

# COMMAND ----------

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

cl_ads = spark.conf.get('spark.var.catalog.ads')
dt = dbutils.widgets.get("dt")
current_date = datetime.strptime(dt, '%Y-%m-%d')
last_month_date = current_date - relativedelta(months=1)
mth = last_month_date.strftime("%Y%m")

table_name = f'{cl_ads}.fin_cpt.ads_bmi_golden_mf'
out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt_bmi_golden/'
file_name = f'cpt_bmi_golden_{mth}.csv'
full_output_path = os.path.join(out_path, file_name)

dbutils.fs.mkdirs(out_path)

try:
    if dbutils.fs.ls(full_output_path):
        dbutils.fs.rm(full_output_path)
        print(f"已删除同名旧文件：{full_output_path}")
except Exception as e:
    print(f"未检测到同名旧文件，无需删除：{full_output_path}")

df = spark.sql(f'''
    select 
		 MONTH
		,BU_CODE
		,BU_NAME
		,CUSTOMER_TYPE_CODE
        ,CASE   WHEN UPPER(SITE_NAME) LIKE '%TMALL%'  THEN 'EC'
                WHEN UPPER(SITE_NAME) LIKE '%JD%'     THEN 'EC'
                WHEN UPPER(SITE_NAME) LIKE '%VIP%'    THEN 'EC'
                WHEN UPPER(SITE_NAME) LIKE '%PDD%'    THEN 'EC'
                ELSE CUSTOMER_TYPE
                END AS CUSTOMER_TYPE
		,CASE   WHEN UPPER(SITE_CODE) LIKE '%TMALL%'  THEN 'TMALL'
                WHEN UPPER(SITE_CODE) LIKE '%JD%'     THEN 'JD'
                WHEN UPPER(SITE_CODE) LIKE '%VIP%'    THEN 'VIP'
                WHEN UPPER(SITE_CODE) LIKE '%PDD%'    THEN 'PDD'
                WHEN UPPER(SITE_CODE) LIKE '%DOUYIN%'    THEN 'DOUYIN'
                ELSE SITE_CODE
                END AS SITE_CODE
        ,CASE   WHEN UPPER(SITE_NAME) LIKE '%TMALL%' THEN 'TMALL'
                WHEN UPPER(SITE_NAME) LIKE '%JD%'    THEN 'JD'
                WHEN UPPER(SITE_NAME) LIKE '%VIP%'    THEN 'VIP'
                WHEN UPPER(SITE_NAME) LIKE '%PDD%'    THEN 'PDD'
                WHEN UPPER(SITE_NAME) LIKE '%DOUYIN%'    THEN 'DOUYIN'
                ELSE SITE_NAME
                END AS SITE_NAME
		,STORE_CODE
		,STORE_NAME
		,CATEGORY_CODE
		,CATEGORY_NAME
		,BRAND_CODE
		,BRAND_NAME
		,PRODUCT_LINE_GROUP_CODE
		,PRODUCT_LINE_GROUP
		,INDEX_TYPE
		,VALUE
		,CREATE_BY
		,DW_CREATE_TIME AS CREATE_TIME
    from {table_name} where dt = '{dt}'
    order by MONTH,BU_CODE,BU_NAME,CUSTOMER_TYPE_CODE,CUSTOMER_TYPE,SITE_CODE,SITE_NAME,STORE_NAME,CATEGORY_NAME,BRAND_NAME,PRODUCT_LINE_GROUP,INDEX_TYPE;
''')

temp_write_path = f"{out_path}_temp"
(
    df.coalesce(1) 
      .write
      .mode('overwrite')
      .option('header', 'true')
      .option('sep', ',')
      .option('encoding', 'utf-8')
      .csv(temp_write_path) 
)

csv_files = [f for f in dbutils.fs.ls(temp_write_path) if f.name.endswith('.csv') and not f.name.startswith('_')]
if csv_files:
    original_csv_path = csv_files[0].path
    dbutils.fs.mv(original_csv_path, full_output_path)
    print(f"新文件已生成：{full_output_path}")
    
    dbutils.fs.rm(temp_write_path, recurse=True)
else:
    raise Exception("未生成有效CSV文件，请检查数据是否为空")

for file_info in dbutils.fs.ls(out_path):
    if file_info.name.startswith('_'):
        dbutils.fs.rm(file_info.path)

print(f"文件导出完成，最终路径：{full_output_path}")