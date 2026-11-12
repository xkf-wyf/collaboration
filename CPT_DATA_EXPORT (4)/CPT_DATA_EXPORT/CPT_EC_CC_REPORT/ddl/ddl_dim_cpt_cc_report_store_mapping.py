# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping (
# MAGIC customer_group	String	COMMENT '客户组名称',
# MAGIC store_name	String	COMMENT '店铺名称',
# MAGIC cpt_scope	String	COMMENT 'CPT适用范围',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC etl_time	Timestamp	COMMENT '数据更新时间'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping
# MAGIC SET TBLPROPERTIES ('comment' = '门店mapping数据dim表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'dim_store_mapping'
# MAGIC );