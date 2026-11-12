-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- Customer Hierachy-Order Time接口
-- v1.0 jin.zhen@chiefclouds.com 2025-06-26
-- 描述：每月第4个工作日回传最新Customer Hierachy
-- **********************************************************************

drop table if exists ${spark.var.catalog.dim}.fin.dim_customer_2c_mf;
create table if not exists ${spark.var.catalog.dim}.fin.dim_customer_2c_mf
(
	  bu_code               string comment 'BU编码'
	 ,bu_name               string comment 'BU名称'
	 ,customer_type_code    string comment '客户类型编码'
	 ,customer_type         string comment '客户类型'
	 ,site_code             string comment 'Site编码'
	 ,site_name_en          string comment 'Site英文名称'
	 ,site_name_cn          string comment 'Site中文名称'
	 ,store_code            string comment 'Store编码'
	 ,store_name            string comment 'Store名称'
	 ,store_desc            string comment 'Store中文名称'
	 ,soldto_code           string comment 'Soldto编码'
	 ,soldto_name           string comment 'Soldto名称'
	 ,on_offline            string comment '线上/线下'
	 ,is_active             string comment '状态'
	 ,key_cust1_cd          string comment 'KEY_CUST1_CD'
	 ,key_cust1_name        string comment 'KEY_CUST1_NAME'
	 ,key_cust2_cd          string comment 'KEY_CUST2_CD'
	 ,key_cust2_name        string comment 'KEY_CUST2_NAME'
	 ,key_cust3_cd          string comment 'KEY_CUST3_CD'
	 ,key_cust3_name        string comment 'KEY_CUST3_NAME'
	 ,key_cust4_cd          string comment 'KEY_CUST4_CD'
	 ,key_cust4_name        string comment 'KEY_CUST4_NAME'
	 ,key_cust5_cd          string comment 'KEY_CUST5_CD'
	 ,key_cust5_name        string comment 'KEY_CUST5_NAME'
	 ,key_cust6_cd          string comment 'KEY_CUST6_CD'
	 ,key_cust6_name        string comment 'KEY_CUST6_NAME'
	 ,create_by             string comment '创建人'
	 ,create_time           string comment '创建时间'
)
using delta
partitioned by (dt string comment '天分区')
comment 'Customer Hierachy'
;

alter table ${spark.var.catalog.dim}.fin.dim_customer_2c_mf set owner to `${spark.var.table.owner}`;