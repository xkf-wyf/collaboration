-- Databricks notebook source
-- dst 20260904  去掉 tmall super和tmall super -ul合并成tmall super -ul 的逻辑

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import re
-- MAGIC
-- MAGIC def format_packsize_stock(expression):
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
-- MAGIC spark.udf.register("format_packsize_stock", format_packsize_stock, StringType())
-- MAGIC

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("start_mth", "2026-01")
-- MAGIC dbutils.widgets.text("end_mth", "2026-02")
-- MAGIC dbutils.widgets.text("dt", "2026-03-18")

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dim}.ddm.dim_sku_pack_size
-- source table: ${spark.var.catalog.dim}.ddm.dim_store
-- source table: ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf
-- source table: ${spark.var.catalog.ads}.cd_bi.ads_omni_base
-- source table: ${spark.var.catalog.dim}.cd.dim_product
-- target table: ${spark.var.catalog.ads}.fin_cpt.ads_omni_stock_mf 
-- Description:   
-- v1.0 jin.zhen@chiefclouds.com   2025-06-11   创建
-- v1.1 haolong.wu@chiefclouds.com 2025-12-04   PDD - VSL切DTC后冗余一份机制打标
-- v2.1 iris.lin 2026-04-24修改,store_name的取值需要从原来的national_ex4换成national_ex25,site_name的取值从原来的national_ex3换成national_ex4
-- v2.2 iris.lin 2026-05-09修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex4(site)作为store_name
-- v2.3 iris.lin 2026-05-12修改,需要剔除PC的特殊香型,core_pack_group = 'PW LUX LUX CORE SC 550 LOVE FOREVER' 
-- v2.4 iris.lin 2026-05-13修改,当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name,site_name的取值需要取national_ex3
-- 逻辑描述：
--    1、接口文件名： cpt_omni_gsv_yyyymm.csv
--    2、每月第4个工作日回传M-1月一级GSV
-- v1.1 jin.zhen@chiefclouds.com 2025/06/11
-- 逻辑描述：
--    1、新增字段：variant（香型）
--    2、调整core_pack_group字段 取数逻辑
-- v1.2 wu.bingling@unilever-china.com 2026/02/06
-- 逻辑描述：
--    1、新增字段：BU_CODE（BU编码）、BU_NAME（BU名称）、CUSTOMER_TYPE_CODE（Channel编码）、CUSTOMER_TYPE（Channel名称）、SITE_CODE（Site编码）、SITE_NAME（Site名称）、CATEGORY_CODE（Category编码）、CATEGORY_NAME（Category名称）、BRAND_CODE（Brand编码）、BRAND_NAME（Brand名称）、PRODUCT_LINE_GROUP_CODE（品线编码）、PRODUCT_LINE_GROUP（品线名称）
--    2、调整initial_stock字段取数逻辑
--    3、PC取机制时不匹配特殊香型


-- 机制表过滤 ： 过滤掉手工表中已经映射的core_pack_group
create or replace table ${spark.var.catalog.tmp}.fin.tmp_omni_stock_mf_zj as
select
	distinct 
-- core_pack_group
  CASE 
        WHEN core_pack_group = 'PW LUX LUX CORE SC 550 LOVE FOREVER' 
        THEN 'PW LUX LUX CORE SC 550'
        ELSE core_pack_group
    END as core_pack_group
	,concat(category_sku,brand_sku,product_line_group,format_packsize_stock(nvl(main_pack,'')) )  as core_new
	,b.customer  as store_name
from ${spark.var.catalog.dim}.ddm.dim_sku_pack_size a
left join 
(
    select  distinct upper(trim(customer)) as customer,shop_id,shop_name
    from ${spark.var.catalog.dim}.ddm.dim_store
    where status = 1  and shop_id <> ''
		union
		select 'PDD - VSL','621699362','Vaseline凡士林官方旗舰店'    -- PDD - VSL切DTC后冗余一份机制打标
) b
	on nvl(a.shop_id,'') = nvl(b.shop_id,'')
where not exists (
  select 1 from ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf c 
  where contains(a.core_pack_group,c.target_core_pack)           -- 模糊匹配
)
and end_time = '9999-12-31'
and a.channel <> 'DOUYIN'
;
alter table ${spark.var.catalog.tmp}.fin.tmp_omni_stock_mf_zj set owner to `${spark.var.table.owner}`;

-- 先匹配普通香型
create or replace table ${spark.var.catalog.tmp}.fin.tmp_omni_stock_mf as
select 	replace(a.mth,'-','' )    as month
	  ,b.division						     	  as bu_name
	  ,c.customer_type
	  ,c.site_name
	  ,b.category_short						  as category_name
	  ,b.cg_sub_brand						    as brand_name
	  ,b.national_ex42						  as product_line_group
    ,c.store_name                 as store_name
    ,d.core_pack_group            as core_pack_group
	  ,a.initial_stock
	  ,b.division_short						  as bu
	  ,b.variant                    as variant             --香型
	  ,concat_ws(' ',b.category_short,b.cg_sub_brand,b.national_ex42
		,format_packsize_stock(nvl(b.national_ex44,'')))  as source_core_pack
	  ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss')	as etl_time
from (
		select 	mth,sku_code,store_code
				,sum(theory_stock*1000) as initial_stock            -- 原来是千元
		from 	${spark.var.catalog.ads}.cd_bi.ads_omni_base_monthly_fix_mf
		where 	mth between '$start_mth' and '$end_mth'
				and ul_day = last_day(ul_day)
				and sales_type = '2C'
		group by mth,sku_code,store_code
	) a
left join ${spark.var.catalog.dim}.cd.dim_product b on b.is_current = 1 and a.sku_code = b.sku_code
left join (
		select 	store_code 
		-- ,max(national_ex25)  as store_name
		--2026-05-13修改，当national_ex1=ONLINE，则取ex25(store)为store_name,national_ex1=OFFLINE,OTHERS,则取ex3(site)作为store_name
		,case when max(national_ex1)='ONLINE' then max(national_ex25) else max(national_ex3) end as  store_name  
		,max(national_ex2)  as customer_type
		,max(national_ex3)  as site_name
		from 	${spark.var.catalog.dim}.cd.dim_store
    where national_ex9 != ''      --2026-08 Store_name不唯一增加相关过滤条件
		group by store_code
	) c on a.store_code = c.store_code
left join ${spark.var.catalog.tmp}.fin.tmp_omni_stock_mf_zj d
    on concat(b.category_short, b.cg_sub_brand,b.national_ex42,format_packsize_stock(nvl(b.national_ex44,''))) = d.core_new
		and c.store_name = d.store_name
;
alter table ${spark.var.catalog.tmp}.fin.tmp_omni_stock_mf set owner to `${spark.var.table.owner}`;


-- 再匹配特殊香型
-- 入库
set spark.sql.sources.partitionOverwriteMode=dynamic;

INSERT OVERWRITE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_omni_stock_mf  PARTITION(dt)
(
  month,                -- 月份
  bu_code,              -- 业务单元编码
  bu_name,              -- 业务单元名称
  customer_type_code,   -- 客户类型编码
  customer_type,        -- 客户类型名称
  site_code,            -- 站点编码
  site_name,            -- 站点名称
  store_code,           -- 门店编码
  store_name,           -- 门店名称
  category_code,        -- 品类编码
  category_name,        -- 品类名称
  brand_code,           -- 品牌编码
  brand_name,           -- 品牌名称
  product_line_group_code, -- 产品线组编码
  product_line_group,   -- 产品线组名称
  core_pack_group_code, -- 核心包装组编码
  core_pack_group,      -- 核心包装组名称
  initial_stock,        -- 期初库存总量
  create_by,
  dw_create_time,
  dw_last_update_time,
  dw_batch_num,
  dt 
)
SELECT
  a.month,
  ''                                      AS bu_code,
  a.bu_name,
  ''                                      AS customer_type_code,
  a.customer_type,
  ''                                      AS site_code,
  a.site_name,
  ''                                      AS store_code,
  case  when a.store_name='JD - REGENERATE' then 'JD - UL'  else a.store_name end as store_name,  -- 20260904
  ''                                      AS category_code,
  a.category_name,
  ''                                      AS brand_code,
  a.brand_name,
  ''                                      AS product_line_group_code,
  a.product_line_group,
  ''                                      AS core_pack_group_code,
  -- 核心包装组逻辑：PC业务用原字段，其他业务取映射值（无则用原字段）
  CASE 
    WHEN a.bu = 'PC' THEN a.core_pack_group 
    ELSE NVL(b.target_core_pack, a.core_pack_group)  
  END AS core_pack_group,
  SUM(initial_stock)                        AS initial_stock,
  'Automatic'                               AS create_by,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time,
    cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num,
    '$dt'                                                             as dt
FROM ${spark.var.catalog.tmp}.fin.tmp_omni_stock_mf a 
LEFT JOIN ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf b 
  ON a.source_core_pack = b.source_core_pack 
  AND a.variant = b.variant_sap
GROUP BY 
  month,
  a.bu,
  a.bu_name,
  a.customer_type,
  a.site_name,
  a.category_name,
  a.brand_name,
  a.product_line_group,
  case when a.store_name='JD - REGENERATE' then 'JD - UL'  else a.store_name end, -- 20260904
  a.core_pack_group,
  CASE 
    WHEN a.bu = 'PC' THEN a.core_pack_group 
    ELSE NVL(b.target_core_pack, a.core_pack_group)  
  END
;