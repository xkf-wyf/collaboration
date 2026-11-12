-- Databricks notebook source
 -- adb sql
-- **********************************************************************
-- Product Hierarchy-Order Time接口
-- v1.0 jin.zhen@chiefclouds.com 2025-06-26
-- 描述：每月第4个工作日回传最新Product Hierarchy
-- **********************************************************************

drop table if exists ${spark.var.catalog.dim}.fin.dim_product_2c_mf;
create table if not exists ${spark.var.catalog.dim}.fin.dim_product_2c_mf
(
	  product_code                  string comment '产品代码'
	 ,product_name_cn              string comment '产品中文名称'
	 ,product_name_en              string comment '产品英文名称'
	 ,global_l1_divisioncode       string comment 'GLOBAL_L1_DIVISIONCODE'
	 ,global_l1_divisionname       string comment 'GLOBAL_L1_DIVISIONNAME'
	 ,global_l2_subdivisioncode    string comment 'GLOBAL_L2_SUBDIVISIONCOD'
	 ,global_l2_subdivisionname    string comment 'GLOBAL_L2_SUBDIVISIONNAM'
	 ,global_l3_categorycode       string comment 'GLOBAL_L3_CATEGORYCODE'
	 ,global_l3_categoryname       string comment 'GLOBAL_L3_CATEGORYNAME'
	 ,global_l4_marketcode         string comment 'GLOBAL_L4_MARKETCODE'
	 ,global_l4_marketname         string comment 'GLOBAL_L4_MARKETNAME'
	 ,global_l5_corpbrandcode      string comment 'GLOBAL_L5_CORPBRANDCODE'
	 ,global_l5_corpbrandname      string comment 'GLOBAL_L5_CORPBRANDNAME'
	 ,global_l6_sectorcode         string comment 'GLOBAL_L6_SECTORCODE'
	 ,global_l6_sectorname         string comment 'GLOBAL_L6_SECTORNAME'
	 ,global_l7_corpprogcode       string comment 'GLOBAL_L7_CORPPROGCODE'
	 ,global_l7_corpprogname       string comment 'GLOBAL_L7_CORPPROGNAME'
	 ,global_l8_subbrand_code      string comment 'GLOBAL_L8_SUBBRAND_CODE'
	 ,global_l8_subbrand_name      string comment 'GLOBAL_L8_SUBBRAND_NAME'
	 ,global_l9_pack_code          string comment 'GLOBAL_L9_PACK_CODE'
	 ,global_l9_pack_name          string comment 'GLOBAL_L9_PACK_NAME'
	 ,state                        string comment '产品状态'
	 ,bu_code                      string comment '业务单元编码'
	 ,bu_name_en                   string comment '业务单元英文名称'
	 ,bu_abbrname                  string comment '业务单元缩写'
	 ,bu_name_cn                   string comment '业务单元中文名称'
	 ,category_code                string comment '品类编码'
	 ,category_name_en             string comment '品类名称英文'
	 ,category_abbrname            string comment '品类名称缩写'
	 ,category_name_cn             string comment '品类名称中文'
	 ,subcategory_code             string comment '子品类编码'
	 ,subcategory_name_en          string comment '子品类名称英文'
	 ,subcategory_name_cn          string comment '子品类名称中文'
	 ,brand_code                   string comment '品牌编码'
	 ,brand_name_en                string comment '品牌名称英文'
	 ,brand_name_cn                string comment '品牌名称中文'
	 ,subbrand_code                string comment '子品牌编码'
	 ,subbrand_name                string comment '子品牌名称'
	 ,product_line_group_code      string comment '产品线组编码'
	 ,product_line_group           string comment '产品线组'
	 ,packsize                     string comment '规格'
	 ,core_pack_group_code         string comment 'CORE_PACK_GROUP编码'
	 ,core_pack_group              string comment 'CORE_PACK_GROUP名称'
	 ,aroma_type                   string comment '香型'
	 ,box_dimension                string comment '箱规单位中文'
	 ,minimum_saleable_unit        string comment '最小可售单位'
	 ,product_type                 string comment '产品类别'
	 ,net_weight                   string comment '净重'
	 ,create_by                    string comment '创建人'
	 ,create_time                  string comment '创建时间'
)
using delta
partitioned by (dt string comment '天分区')
comment 'Product Hierarchy'
;

alter table ${spark.var.catalog.dim}.fin.dim_product_2c_mf set owner to `${spark.var.table.owner}`;