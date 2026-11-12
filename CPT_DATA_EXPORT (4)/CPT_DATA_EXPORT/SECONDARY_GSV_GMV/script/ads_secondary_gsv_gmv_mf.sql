-- Databricks notebook source
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑
-- dst 20261016  PDD - VSL 补上site、channel

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("dt", "2026-03-05")
-- MAGIC dbutils.widgets.text("start_mth", "2026-01")
-- MAGIC dbutils.widgets.text("end_mth", "2026-02")

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: 
-- target table:  ${spark.var.catalog.ads}.fin_cpt.ads_secondary_gsv_gmv_mf
-- Description:   
-- v1.0 jin.zhen@chiefclouds.com 2025/06/11
-- 逻辑描述：
-- Scope ：
-- Item销售事实表：prod_dws.ddm.dws_trd_total_sku_sales_df  取日的数据聚合到月，退后gmv指标：gmv_after_refund
-- 产品机制表：prod_dim.ddm.dim_sku_pack_size
-- 产品主数据：prod_dim.cd.dim_product 
-- 产品匹配：prod_dim.cd.dim_sku_matching
-- 组套匹配：${spark.var.schema.dim.cd}.dim_bundle_matching
-- sku_id & sku mapping： ${spark.var.catalog.dim}.cd.dim_item_sku_mapping （E3 & DTC Mapping)
-- 价格：${spark.var.schema.dim.cd}.dim_product_listprice
-- 店铺表：prod_dim.ddm.dim_store
-- Logic：只取机制表和sku_matching表交集的数据
-- 1、取维度 prod_dim.ddm.dim_sku_pack_size 的维度，通过shop_id + item_id + sku_id Maping 取得聚合 KPI 
-- 2、取gmv
--      2.1 follow 黄金公式清洗过滤逻辑 但不过滤品牌
--      2.2 VIP 单独做逻辑  ${spark.var.catalog.dwd}.ddm.dwd_vip_trd_barcode_sales_df
--      2.3 JD 剔除ToB  
--            通过Item_id + day 关联${spark.var.catalog.dwd}.ddm.dwd_mkt_ec_sales_tob_di，取2B的GMV，然后用 total_gmv - 2B_gmv
-- 3、取gsv
--      3.1 组套产品匹配+组套匹配 + sku&item Mapping到ul_sku_code
--      3.2 通过ul_sku_code 找 LP （若为赠品和小样，不需要计算gsv）
--      3.3 qty = 组套uom * 销量qty
--      3.4 gsv = LP * qty
--      3.5 TMALL/PDD/VIP  单独做逻辑处理；JD 剔除ToB
-- v1.1 调整：
--    天猫：202509月之前用 他们给的手工表，202509月之后的使用 ${spark.var.catalog.dim}.cd.dim_item_sku_mapping表
--   cpt_second_sales_yyyymm.csv
-- v1.2 haolong.wu@chiefclouds.com 2025-12-04   PDD - VSL切DTC后要从PDD - UL中拆出来, 跟着DDM hardcode处理; 
--                                              PDD Sku Mapping的关联逻辑和其他DTC店不一样, 修改关联条件
-- v1.3 qing.liu@chiefclouds.com 2026-02-09   LP维表新增过滤where pricingunit not in ('HK','TW')
-- v1.4 iris.lin 2026-04-24修改,site_name的取值从原来的national_ex3换成national_ex4
-- v1.5 iris.lin 2026-05-13修改,site_name的取值需要取national_ex3
-- v1.6 iris.lin 2026-06-29修改,表cd.dim_store,需要取national_ex3作为site_name
-- v1.7 iris.lin 2026-07-06修改,表cd.dim_product,需要修改取数字段，删除report前缀
-- v1.8 iris.lin 2026-08-03修改,  数据表 prod_dim.ddm.dim_store 的逻辑变更，将影响各接口中 customer_type 字段的取值逻辑：其数据来源需由原 customer_type 字段切换为 channel 字段。

-- 价格表
create or replace table ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc
as 
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
       ,b.matl_grp_cn as report_matl_grp_cn  --20260706，管道报错，需要修改取数字段，删除report前缀
       ,case when a.unitofmeasure='CS'
             then if(coalesce(b.base_uom_conv_num,0)=0,0,a.listprice/b.base_uom_conv_num)
        else a.listprice end as listprice_pc
      ,b.division as bu_name
      ,b.category_short as category_name
      ,b.cg_sub_brand as brand_name
      ,b.national_ex42 as product_line_group
from cte_sku_code_all c
left join (select * from ${spark.var.catalog.dim}.cd.dim_product where is_current=1) b
on c.sku_code = b.sku_code
left join (select * from ${spark.var.catalog.dim}.cd.dim_product_listprice where pricingunit not in ('HK','TW')) a  on c.sku_code = a.sku_code
;
alter table ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc set owner to `${spark.var.table.owner}`;


-- COMMAND ----------

-- VIP的数据源
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_vip_data
as
select
  a.*,b.customer
  ,c.ul_sku_code       as sku_code 
  ,c.source_customer   as source_customer
  ,b.shop_name         as shop_name
from  
(
  select
     date_time                    as period_key 
    ,shop_id                      as shop_id
    ,osn                          as item_id
    ,merchandise_no               as sku_id
    ,barcode                      as barcode
    ,sum(goods_acture_amt)        as gmv_before_refund
    ,sum(result_goods_acture_amt) as gmv     -- gmv_after_refund 
    ,sum(result_goods_acture_num) as qty
    ,'VIP'                        as source_type
    ,'VIP'                        as platform
  from ${spark.var.catalog.dwd}.ddm.dwd_vip_trd_barcode_sales_df
  where left(date_time,7) >= '$start_mth' and left(date_time,7) <= '$end_mth'
  group by shop_id,date_time,osn,merchandise_no,barcode
) a 
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id,shop_name
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
) b 
on nvl(a.shop_id,'') = nvl(b.shop_id,'')
left join ${spark.var.catalog.dim}.cd.dim_sku_matching c 
 on a.barcode = c.source_sku_code and 
  upper(b.shop_name) = upper(substring(c.source_customer,CHARINDEX('-',c.source_customer)+2,len(c.source_customer)))
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_vip_data set owner to `${spark.var.table.owner}`;

-- 计算VIP的 bundle
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_vip_bundle
as
with cte_lp as 
(
  select
    a.period_key,a.shop_id,a.item_id,a.sku_id,a.customer,a.barcode,a.source_type,a.platform
    ,coalesce(b.ul_sku_code,a.sku_code)             as sku_code
    ,a.gmv_before_refund
    ,a.gmv
    ,case when b.sid is not null then a.qty*b.bom_num else a.qty end   as pay_qty
    ,case when b.sid is not null then b.bom_num else b.bom_num end     as bom_num
    ,case when b.sid is not null then 1 else 0 end                         as is_bundle
    ,case when coalesce(b.ul_sku_code,a.sku_code)is null then 0.0001 else c.listprice_pc end as listprice
    ,c.bu_name
    ,c.category_name
    ,c.brand_name
    ,c.product_line_group
  from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_vip_data a 
  left join ${spark.var.catalog.dim}.cd.dim_bundle_matching b 
    on a.barcode = b.item_code  
    and upper(a.shop_name) = upper(substring(b.src_customer,CHARINDEX('-',b.src_customer)+2,len(b.src_customer)))
  left join ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc c 
    on coalesce(b.ul_sku_code,a.sku_code,'OTHERS') = c.sku_code 
      and a.period_key >= c.start_date
      and a.period_key <= c.end_date	
)
,cte_data as 
(
  select
    a.*
    ,b.total_listprice
    ,b.total_bom_num
    ,if(a.is_bundle = 0,1,if(nvl(b.total_listprice,0) = 0, 0, (a.bom_num * a.listprice) / total_listprice))     as lp_contri
  from cte_lp a 
  left join 
  (
      select t.item_id,t.sku_id,t.period_key
          ,sum(t.bom_num*t.listprice) as total_listprice
          ,sum(t.bom_num)   as total_bom_num
    from (
          select item_id,sku_id,sku_code,listprice,bom_num,period_key
        from cte_lp
        group by item_id,sku_id,sku_code,listprice,bom_num,period_key
        ) t 
    group by t.item_id,t.sku_id,t.period_key
  ) b 
    on a.item_id = b.item_id
        and a.sku_id = b.sku_id
        and a.period_key = b.period_key
)
select
	 a.period_key
	,a.shop_id
	,a.item_id
	,a.sku_id
	,a.customer
	,a.sku_code
  ,a.gmv_before_refund*a.lp_contri as gmv_before_refund
	,a.gmv*a.lp_contri as gmv 
	,a.pay_qty
	,a.bom_num
	,a.is_bundle
	,a.listprice
	,a.total_listprice
	,a.total_bom_num
	,a.lp_contri
	,a.source_type
	,a.platform
  ,a.bu_name
  ,a.category_name
  ,a.brand_name
  ,a.product_line_group
from cte_data a 
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_vip_bundle set owner to `${spark.var.table.owner}`;

-- COMMAND ----------

-- 天猫的数据源计算 
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_data
as 
select 
  item_id,period_key
  ,gmv as gmv_before_refund
  ,gmv_after_refund as gmv
  ,qty
  ,a.shop_id,shop_name,sku_id,sku_name,b.customer,platform,source_type
from ${spark.var.catalog.dws}.ddm.dws_trd_total_sku_sales_df a 
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
) b 
on nvl(a.shop_id,'') = nvl(b.shop_id,'')
where a.period_type='日' and left(a.period_key,7) >= '$start_mth' and left(a.period_key,7) <= '$end_mth'
      and b.customer in ('TMALL FGS - AHC','TMALL FGS - AHC CBE')
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_data set owner to `${spark.var.table.owner}`;

-- 计算TM的 bundle          优先取 sku_matching的匹配
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_bundle
as
with cte_lp as 
(
     select
        a.period_key,a.shop_id,a.item_id,a.sku_id,a.customer,a.source_type,a.platform
        ,b.du_code             as sku_code
        ,a.gmv_before_refund
        ,a.gmv
        ,case when b.link_code is not null then a.qty*b.bom_num 
          else a.qty end   as pay_qty
        ,case when b.link_code is not null then b.bom_num 
          else 0 end     as bom_num
        ,if(b.link_code is not null ,1,0)         as is_bundle
        ,case when b.du_code is null then 0.0001 else c.listprice_pc end  as listprice
        ,c.bu_name
        ,c.category_name
        ,c.brand_name
        ,c.product_line_group
    from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_data a
    left join 
    (
      select distinct link_code,source_sku_code,du_code,a.bom_num,1 as flag
      from ${spark.var.catalog.dim}.cd.dim_cpt_bundle_mapping a 
      inner join ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc b
      on a.du_code = b.sku_code
      where nvl(b.listprice_pc,0) >0
    ) b
    on a.item_id = b.link_code and a.sku_id = b.source_sku_code
    left join ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc c 
    on b.du_code = c.sku_code 
        and a.period_key >= c.start_date
        and a.period_key <= c.end_date
    where (left(a.period_key,7) < '2025-09' and a.customer = 'TMALL FGS - AHC') 
      or a.customer = 'TMALL FGS - AHC CBE'

    union all
     select
        a.period_key,a.shop_id,a.item_id,a.sku_id,a.customer,a.source_type,a.platform
        ,d.tc_goods_sku            as sku_code
        ,a.gmv_before_refund
        ,a.gmv
        ,case 
          when d.outer_goods_id is not null then a.qty * d.tc_goods_sl 
          else a.qty end   as pay_qty
        ,case 
            when d.outer_goods_id is not null then d.tc_goods_sl
          else 0 end     as bom_num
        ,if(d.outer_goods_id is not null,1,0)         as is_bundle
        ,case when d.tc_goods_sku is null then 0.0001 else c.listprice_pc end  as listprice
        ,c.bu_name
        ,c.category_name
        ,c.brand_name
        ,c.product_line_group
    from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_data a
    left join ${spark.var.catalog.dim}.cd.dim_item_sku_mapping d
      on a.item_id = d.outer_goods_id and a.sku_id = d.outer_goods_sku_id
        and a.period_key>=d.start_date
		    and a.period_key<=d.end_date
    left join ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc c 
    on d.tc_goods_sku = c.sku_code 
        and a.period_key >= c.start_date
        and a.period_key <= c.end_date
    where left(a.period_key,7) >= '2025-09' and a.customer = 'TMALL FGS - AHC'
)
,cte_data as 
(
  select
    a.*
    ,b.total_listprice
    ,b.total_bom_num
    ,if(a.is_bundle = 0,1,if(nvl(b.total_listprice,0) = 0, 0, (a.bom_num * a.listprice) / total_listprice))     as lp_contri
  from cte_lp a 
  left join 
  (
      select t.item_id,t.sku_id,t.period_key
          ,sum(t.bom_num*t.listprice) as total_listprice
          ,sum(t.bom_num)   as total_bom_num
    from (
          select item_id,sku_id,sku_code,listprice,bom_num,period_key
        from cte_lp
        group by item_id,sku_id,sku_code,listprice,bom_num,period_key
        ) t 
    group by t.item_id,t.sku_id,t.period_key
  ) b 
    on a.item_id = b.item_id
        and a.sku_id = b.sku_id
        and a.period_key = b.period_key
)
select
	a.period_key
	,a.shop_id
	,a.item_id
	,a.sku_id
	,a.customer
	,a.sku_code
  ,case when nvl(lp_contri,0)>0 then a.gmv_before_refund*lp_contri else a.gmv_before_refund end as gmv_before_refund
	,case when nvl(lp_contri,0)>0 then a.gmv*lp_contri else a.gmv end as gmv  
	,a.pay_qty
	,a.bom_num
	,a.is_bundle
	,a.listprice
	,a.total_listprice
	,a.total_bom_num
	,a.lp_contri
	,a.source_type
	,a.platform
  ,a.bu_name
  ,a.category_name
  ,a.brand_name
  ,a.product_line_group
from cte_data a 
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_bundle set owner to `${spark.var.table.owner}`;

-- COMMAND ----------

-- 猫超的数据源替换成新的数据源
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_supper_data
as
select 
	 a.*
	,b.customer
from 
(
  select 
    t2.target_code as shop_id
    ,t2.target_name as shop_name
    ,item_id  as item_id
    ,item_name as item_name
    ,real_sku_id as sku_id
    ,sku_property as sku_name
    ,date_format(to_date(date_time, 'yyyyMMdd'), 'yyyy-MM-dd')  as period_key
    ,pay_ord_amt as gmv_before_refund --增加退前GMV Eddie
    ,real_pay_ord_amt as gmv
    ,pay_itm_qty - refund_itm_qty_end as qty
    ,'TMALL SUPER' as platform
    ,'PLATFORM_B2C'  as source_type
    ,'日' as period_type
  from ${spark.var.catalog.ods}.int_hologres.ods_tm_market_trd_sku_sales_day_di t1 
  left join (select * from ${spark.var.catalog.dim}.ddm.dim_pub_standard_mapping where map_type = 'shop' and platform='TMALL SUPER') t2
  on t1.supplier_code=t2.source_code
  where date_format(to_date(t1.date_time, 'yyyyMMdd'), 'yyyy-MM') >= :start_mth
    and date_format(to_date(t1.date_time, 'yyyyMMdd'), 'yyyy-MM') <= :end_mth
) a 
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
) b
on nvl(a.shop_id,'') = nvl(b.shop_id,'')
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_supper_data set owner to `${spark.var.table.owner}`;

-- 单独算JD 的数据源： 需要去除 tob的gmv和gsv
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_jd_data
as
select
    a.item_id
    ,string(to_date(a.start_date, 'yyyyMMdd')) as period_key
    ,a.gmv-nvl(b.tob_gmv,0)             as gmv_before_refund  -- 增加退前GMV Eddie 20260402
    ,a.gmv-nvl(b.tob_gmv,0)             as gmv
    ,a.qty-coalesce(b.tob_qty,0)        as qty
    ,c.shop_id                          as shop_id
    ,c.shop_name                        as shop_name
    ,''                                 as sku_id
    ,''                                 as sku_name
    ,d.customer                         as customer
    ,'JD'                               as platform
from  
(
  select
    a.item_id,replace(a.start_date,'-','') as start_date
    ,sum(cast(coalesce(a.gmv_after_refund,0) as decimal(16,2))) as gmv
    ,sum(coalesce(a.qty,0))  as qty
  from  
  (
    select 
      *
    from ${spark.var.catalog.dws}.ddm.dws_trd_total_sku_sales_df 
    where period_type = '日' and platform = 'JD' 
      and left(period_key,7) >= '$start_mth' and left(period_key,7) <= '$end_mth'
  ) a 
  group by a.item_id,a.start_date
) a 
left join 
(
  select 
  stat_date  as period 
  ,item_id
  ,sum(coalesce(pay_ord_amt,0)) as tob_gmv
  ,sum(coalesce(pay_ord_qty,0)) as tob_qty
  ,'Day' as period_type
  from ${spark.var.catalog.dwd}.ddm.dwd_mkt_ec_sales_tob_di
  where platform='JD' and upper(type) = 'TOB'
  and left(stat_date,6) >= replace('$start_mth','-','') 
  and left(stat_date,6) <= replace('$end_mth','-','') 
  group by 
  stat_date  
  ,item_id
  ,type
) b
on a.item_id = b.item_id  and a.start_date = replace(b.period,'/','')
left join 
(
  select * from ${spark.var.catalog.dim}.ddm.dim_prd_item 
  where end_time = '9999-12-31' and is_current = 1
) c 
on a.item_id = c.item_id
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
) d 
on nvl(c.shop_id,'') = nvl(d.shop_id,'')
where left(a.start_date,6) >= replace('$start_mth','-','') 
  and left(a.start_date,6) <= replace('$end_mth','-','') 
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_jd_data set owner to `${spark.var.table.owner}`;




-- COMMAND ----------

-- 数据源汇总
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_sku_sales_source
as 
select 
  item_id,period_key
  ,gmv   as  gmv_before_refund
  ,gmv_after_refund as gmv
  ,case when a.platform = 'PDD' then buyer_cnt else qty end as qty   -- 拼多多 使用 支付买家数
  ,a.shop_id
  ,shop_name,sku_id,sku_name
  ,if(a.period_key > '2025-10-16' and a.shop_id = '621699362', 'PDD - VSL', d.customer) as customer     -- 20251204修改
  ,platform
  ,source_type
from ${spark.var.catalog.dws}.ddm.dws_trd_total_sku_sales_df a 
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
) d 
on nvl(a.shop_id,'') = nvl(d.shop_id,'')
where a.period_type='日' and left(a.period_key,7) >= '$start_mth' 
      and left(a.period_key,7) <= '$end_mth'
      and a.platform not in ('JD','VIP','TMALL SUPER')
      and d.customer <> 'TMALL FGS - AHC CBE' and d.customer <> 'TMALL FGS - AHC'
union all

-- 合并 JD的数据
select
      a.*,b.source_type
from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_jd_data a 
left join 
(
      select 
      distinct a.item_id,source_type
      from ${spark.var.catalog.dws}.ddm.dws_trd_total_sku_sales_df a 
      where a.period_type='日' and left(a.period_key,7) >= '$start_mth' 
        and left(a.period_key,7) <= '$end_mth'
            and a.platform = 'JD'
) b 
 on a.item_id = b.item_id

-- 猫超
 union all
 select
  item_id,period_key
  ,gmv_before_refund
  ,gmv
  ,qty
  ,shop_id
  ,shop_name,sku_id,sku_name,customer,platform
  ,source_type
 from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_supper_data
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_sku_sales_source set owner to `${spark.var.table.owner}`;

-- COMMAND ----------

---- bundle拆分逻辑
-- ul_sku_code 匹配
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales 
as
select 
 a.*
 ,nvl(b.ul_sku_code,c.goods_sn) as ul_sku_code
from (select * from ${spark.var.catalog.tmp}.fin.tmp_trd_total_sku_sales_source 
      where platform='JD'
      ) a 
left join (
            select * 
            from ${spark.var.catalog.dim}.cd.dim_sku_matching
            where source_type='PLATFORM_B2C'
            ) b on a.item_id = b.source_sku_code 
               and upper(a.shop_name) = upper(substring(b.source_customer,CHARINDEX('-',b.source_customer)+2,len(b.source_customer)))
left join ${spark.var.catalog.dim}.cd.dim_item_sku_mapping c 
          on a.item_id = c.outer_goods_id and a.sku_id = c.outer_goods_sku_id
		  and a.source_type = c.source_type
		  and a.period_key>=c.start_date
		  and a.period_key<=c.end_date
		  and c.is_tc='否'                              -- 非组套
union all 
select 
 a.*
 ,nvl(b.ul_sku_code,c.goods_sn) as ul_sku_code
from (select * from ${spark.var.catalog.tmp}.fin.tmp_trd_total_sku_sales_source 
      where platform<>'JD'
      ) a 
left join (
            select * 
            from ${spark.var.catalog.dim}.cd.dim_sku_matching
            where source_type='PLATFORM_B2C'
            ) b on concat(a.item_id,'_',a.sku_id) = b.source_sku_code 
            and upper(a.shop_name) = upper(substring(b.source_customer,CHARINDEX('-',b.source_customer)+2,len(b.source_customer)))
left join ( 
            -- 20251204修改
            select
               t1.store_code,store_name
               ,if(t2.site = 'PDD' and source_type = 'DTC', outer_goods_sku_id, outer_goods_id)                      as outer_goods_id
               ,if(t2.site = 'PDD' and source_type = 'DTC', split_part(outer_goods_id,'-',2), outer_goods_sku_id)    as outer_goods_sku_id
               ,goods_sn,tc_goods_sku,is_tc,tc_goods_sl
               ,start_date,end_date,source_type
            from ${spark.var.catalog.dim}.cd.dim_item_sku_mapping  t1
            left join (
                select 	store_code
                            ,max(national_ex3)  as site
                from 	${spark.var.catalog.dim}.cd.dim_store
                group by store_code
            ) t2
            on t1.store_code = t2.store_code
) c 
      on a.item_id = c.outer_goods_id and a.sku_id = c.outer_goods_sku_id
      and a.source_type = c.source_type
      and a.period_key>=c.start_date
      and a.period_key<=c.end_date
      and c.is_tc='否'                              -- 非组套
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales set owner to `${spark.var.table.owner}`;



-- 组套拆分
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_bundle
as
with cte_bundle as 
(
   select 
     a.*
	  ,coalesce(b.ul_sku_code, c.tc_goods_sku, a.ul_sku_code) as sku_code
    ,case when b.sid is not null then a.qty * b.bom_num
          when c.outer_goods_id is not null then a.qty * c.tc_goods_sl
          else a.qty end as pay_qty	  		  
    ,case when b.sid is not null then b.bom_num
          when c.outer_goods_id is not null then c.tc_goods_sl
          else 0 end as bom_num
    ,if(b.sid is not null or c.outer_goods_id is not null,1,0)  as is_bundle
     from (select * from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales
           where platform='JD'
          ) a 
   left join (select *
                       from ${spark.var.catalog.dim}.cd.dim_bundle_matching
                       where source_type = 'PLATFORM_B2C'
   		  ) b  on  a.platform='JD' and  a.item_id = b.item_code
		       and upper(a.shop_name) = upper(substring(b.src_customer,CHARINDEX('-',b.src_customer)+2,len(b.src_customer)))
   left join ${spark.var.catalog.dim}.cd.dim_item_sku_mapping c 
             on a.item_id = c.outer_goods_id and a.sku_id = c.outer_goods_sku_id
   		  and a.source_type = c.source_type
		  and a.period_key>=c.start_date
		  and a.period_key<=c.end_date
		  and c.is_tc='是'                             -- 组套
union all 
   select 
     a.*
	  ,coalesce(b.ul_sku_code, c.tc_goods_sku, a.ul_sku_code) as sku_code
    ,case when b.sid is not null then a.qty * b.bom_num
          when c.outer_goods_id is not null then a.qty * c.tc_goods_sl
          else a.qty end as pay_qty
    ,case when b.sid is not null then b.bom_num
          when c.outer_goods_id is not null then c.tc_goods_sl
          else 0 end as bom_num
    ,if(b.sid is not null or c.outer_goods_id is not null,1,0)  as is_bundle
     from (select * from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales
           where platform<>'JD'
          ) a 
   left join (select *
                       from ${spark.var.catalog.dim}.cd.dim_bundle_matching
                       where source_type = 'PLATFORM_B2C'
   		  ) b  on  a.platform<>'JD' and concat(a.item_id,'_',a.sku_id) = b.item_code  
		   and upper(a.shop_name) = upper(substring(b.src_customer,CHARINDEX('-',b.src_customer)+2,len(b.src_customer)))
   left join (
            -- 20251204修改
            select
                  t1.store_code,store_name
                  ,if(t2.site = 'PDD' and source_type = 'DTC', outer_goods_sku_id, outer_goods_id)                      as outer_goods_id
                  ,if(t2.site = 'PDD' and source_type = 'DTC', split_part(outer_goods_id,'-',2), outer_goods_sku_id)    as outer_goods_sku_id
                  ,goods_sn,tc_goods_sku,is_tc,tc_goods_sl
                  ,start_date,end_date,source_type
            from ${spark.var.catalog.dim}.cd.dim_item_sku_mapping t1
            left join (
                  select 	store_code
                              ,max(national_ex3)  as site
                  from 	${spark.var.catalog.dim}.cd.dim_store
                  group by store_code
            ) t2
            on t1.store_code = t2.store_code
      ) c 
      on a.item_id = c.outer_goods_id and a.sku_id = c.outer_goods_sku_id
      and a.source_type = c.source_type
      and a.period_key>=c.start_date
      and a.period_key<=c.end_date
      and c.is_tc='是'                             -- 组套
)
,cte_listPrice as 
(
   select a.*
         ,case when d.sku_code is null or d.listprice_pc is null 
            then 0.0001 else d.listprice_pc end  as listprice 
         ,d.report_matl_grp_cn
         ,d.bu_name
         ,d.category_name
         ,d.brand_name
         ,d.product_line_group
   from cte_bundle a 
   left join ${spark.var.catalog.tmp}.fin.tmp_dws_trd_total_item_sales_listprice_pc d 
          on  a.sku_code = d.sku_code
		  and a.period_key>=d.start_date
		  and a.period_key<=d.end_date
)
,cte_total_price_qty as 
(
    select a.*
	       ,b.total_listprice
		     ,b.total_bom_num
		   ,if(a.is_bundle = 0,1,if(nvl(b.total_listprice,0) = 0, 0, (a.bom_num * a.listprice) / total_listprice))     as lp_contri
    from cte_listPrice a 
    left join (
               select t.item_id,t.sku_id,t.period_key,upper(t.shop_name) as shop_name
                      ,sum(t.bom_num*t.listprice) as total_listprice
               	      ,sum(t.bom_num)   as total_bom_num
               from (
                     select item_id,sku_id,sku_code,listprice,bom_num,period_key,shop_name
               		 from cte_listPrice
               		 group by item_id,sku_id,sku_code,listprice,bom_num,period_key,shop_name
                   ) t 
    		    group by t.item_id,t.sku_id,t.period_key,upper(t.shop_name)
    		  ) b 
    		  on a.item_id = b.item_id
             and a.sku_id = b.sku_id
             and a.period_key = b.period_key
			 and upper(a.shop_name) = upper(b.shop_name)
)
select 
 a.*
 ,a.gmv_before_refund *a.lp_contri as new_gmv_before_refund
 ,a.gmv*a.lp_contri as new_gmv
from cte_total_price_qty a 
;	  
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_bundle set owner to `${spark.var.table.owner}`;


-- COMMAND ----------

-- 数据合并（方便对数）
create or replace table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_all
as
with cte_data as 
(
  select 
    period_key,shop_id,item_id,sku_id,customer,sku_code,gmv_before_refund,gmv,pay_qty,bom_num,is_bundle
    ,listprice,total_listprice,total_bom_num,lp_contri,source_type,platform,bu_name,category_name,brand_name,product_line_group
  from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_vip_bundle
  union all
  select  
    period_key,shop_id,item_id,sku_id,customer,sku_code,gmv_before_refund,gmv,pay_qty,bom_num,is_bundle
    ,listprice,total_listprice,total_bom_num,lp_contri,source_type,platform,bu_name,category_name,brand_name,product_line_group
  from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_tm_bundle
  union all
  select
    period_key,shop_id,item_id,sku_id,customer,sku_code,new_gmv_before_refund as gmv_before_refund,new_gmv as gmv,pay_qty,bom_num,is_bundle
    ,listprice,total_listprice,total_bom_num,lp_contri,source_type,platform,bu_name,category_name,brand_name,product_line_group
  from ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_bundle
) 
select
  a.*
  ,nvl(a.pay_qty,0)* nvl(a.listprice,0)             as gsv
  ,case when a.platform = 'JD' then c.pack_size else b.pack_size end as pack_size
  ,case when a.platform = 'JD' then c.core_pack_group else b.core_pack_group end as core_pack_group
  ,case when a.platform = 'JD' then c.is_main_product else b.is_main_product end as is_main_product
  ,case when a.customer in ('TMALL FGS - AHC CBE','TMALL FGS - AHC') 
            and nvl(b.flag,0) = 1 and nvl(d.flag,0) = 1          then 1
        when a.platform = 'JD' and nvl(c.flag,0) = 1 and nvl(f.flag,0) = 1 then 1
        when  nvl(b.flag,0)+nvl(c.flag,0) >= 1 then 1 else 0 end as flag
  ,case when a.platform = 'JD' then f.item_name else d.item_name end as item_name
  ,case when a.platform = 'JD' then f.category else d.category end as category
  ,case when a.platform = 'JD' then f.brand else d.brand end as brand
  ,case when a.platform = 'JD' then f.bu else d.bu end as bu
  ,e.shop_name
  -- ,case when a.platform = 'JD' then f.product_line_group else d.product_line_group end as product_line_group
  ,case when a.customer = 'PDD - VSL' then  'EC'   else  e.customer_type   end as customer_type  -- 20261016
  ,case when a.customer = 'PDD - VSL' then  'PDD'  else  e.site_name   end as site_name          -- 20261016
from cte_data a 
left join 
(
  select 
    distinct item_id,sku_id,shop_id,max(pack_size) as pack_size
    ,core_pack_group,max(is_main_product) as is_main_product
    ,1  as flag
  from ${spark.var.catalog.dim}.ddm.dim_sku_pack_size
  where end_time = '9999-12-31' 
  and channel <> 'DOUYIN'
  group by item_id,sku_id,shop_id,core_pack_group
) b 
  on a.item_id = b.item_id and a.sku_id = b.sku_id and a.shop_id = b.shop_id and a.platform <> 'JD'
left join 
(
  select 
    distinct item_id,shop_id,max(pack_size) as pack_size
    ,core_pack_group,max(is_main_product) as is_main_product
    ,1 as flag
  from ${spark.var.catalog.dim}.ddm.dim_sku_pack_size
  where end_time = '9999-12-31' 
  and channel <> 'DOUYIN'
  group by item_id,shop_id,core_pack_group
) c
  on a.item_id = c.item_id and  a.shop_id = c.shop_id and a.platform = 'JD'
left join (
    select *,1 as flag
    from ${spark.var.catalog.dim}.ddm.dim_prd_sku   -- 打标表
    where is_current = 1
  ) d
  on a.item_id = d.item_id and a.sku_id = d.sku_id
  and a.period_key between d.start_time and d.end_time and a.platform <> 'JD'
  and d.item_name not like '%购物金%' 
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id,shop_name
      -- ,customer_type   --2026-08-03修改取数逻辑，由原 customer_type 字段切换为 channel 字段
      ,channel as customer_type
      ,customer_group as site_name
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
)e 
  on a.shop_id =e.shop_id and a.customer = e.customer
left join (
    select *,1 as flag
    from ${spark.var.catalog.dim}.ddm.dim_prd_sku   -- 打标表
    where is_current = 1
  ) f
  on a.item_id = f.item_id 
  and a.period_key between f.start_time and f.end_time and f.platform = 'JD'
  and f.item_name not like '%购物金%' 
;
alter table ${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_all set owner to `${spark.var.table.owner}`;

-- COMMAND ----------

-- 入库 new
-- 参数设置
set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_secondary_gsv_gmv_mf partition(dt)
(month
,bu_code
,bu_name
,customer_type_code
,customer_type
,site_code
,site_name
,sales_type
,store_code
,store_name
,category_code
,category_name
,brand_code
,brand_name
,product_line_group_code
,product_line_group
,core_pack_group_code
,core_pack_group
,item_group_code
,item_group_name
,secondary_gmv_amount
,secondary_gsv_amount
,create_by
,dw_create_time
,dw_last_update_time
,dw_batch_num
,dt )
select 
  replace(left(a.period_key,7),'-','')                     as month
  ,''                                                      as bu_code
  ,a.bu_name
  ,''                                                      as customer_type_code
  ,a.customer_type
  ,''                                                      as site_code
  ,a.site_name
  ,'2C'                                                    as sales_type
  ,''                                                      as store_code
  ,case when a.customer ='JD - REGENERATE' then 'JD - UL' else a.customer end    as store_name  -- 20260904
  ,''                                                      as category_code
  ,a.category_name
  ,''                                                      as brand_code
  ,a.brand_name
  ,''                                                      as product_line_group_code
  ,a.product_line_group
  ,''                                                      as core_pack_group_code
  ,a.core_pack_group
  ,''                                                      as item_group_code
  ,a.pack_size                                             as item_group_name
  ,cast(sum(a.gmv) as decimal(38,2))                       as secondary_gmv_amount
  ,cast(sum(case when is_main_product= 0 then 0 else a.gsv end) as decimal(38,2))  as secondary_gsv_amount 
  ,'Automatic'                                                       as create_by
  ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time
  ,cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time
  ,cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
  ,'$dt'                                                             as dt
from 
${spark.var.catalog.tmp}.fin.tmp_trd_total_item_sales_all a 
where a.bu in ('HOME CARE','BEAUTY&WELLBEING','PERSONAL CARE') 
and a.flag = 1 and nvl(sku_code,'') <> ''
group by replace(left(a.period_key,7),'-',''),a.core_pack_group,a.pack_size
,case when a.customer ='JD - REGENERATE' then 'JD - UL' else a.customer end -- 20260904
,a.bu_name,a.customer_type,a.site_name,a.category_name,a.brand_name,a.product_line_group
