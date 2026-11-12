# Databricks notebook source
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

cl_ads = spark.conf.get('spark.var.catalog.ads')
dt = dbutils.widgets.get("dt")
current_date = datetime.strptime(dt, '%Y-%m-%d')
last_month_date = current_date - relativedelta(months=1)
mth = last_month_date.strftime("%Y%m")

table_name = f'{cl_ads}.fin_cpt.ads_omni_secondary_gsv_mf'
out_path = f'/Volumes/{cl_ads}/fin_cpt/vol_cpt_outbound_cpt/cpt/cpt_omni_secondarygsv/'
file_name = f'cpt_omni_secondarygsv_{mth}.csv'
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
        ,CUSTOMER_TYPE
        ,SITE_CODE
        ,SITE_NAME
        ,SALES_TYPE
        ,STORE_CODE
        ,STORE_NAME
        ,CATEGORY_CODE
        ,CATEGORY_NAME
        ,BRAND_CODE
        ,BRAND_NAME
        ,PRODUCT_LINE_GROUP_CODE
        ,PRODUCT_LINE_GROUP
        ,SECONDARY_GSV_AMOUNT
        ,CREATE_BY
        ,DW_CREATE_TIME AS CREATE_TIME
    from {table_name} 
    where dt = '{dt}'
    order by MONTH, BU_NAME, CUSTOMER_TYPE, SITE_NAME, SALES_TYPE, STORE_NAME, CATEGORY_NAME, BRAND_NAME, PRODUCT_LINE_GROUP;
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