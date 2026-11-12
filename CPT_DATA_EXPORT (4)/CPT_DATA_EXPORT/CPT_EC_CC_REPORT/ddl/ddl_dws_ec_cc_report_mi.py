# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi (
# MAGIC month	String	COMMENT '月份',
# MAGIC bu_code	String	COMMENT 'BU编码',
# MAGIC bu_name	String	COMMENT 'BU名称',
# MAGIC category_code	String	COMMENT '品类编码',
# MAGIC category_name	String	COMMENT '品类名称',
# MAGIC brand_code	String	COMMENT '品牌编码',
# MAGIC brand_name	String	COMMENT '品牌名称',
# MAGIC product_line_group_code	String	COMMENT '品线组编码',
# MAGIC product_line_group_name	String	COMMENT '品线组名称',
# MAGIC site_code	String	COMMENT 'Site编码',
# MAGIC site_name	String	COMMENT 'Site名称',
# MAGIC store_code	String	COMMENT 'Store编码',
# MAGIC store_name	String	COMMENT 'Store名称',
# MAGIC index_type	String	COMMENT '指标名称',
# MAGIC value_untaxed	decimal(20,2)	COMMENT '指标值-未税金额(RMB 元)',
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
# MAGIC alter table ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi
# MAGIC SET TBLPROPERTIES ('comment' = 'cc_report dws结果表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'dws_cc_report'
# MAGIC );