-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- 一级GSV-Order Time接口
-- v2.0 xi.lin 20260203
-- 描述：每月第5日回传M-1月期初理论库存
-- **********************************************************************

drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_omni_gsv_mf;
create table if not exists ${spark.var.catalog.ads}.fin_cpt.ads_omni_gsv_mf
(
 month                     string comment '月份'
,bu_code                  string comment 'BU编码'
,bu_name                  string comment 'BU名称'
,customer_type_code       string comment 'Channel编码'
,customer_type            string comment 'Channel名称'
,site_code                string comment 'Site编码'
,site_name                string comment 'Site名称'
,store_code                string comment 'Store编码'
,store_name                string comment 'Store名称'
,category_code             string comment '品类编码'
,category_name             string comment '品类名称'
,brand_code                string comment '品牌编码'
,brand_name                string comment '品牌名称'
,product_line_group_code   string comment '产品线组编码'
,product_line_group        string comment '产品线组名称'
,primary_gsv_amount        decimal(38,6) comment '一级GSV Amount'
   ,create_by                 string comment '创建人'
   ,dw_create_time            timestamp comment '创建时间'
   ,dw_last_update_time       timestamp comment '最后更新时间'
   ,dw_batch_num              bigint comment '批次号'
)
using delta
partitioned by (dt string comment '天分区')
comment 'ads_omni_gsv_mf'
;

alter table ${spark.var.catalog.ads}.fin_cpt.ads_omni_gsv_mf set owner to `${spark.var.table.owner}`;