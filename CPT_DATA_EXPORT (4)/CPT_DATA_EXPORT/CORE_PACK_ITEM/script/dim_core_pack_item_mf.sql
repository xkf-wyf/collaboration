-- Databricks notebook source
-- dst 20260904   去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑
-- dst 20260917   TMALL的site名称变更成最新名称：TMALL FGS、TMALL SUPER 》》 TMALL
-- dst 20260917   PDD - VSL切DTC后冗余一份机制打标
-- dst 20260918   补回 tmall super和tmall super -ul合并成tmall super -ul 的逻辑
-- dst 20261016   去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("dt", "2026-03-11")

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import re
-- MAGIC
-- MAGIC def format_packsize(expression):
-- MAGIC     def kg_to_num(match):
-- MAGIC         num_str = match.group(1)
-- MAGIC         # 转换为浮点数，乘以1000，转为整数
-- MAGIC         value = int(float(num_str) * 1000)
-- MAGIC         return str(value)
-- MAGIC     
-- MAGIC     # 去单位
-- MAGIC     expression = re.sub(r'(\d+(?:\.\d+)?)KG', kg_to_num, expression)
-- MAGIC     expression = re.sub(r'GX|X', '*', expression)
-- MAGIC     expression = re.sub(r'(\d+)G', r'\1', expression)
-- MAGIC     expression = re.sub(r'\*1(?=\+|$)', '', expression)
-- MAGIC     return expression
-- MAGIC
-- MAGIC # 注册为 SQL UDF
-- MAGIC from pyspark.sql.types import StringType
-- MAGIC from pyspark.sql.functions import udf
-- MAGIC spark.udf.register("format_packsize", format_packsize, StringType())
-- MAGIC
-- MAGIC # format_packsize('4.88KGX2+300GX1+200GX14')

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dim}.ddm.dim_sku_pack_size	 sku粒度pack_size打标表
-- source table: ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf  特殊香型的产品机制关系表
-- source table: ${spark.var.catalog.dim}.ddm.dim_store	店铺表
-- source table: ${spark.var.catalog.dim}.cd.dim_product	产品主数据
-- source table: ${spark.var.catalog.dim}.cd.dim_product_listprice	产品LP主数据
-- source table: ${spark.var.catalog.dwd}.cd.dwd_primary_sales_bdl  一级销量事实表
-- target table:  ${spark.var.catalog.dim}.fin.dim_core_pack_item_mf 最终报告表
-- Description:   
-- v1.0 haolong.wu@chiefclouds.com 2025-06-30   创建
-- v1.1 haolong.wu@chiefclouds.com 2025-08-04   LP取值逻辑由最大LP改为rolling 6月销量最大的LP
-- v1.2 haolong.wu@chiefclouds.com 2025-09-03   特殊香型的机制下钻到香型
-- v1.3 haolong.wu@chiefclouds.com 2025-09-03   PDD - VSL切DTC后冗余一份机制打标
-- v1.4 ouyang.xiaowel@unilever-china.com 2026-02-04   dim_core_pack_item_mf新增字段
-- ALTER TABLE ${spark.var.catalog.dim}.fin.dim_core_pack_item_mf
-- ADD COLUMNS (
--     bu_code STRING COMMENT 'BU编码',
--     bu_name STRING COMMENT 'BU名称',
--     customer_type_code STRING COMMENT 'Channel编码',
--     customer_type STRING COMMENT 'Channel名称',
--     site_code STRING COMMENT 'Site编码',
--     site_name STRING COMMENT 'Site名称',
--     category_code STRING COMMENT 'Category编码',
--     category_name STRING COMMENT 'Category名称',
--     brand_code STRING COMMENT 'Brand编码',
--     brand_name STRING COMMENT 'Brand名称',
--     product_line_group_code STRING COMMENT '品线编码',
--     product_line_group STRING COMMENT '品线名称'
-- );
-- v1.5 lin.peishan@unilever-china.com 2026-07-06，管道报错，需要修改取数字段，删除【report_】前缀字段：请使用对应去除前缀的产品字段 
-- v1.6 lin.peishan@unilever-china.com 2026-08-03，数据表 prod_dim.ddm.dim_store 的逻辑变更，将影响各接口中 customer_type 字段的取值逻辑：其数据来源需由原 customer_type 字段切换为 channel 字段。
-- 逻辑描述：
--    1、接口文件名： cpt_core_pack_item_yyyymm.csv
--    2.1、UL SKU CODE 和 机制表Mapping逻辑：category + brand + product_line_group + pack_size  = core_pack_group_detail
--    2.2、特殊香型的sku_code先与香型Mapping表关联转换成带香型的机制，再和机制表的core_pack_group_detail匹配
--    3、若一个core_pack_group_detail有多个不同的LP取数逻辑：取rolling 6个月一级销量sum最大的SKU的LP，都无销量，则取LP最大的LP
--    4、By core_pack_group + item_group_name 的机制LP的生成逻辑：pack_list_price = sum(core_pack_group_detail的LP * qty) 
--    5、机制表的是否主品字段标识小样，小样的LP=0，LP保留两位小数
--    6、每月第4个工作日回传最新产品机制主数据

set spark.sql.sources.partitionOverwriteMode=dynamic;

create or replace table ${spark.var.catalog.tmp}.fin.tmp_core_pack_item_listprice
with cte_sku_code_all as (
select distinct sku_code from ${spark.var.catalog.dim}.cd.dim_product
union
select distinct sku_code from ${spark.var.catalog.dim}.cd.dim_product_listprice where pricingunit not in ('HK','TW')
)
select  c.sku_code
       ,a.unitofmeasure
       ,nvl(a.start_date,'1900-01-01') as start_date
       ,nvl(a.end_date,'9999-12-31')   as end_date
       ,a.listprice
       ,b.base_uom
       ,b.base_uom_conv_num
       ,b.matl_grp_cn as report_matl_grp_cn   --20260706，管道报错，需要修改取数字段，删除report前缀
       ,case when a.unitofmeasure='CS'
             then if(coalesce(b.base_uom_conv_num,0)=0,0,a.listprice/b.base_uom_conv_num)
        else a.listprice end as listprice_pc
from cte_sku_code_all c
left join (select * from ${spark.var.catalog.dim}.cd.dim_product where is_current=1) b
on c.sku_code = b.sku_code
left join (select * from ${spark.var.catalog.dim}.cd.dim_product_listprice where pricingunit not in ('HK','TW')) a  on c.sku_code = a.sku_code
;
alter table ${spark.var.catalog.tmp}.fin.tmp_core_pack_item_listprice set owner to `${spark.var.table.owner}`;

create or replace table ${spark.var.catalog.tmp}.fin.tmp_core_pack_group_detail_listprice
select
    t1.sku_code
    ,t1.sku_name
    ,t1.core_pack_group_detail
    ,coalesce(t2.rolling_6mth_gsv,0) as rolling_6mth_gsv
    ,round(t3.listprice_pc,2) as listprice
    ,row_number() over(partition by t1.core_pack_group_detail order by t2.rolling_6mth_gsv desc, t1.sku_code asc) rn
    ,sum(coalesce(t2.rolling_6mth_gsv,0)) over(partition by t1.core_pack_group_detail) as sum_rolling_6mth_gsv
    ,round(max(t3.listprice_pc) over(partition by t1.core_pack_group_detail),2) as max_listprice
from (
  select 
       a.sku_code
      ,a.sku_name_cn as sku_name
      ,a.division as bu
      ,a.category_short as category
      ,a.cg_sub_brand as brand
-- 20260706，管道报错，需要修改取数字段，删除report前缀
      ,a.national_ex41 as pack_size
      ,a.national_ex42 as product_line_group
      ,a.variant       as report_variant
      ,coalesce(b.target_core_pack
                ,concat_ws(' ',a.category_short,a.cg_sub_brand,a.national_ex42,format_packsize(a.national_ex41))) as core_pack_group_detail
  from ${spark.var.catalog.dim}.cd.dim_product a
  left join ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf b
    on concat_ws(' ',a.category_short,a.cg_sub_brand,a.national_ex42,format_packsize(a.national_ex41)) = b.source_core_pack 
    and a.variant = b.variant_sap
  where a.is_current = 1
  and a.matl_grp_cn != '赠品和小样'
) t1
left join (
  select 
      sku_code,sum(kpi_gsv) as rolling_6mth_gsv
  from ${spark.var.catalog.dwd}.cd.dwd_primary_sales_bdl
  where order_status = 'PS'
  and mth >= date_format(add_months(to_date('$dt'), -6), 'yyyy-MM')
  and mth <= date_format(add_months(to_date('$dt'), -1), 'yyyy-MM')
  group by sku_code  
) t2
on t1.sku_code = t2.sku_code
left join ${spark.var.catalog.tmp}.fin.tmp_core_pack_item_listprice t3
on t1.sku_code = t3.sku_code
and '$dt' >= t3.start_date and '$dt' <= t3.end_date
;
alter table ${spark.var.catalog.tmp}.fin.tmp_core_pack_group_detail_listprice set owner to `${spark.var.table.owner}`;


insert overwrite table ${spark.var.catalog.dim}.fin.dim_core_pack_item_mf partition(dt)
(
      bu_code
    ,bu_name
    ,customer_type_code
    ,customer_type
    ,site_code
    ,site_name
    ,category_code
    ,category_name
    ,brand_code
    ,brand_name
    ,product_line_group_code
    ,product_line_group
    ,store_code
    ,store_name
    ,core_pack_group_code
    ,core_pack_group
    ,item_group_code
    ,item_group_name
    ,is_main_product
    ,main_product_code
    ,main_product_name
    ,sample_code
    ,sample_name
    ,quantity
    ,list_price
    ,pack_list_price
    ,create_by
    ,dw_create_time
    ,dw_last_update_time
    ,dw_batch_num
    ,dt 
)
select distinct
    bu_code
    ,bu_name
    ,customer_type_code
    ,customer_type
    ,site_code
    ,site_name   --20260917
    ,category_code
    ,category_name
    ,brand_code
    ,brand_name
    ,product_line_group_code
    ,product_line_group
    ,''                                                   as store_code
    ,case -- when customer = 'TMALL SUPER' then 'TMALL SUPER - UL'  -- 20260918
          -- when customer = 'TMALL SUPER - UL' then 'TMALL SUPER'  -- 20261018
          when customer ='JD - REGENERATE' then 'JD - UL' else customer end    as store_name  -- 20260904
    ,''                                                   as core_pack_group_code
    ,core_pack_group                                      as core_pack_group
    ,''                                                   as item_group_code
    ,pack_size                                            as item_group_name
    ,is_main_product                                      as is_main_product
    ,''                                                   as main_product_code
    ,if(is_main_product='1',core_pack_group_detail,'')    as main_product_name
    ,''                                                   as sample_code
    ,if(is_main_product='0',core_pack_group_detail,'')    as sample_name
    ,cast(detail_qty as decimal(38,8))                                           as quantity
    ,cast(round(detail_list_price,2) as decimal(38,2))                           as list_price
    ,cast(if(first_value(detail_list_price) over(partition by item_id,sku_id,customer order by detail_list_price) is null
        ,null
        ,round(sum(detail_qty*detail_list_price) over(partition by item_id,sku_id,customer),2)) as decimal(38,8)) as pack_list_price
    ,'Automatic'                                                       as create_by
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
    ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
    ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
    ,'$dt'                                                             as dt
from (
  select distinct
      t1.item_id
      ,t1.sku_id
      ,t2.customer
      ,t1.core_pack_group
      ,t1.pack_size
      ,t1.is_main_product
      ,t1.core_pack_group_detail
      ,sum(t1.qty) over(partition by t1.item_id,t1.sku_id,t2.customer,t1.core_pack_group_detail,t1.is_main_product) as detail_qty    
      -- sum原因：打标拆到品线，需要聚合到品线组，LARTISAN PEACH 470 + LARTISAN 470 = LARTISAN 470*2
      ,if(t1.is_main_product='0',0,t3.list_price) as detail_list_price,
      '' as bu_code,
      t1.bu_sku as bu_name,
      '' as customer_type_code,
      t2.customer_type as customer_type,
      '' as site_code,
      t2.site_name as site_name,
      '' as category_code,
      t1.category_sku as category_name,
      '' as brand_code,
      t1.brand_sku as brand_name,
      '' as product_line_group_code,
      t1.product_line_group as product_line_group

  from (select 
item_id
,shop_id
,sku_id
,core_pack_group
,pack_size
,is_main_product
,core_pack_group_detail
,qty   
,channel
,bu_sku
,category_sku  
,brand_sku 
,product_line_group 
  from ${spark.var.catalog.dim}.ddm.dim_sku_pack_size 
  where end_time = '9999-12-31'
  and channel <> 'DOUYIN'
  and sku_id <>  '0'
  group by item_id
,sku_id
,shop_id
,core_pack_group
,pack_size
,is_main_product
,core_pack_group_detail
,qty   
,channel
,bu_sku
,category_sku  
,brand_sku 
,product_line_group) t1
  left join (
      select shop_id,customer,
      -- customer_type as customer_type, --2026-08-03修改取数逻辑，由原 customer_type 字段切换为 channel 字段
      channel as customer_type,
      if(customer_group like '%TMALL%', 'TMALL', customer_group) as site_name
      from ${spark.var.catalog.dim}.ddm.dim_store
      where status = 1
      union
      select '621699362' as shop_id, 'PDD - VSL' as customer,'EC' customer_type ,'PDD' site_name      -- PDD - VSL切DTC后冗余一份机制打标 20260917
  ) t2
  on t1.shop_id = t2.shop_id
  left join (
    select
        core_pack_group_detail
        ,if(sum_rolling_6mth_gsv = 0, max_listprice, listprice) as list_price 
    from ${spark.var.catalog.tmp}.fin.tmp_core_pack_group_detail_listprice
    where rn = 1
  ) t3
  on t1.core_pack_group_detail = t3.core_pack_group_detail
)
;