# Databricks notebook source
# MAGIC %sql
# MAGIC  -- adb sql
# MAGIC -- **********************************************************************
# MAGIC -- dtc_bmi_spending_mf
# MAGIC -- v1.0 wu.bingling@unilever-china.com 2026-03-03
# MAGIC -- **********************************************************************
# MAGIC
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_dtc_bmi_spending_mf;
# MAGIC create table if not exists ${spark.var.catalog.ads}.fin_cpt.ads_dtc_bmi_spending_mf
# MAGIC (
# MAGIC 	 month            string comment '月份'
# MAGIC 	,bu_code          string COMMENT 'BU编码'
# MAGIC    ,bu_name          string COMMENT 'BU名称'
# MAGIC 	,store_code       string comment 'Store编码'
# MAGIC 	,store_name       string comment 'Store名称'     
# MAGIC    ,category_code    string COMMENT 'Category编码'
# MAGIC    ,category_name    string COMMENT 'Category名称'
# MAGIC    ,brand_code       string COMMENT '品牌编码'
# MAGIC    ,brand_name       string COMMENT '品牌名称'
# MAGIC    ,product_line_group_code   string COMMENT '产品线组编码'
# MAGIC    ,product_line_group        string COMMENT '产品线组名称'
# MAGIC    ,item_id                   string COMMENT '商品编码'
# MAGIC    ,item_name                 string COMMENT '商品名称'
# MAGIC    ,gmv_before_refund         decimal(38,8) comment 'GMV退前'
# MAGIC    ,gmv_after_refund          decimal(38,8) COMMENT 'GMV退后'
# MAGIC    ,cps_spending              decimal(38,8) COMMENT 'CPS 投放费用'
# MAGIC    ,cps_ratio                 decimal(38,8) COMMENT 'CPS 费用占比'
# MAGIC    ,source                    string COMMENT '来源'
# MAGIC 	,create_by                 string comment '创建人'
# MAGIC    ,dw_create_time            timestamp comment '创建时间'
# MAGIC    ,dw_last_update_time       timestamp comment '最后更新时间'
# MAGIC    ,dw_batch_num              bigint comment '批次号'
# MAGIC )
# MAGIC using delta
# MAGIC partitioned by (dt string comment '天分区')
# MAGIC comment 'ads_dtc_bmi_spending_mf,DTC BMI-ads结果表'
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_dtc_bmi_spending_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_dtc_bmi_spending_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'dtc_bmi_spending',
# MAGIC 'datasetname' = 'ads_dtc_bmi_spending'
# MAGIC );