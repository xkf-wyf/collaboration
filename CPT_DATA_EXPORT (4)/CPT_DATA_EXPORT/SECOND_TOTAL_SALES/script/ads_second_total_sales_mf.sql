-- Databricks notebook source
-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dws}.ddm.dws_trd_total_item_sales_
-- source table: ${spark.var.catalog.dim}.ddm.dim_prd_item
-- source table: ${spark.var.catalog.dim}.ddm.dim_store 
-- source table: ${spark.var.catalog.dwd}.ddm.dwd_mkt_ec_sales_tob_di
-- target table:  ${spark.var.catalog.ads}.fin_cpt.ads_second_total_sales_mf 最终报告表
-- Description:   
-- v1.0 haolong.wu@chiefclouds.com 2025-07-28   创建
-- v1.1 haolong.wu@chiefclouds.com 2025-12-04   PDD - VSL切DTC后要从PDD - UL中拆出来, 跟着DDM hardcode处理
-- v2.0 Eddie Liang  新增维度属性，新增2B GMV逻辑，2B 从日销看板获取
-- v2.1 iris.lin@ 2026-08-03修改,数据表 prod_dim.ddm.dim_store 的逻辑变更，将影响各接口中 customer_type 字段的取值逻辑：其数据来源需由原 customer_type 字段切换为 channel 字段。
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- 逻辑描述：
--    1、事实表与维度表通过item_id关联，按月+store+categoyr+brand汇总gmv_after_refund & gmv
--    2、JD 剔除ToB：通过Item_id + day 关联${spark.var.catalog.dwd}.ddm.dwd_mkt_ec_sales_tob_di，取2B的GMV，然后用 total_gmv - 2B_gmv
--    3、剔除购物金，过滤掉item_name含"购物金"的item_id
--    4、接口文件名： cpt_second_total_sales_yyyymm.csv
--    5、每月第5个工作日回传M-1月二级GMV Total
-- v1.2 wu.bingling@unilever-china.com 2026-02-11
-- 逻辑描述：
--    1、新增字段：BU_CODE（BU编码）、BU_NAME（BU名称）、CUSTOMER_TYPE_CODE（Channel编码）、CUSTOMER_TYPE（Channel名称）、SITE_CODE（Site编码）、SITE_NAME（Site名称）、SALES_TYPE

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from dateutil.relativedelta import relativedelta
-- MAGIC from datetime import datetime, timedelta
-- MAGIC import pandas as pd
-- MAGIC try:
-- MAGIC     dt = dbutils.widgets.get('dt')
-- MAGIC     start_mth = dbutils.widgets.get('start_mth')
-- MAGIC     end_mth = dbutils.widgets.get('end_mth')
-- MAGIC     data_version = datetime.strptime(dt, "%Y-%m-%d").strftime("%Y%m%d%H%M%S%f")[:-3]
-- MAGIC     d = datetime.strptime(dt, "%Y-%m-%d")
-- MAGIC     year = d.isocalendar()[0]
-- MAGIC     week = d.isocalendar()[1]
-- MAGIC     week_version = '%d_WK%02d' % (year, week)
-- MAGIC     print(dt, week_version, data_version)
-- MAGIC except:
-- MAGIC     dt = (datetime.utcnow() + relativedelta(hours=8)).strftime("%Y-%m-%d")
-- MAGIC     data_version = (datetime.utcnow() + relativedelta(hours=8)).strftime("%Y%m%d%H%M%S%f")[:-3]
-- MAGIC     year = datetime.strptime(dt, "%Y-%m-%d").isocalendar()[0]
-- MAGIC     week = datetime.strptime(dt, "%Y-%m-%d").isocalendar()[1]
-- MAGIC     week_version = '%d_WK%02d' % (year, week)
-- MAGIC     print('[WARNING]:did\'t get dt, and set to default:', dt, week_version, data_version)
-- MAGIC finally:    
-- MAGIC     #获取spark环境变量
-- MAGIC     catalog_ods = spark.conf.get("spark.var.catalog.ods")
-- MAGIC     catalog_dim = spark.conf.get("spark.var.catalog.dim")
-- MAGIC     catalog_dwd = spark.conf.get("spark.var.catalog.dwd")
-- MAGIC     catalog_dws = spark.conf.get("spark.var.catalog.dws")
-- MAGIC     catalog_ads = spark.conf.get("spark.var.catalog.ads")
-- MAGIC     spark.conf.set("var.dt", dt)
-- MAGIC     spark.conf.set("var.wk", week_version)
-- MAGIC     spark.conf.set("var.data_version", data_version)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC query_2c=f"""select 
-- MAGIC     replace(substr(t1.period_key,1,7),'-','')     as month
-- MAGIC     ,''                                           as bu_code
-- MAGIC     ,t3.bu                                        as bu_name
-- MAGIC     ,''                                           as customer_type_code
-- MAGIC     ,t2.channel                             as customer_type
-- MAGIC     ,''                                           as site_code
-- MAGIC     ,t2.customer_group                            as site_name
-- MAGIC     ,'2C'                                    as sales_type
-- MAGIC     ,''                                           as store_code
-- MAGIC     ,if(t1.period_key > '2025-10-16' and t1.shop_id = '621699362', 'PDD - VSL',
-- MAGIC      case when t2.customer='JD - REGENERATE' then 'JD - UL' else t2.customer end 
-- MAGIC      ) as store_name    -- 20251204修改--20260410修改
-- MAGIC     ,''                                           as category_code
-- MAGIC     ,t3.category                                  as category_name
-- MAGIC     ,''                                           as brand_code
-- MAGIC     ,t3.brand                                     as brand_name
-- MAGIC     ,''                                           as product_line_group_code
-- MAGIC     ,t3.product_line_group                        as product_line_group
-- MAGIC     ,cast(sum(coalesce(gmv_after_refund,0) - coalesce(toB_gmv,0))as decimal(38,6))  as secondary_after_gmv_amount
-- MAGIC     ,cast(sum(coalesce(gmv,0) - coalesce(toB_gmv,0))as decimal(38,6))               as secondary_gmv_amount
-- MAGIC     ,'Automatic'                                  as create_by
-- MAGIC from {catalog_dws}.ddm.dws_trd_total_item_sales_df t1
-- MAGIC left join {catalog_dim}.ddm.dim_store t2
-- MAGIC on t1.shop_id = t2.shop_id and t2.status = 1
-- MAGIC left join (
-- MAGIC   select *
-- MAGIC   from {catalog_dim}.ddm.dim_prd_item
-- MAGIC   where is_current = 1 
-- MAGIC ) t3
-- MAGIC on t1.item_id = t3.item_id and if(t1.platform in ('VIP','TMALL SUPER'),t1.shop_id,t1.platform) = if(t3.platform in ('VIP','TMALL SUPER'),t3.shop_id,t3.platform)
-- MAGIC and t1.period_key between t3.start_time and t3.end_time
-- MAGIC left join (
-- MAGIC   -- JD toB Day
-- MAGIC   select 
-- MAGIC       concat(substr(stat_date,1,4),'-',substr(stat_date,5,2),'-',substr(stat_date,7,2)) as period_key
-- MAGIC       ,item_id
-- MAGIC       ,sum(coalesce(pay_ord_amt,0)) as toB_gmv
-- MAGIC       ,type
-- MAGIC   from {catalog_dwd}.ddm.dwd_mkt_ec_sales_tob_di
-- MAGIC   where platform='JD' 
-- MAGIC   and type = 'ToB' 
-- MAGIC   group by stat_date,item_id,type
-- MAGIC ) t4
-- MAGIC on t1.period_key = t4.period_key and t1.item_id = t4.item_id and t1.platform = 'JD'
-- MAGIC where t1.period_type='日' 
-- MAGIC and substr(t1.period_key,1,7) between '{start_mth}' and '{end_mth}'
-- MAGIC and coalesce(t3.item_name,'') not like '%购物金%'
-- MAGIC group by if(t1.period_key > '2025-10-16' and t1.shop_id = '621699362', 'PDD - VSL',case when t2.customer='JD - REGENERATE' then 'JD - UL' else t2.customer end )
-- MAGIC         ,replace(substr(t1.period_key,1,7),'-','')
-- MAGIC         ,t3.category,t3.brand
-- MAGIC         ,t3.product_line_group
-- MAGIC         ,t3.bu
-- MAGIC         ,t2.channel
-- MAGIC         ,t2.customer_group
-- MAGIC         ,t4.type """
-- MAGIC df = spark.sql(query_2c)
-- MAGIC df.createOrReplaceTempView("tmp_2c_gmv")
-- MAGIC

-- COMMAND ----------

-- MAGIC %python
-- MAGIC query_2b=f"""SELECT 
-- MAGIC     so.mth                                  AS month
-- MAGIC   , ''                                      AS bu_code
-- MAGIC   , prd.bu                                  AS bu_name
-- MAGIC   , ''                                      AS customer_type_code
-- MAGIC   , st.customer_type                        AS customer_type
-- MAGIC   , ''                                      AS site_code
-- MAGIC   , st.customer_group                       AS site_name
-- MAGIC   , '2B'                                    AS sales_type
-- MAGIC   , ''                                      AS store_code
-- MAGIC   , st.customer                             AS store_name
-- MAGIC   , ''                                      AS category_code
-- MAGIC   , prd.category                            AS category_name
-- MAGIC   , ''                                      AS brand_code
-- MAGIC   , prd.brand                               AS brand_name
-- MAGIC   , ''                                      AS product_line_group_code
-- MAGIC   , plgmp.product_line_group                AS product_line_group
-- MAGIC   , SUM(so.nmv)                             AS secondary_gmv_amount
-- MAGIC   , SUM(so.gmv)                             AS secondary_after_gmv_amount
-- MAGIC   , 'Automatic'                             AS create_by
-- MAGIC FROM 
-- MAGIC     {catalog_ads}.ddm_dset.ads_ec_daily_sales_fact_sales so
-- MAGIC LEFT JOIN 
-- MAGIC      {catalog_ads}.ddm_dset.ads_ec_daily_sales_dim_product prd 
-- MAGIC     ON so.item_key = prd.item_key
-- MAGIC LEFT JOIN 
-- MAGIC      (select max(channel) customer_type,max(customer_group) customer_group,customer from {catalog_dim}.ddm.dim_store where is_current=1 group by customer) st 
-- MAGIC     ON prd.store_name = st.customer
-- MAGIC LEFT JOIN 
-- MAGIC     {catalog_dim}.ddm.dim_prd_line_group_mapping plgmp
-- MAGIC     ON prd.product_line = plgmp.product_line and prd.bu=plgmp.bu and prd.category=plgmp.category and prd.brand=plgmp.brand
-- MAGIC WHERE so.external_group_name_1 = 'ToB' 
-- MAGIC and so.mth  between '{start_mth}' and '{end_mth}'
-- MAGIC GROUP BY 
-- MAGIC     so.mth
-- MAGIC   , prd.bu
-- MAGIC   , st.customer_type
-- MAGIC   , st.customer_group
-- MAGIC   , st.customer
-- MAGIC   , prd.category
-- MAGIC   , prd.brand
-- MAGIC   , plgmp.product_line_group """
-- MAGIC print (query_2b)
-- MAGIC df = spark.sql(query_2b)
-- MAGIC df.createOrReplaceTempView("tmp_2b_gmv")

-- COMMAND ----------

set spark.sql.sources.partitionOverwriteMode=dynamic;
insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_second_total_sales_mf partition(dt)
(month
, bu_code
, bu_name
, customer_type_code
, customer_type
, site_code
, site_name
, sales_type
, store_code
, store_name
, category_code
, category_name
, brand_code
, brand_name
, product_line_group_code
, product_line_group
, secondary_after_gmv_amount
, secondary_gmv_amount
, create_by
, dw_create_time
, dw_last_update_time
, dw_batch_num  
, dt)
SELECT 
month
, bu_code
, bu_name
, customer_type_code
, customer_type
, site_code
, site_name
, sales_type
, store_code
, store_name --20260904
, category_code
, category_name
, brand_code
, brand_name
, product_line_group_code
, product_line_group
, secondary_after_gmv_amount
, secondary_gmv_amount
, create_by
,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_create_time
,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_last_update_time
,cast(date_format(from_utc_timestamp(current_timestamp(),'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint) as dw_batch_num  
,'${var.dt}' as dt
FROM tmp_2b_gmv  where nvl(store_name,'') <>''
union all 
select 
month
, bu_code
, bu_name
, customer_type_code
, customer_type
, site_code
, site_name
, sales_type
, store_code
, store_name --20260904
, category_code
, category_name
, brand_code
, brand_name
, product_line_group_code
, product_line_group
, secondary_after_gmv_amount
, secondary_gmv_amount
, create_by
,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_create_time
,cast(date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp)	as dw_last_update_time
,cast(date_format(from_utc_timestamp(current_timestamp(),'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint) as dw_batch_num  
,'${var.dt}' as dt
FROM tmp_2c_gmv where nvl(store_name,'') <>''