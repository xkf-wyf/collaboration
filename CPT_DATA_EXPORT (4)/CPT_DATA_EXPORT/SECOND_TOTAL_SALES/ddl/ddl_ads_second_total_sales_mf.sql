-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- 二级GMV Total-Order Time接口
-- v1.1 wu.bingling@unilever-china.com 2026-02-12
-- 描述：重建ads_second_total_sales_mf表
-- **********************************************************************

drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_second_total_sales_mf;
create table if not exists ${spark.var.catalog.ads}.fin_cpt.ads_second_total_sales_mf
(
	month						string comment '月份'
    ,bu_code                    string comment 'BU编码'
    ,bu_name                    string comment 'BU名称'
    ,customer_type_code         string comment 'Channel编码'
    ,customer_type              string comment 'Channel名称'
    ,site_code                  string comment 'Site编码'
    ,site_name                  string comment 'Site名称'
    ,sales_type                 string comment '销售类型' 
    ,store_code				        	string comment 'Store编码'
    ,store_name			        		string comment 'Store名称'
    ,category_code	      			string comment '品类编码'
    ,category_name		      		string comment '品类名称'
    ,brand_code		        			string comment '品牌编码'
    ,brand_name		        			string comment '品牌名称'
    ,product_line_group_code   	string comment '产品线组编码'
    ,product_line_group			    string comment '产品线组名称'
    ,secondary_after_gmv_amount decimal(38,6) comment '二级GMVAmount（含税）-退后(元)'
    ,secondary_gmv_amount 	  	decimal(38,6) comment '二级GMVAmount（含税）-退前(元)'
    ,create_by                	string comment '创建人'
    ,dw_create_time             timestamp comment '创建时间'
    ,dw_last_update_time        timestamp comment '最后更新时间'
    ,dw_batch_num               bigint comment '批次号'
)
using delta
partitioned by (dt string comment '天分区')
comment '二级GMV Total ads结果表'
;

alter table ${spark.var.catalog.ads}.fin_cpt.ads_second_total_sales_mf set owner to `${spark.var.table.owner}`;



alter table ${spark.var.catalog.ads}.fin_cpt.ads_second_total_sales_mf
set TAGS (
'project' = 'CPT',
'datasetgroupname' = 'SecondarySales',
'datasetname' = 'SecondarySales'
);