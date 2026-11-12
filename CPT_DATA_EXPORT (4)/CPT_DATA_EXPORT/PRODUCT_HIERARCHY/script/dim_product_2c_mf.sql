-- Databricks notebook source
-- MAGIC %python
-- MAGIC dbutils.widgets.text('dt','2026-03-13','月份')

-- COMMAND ----------

-- adb sql
-- **********************************************************************
-- source table: ${spark.var.catalog.dim}.cd.dim_product	产品主数据
-- target table:  ${spark.var.catalog.dim}.fin.dim_product_2c_mf 最终报告表
-- Description:   
-- v1.0 jin.zhen@chiefclouds.com 2025/06/26
-- 逻辑描述：
--    1、接口文件名： cpt_product_hierarchy_yyyymm.csv
--    2、取产品主数据 is_current=1
--    3、每月第4个工作日回传最新Product Hierarchy

set spark.sql.sources.partitionOverwriteMode=dynamic;

insert overwrite table ${spark.var.catalog.dim}.fin.dim_product_2c_mf partition(dt)
(
  product_code
  ,product_name_cn
  ,product_name_en
  ,global_l1_divisioncode
  ,global_l1_divisionname
  ,global_l2_subdivisioncode
  ,global_l2_subdivisionname
  ,global_l3_categorycode
  ,global_l3_categoryname
  ,global_l4_marketcode
  ,global_l4_marketname
  ,global_l5_corpbrandcode
  ,global_l5_corpbrandname
  ,global_l6_sectorcode
  ,global_l6_sectorname
  ,global_l7_corpprogcode
  ,global_l7_corpprogname
  ,global_l8_subbrand_code
  ,global_l8_subbrand_name
  ,global_l9_pack_code
  ,global_l9_pack_name
  ,state
  ,bu_code
  ,bu_name_en
  ,bu_abbrname
  ,bu_name_cn
  ,category_code
  ,category_name_en
  ,category_abbrname
  ,category_name_cn
  ,subcategory_code
  ,subcategory_name_en
  ,subcategory_name_cn
  ,brand_code
  ,brand_name_en
  ,brand_name_cn
  ,subbrand_code
  ,subbrand_name
  ,product_line_group_code
  ,product_line_group
  ,packsize
  ,core_pack_group_code
  ,core_pack_group
  ,aroma_type
  ,box_dimension
  ,minimum_saleable_unit
  ,product_type
  ,net_weight
  ,create_by
  ,create_time
  ,dt
)
select 
	distinct
	 a.sku_code                      as product_code
	 ,a.sku_name_cn                  as product_name_cn
	 ,a.sku_name_en                  as product_name_en
	 ,a.global_l1_divisioncode       as global_l1_divisioncode
	 ,a.global_l1_divisionname       as global_l1_divisionname
	 ,a.global_l2_subdivisioncode    as global_l2_subdivisioncode
	 ,a.global_l2_subdivisionname    as global_l2_subdivisionname
	 ,a.global_l3_categorycode       as global_l3_categorycode
	 ,a.global_l3_categoryname       as global_l3_categoryname
	 ,a.global_l4_marketcode         as global_l4_marketcode
	 ,a.global_l4_marketname         as global_l4_marketname
	 ,a.global_l5_corpbrandcode      as global_l5_corpbrandcode
	 ,a.global_l5_corpbrandname      as global_l5_corpbrandname
	 ,a.global_l6_sectorcode         as global_l6_sectorcode
	 ,a.global_l6_sectorname         as global_l6_sectorname
	 ,a.global_l7_corpprogcode       as global_l7_corpprogcode
	 ,a.global_l7_corpprogname       as global_l7_corpprogname
	 ,a.global_l8_subbrand_code      as global_l8_subbrand_code
	 ,a.global_l8_subbrand_name      as global_l8_subbrand_name
	 ,a.global_l9_pack_code          as global_l9_pack_code
	 ,a.global_l9_pack_name          as global_l9_pack_name
	 ,case when a.is_active = 10 then '在售不产'
	 			 when a.is_active = 3  then '在产在售'
				 when a.is_active = 6  then '不产不售-0库存'
				 when a.is_active = 11 then '不产不售-有库存'
				 when a.is_active = 5  then '新品'
			else '' end                  as state
	 ,''                             as bu_code
	 ,a.division                     as bu_name_en
	 ,a.division_short               as bu_abbrname
	 ,''                             as bu_name_cn
	 ,''                             as category_code
	 ,a.category                     as category_name_en
	 ,a.category_short               as category_abbrname
	 ,a.category_cn                  as category_name_cn
	 ,''                             as subcategory_code
	 ,a.sub_category                 as subcategory_name_en
	 ,a.sub_category_cn              as subcategory_name_cn
	 ,''                             as brand_code
	 ,a.cg_sub_brand                 as brand_name_en
	 ,a.brand_cn                     as brand_name_cn
	 ,''                             as subbrand_code
	 ,a.sub_brand                    as subbrand_name
	 ,''                             as product_line_group_code
	 ,a.national_ex42                as product_line_group
	 ,a.national_ex41                as packsize
	 ,''                             as core_pack_group_code
	 ,''                             as core_pack_group
	 ,a.variant                      as aroma_type
	 ,a.base_uom_cn                  as box_dimension
	 ,a.min_unit                     as minimum_saleable_unit
	 ,a.matl_grp_cn                  as product_type
	 ,a.national_ex39                as net_weight
   ,'Automatic'                    as create_by
   ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as create_time
   ,'$dt'                            as dt
from ${spark.var.catalog.dim}.cd.dim_product a 
where a.is_current = 1
;