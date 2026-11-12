# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc (
# MAGIC ph8	string							COMMENT '产品层级L8（product hierarchy L8）',
# MAGIC bu	string							COMMENT 'bu',
# MAGIC category	string					COMMENT '品类',
# MAGIC brand	string						COMMENT '品牌',
# MAGIC product_line_group	String			COMMENT '品线组',
# MAGIC remark	String						COMMENT '备注',
# MAGIC dw_create_time	Timestamp		COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC etl_time	Timestamp			COMMENT '数据更新时间'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc
# MAGIC SET TBLPROPERTIES ('comment' = 'ph8无法匹配的清单-手工plg-mapping数据ods表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'ods_ph8_mapping'
# MAGIC );