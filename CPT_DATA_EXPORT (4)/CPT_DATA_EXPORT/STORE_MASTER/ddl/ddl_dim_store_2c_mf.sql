-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- Store Master Data-Order Time接口
-- v1.0 jin.zhen@chiefclouds.com 2025-06-26
-- 描述：每月第4个工作日回传最新Store Master Data
-- **********************************************************************

drop table if exists ${spark.var.catalog.dim}.fin.dim_store_2c_mf;
create table if not exists ${spark.var.catalog.dim}.fin.dim_store_2c_mf
(
	  customer_type_code  string comment '客户类型编码'
	 ,customer_type       string comment '客户类型名称'
	 ,on_offline          string comment '线上/线下'
	 ,site_code           string comment 'Site编码'
	 ,site_name           string comment 'Site名称'
	 ,store_code          string comment 'Store编码'
	 ,store_name          string comment 'Store名称'
	 ,create_by						string comment '创建人'							
	 ,create_time					string comment '创建时间'	
)
using delta
partitioned by (dt string comment '天分区')
comment 'Store Master'
;

alter table ${spark.var.catalog.dim}.fin.dim_store_2c_mf set owner to `${spark.var.table.owner}`;