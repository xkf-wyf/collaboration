-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- 特殊香型的产品机制关系表 接入层
-- v1.0 haolong.wu@chiefclouds.com 2025-09-03
-- **********************************************************************
drop table if exists ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf;
create table if not exists ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf
(
		 category_sku_detail								string comment '品类'														
		,brand_sku_detail								    string comment '品牌'							
		,product_line_group_detail			    string comment '品线组'												
		,core_pack_group_detail					    string comment 'Core_Pack明细'										
		,variant_sap					              string comment 'SAP香型'										
		,variant_csp					              string comment 'CSP子定义香型'										
		,target_core_pack_group_detail			string comment '目标Core_Pack明细'										
		,create_by								          string comment '创建人'							
		,create_time							          string comment '创建时间'								
)
using delta
partitioned by (dt string comment '天分区')
comment '特殊香型的产品机制关系表 接入层'
;

alter table ${spark.var.catalog.ods}.int_manual.ods_core_pack_variant_mapping_mf set owner to `${spark.var.table.owner}`;

-- COMMAND ----------

 -- adb sql
-- **********************************************************************
-- 特殊香型的产品机制关系表 维度层
-- v1.0 haolong.wu@chiefclouds.com 2025-09-03
-- **********************************************************************
drop table if exists ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf;
create table if not exists ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf
(
		 category														string comment '品类'														
		,brand								    					string comment '品牌'							
		,product_line_group			    				string comment '品线组'												
		,source_core_pack					    			string comment '源Core_Pack'										
		,variant_sap					              string comment 'SAP香型'										
		,variant_csp					              string comment 'CSP子定义香型'										
		,target_core_pack										string comment '目标Core_Pack'										
		,create_by								          string comment '创建人'							
		,create_time							          string comment '创建时间'								
)
using delta
comment '特殊香型的产品机制关系表 维度层'
;

alter table ${spark.var.catalog.dim}.fin.dim_core_pack_variant_mapping_mf set owner to `${spark.var.table.owner}`;
