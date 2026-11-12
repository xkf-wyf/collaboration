# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping (
# MAGIC source	String	COMMENT '数据来源',
# MAGIC bmi_spend_type	String	COMMENT '指标类型-业务提供',
# MAGIC source_index_type	String	COMMENT '指标类型-数据端提供',
# MAGIC output_index_type String	COMMENT '指标类型-最终展示',
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
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping
# MAGIC SET TBLPROPERTIES ('comment' = 'pfm 指标名称mapping数据dim表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'MasterData',
# MAGIC 'datasetname' = 'IndexMapping'
# MAGIC );