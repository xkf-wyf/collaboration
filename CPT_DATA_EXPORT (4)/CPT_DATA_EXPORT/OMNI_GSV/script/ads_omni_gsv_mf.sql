-- Databricks notebook source
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("start_mth", "2025-01")
-- MAGIC dbutils.widgets.text("end_mth", "2026-02")
-- MAGIC dbutils.widgets.text("dt", "2026-03-05")

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: 
-- target table:  ${spark.var.catalog.ads}.cpt.ads_omni_gsv_exp 
-- Description:   
-- v2.0 xi.lin 20260203
-- v2.1 iris.lin 2026-04-24修改,store_name的取值需要从原来的national_ex4换成national_ex25,site_name的取值从原来的national_ex3换成national_ex4
-- v2.2 iris.lin 2026-05-09修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex4(site)作为store_name
-- v2.3 iris.lin 2026-05-13修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name,site_name的取值需要取national_ex3
-- 逻辑描述：
--    1、接口文件名： cpt_omni_gsv_yyyymm.csv
--    2、每月第5个工作日回传M-1月一级GSV
set spark.sql.sources.partitionOverwriteMode=dynamic;

with cte_base as (
	select 	a.mth
		  ,sku.category_short
			,sku.cg_sub_brand
      ,sku.division
      ,st.national_ex2
      ,st.national_ex3
			,nvl(nullif(st.national_ex25,''),'OTHERS')			as store_name
			,nvl(nullif(sku.national_ex42,''),'OTHERS')			as product_line_group
			,sum(mtd_primary_sales*1000)								as primary_gsv_amount           -- 原来是千元
	from 	(
			select 	mth,sku_code,store_code
					,sum(primary_sales) as mtd_primary_sales
			from 	${spark.var.catalog.ads}.cd_bi.ads_omni_base_monthly_fix_mf --使用月结表
			-- 		,sum(mtd_primary_sales) as mtd_primary_sales
			-- from 	${spark.var.catalog.ads}.cd_bi.ads_omni_base
			where 	mth between '$start_mth' and '$end_mth'
					and ul_day = last_day(ul_day)
					and sales_type = '2C'
			group by mth,sku_code,store_code
			) a
	left join ${spark.var.catalog.dim}.cd.dim_product sku on sku.is_current = 1 and a.sku_code = sku.sku_code
	left join (
		select 	store_code
				-- ,max(national_ex25)  as national_ex25
		--2026-05-13修改，当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name
		,case when max(national_ex1)='ONLINE' then max(national_ex25) else max(national_ex3) end as  national_ex25 
        ,max(national_ex2) as national_ex2
        ,max(national_ex3) as national_ex3
		from 	${spark.var.catalog.dim}.cd.dim_store
		where national_ex9 != ''			--2026-08-24修改，Store_name不唯一需加该过滤条件
		group by store_code
			) st on a.store_code = st.store_code
	group by a.mth,sku.category_short,sku.cg_sub_brand,sku.division
      ,st.national_ex2
      ,st.national_ex3
			,nvl(nullif(st.national_ex25,''),'OTHERS')
			,nvl(nullif(sku.national_ex42,''),'OTHERS')
)
insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_omni_gsv_mf partition(dt)
(
	 	 month
    ,bu_code
    ,bu_name
    ,customer_type_code
    ,customer_type
    ,site_code
    ,site_name
		,store_code
		,store_name
		,category_code
		,category_name
		,brand_code 
		,brand_name
		,product_line_group_code
		,product_line_group
		,primary_gsv_amount
    ,create_by
    ,dw_create_time
    ,dw_last_update_time
    ,dw_batch_num
    ,dt
)
select 	replace(mth,'-','')	as month
    ,''                     as bu_code
    ,division               as bu_name
    ,''                     as customer_type_code
    ,national_ex2           as customer_type
    ,''                     as site_code
    ,national_ex3           as site_name
		,''				            	as store_code
		,case when store_name='JD - REGENERATE' then 'JD - UL' else store_name  end as store_name   --20260410 20260904
		,''                     as category_code
		,category_short         as category_name
		,''                     as brand_code 
		,cg_sub_brand           as brand_name
		,''					            as product_line_group_code
		,product_line_group
		,primary_gsv_amount
    ,'Automatic'                                                       as create_by
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
    ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
    ,'$dt'                                                             as dt
from 	cte_base
where 	nvl(primary_gsv_amount,0) <> 0 
;
