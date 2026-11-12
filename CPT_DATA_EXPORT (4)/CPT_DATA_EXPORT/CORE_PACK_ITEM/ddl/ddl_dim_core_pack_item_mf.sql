-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- 产品机制接口
-- v1.0 haolong.wu@chiefclouds.com 2025-06-30
-- 描述：每月第4个工作日回传最新产品机制
-- **********************************************************************

drop table if exists ${spark.var.catalog.dim}.fin.dim_core_pack_item_mf;
create table if not exists ${spark.var.catalog.dim}.fin.dim_core_pack_item_mf
(
			bu_code STRING COMMENT 'BU编码'
		,bu_name STRING COMMENT 'BU名称'
		,customer_type_code STRING COMMENT 'Channel编码'
		,customer_type STRING COMMENT 'Channel名称'
		,site_code STRING COMMENT 'Site编码'
		,site_name STRING COMMENT 'Site名称'
		,category_code STRING COMMENT 'Category编码'
		,category_name STRING COMMENT 'Category名称'
		,brand_code STRING COMMENT 'Brand编码'
		,brand_name STRING COMMENT 'Brand名称'
		,product_line_group_code STRING COMMENT '品线编码'
		,product_line_group STRING COMMENT '品线名称'	
		,store_code								string comment 'Store编码'														
		,store_name								string comment 'Store名称'							
		,core_pack_group_code			string comment 'Core_Pack_Group编码'												
		,core_pack_group					string comment 'Core_Pack_Group名称'										
		,item_group_code					string comment '产品机制编码'										
		,item_group_name					string comment '产品机制名称'										
		,is_main_product					string comment '是否主品'										
		,main_product_code				string comment '主品编码'											
		,main_product_name				string comment '主品名称'											
		,sample_code							string comment '小样编码'								
		,sample_name							string comment '小样名称'								
		,quantity									decimal(38,8) comment '数量'				
		,list_price								decimal(38,2) comment '产品价格'
		,pack_list_price					decimal(38,8) comment '产品机制价格'						
   ,create_by                 string comment '创建人'
   ,dw_create_time            timestamp comment '创建时间'
   ,dw_last_update_time       timestamp comment '最后更新时间'
   ,dw_batch_num              bigint comment '批次号'
)
using delta
partitioned by (dt string comment '天分区')
comment '产品机制'
;

alter table ${spark.var.catalog.dim}.fin.dim_core_pack_item_mf set owner to `${spark.var.table.owner}`;