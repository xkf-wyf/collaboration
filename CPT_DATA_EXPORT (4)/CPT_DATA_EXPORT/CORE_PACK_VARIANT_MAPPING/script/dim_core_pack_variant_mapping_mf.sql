-- Databricks notebook source
-- spark sql
-- **********************************************************************
-- 特殊香型的产品机制关系表 维度层
-- source: ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf
-- target: ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf
-- v1.0 haolong.wu@chiefclouds.com 2025-09-03
-- **********************************************************************
-- 参数设置
set spark.sql.sources.partitionOverwriteMode=dynamic;

-- 内容转大写
-- 剔除前后两头的空格
insert overwrite table ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf
select           
   upper(nvl(trim(category_sku_detail					 ), '')) as category					            
  ,upper(nvl(trim(brand_sku_detail						 ), '')) as brand						            
  ,upper(nvl(trim(product_line_group_detail		 ), '')) as product_line_group		   
  ,upper(nvl(trim(core_pack_group_detail			 ), '')) as source_core_pack			            
  ,upper(nvl(trim(variant_sap					         ), '')) as variant_sap					                    
  ,upper(nvl(trim(variant_csp					         ), '')) as variant_csp					           
  ,upper(nvl(trim(target_core_pack_group_detail), '')) as target_core_pack   
  ,'Automatic'                                                                                  as create_by
  ,date_format(from_utc_timestamp(current_timestamp,'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss')    as etl_date
from ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf
where dt = '$dt'
;
