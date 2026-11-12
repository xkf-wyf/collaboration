# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc (
# MAGIC item_code	String	COMMENT '源数据-指标编码',
# MAGIC item_name	String	COMMENT '源数据-指标名称',
# MAGIC cpt_index_mapping	String	COMMENT 'CPT标准化指标名称',
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
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc
# MAGIC SET TBLPROPERTIES ('comment' = '指标mapping数据ods表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_adhoc
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'ods_index_mapping'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc (
# MAGIC item_code	String	COMMENT '源数据-指标编码',
# MAGIC item_name	String	COMMENT '源数据-指标名称',
# MAGIC cpt_index_mapping	String	COMMENT 'CPT标准化指标名称',
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
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc
# MAGIC SET TBLPROPERTIES ('comment' = '指标mapping数据ods表_2025年版本');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'ods_index_mapping'
# MAGIC );
# MAGIC