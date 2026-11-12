-- Databricks notebook source
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("start_mth", "2025-01")
-- MAGIC dbutils.widgets.text("end_mth", "2026-03")
-- MAGIC dbutils.widgets.text("dt", "2026-03-05")

-- COMMAND ----------

-- adb sql

-- **********************************************************************
-- source table: ${spark.var.catalog.ads}.cd_bi.ads_omni_base
-- source table: ${spark.var.catalog.dim}.cd.dim_product
-- source table: ${spark.var.catalog.dim}.cd.dim_store
-- source table: ${spark.var.catalog.ads}.ddm_dset.ads_ec_daily_sales_fact_sales
-- source table: ${spark.var.catalog.ads}.ddm_dset.ads_ec_daily_sales_dim_product
-- source table: ${spark.var.catalog.dim}.cd.dim_cpp_adjustment
-- target table: ${spark.var.catalog.ads}.fin_cpt.ads_omni_stock_total_mf
-- Description:   
-- v1.0 jin.zhen@chiefclouds.com 2025/06/11
-- v2.1 iris.lin 2026-04-24修改,store_name的取值需要从原来的national_ex4换成national_ex25,site_name的取值从原来的national_ex3换成national_ex4
-- v2.2 iris.lin 2026-05-09修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex4(site)作为store_name
-- v2.3 iris.lin 2026-05-13修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name,site_name的取值需要取national_ex3



-- 逻辑描述：
--    1、接口文件名： cpt_omni_stock_total_yyyymm.csv
--    2、每月第4个工作日回传M-1月一级GSV
-- v1.1 wu.bingling@unilever-china.com 2026/02/06
-- 逻辑描述：
--    1、新增字段：customer_type_code（Channel编码）、customer_type（Channel名称）、site_code（Site编码）、site_name（Site名称）
--    2、调整initial_stock字段取数逻辑

set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_omni_stock_total_mf partition(dt)
(month,
  customer_type_code,
  customer_type,
  site_code,
  site_name,
  store_code,
  store_name,
  bu,
  category,
  brand,
  product_line_group_code,
  product_line_group,
  initial_stock,
  create_by,
  dw_create_time,
  dw_last_update_time,
  dw_batch_num,
  dt )
select 	replace(a.mth,'-','' )        as month
			   ,''							            as customer_type_code
			   ,d.customer_type
	    	 ,'' 						              as site_code
			   ,d.site_name
         	,''   	 			     	          as store_code
		    ,  case  when d.store_name='JD - REGENERATE' then 'JD - UL' else d.store_name end as store_name -- 20260904
			  ,b.division                   as bu
			  ,b.category_short             as category
			  ,b.cg_sub_brand               as brand
        	,''                           as product_line_group_code
        	,b.national_ex42              as product_line_group
			,sum(a.initial_stock)								as initial_stock
			,'Automatic'                                                       as create_by
			,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
			,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
			,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
			,'$dt'                                                             as dt
	from 	(
			select 	mth,sku_code,store_code,
					  sum(theory_stock*1000) as initial_stock 
			from 	${spark.var.catalog.ads}.cd_bi.ads_omni_base_monthly_fix_mf
			where 	mth between  '$start_mth' and '$end_mth'
					and ul_day = last_day(ul_day)
					and sales_type = '2C'
			group by mth,sku_code,store_code
			) a
	left join ${spark.var.catalog.dim}.cd.dim_product b on b.is_current = 1 and a.sku_code = b.sku_code
  left join (
		select 	store_code
				,max(national_ex2)  as customer_type
				,max(national_ex3)  as site_name
				-- ,max(national_ex25)  as store_name
		--2026-05-13修改，当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name
		,case when max(national_ex1)='ONLINE' then max(national_ex25) else max(national_ex3) end as  store_name 
		from 	${spark.var.catalog.dim}.cd.dim_store
		where national_ex9 != ''      --2026-08 Store_name不唯一增加相关过滤条件
		group by store_code
			) d on a.store_code = d.store_code
group by a.mth
,case when d.store_name='JD - REGENERATE' then 'JD - UL' else d.store_name end -- 20260904
,b.national_ex42,b.category_short,b.cg_sub_brand,b.division,d.site_name,d.customer_type;