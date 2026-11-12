-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- 二级GSV、GMV-Order Time接口
-- v1.0 jin.zhen@chiefclouds.com 2025-06-26
-- 描述：每月第4个工作日回传M-1月二级GSV、GMV
-- **********************************************************************

drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_secondary_gsv_gmv_mf;
create table if not exists ${spark.var.catalog.ads}.fin_cpt.ads_secondary_gsv_gmv_mf
(
	 month                   string	comment '月份'
    ,bu_code string COMMENT 'BU编码'
    ,bu_name string COMMENT 'BU名称'
    ,customer_type_code string COMMENT 'Channel编码'
    ,customer_type string COMMENT 'Channel名称'
    ,site_code string COMMENT 'Site编码'
    ,site_name string COMMENT 'Site名称'
    ,sales_type string COMMENT '销售类型'
	,store_code              string	comment 'Store编码' 
	,store_name              string	comment 'Store名称'
    ,category_code string COMMENT 'Category编码'
    ,category_name string COMMENT 'Category名称'
    ,brand_code string COMMENT 'Brand编码'
    ,brand_name string COMMENT 'Brand名称'
    ,product_line_group_code string COMMENT '品线编码'
    ,product_line_group string COMMENT '品线名称'
	,core_pack_group_code    string	comment 'Core_Pack_Group编码'
  	,core_pack_group         string	comment 'Core_Pack_Group名称'
	,item_group_code         string	comment '产品机制编码'
	,item_group_name         string	comment '产品机制名称'
	,secondary_gmv_amount    decimal(38,2)	comment '二级GMVAmount（含税）'
	,secondary_gsv_amount    decimal(38,2)	comment '二级GSVAmount(未税）'
    ,create_by                 string comment '创建人'
    ,dw_create_time            timestamp comment '创建时间'
    ,dw_last_update_time       timestamp comment '最后更新时间'
    ,dw_batch_num              bigint comment '批次号'
)
using delta
partitioned by (dt string comment '天分区')
comment 'ads_secondary_gsv_gmv_mf'
;

alter table ${spark.var.catalog.ads}.fin_cpt.ads_secondary_gsv_gmv_mf set owner to `${spark.var.table.owner}`;
