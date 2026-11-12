-- Databricks notebook source
-- 20261016 dst 修改tmall的site_code\site_name

-- COMMAND ----------

-- DBTITLE 1,tmp_tmall_super_bill_mi_bystore
-- **********************************************************************
-- source table: ${spark.var.catalog.dws}.ddm.dws_tmall_super_bill_mi                   --猫超账单表
-- source table: ${spark.var.catalog.dws}.ddm.dws_pdd_bill_mi                           --pdd账单表
-- source table: ${spark.var.catalog.tmp}.fin.tmp_tmall_super_bill_mi_bystore           --猫超bystore账单临时表
-- source table: ${spark.var.catalog.tmp}.fin.tmp_pdd_bill_mi_bystore                   --pdd bystore账单临时表
-- source table: ${spark.var.catalog.dim}.cd.dim_product                                --产品主数据 
-- source table: ${spark.var.catalog.dim}.fin.dim_platform_finance_spending_mapping     --UL平台费用类型映射表
-- source table: ${spark.var.catalog.dws}.fin.dws_ec_platform_bill_mi                   --账单合并表

-- target table: ${spark.var.catalog.ads}.fin_cpt.ads_ec_platform_bill_mi               --账单结果表

-- Description:   
-- v1.0 iris.lin@systex.com.cn 2026-01-15  创建
-- v1.1 iris.lin@systex.com.cn 2026-03-17  DDM将数据清洗放到dws前，CPT不做数据清洗



-- 猫超
create or replace table ${spark.var.catalog.tmp}.fin.tmp_tmall_super_bill_mi_bystore
WITH maochao_t0 AS (
  SELECT
    t.mth AS mth,
    case when t.bu='PC' then 'PERSONAL CARE'
          when t.bu='HC' then 'HOME CARE'
          else t.bu end as bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group, 
    t.fee_type,
    SUM(NVL(t.untaxed_amount, 0)) AS untaxed_amount
  FROM
    ${spark.var.catalog.dws}.ddm.dws_tmall_super_bill_mi t
      -- LEFT JOIN ${spark.var.catalog.dim}.ddm.dim_tmall_super_product_mapping m
      --   ON t.backend_product_code = m.backend_product_code
  WHERE 1=1
    -- and LOWER(t.category) in ('hair', 'hair-nexxus', 'skin') --20260317注释，取消bu=B&W的限制。得到三个bu的数据。
    and t.fee_type IN (
      '百亿补贴佣金',
      '淘客U选返佣',
      '营销活动-淘客',
      '营销活动-淘客团长服务费',
      '达播佣金',
      '店播佣金',
      '品牌新享',
      '供应商承担优惠金额',
      '收入金额',
      '商品成本',
      '平台费',
      'Total CPP'
    )
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    t.fee_type
)
,

maochao_t1 as (
select 
t.mth,
upper(t.bu) as bu,
upper(t.category) as category,
upper(t.brand) as brand,
upper(t.product_line_group) as product_line_group, 
fee_type,
t.untaxed_amount
from maochao_t0 t
)
,

maochao_t2 AS (
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    'GMV' AS metric,
    SUM(
      CASE
        WHEN t.fee_type = '收入金额' THEN NVL(t.untaxed_amount, 0)
        ELSE 0
      END
    )
    - SUM(
      CASE
        WHEN t.fee_type = '供应商承担优惠金额' THEN NVL(t.untaxed_amount, 0)
        ELSE 0
      END
    ) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type IN ('收入金额', '供应商承担优惠金额')
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    'GSV' AS metric,
    SUM(NVL(t.untaxed_amount, 0)) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type = '商品成本'
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    'Total CPP' AS metric,
    ABS(SUM(NVL(t.untaxed_amount, 0))) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type = 'Total CPP'
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    '平台费' AS metric,
    ABS(SUM(NVL(t.untaxed_amount, 0))) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type = '平台费'
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    'BMI-CPS' AS metric,
    ABS(SUM(NVL(t.untaxed_amount, 0))) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type IN ('百亿补贴佣金', '淘客U选返佣', '营销活动-淘客', '营销活动-淘客团长服务费')
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    'BMI-Livestream' AS metric,
    ABS(SUM(NVL(t.untaxed_amount, 0))) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type IN ('达播佣金', '店播佣金')
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group,
    'BMI-品牌新享' AS metric,
    ABS(SUM(NVL(t.untaxed_amount, 0))) AS value
  FROM
    maochao_t1 t
  WHERE
    t.fee_type = '品牌新享'
  GROUP BY
    t.mth,
    t.bu,
    --t.backend_product_code,
    t.category,
    t.brand,
    t.product_line_group

),
maochao_bill as (
  select
    t.mth bill_month,
    '' source_sku_code,
    '' sku_code,
    t.bu bu_code,
    t.bu bu_name,
    t.category category_code,
    t.category category_name,
    t.brand brand_code,
    t.brand brand_name,
    t.product_line_group product_line_group_code,
    t.product_line_group product_line_group_name,
    'TMALL' site_code,  -- 20261016 
    'TMALL' site_name,  -- 20261016 
    'TMALL SUPER - UL' source_store_name,
    'TMALL SUPER - UL' store_code,
    'TMALL SUPER - UL' store_name,
    m.fee_type_platform fee_type_platform,
    m.spending_type_fin spending_type_fin,
        -- 核心修改：根据 metric 动态选择倍率
    CASE 
        WHEN t.metric IN ('GMV', 'GSV') THEN t.value * 1.13
        ELSE t.value * 1.06 
    END amount_taxed,
    t.value amount_untaxed,
    now() + INTERVAL 8 HOURS dw_create_time,
    now() + INTERVAL 8 HOURS dw_last_update_time,
    now() + INTERVAL 8 HOURS etl_time
  from
    maochao_t2 t
      left join ${spark.var.catalog.dim}.fin.dim_platform_finance_spending_mapping m
        on m.platform_name = 'Tmall Super'
        and t.metric = m.fee_type_platform
)
select 
  *
FROM
  maochao_bill
  ;


-- COMMAND ----------

-- DBTITLE 1,tmp_pdd_bill_mi_bystore
-- PDD
create or replace table ${spark.var.catalog.tmp}.fin.tmp_pdd_bill_mi_bystore
with dim_product as (
select 
 division
,division_short
,category
,brand
,product_line_group 
,sku_code
from (
select 
division as division  
,division_short as division_short
,category_short as category
,cg_sub_brand as brand
,national_ex42 as product_line_group
,sku_code
,etl_date
,row_number() over(partition by sku_code order by etl_date desc) rn
from ${spark.var.catalog.dim}.cd.dim_product t
) a
where rn=1
),
pdd_t1 AS (
  SELECT
    t.mth,
    nvl(m.division, m2.division) bu,
    t.ul_sku_code,
    t.category,
    t.brand,
    t.product_line_group,
    SUM(NVL(t.gsv, 0)) AS gsv,
    SUM(NVL(t.gmv, 0)) AS gmv, -- 销售出库Gmv
    SUM(NVL(t.positive_reward_fee, 0)) AS positive_reward_fee, -- 好评有礼Gmv
    SUM(NVL(t.statistics_return_gsv, 0)) AS statistics_return_gsv, -- 退货GSV
    SUM(NVL(t.statistics_return_gmv, 0)) AS statistics_return_gmv -- 退货Gmv
  FROM
    ${spark.var.catalog.dws}.ddm.dws_pdd_bill_mi t
      left join dim_product m
        on t.ul_sku_code = m.sku_code
      left join 
      (select distinct division,division_short from dim_product dp) m2
        on t.bu = m2.division_short
  where
    t.product_name <> '历史订单'
    -- and LOWER(t.category) in ('hair','skin') --20260317注释，取消bu=B&W的限制。得到三个bu的数据。
  GROUP BY
    t.mth,
    nvl(m.division, m2.division),
    t.ul_sku_code,
    t.category,
    t.brand,
    t.product_line_group
),
pdd_t2 AS (
  SELECT
    t.mth,
    t.bu,
    t.ul_sku_code,
    t.category,
    t.brand,
    t.product_line_group,
    'GMV' AS metric,
    (t.gmv + t.positive_reward_fee + t.statistics_return_gmv)  AS taxed_value,
    (t.gmv + t.positive_reward_fee + t.statistics_return_gmv) / 1.13 AS untaxed_value
  FROM
    pdd_t1 t
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    t.ul_sku_code,
    t.category,
    t.brand,
    t.product_line_group,
    'GSV' AS metric, --此处不要改为Secondary GSV，标准名称会在dim表维护
    (t.gsv + t.statistics_return_gsv)  AS taxed_value,
    (t.gsv + t.statistics_return_gsv) / 1.13 AS untaxed_value
  FROM
    pdd_t1 t
  UNION ALL
  SELECT
    t.mth,
    t.bu,
    t.ul_sku_code,
    t.category,
    t.brand,
    t.product_line_group,
    'CPP' AS metric,
    ((t.gsv + t.statistics_return_gsv) - (t.gmv + t.positive_reward_fee + t.statistics_return_gmv))  AS taxed_value,
    ((t.gsv + t.statistics_return_gsv) - (t.gmv + t.positive_reward_fee + t.statistics_return_gmv)) /1.13  AS untaxed_value
  FROM
    pdd_t1 t

),
pdd_bill as (
  SELECT
    t.mth bill_month,
    t.ul_sku_code source_sku_code,
    t.ul_sku_code sku_code,
    t.bu bu_code,
    t.bu bu_name,
    t.category category_code,
    t.category category_name,
    t.brand brand_code,
    t.brand brand_name,
    t.product_line_group product_line_group_code,
    t.product_line_group product_line_group_name,
    'PDD' site_code,
    'PDD' site_name,
    'PDD - UL' source_store_name,
    'PDD - UL' store_code,
    'PDD - UL' store_name,
    m.fee_type_platform fee_type_platform,
    m.spending_type_fin spending_type_fin,
    t.taxed_value amount_taxed,
    t.untaxed_value  as amount_untaxed,
    now() + INTERVAL 8 HOURS as dw_create_time,
    now() + INTERVAL 8 HOURS as dw_last_update_time,
    now() + INTERVAL 8 HOURS as etl_time
  FROM
    pdd_t2 t
      left join ${spark.var.catalog.dim}.fin.dim_platform_finance_spending_mapping m
        on m.platform_name = 'PDD'
        and t.metric = m.fee_type_platform
)
select
  *
from
  pdd_bill
  ;

-- COMMAND ----------

-- DBTITLE 1,dws_ec_platform_bill_mi
--platform_bill dws
insert overwrite table ${spark.var.catalog.dws}.fin.dws_ec_platform_bill_mi
  select 
	bill_month
	,source_sku_code
	,sku_code
	,bu_code
	,bu_name
	,category_code
	,category_name
	,brand_code
	,brand_name
	,product_line_group_code
	,product_line_group_name
	,site_code
	,site_name
	,source_store_name
	,store_code
	,store_name
	,fee_type_platform
	,spending_type_fin
	,amount_taxed
	,amount_untaxed
	,dw_create_time
	,dw_last_update_time
	,etl_time
  from
    ${spark.var.catalog.tmp}.fin.tmp_tmall_super_bill_mi_bystore
  union all
  select
	bill_month
	,source_sku_code
	,sku_code
	,bu_code
	,bu_name
	,category_code
	,category_name
	,brand_code
	,brand_name
	,product_line_group_code
	,product_line_group_name
	,site_code
	,site_name
	,source_store_name
	,store_code
	,store_name
	,fee_type_platform
	,spending_type_fin
	,amount_taxed
	,amount_untaxed
	,dw_create_time
	,dw_last_update_time
	,etl_time
  from
    ${spark.var.catalog.tmp}.fin.tmp_pdd_bill_mi_bystore;

-- COMMAND ----------

-- DBTITLE 1,ads_ec_platform_bill_mi
--platform_bill ads
insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_ec_platform_bill_mi(
    month,
    bu_code,
    bu_name,
    category_code,
    category_name,
    brand_code,
    brand_name,
    product_line_group_code,
    product_line_group_name,
    business_type,
    site_code,
    site_name,
    store_code,
    store_name,
    spending_type_fin,
    amount_taxed,
    amount_untaxed,
    create_by,
    dw_create_time,
    dw_last_update_time,
    etl_time
)
  select
    REPLACE(bill_month,'-','') AS month,
    bu_code,
    bu_name,
    CASE WHEN UPPER(category_code) = 'HAIR-NEXXUS' THEN 'HAIR' ELSE UPPER(category_code) END AS category_code,
    CASE WHEN UPPER(category_name) = 'HAIR-NEXXUS' THEN 'HAIR' ELSE UPPER(category_name) END AS category_name,
    UPPER(brand_code) AS brand_code,
    UPPER(brand_name) AS brand_name,
    UPPER(product_line_group_code) AS product_line_group_code,
    UPPER(product_line_group_name) AS product_line_group_name,
    '2C' business_type,
    site_code,
    site_name,
    store_code,
    store_name,
    spending_type_fin,
    sum(amount_taxed) amount_taxed,
    sum(amount_untaxed) amount_untaxed,
    'Automatic' create_by,
    now() + INTERVAL 8 HOURS as dw_create_time,
    now() + INTERVAL 8 HOURS as dw_last_update_time,
    now() + INTERVAL 8 HOURS as etl_time
  from
    ${spark.var.catalog.dws}.fin.dws_ec_platform_bill_mi
  group by
    bill_month,
    bu_code,
    bu_name,
    category_code,
    category_name,
    brand_code,
    brand_name,
    product_line_group_code,
    product_line_group_name,
    site_code,
    site_name,
    store_code,
    store_name,
    spending_type_fin