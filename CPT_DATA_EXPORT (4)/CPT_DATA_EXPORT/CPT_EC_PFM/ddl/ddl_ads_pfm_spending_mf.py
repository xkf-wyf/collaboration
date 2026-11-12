# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf (
# MAGIC month	String	COMMENT '月份',
# MAGIC bu_code	String	COMMENT 'BU编码',
# MAGIC bu_name	String	COMMENT 'BU名称',
# MAGIC category_code	String	COMMENT '品类编码',
# MAGIC category_name	String	COMMENT '品类名称',
# MAGIC brand_code	String	COMMENT '品牌编码',
# MAGIC brand_name	String	COMMENT '品牌名称',
# MAGIC product_line_group_code	String	COMMENT '品线编码',
# MAGIC product_line_group_name	String	COMMENT '品线名称',
# MAGIC site_code	String	COMMENT 'Site编码',
# MAGIC site_name	String	COMMENT 'Site名称',
# MAGIC store_code	String	COMMENT 'Store编码',
# MAGIC store_name	String	COMMENT 'Store名称',
# MAGIC index_type	String	COMMENT 'PFM指标名称',
# MAGIC value_untaxed	decimal(20,2)	COMMENT '指标结果-未税金额(RMB 元)',
# MAGIC value_taxed	decimal(20,2)	COMMENT '指标结果-含税金额(RMB 元)',
# MAGIC source	String	COMMENT '数据来源',
# MAGIC create_by	String	COMMENT '创建人',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC etl_time	Timestamp	COMMENT '数据加载时间'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'pfm ads结果表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'pfm',
# MAGIC 'datasetname' = 'ads_pfm'
# MAGIC );