# Databricks notebook source
# MAGIC %md
# MAGIC     @Output：
# MAGIC             ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf
# MAGIC     @Input：
# MAGIC             /Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/md_plan_template_configuration/{dt}/
# MAGIC     @Descript:
# MAGIC             加载PLAN TEMPLATE CONFIGURATION接口数据
# MAGIC     @Owner: kaifan.xu
# MAGIC     @Modified [1]:

# COMMAND ----------

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

from pyspark.sql import functions as fn
src_table='md_plan_template_configuration'
blob_path=f'/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/md_plan_template_configuration/{dt}/'
print(blob_path)
display(dbutils.fs.ls(blob_path))
df = spark.read.format("parquet").option("header","true").load(blob_path)
print("source file rowcnt is: " + str(df.count()))
df.createOrReplaceTempView(src_table)

# COMMAND ----------

# MAGIC %sql
# MAGIC insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf
# MAGIC select 
# MAGIC     id
# MAGIC , period_code
# MAGIC , indicator_type
# MAGIC , index_type_code
# MAGIC , index_type
# MAGIC , package_item_sub_type_code
# MAGIC , package_item_sub_type
# MAGIC , three_level_classification_code
# MAGIC , three_level_classification_name
# MAGIC , unit
# MAGIC , data_source
# MAGIC , actual_item_mapping
# MAGIC , parent_id
# MAGIC , sort
# MAGIC , state
# MAGIC , delete_flag
# MAGIC , create_by
# MAGIC , create_date
# MAGIC , update_by
# MAGIC , update_date
# MAGIC , period_name
# MAGIC , detail_report_mapping
# MAGIC , is_show
# MAGIC , now() + INTERVAL 8 HOURS as dw_create_time
# MAGIC , now() + INTERVAL 8 HOURS as dw_last_update_time
# MAGIC , '${var.data_version}' as dw_batch_num
# MAGIC from md_plan_template_configuration