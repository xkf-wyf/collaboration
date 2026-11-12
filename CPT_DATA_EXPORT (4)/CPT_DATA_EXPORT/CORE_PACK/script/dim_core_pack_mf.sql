-- Databricks notebook source
-- MAGIC %python
-- MAGIC dbutils.widgets.text("start_mth", "2026-01")
-- MAGIC dbutils.widgets.text("end_mth", "2026-02")
-- MAGIC dbutils.widgets.text("dt", "2026-03-20")

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dim}.ddm.dim_sku_pack_size	sku粒度pack_size打标表
-- target table:  ${spark.var.catalog.dim}.fin.dim_core_pack_mf 最终报告表
-- Description:   
-- v1.0 haolong.wu@chiefclouds.com 2025-06-30
-- 逻辑描述：
--    1、接口文件名： cpt_core_pack_yyyymm.csv
--    2、取 prod_dim.ddm.dim_sku_pack_size where end_time = '9999-12-31' 去重
--    3、每月第4个工作日回传最新Core Pack Group Master Data

set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.dim}.fin.dim_core_pack_mf partition(dt)
(
     bu_code                            
    ,bu_name_en
    ,category_code    
    ,category_name_en              
    ,subbrand_code    
    ,subbrand_name            
    ,product_line_group_code    
    ,product_line_group
    ,core_pack_group_code    
    ,core_pack_group                  
    ,create_by
    ,dw_create_time
    ,dw_last_update_time
    ,dw_batch_num
    ,dt  
)
select distinct
    ''                                            as bu_code                            
    ,bu_sku                                       as bu_name_en
    ,''                                           as category_code    
    ,category_sku                                 as category_name_en              
    ,''                                           as subbrand_code    
    ,brand_sku                                    as subbrand_name            
    ,''                                           as product_line_group_code    
    ,product_line_group                           as product_line_group
    ,''                                           as core_pack_group_code    
    ,core_pack_group                              as core_pack_group                  
    ,'Automatic'                                                       as create_by
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
    ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
    ,'$dt'                                                             as dt
from ${spark.var.catalog.dim}.ddm.dim_sku_pack_size
where end_time = '9999-12-31'
and channel <> 'DOUYIN'
;