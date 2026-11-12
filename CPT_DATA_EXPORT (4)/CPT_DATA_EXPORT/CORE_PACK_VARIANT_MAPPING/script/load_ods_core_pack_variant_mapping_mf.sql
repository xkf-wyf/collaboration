-- Databricks notebook source
-- MAGIC %py
-- MAGIC !pip install openpyxl
-- MAGIC import pandas as pd
-- MAGIC
-- MAGIC # 这里文件中约定的日期格式为 yyyymmdd ,文件中的分割符为 逗号
-- MAGIC dt = dbutils.widgets.get("dt").replace('-','')
-- MAGIC cl_dim = spark.conf.get('spark.var.catalog.dim')
-- MAGIC
-- MAGIC df = pd.read_excel(f'/Volumes/{cl_dim}/fin/vol_cpt_inbound_manual/dim_core_pack_variant_mapping/dim_core_pack_variant_mapping_{dt}.xlsx',dtype='str')
-- MAGIC # 将pdf 转成 spark的dataframe
-- MAGIC df = spark.createDataFrame(df)
-- MAGIC # 创建临时视图
-- MAGIC df.createOrReplaceTempView("tmp_core_pack_variant_mapping")

-- COMMAND ----------

-- spark sql
-- **********************************************************************
-- 特殊香型的产品机制关系表 接入层
-- source: tmp_core_pack_variant_mapping
-- target: ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf
-- v1.0 haolong.wu@chiefclouds.com 2025-09-03
-- **********************************************************************

--参数设置
set spark.sql.sources.partitionOverwriteMode=dynamic;

--数据接入
insert overwrite table ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf partition (dt)
select 
    *
    ,'Automatic'                                                                                  as create_by
    ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss')    as etl_date
    ,'$dt'                                                                                        as dt
from tmp_core_pack_variant_mapping;
