-- Databricks notebook source
-- 20260904 dst 去掉 or a.hpc_dt_code ='18052566'
-- 20260908 dst 补回  a.hpc_dt_code ='18052566' 唯一条店铺主数据

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text('dt','2026-03-13','月份')

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dim}.cd.dim_store	门店主数据
-- target table:  ${spark.var.catalog.dim}.fin.dim_store_2c_mf 最终报告表
-- Description:   
-- v1.0 jin.zhen@chiefclouds.com 2025/06/26
-- v2.0 iris.lin 20260424修改,store_name的取值需要从原来的national_ex4换成national_ex25。national_ex2 in ('KA EC','SOCIAL EC')改为('EC','SOCIAL')。site_name的取值从原来的national_ex3换成national_ex4 
-- v2.1 iris.lin 20260509,新增筛选条件a.national_ex4  not like '%POP%' and a.national_ex4  not in ('REDBOOK FGS','SPECIAL WS','SHEIN FGS')
-- v2.3 iris.lin 20260513修改,site_name的取值需要取national_ex3，过滤条件的national_ex4保持不变

-- 逻辑描述：
--    1、接口文件名： cpt_store_master_yyyymm.csv
--    2、取门店主数据 national_ex2 in ('KA EC','SOCIAL EC')
--    3、每月第4个工作日回传最新Store Maser Data

set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.dim}.fin.dim_store_2c_mf partition(dt)
(
  customer_type_code
  ,customer_type
  ,on_offline
  ,site_code
  ,site_name
  ,store_code
  ,store_name
  ,create_by
  ,create_time
  ,dt
)
select
  distinct
	  ''              as customer_type_code
	 ,a.national_ex2  as customer_type
	 ,a.national_ex1  as on_offline
	 ,''              as site_code
	 ,a.national_ex3  as site_name
	 ,''              as store_code
	 ,a.national_ex25 as store_name
   ,'Automatic'                                  as create_by
   ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as create_time
   ,'${dt}'                                        as dt 
from ${spark.var.catalog.dim}.cd.dim_store a 
where a.national_ex2 in ('EC','SOCIAL')
and a.national_ex4  not like '%POP%' 
and a.national_ex4  not in ('REDBOOK FGS','SPECIAL WS','SHEIN FGS') --20260509-新增筛选条件
AND a.hpc_dt_code <> '18052566'
union 
select
  distinct
	  ''              as customer_type_code
	 ,a.national_ex2  as customer_type
	 ,a.national_ex1  as on_offline
	 ,''              as site_code
	 , 'PDD'          as site_name
	 ,''              as store_code
	 , '拼多多分销-间供直送'   as store_name
   ,'Automatic'                                  as create_by
   ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as create_time
   ,'${dt}'                                        as dt 
from ${spark.var.catalog.dim}.cd.dim_store a 
where  a.hpc_dt_code ='18052566' and national_ex1='ONLINE' and national_ex2='EC'
;