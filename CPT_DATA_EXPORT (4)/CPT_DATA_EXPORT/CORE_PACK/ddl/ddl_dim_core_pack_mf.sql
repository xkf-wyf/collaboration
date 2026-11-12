-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- Core Pack Group Master Data接口
-- v1.0 haolong.wu@chiefclouds.com 2025-06-30
-- 描述：每月第4个工作日回传最新Core Pack Group Master Data
-- **********************************************************************

drop table if exists ${spark.var.catalog.dim}.fin.dim_core_pack_mf;
create table if not exists ${spark.var.catalog.dim}.fin.dim_core_pack_mf
(
		bu_code                		string comment '业务单元编码'			
		,bu_name_en             	string comment '业务单元英文名称'		
		,category_code          	string comment '品类编码'		
		,category_name_en       	string comment '品类名称英文'		
		,subbrand_code          	string comment '子品牌编码'		
		,subbrand_name          	string comment '子品牌名称'		
		,product_line_group_code	string comment '产品线组编码'		
		,product_line_group     	string comment '产品线组'		
		,core_pack_group_code   	string comment 'CORE_PACK_GROUP编码'
		,core_pack_group		      string comment 'CORE_PACK_GROUP'
		,create_by                 string comment '创建人'
		,dw_create_time            timestamp comment '创建时间'
		,dw_last_update_time       timestamp comment '最后更新时间'
		,dw_batch_num              bigint comment '批次号'
)
using delta
partitioned by (dt string comment '天分区')
comment 'Core Pack Group Master Data'
;

alter table ${spark.var.catalog.dim}.fin.dim_core_pack_mf set owner to `${spark.var.table.owner}`;

alter table ${spark.var.catalog.dim}.fin.dim_core_pack_mf
set TAGS (
'project' = 'CPT',
'datasetgroupname' = 'core_pack',
'datasetname' = 'dim_core_pack'
);
