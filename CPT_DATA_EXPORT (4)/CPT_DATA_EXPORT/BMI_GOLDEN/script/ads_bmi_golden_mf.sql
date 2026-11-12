-- Databricks notebook source
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("dt", '2026-03-31')
-- MAGIC dbutils.widgets.text("start_mth", '2025-01')
-- MAGIC dbutils.widgets.text("end_mth", '2026-02')

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.ads}.ddm_dset.ads_ec_g_fomular_ndy_traffic_fact	黄金公式二期流量事实表
-- source table: ${spark.var.catalog.ads}.ddm_dset.ads_ec_g_fomular_dim_traffic_metric_cfg	二期指标配置表
-- target table: ${spark.var.catalog.ads}.fin_cpt.ads_bmi_golden_mf 最终报告表
-- Description:   
-- v2.0 xi.lin 2026-02-05
-- v2.1 iris.lin 2026-04-24修改,store_name的取值需要从原来的national_ex4换成national_ex25
-- v2.2 iris.lin 2026-05-11修改,需要增加national_ex4(site)的限制条件
-- v2.3 iris.lin 2026-06-11修改，修改dim_store的取数逻辑，只取distinct national_ex2,national_ex25，不再用max()的逻辑
--    1、接口文件名： cpt_bmi_golden_yyyymm.csv
--    2、取 prod_ads.ddm_dset.ads_ec_g_fomular_ndy_traffic_fact
--       关联prod_ads.ddm_dset.ads_ec_g_fomular_dim_traffic_metric_cfg
--    3、每月第5个工作日回传M-1月BMI Golden Formula Act(含二级GMV)

set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_bmi_golden_mf partition(dt)
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
    ,index_type
    ,value
    ,create_by
    ,dw_create_time
    ,dw_last_update_time
    ,dw_batch_num
    ,dt 
)
select
    replace(period,'-','')                        as month
    ,''                                           as bu_code
    ,t1.bu                                        as bu_name
    ,''                                           as customer_type_code
    ,t3.national_ex2                              as customer_type
    ,''                                           as site_code
    ,t1.site                                      as site_name
    ,''                                           as store_code
    ,case when store_group ='JD - REGENERATE' then 'JD - UL'  else store_group end   as store_name -- 20260904
    ,''                                           as category_code
    ,category                                     as category_name
    ,''                                           as brand_code
    ,brand                                        as brand_name
    ,''                                           as product_line_group_code
    ,product_group                                as product_line_group
    ,t2.column_name                               as index_type
    ,cast(sum(value) as decimal(38,8))            as value
    ,'Automatic'                                                       as create_by
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
    ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
    ,'$dt'                                                             as dt
from ${spark.var.catalog.ads}.ddm_dset.ads_ec_g_fomular_ndy_traffic_fact t1 
left join ${spark.var.catalog.ads}.ddm_dset.ads_ec_g_fomular_dim_traffic_metric_cfg t2
on t1.metric_id = t2.metric_id
left join (
		select 	distinct national_ex2,national_ex25
		from 	${spark.var.catalog.dim}.cd.dim_store
        where national_ex4  not like '%POP%' and national_ex4  not in ('REDBOOK FGS','SPECIAL WS','SHEIN FGS')
			) t3 on t1.store_group = t3.national_ex25
where period_type = 'Month' 
and period between '$start_mth' and '$end_mth'
group by period,store_group,category,brand,product_group,t2.column_name,t3.national_ex2,t1.bu,t1.site
having index_type is not null
;