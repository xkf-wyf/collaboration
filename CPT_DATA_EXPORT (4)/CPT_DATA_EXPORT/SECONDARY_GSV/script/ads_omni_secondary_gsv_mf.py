# Databricks notebook source
# MAGIC %sql
# MAGIC -- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

# COMMAND ----------

dbutils.widgets.text("dt", "2026-03-05")
dbutils.widgets.text("start_mth", "2026-01")
dbutils.widgets.text("end_mth", "2026-02")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- adb sql
# MAGIC -- **********************************************************************
# MAGIC -- source table:
# MAGIC   --  ${spark.var.catalog.ads}.cd_bi.ads_omni_base_monthly_fix_mf
# MAGIC   --  ${spark.var.catalog.dim}.cd.dim_product
# MAGIC   --  ${spark.var.catalog.dim}.cd.dim_store
# MAGIC -- target table:  ${spark.var.catalog.ads}.cpt.ads_omni_secondary_gsv_mf 
# MAGIC -- Description:   
# MAGIC -- v2.0 Eddie.Liang 20260224
# MAGIC -- v2.1 iris.lin 2026-04-24修改,store_name的取值需要从原来的national_ex4换成national_ex25,site_name的取值从原来的national_ex3换成national_ex4
# MAGIC -- v2.2 iris.lin 2026-05-09修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex4(site)作为store_name
# MAGIC -- v2.3 iris.lin 2026-05-13修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name,site_name的取值需要取national_ex3
# MAGIC -- v2.4 iris.lin 2026-07-15修改,新增逻辑，临时方案：上游提供逻辑，把DOUYIN - NOT DTC店铺的数据从omni_base_monthly补充进来
# MAGIC
# MAGIC -- 逻辑描述：
# MAGIC --    1、接口文件名： cpt_omni_gsv_yyyymm.csv
# MAGIC --    2、每月第5个工作日回传M-1月一级GSV
# MAGIC set spark.sql.sources.partitionOverwriteMode=dynamic;
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_omni_secondary_gsv_mf partition(dt)
# MAGIC (
# MAGIC month,
# MAGIC bu_code,
# MAGIC bu_name,
# MAGIC customer_type_code,
# MAGIC customer_type,
# MAGIC site_code,
# MAGIC site_name,
# MAGIC sales_type,
# MAGIC store_code,
# MAGIC store_name,
# MAGIC category_code,
# MAGIC category_name,
# MAGIC brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_code,
# MAGIC product_line_group,
# MAGIC secondary_gsv_amount,
# MAGIC create_by,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num,
# MAGIC dt
# MAGIC )
# MAGIC select 	replace(mth,'-','')	as month
# MAGIC     ,''                     as bu_code
# MAGIC     ,division               as bu_name
# MAGIC     ,''                     as customer_type_code
# MAGIC     ,national_ex2           as customer_type
# MAGIC     ,''                     as site_code
# MAGIC     ,national_ex3           as site_name
# MAGIC     ,sales_type     
# MAGIC 		,''				            	as store_code
# MAGIC 		,case when store_name='JD - REGENERATE' then 'JD - UL' else store_name end as store_name  -- 20260904                            
# MAGIC 		,''                     as category_code
# MAGIC 		,category_short         as category_name
# MAGIC 		,''                     as brand_code 
# MAGIC 		,cg_sub_brand           as brand_name
# MAGIC 		,''					            as product_line_group_code
# MAGIC 		,product_line_group
# MAGIC 		,secondary_gsv_amount
# MAGIC 		,'Automatic'	        	as create_by
# MAGIC 		,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_create_time
# MAGIC 		,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_last_update_time
# MAGIC 		,cast(date_format(from_utc_timestamp(current_timestamp(),'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint) as dw_batch_num
# MAGIC     ,'$dt' as dt
# MAGIC from 	 (
# MAGIC 	select 	a.mth
# MAGIC       ,sku.category_short
# MAGIC 			,sku.cg_sub_brand
# MAGIC       ,sku.division
# MAGIC       ,st.national_ex2
# MAGIC       ,st.national_ex3
# MAGIC 		  ,sku.category_short
# MAGIC 			,sku.cg_sub_brand
# MAGIC 			,a.sales_type
# MAGIC 			,nvl(nullif(st.national_ex25,''),'OTHERS')			as store_name
# MAGIC 			,nvl(nullif(sku.national_ex42,''),'OTHERS')			as product_line_group
# MAGIC 			,sum(second_sales*1000)								as secondary_gsv_amount           -- 原来是千元
# MAGIC 	from 	(
# MAGIC 			select 	mth,sku_code,store_code,sales_type
# MAGIC 			,sum(second_sales) as second_sales
# MAGIC 			from 	 ${spark.var.catalog.ads}.cd_bi.ads_omni_base_monthly_fix_mf
# MAGIC 			where 1=1
# MAGIC       		and	mth between '$start_mth' and '$end_mth'
# MAGIC 			and ul_day = last_day(ul_day)
# MAGIC 			group by mth,sku_code,store_code,sales_type
# MAGIC 			
# MAGIC 			-- 20260714,新增逻辑，临时方案：上游提供逻辑，把DOUYIN - NOT DTC店铺的数据从omni_base_monthly补充进来
# MAGIC 			-- 202501-202606,DOUYIN - NOT DTC店铺的数据是522788.674762。如果多出来其他store_code的数据，需要做过滤剔除
# MAGIC 			union all
# MAGIC 			
# MAGIC 			select 	mth,sku_code
# MAGIC 			,case when store_code='DAIBUCHONG' then '20240913EC00023' else store_code end as store_code
# MAGIC 			,sales_type
# MAGIC 			,sum(second_sales) as second_sales
# MAGIC 			from 	 ${spark.var.catalog.ads}.cd_bi.ads_omni_base_monthly
# MAGIC 			where 1=1
# MAGIC       		and	mth between '$start_mth' and '$end_mth'
# MAGIC 			and ul_day = last_day(ul_day)
# MAGIC 			and soldto_code='15512243'
# MAGIC 			and sku_bu='HC'
# MAGIC 			and second_sales is not null
# MAGIC 			and store_code  not in ('2025-B-010-24029')
# MAGIC 			group by mth,sku_code,store_code,sales_type
# MAGIC 		
# MAGIC 			) a
# MAGIC 	left join ${spark.var.catalog.dim}.cd.dim_product sku on sku.is_current = 1 and a.sku_code = sku.sku_code
# MAGIC 	left join (
# MAGIC 		select 	store_code
# MAGIC 		-- ,max(national_ex25)  as national_ex25
# MAGIC 		--2026-05-13修改，当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name
# MAGIC 		,case when max(national_ex1)='ONLINE' then max(national_ex25) else max(national_ex3) end as  national_ex25 
# MAGIC         ,max(national_ex2) as national_ex2
# MAGIC         ,max(national_ex3) as national_ex3
# MAGIC 		from 	${spark.var.catalog.dim}.cd.dim_store
# MAGIC 		where national_ex9 != ''			--2026-08-24修改，Store_name不唯一需加该过滤条件
# MAGIC 		group by store_code
# MAGIC 			) st on a.store_code = st.store_code
# MAGIC 	group by a.mth,sku.category_short,sku.cg_sub_brand,sku.division,a.sales_type
# MAGIC       ,st.national_ex2
# MAGIC       ,st.national_ex3
# MAGIC 			,nvl(nullif(st.national_ex25,''),'OTHERS')
# MAGIC 			,nvl(nullif(sku.national_ex42,''),'OTHERS')
# MAGIC ) cte_base
# MAGIC where 	nvl(secondary_gsv_amount,0) <> 0 
# MAGIC ;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(1) ,dt from ${spark.var.catalog.ads}.fin_cpt.ads_omni_secondary_gsv_mf group by dt