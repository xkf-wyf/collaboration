# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc (
# MAGIC cc_bu	string							COMMENT 'cc业务单元',
# MAGIC cc_category	string							COMMENT 'cc系列',
# MAGIC cc_brand	string					COMMENT 'cc品牌',
# MAGIC cc_product_line	string						COMMENT 'cc品线组',
# MAGIC cpt_category	String			COMMENT 'cpt系列',
# MAGIC cpt_brand string			COMMENT 'cpt品牌',
# MAGIC cpt_plg string			COMMENT 'cpt品线组',
# MAGIC remark	string						COMMENT '备注',
# MAGIC dw_create_time	Timestamp		COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC dw_batch_num  string COMMENT '批次号，20260527'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc
# MAGIC SET TBLPROPERTIES ('comment' = '2026年bu,category,brand,plg的mapping数据ods表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_plg_mapping_adhoc
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'ods_plg_mapping'
# MAGIC );