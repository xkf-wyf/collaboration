-- Databricks notebook source
-- MAGIC %python
-- MAGIC dbutils.widgets.text('dt','2026-03-20')

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dim}.cd.dim_customer	客户主数据
-- target table: ${spark.var.catalog.dim}.fin.dim_customer_2c_mf
-- Description:   
-- v1.0 jin.zhen@chiefclouds.com 2025/06/11
-- 逻辑描述：
--    1、接口文件名： cpt_customer_hierachy_yyyymm.csv
--    2、每月第4个工作日回传最新Customer Hierachy

set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.dim}.fin.dim_customer_2c_mf partition(dt)
(
  bu_code
  ,bu_name
  ,customer_type_code
  ,customer_type
  ,site_code
  ,site_name_en
  ,site_name_cn
  ,store_code
  ,store_name
  ,store_desc
  ,soldto_code
  ,soldto_name
  ,on_offline
  ,is_active
  ,key_cust1_cd
  ,key_cust1_name
  ,key_cust2_cd
  ,key_cust2_name
  ,key_cust3_cd
  ,key_cust3_name
  ,key_cust4_cd
  ,key_cust4_name
  ,key_cust5_cd
  ,key_cust5_name
  ,key_cust6_cd
  ,key_cust6_name
  ,create_by
  ,create_time
  ,dt
)
select 
distinct
	  ''                  as    bu_code
    ,case a.bu_type 
    when 'HC'  then 'HOME CARE'
    when 'BPC' then 'BEAUTY&WELLBEING'
    when 'PC'  then 'PERSONAL CARE'
    end as bu_name
	 ,''                  as    customer_type_code
	 ,a.customer_type     as    customer_type
	 ,''                  as    site_code
	 ,a.account_group_en  as    site_name_en
	 ,a.account_group_cn  as    site_name_cn
   ,''                  as    store_code
   ,a.banner_en         as    store_name
	 ,a.banner_cn         as    store_desc
	 ,a.soldto_code       as    soldto_code
	 ,a.soldto_name       as    soldto_name
	 ,a.on_offline        as    on_offline
	 ,a.is_active         as    is_active
	 ,a.key_cust1_cd      as    key_cust1_cd
	 ,a.key_cust1_name    as    key_cust1_name
	 ,a.key_cust2_cd      as    key_cust2_cd
	 ,a.key_cust2_name    as    key_cust2_name
	 ,a.key_cust3_cd      as    key_cust3_cd
	 ,a.key_cust3_name    as    key_cust3_name
	 ,a.key_cust4_cd      as    key_cust4_cd
	 ,a.key_cust4_name    as    key_cust4_name
	 ,a.key_cust5_cd      as    key_cust5_cd
	 ,a.key_cust5_name    as    key_cust5_name
	 ,a.key_cust6_cd      as    key_cust6_cd
	 ,a.key_cust6_name    as    key_cust6_name
   ,'Automatic'         as    create_by
   ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as create_time
	 ,'$dt'               as    dt 
from ${spark.var.catalog.dim}.cd.dim_customer a 
where a.bu_type <> 'BW'
;