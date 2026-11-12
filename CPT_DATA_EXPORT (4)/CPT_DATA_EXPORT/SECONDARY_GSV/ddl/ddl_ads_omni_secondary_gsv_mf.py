# Databricks notebook source
# MAGIC %sql
# MAGIC -- 描述：每月第4个工作日回传M-1月二级GSV
# MAGIC -- **********************************************************************
# MAGIC
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_omni_secondary_gsv_mf;
# MAGIC create table if not exists ${spark.var.catalog.ads}.fin_cpt.ads_omni_secondary_gsv_mf
# MAGIC (
# MAGIC  month                     string comment '月份'
# MAGIC ,bu_code                   string comment 'BU编码'
# MAGIC ,bu_name                   string comment 'BU名称'
# MAGIC ,customer_type_code        string comment 'Channel编码'
# MAGIC ,customer_type             string comment 'Channel名称'
# MAGIC ,site_code                 string comment 'Site编码'
# MAGIC ,site_name                 string comment 'Site名称'
# MAGIC ,sales_type                string comment '销售类型（如 2C/2B）' 
# MAGIC ,store_code                string comment 'Store编码'
# MAGIC ,store_name                string comment 'Store名称'
# MAGIC ,category_code             string comment '品类编码'
# MAGIC ,category_name             string comment '品类名称'
# MAGIC ,brand_code                string comment '品牌编码'
# MAGIC ,brand_name                string comment '品牌名称'
# MAGIC ,product_line_group_code   string comment '产品线组编码'
# MAGIC ,product_line_group        string comment '产品线组名称'
# MAGIC ,secondary_gsv_amount      decimal(38,6) comment '二级GSV Amount(元)'
# MAGIC ,create_by                 string comment '创建人'
# MAGIC ,dw_create_time            timestamp comment '创建时间'
# MAGIC ,dw_last_update_time       timestamp comment '最后更新时间'
# MAGIC ,dw_batch_num              bigint comment '批次号'
# MAGIC )
# MAGIC using delta
# MAGIC partitioned by (dt string comment '天分区')
# MAGIC comment 'ads_omni_secondary_gsv_mf,二级GSV ads结果表'
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_omni_secondary_gsv_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_omni_secondary_gsv_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'secondary_gsv',
# MAGIC 'datasetname' = 'ads_secondary_gsv'
# MAGIC );