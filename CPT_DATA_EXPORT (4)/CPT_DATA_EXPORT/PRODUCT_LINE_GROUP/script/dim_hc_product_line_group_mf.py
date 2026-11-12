# Databricks notebook source
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pandas as pd
try:
    dt = dbutils.widgets.get('dt')
    data_version = datetime.strptime(dt, "%Y-%m-%d").strftime("%Y%m%d%H%M%S%f")[:-3]
    d = datetime.strptime(dt, "%Y-%m-%d")
    year = d.isocalendar()[0]
    week = d.isocalendar()[1]
    week_version = '%d_WK%02d' % (year, week)
    print(dt, week_version, data_version)
except:
    dt = (datetime.utcnow() + relativedelta(hours=8)).strftime("%Y-%m-%d")
    data_version = (datetime.utcnow() + relativedelta(hours=8)).strftime("%Y%m%d%H%M%S%f")[:-3]
    year = datetime.strptime(dt, "%Y-%m-%d").isocalendar()[0]
    week = datetime.strptime(dt, "%Y-%m-%d").isocalendar()[1]
    week_version = '%d_WK%02d' % (year, week)
    print('[WARNING]:did\'t get dt, and set to default:', dt, week_version, data_version)
finally:    
    #获取spark环境变量
    catalog_ods = spark.conf.get("spark.var.catalog.ods")
    catalog_dim = spark.conf.get("spark.var.catalog.dim")
    catalog_dwd = spark.conf.get("spark.var.catalog.dwd")
    catalog_dws = spark.conf.get("spark.var.catalog.dws")
    catalog_ads = spark.conf.get("spark.var.catalog.ads")
    spark.conf.set("var.dt", dt)
    spark.conf.set("var.wk", week_version)
    spark.conf.set("var.data_version", data_version)

# COMMAND ----------

query_sql=f"""
select   DISTINCT  
    ''                                           as bu_code
    ,prd.productgroup_name                       as bu_name 
    ,''                                          as category_code
    ,prd.category_short                          as category_name
    ,''                                          as subbrand_code
    ,prd.cg_sub_brand                            as subbrand_name
    ,''                                          as product_line_group_code
    ,prd.product_line_group                      as product_line_group
    ,'Automatic'                                 as create_by
    from (select distinct productgroup_name,productgroup_shortname,category,category_short,cg_sub_brand,product_line_group from {catalog_dim}.cd.dim_product_full) prd
"""
df = spark.sql(query_sql)
df.createOrReplaceTempView("tmp_plg")

# COMMAND ----------

# MAGIC %sql
# MAGIC set spark.sql.sources.partitionOverwriteMode=dynamic;
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_hc_product_line_group_mf partition(dt)
# MAGIC (
# MAGIC      bu_code
# MAGIC     ,bu_name    
# MAGIC     ,category_code
# MAGIC     ,category_name
# MAGIC     ,subbrand_code
# MAGIC     ,subbrand_name
# MAGIC     ,product_line_group_code
# MAGIC     ,product_line_group
# MAGIC     ,create_by
# MAGIC     ,dw_create_time
# MAGIC     ,dw_last_update_time
# MAGIC     ,dw_batch_num
# MAGIC     ,dt 
# MAGIC )
# MAGIC select 
# MAGIC      bu_code
# MAGIC     ,bu_name    
# MAGIC     ,category_code
# MAGIC     ,category_name
# MAGIC     ,subbrand_code
# MAGIC     ,subbrand_name
# MAGIC     ,product_line_group_code
# MAGIC     ,product_line_group
# MAGIC     ,create_by
# MAGIC ,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_create_time
# MAGIC ,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_last_update_time
# MAGIC ,cast(date_format(from_utc_timestamp(current_timestamp(),'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint) as dw_batch_num  
# MAGIC ,'$dt' as dt
# MAGIC from tmp_plg 
# MAGIC where  replace(nvl(bu_name,''),'NULL','') <> ''
# MAGIC and replace(nvl(category_name,''),'NULL','') <> ''
# MAGIC and replace(nvl(subbrand_name,''),'NULL','') <> ''
# MAGIC and replace(nvl(product_line_group,''),'NULL','') <> '';
# MAGIC
# MAGIC  

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ${spark.var.catalog.dim}.fin.dim_hc_product_line_group_mf