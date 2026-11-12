# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping (
# MAGIC period_code	bigint	COMMENT '版本周期',
# MAGIC indicator_type	string	COMMENT '指标来源',
# MAGIC index_type_code	string	COMMENT '源一级指标编码',
# MAGIC index_type	string	COMMENT '源一级指标名称',
# MAGIC package_item_sub_type_code	string	COMMENT '源最细粒度指标编码',
# MAGIC package_item_sub_type	string	COMMENT '源最细粒度指标名称',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC dw_batch_num	string	COMMENT '批次号, 20260527'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi指标dim配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'dim_index'
# MAGIC );