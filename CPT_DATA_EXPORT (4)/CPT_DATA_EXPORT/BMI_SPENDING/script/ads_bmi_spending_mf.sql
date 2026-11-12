-- Databricks notebook source
-- dst 20260903 修改 tmp_cps_spending关联dim_prd_item 维度表的关联条件
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("dt", '')
-- MAGIC dbutils.widgets.text("start_mth", '')
-- MAGIC dbutils.widgets.text("end_mth", '')

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dws}.ddm.dws_pfm_total_item_df	
-- source table: ${spark.var.catalog.ods}.int_hologres.ods_tm_cps_trd_item_sales_di    取settlement_expenses_cost
-- source table: ${spark.var.catalog.ods}.int_hologres.ods_jd_cps_trd_item_sales_di    取spending
-- source table: ${spark.var.catalog.ods}.int_hologres.ods_jd_cps_jdlm_trd_item_sales_di     取total_commisson
-- source table: ${spark.var.catalog.dim}.ddm.dim_jd_cps_mapping   JD的CPS影子链接mapping表
-- source table: ${spark.var.catalog.ods}.int_hologres.ods_vip_cps_trd_sku_sales_di    VIP sku粒度cps表，取commission
-- source table: ${spark.var.catalog.ods}.int_hologres.ods_vip_trd_item_sku_di    VIP item-sku粒度销售表，获取item与sku by day的对应关系
-- source table: ${spark.var.catalog.dim}.ddm.dim_prd_item   商品item维度表
-- source table: ${spark.var.catalog.dim}.ddm.dim_store   店铺维度表
-- target table:  ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf 最终报告表
-- Description:   
-- v1.0 haolong.wu@chiefclouds.com 2025-06-30  创建
-- v1.1 haolong.wu@chiefclouds.com 2025-07-28  DDM将数据清洗放到dws前，CPT不做数据清洗
-- v1.2 haolong.wu@chiefclouds.com 2025-12-04  PDD - VSL切DTC后要从PDD - UL中拆出来, 跟着DDM hardcode处理
-- v1.3 iris.lin@systex.com.cn     2026-01-06  新增字段value_taxed，用于存储原来的value值，现在value逻辑为spending除税后的值，即spending/1.06
-- v1.4 iris.lin@systex.com.cn     2026-06-09  新增逻辑,join的时候，on两个条件，shop_id和platform都得和dim store里匹配的上
-- v1.5 iris.lin@systex.com.cn     2026-08-03  数据表 prod_dim.ddm.dim_store 的逻辑变更，将影响各接口中 customer_type 字段的取值逻辑：其数据来源需由原 customer_type 字段切换为 channel 字段。
-- 逻辑描述：
--    1、接口文件名： cpt_bmi_spending_yyyymm.csv
--    2、CPS从各SITE的ods表取spending，JD需要将没销量的itemid上花费转到有销量的itemid身上，VIP需要将sku粒度的cps花费汇总到item粒度
--    3、RTB/Content/BrandZone/自播从dws_pfm_total_item_df取spending，商品维度的数匹配打标表取打标表的维度后聚合，店铺维度的数直接取事实表的维度进行聚合
--    4、每月第4个工作日回传M-1月BMI Spending Actual

-- 配置动态分区覆盖模式
set spark.sql.sources.partitionOverwriteMode = dynamic;

create or replace table ${spark.var.catalog.tmp}.fin.tmp_cps_spending
select
    'JD' as platform
    ,substr(date_id,1,10) as period_key
    ,coalesce(t2.jd_code,t1.product_id) as item_id    ---DDM 20250716修改从mapping表里面取，能关联上的就用主code，关联不上的还是用原来的sku
    ,spending
from ${spark.var.catalog.ods}.int_hologres.ods_jd_cps_trd_item_sales_di t1 left join
(select distinct cps_code,jd_code from  ${spark.var.catalog.dim}.ddm.dim_jd_cps_mapping) t2 on t1.product_id=t2.cps_code
union all
select
    'JD' as platform
    ,substr(order_date,1,10)
    ,coalesce(t2.jd_code,t1.product_id) as item_id    ---DDM 20250716修改从mapping表里面取，能关联上的就用主code，关联不上的还是用原来的sku
    ,total_commission
from ${spark.var.catalog.ods}.int_hologres.ods_jd_cps_jdlm_trd_item_sales_di t1 left join
(select distinct cps_code,jd_code from  ${spark.var.catalog.dim}.ddm.dim_jd_cps_mapping) t2 on t1.product_id=t2.cps_code
union all
select
    'VIP' as platform
    ,a.dt as period_key
    ,a.osn as item_id
    ,coalesce(sum(b.sku_cps_spending),0) as spending
from (
  select distinct dt,osn,merchandise_no 
  from ${spark.var.catalog.ods}.int_hologres.ods_vip_trd_item_sku_di 
  where period = '日'
) a
left join (
  select 
    date_time
    ,goods_id
    ,sum(commission) as sku_cps_spending
  from ${spark.var.catalog.ods}.int_hologres.ods_vip_cps_trd_sku_sales_di
  where period = '日'
  group by date_time,goods_id
) b
on a.merchandise_no = b.goods_id and a.dt = b.date_time
group by a.dt,a.osn
union all
select
    'TMALL FGS' as platform
    ,date_time
    ,product_id
    ,settlement_expenses_cost 
from ${spark.var.catalog.ods}.int_hologres.ods_tm_cps_trd_item_sales_di
where plan_name <> '全部推广类型' and period = '日'
;
alter table ${spark.var.catalog.tmp}.fin.tmp_cps_spending set owner to `${spark.var.table.owner}`;

-- COMMAND ----------


insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf partition(dt)
--pfm_spending
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
    ,value    --2025-01-06 修改逻辑，除税金额
    ,value_taxed    --2025-01-06 新增字段 
    ,create_by
    ,dw_create_time
    ,dw_last_update_time
    ,dw_batch_num
    ,dt 
)
select
    replace(month,'-','')                         as month
    ,''                                           as bu_code
    ,bu                                           as bu_name
    ,''                                           as customer_type_code
    ,customer_type                                as customer_type
    ,''                                           as site_code        
    ,platform                                     as site_name        
    ,''                                           as store_code
    -- ,customer                                     as store_name  
    ,case  when customer ='JD - REGENERATE' then 'JD - UL' else customer end    as store_name   -- 20260904
    ,''                                           as category_code
    ,category                                     as category_name   
    ,''                                           as brand_code
    ,brand                                        as brand_name                                     
    ,''                                           as product_line_group_code
    ,product_line_group                           as product_line_group
    ,concat('Paid Media-',pfm_type)               as index_type           
    ,cast(round(sum(pfm_spending)/1.06,2) as decimal(38,2))                as value    --2025-01-06 修改逻辑，除税金额 
    ,cast(round(sum(pfm_spending),2) as decimal(38,2))                     as value_taxed    --2025-01-06 新增字段
    ,'Automatic'                                                           as create_by
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
    ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
    ,'$dt'                                                             as dt                           
from (
  -- 能匹配上打标表的用打标表的维度
  select  
      substr(t1.period_key,1,7)   as month                             
      ,if(t1.period_key > '2025-10-16' and t2.shop_id = '621699362', 'PDD - VSL', t3.customer) as customer     -- 20251204修改          
      ,t2.category                as category              
      ,t2.brand                   as brand 
      ,t2.bu                      as bu         
      ,t2.product_line_group      as product_line_group  
      -- ,t3.customer_type           as customer_type   --2026-08-03修改取数逻辑，由原 customer_type 字段切换为 channel 字段
      ,t3.channel                 as customer_type
      ,t3.platform                as platform
      ,t1.pfm_type                as pfm_type
      ,t1.pfm_spending            as pfm_spending
  from ${spark.var.catalog.dws}.ddm.dws_pfm_total_item_df t1
  left join (
    select *
    from ${spark.var.catalog.dim}.ddm.dim_prd_item
    where is_current = 1
  ) t2
  on t1.item_id = t2.item_id and if(t1.platform in ('VIP','TMALL SUPER'),t1.shop_id,t1.platform) = if(t2.platform in ('VIP','TMALL SUPER'),t2.shop_id,t2.platform)
  and t1.period_key >= t2.start_time and t1.period_key <= t2.end_time
  left join (
    select *
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1
  ) t3
  on COALESCE(t2.shop_id,t1.shop_id) = t3.shop_id
  where substr(t1.period_key,1,7) between '${start_mth}' and '${end_mth}'
  and t2.bu is not null
  union all 
  -- 店铺维度的数直接用事实表的维度
  select  
      substr(t1.period_key,1,7)         as month                              
      ,if(t1.period_key > '2025-10-16' and t1.shop_id = '621699362', 'PDD - VSL', t3.customer) as customer     -- 20251204修改              
      ,t1.pfm_category                  as category          
      ,t1.pfm_brand                     as brand
      -- ,t2.bu                         as bu     
      ,t1.pfm_bu                        as bu     --20260331,iris修改
      ,t1.pfm_product_line_group        as product_line_group  
      -- ,t3.customer_type              as customer_type   --2026-08-03修改取数逻辑，由原 customer_type 字段切换为 channel 字段
      ,t3.channel                       as customer_type
      ,t3.platform                      as platform          
      ,t1.pfm_type                      as pfm_type
      ,t1.pfm_spending                  as pfm_spending
  from ${spark.var.catalog.dws}.ddm.dws_pfm_total_item_df t1
  left join (
    select *
    from ${spark.var.catalog.dim}.ddm.dim_prd_item
    where is_current = 1
  ) t2
  on t1.item_id = t2.item_id and if(t1.platform in ('VIP','TMALL SUPER'),t1.shop_id,t1.platform) = if(t2.platform in ('VIP','TMALL SUPER'),t2.shop_id,t2.platform)
  and t1.period_key >= t2.start_time and t1.period_key <= t2.end_time
  left join (
    select *
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1
  ) t3
  on t1.shop_id = t3.shop_id and t1.platform = t3.platform  --20260609，iris新增逻辑
  where substr(t1.period_key,1,7) between '${start_mth}' and '${end_mth}'
  and t2.bu is null
  and (t1.item_id in ('0','-') or (t1.pfm_type = 'Package' and t1.item_id is null))  --店铺维度和京东的0和-,Package的null
  and coalesce(t1.pfm_product_line,'') != '-'       --剔除JD的品线为-的,归不到品线组
)
group by month,category,brand,product_line_group,pfm_type,bu,customer_type,platform
        ,case when customer ='JD - REGENERATE' then 'JD - UL' else customer end -- 20260904
having coalesce(pfm_type,'') != ''
-- cps_spending
union all
select
    replace(substr(t1.period_key,1,7),'-','')     as month
    ,''                                           as bu_code
    ,t2.bu                                        as bu_name
    ,''                                           as customer_type_code
    -- ,t3.customer_type                             as customer_type --2026-08-03修改取数逻辑，由原 customer_type 字段切换为 channel 字段
    ,t3.channel                                   as customer_type
    ,''                                           as site_code        
    ,t3.platform                                  as site_name   
    ,''                                           as store_code
    ,case  when t3.customer ='JD - REGENERATE' then 'JD - UL'  -- 20260904
          else t3.customer end   as store_name   
    ,''                                           as category_code
    ,t2.category                                  as category_name   
    ,''                                           as brand_code
    ,t2.brand                                     as brand_name                                     
    ,''                                           as product_line_group_code
    ,t2.product_line_group                        as product_line_group
    ,'Paid Media-CPS'                             as index_type           
    ,cast(round(sum(spending)/1.06,2) as decimal(38,2))                  as value        --2025-01-06 修改逻辑，除税金额
    ,cast(round(sum(spending),2) as decimal(38,2))                         as value_taxed    --2025-01-06 新增字段     
    ,'Automatic'                                                       as create_by
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
    ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
    ,'$dt'                                                             as dt       
from ${spark.var.catalog.tmp}.fin.tmp_cps_spending t1
left join (
    select *
    from ${spark.var.catalog.dim}.ddm.dim_prd_item
    where is_current = 1
    -- and end_time='9999-12-31'
) t2
on t1.item_id = t2.item_id
-- and t1.period_key >= t2.start_time and t1.period_key <= t2.end_time
and replace(last_day( date_format(to_date(t1.period_key, 'yyyy-MM-dd'), 'yyyy-MM-dd') ) , '-', '') >=  replace(t2.start_time, '-', '')
and replace(last_day( date_format(to_date(t1.period_key, 'yyyy-MM-dd'), 'yyyy-MM-dd') ) , '-', '') <=  replace(t2.end_time, '-', '')   -- 20260903
left join (
  select *
  from ${spark.var.catalog.dim}.ddm.dim_store
  where status = 1
) t3
on t2.shop_id = t3.shop_id
where substr(t1.period_key,1,7) between '${start_mth}' and '${end_mth}'
and t3.customer is not null
group by substr(t1.period_key,1,7),t2.category,t2.brand,t2.product_line_group,t2.bu ,t3.channel,t3.platform 
        ,case  when t3.customer ='JD - REGENERATE' then 'JD - UL'  -- 20260904
               else t3.customer end
;