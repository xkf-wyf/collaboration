# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_sort_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_sort_mapping (
# MAGIC index_level1_name	string	COMMENT 'pbi展示指标第一层名称',
# MAGIC index_level2_name	string	COMMENT 'pbi展示指标第二层名称',
# MAGIC index_level3_name	string	COMMENT 'pbi展示指标第三层名称',
# MAGIC index_level3_code	string	COMMENT 'pbi展示指标第三层编码',
# MAGIC unit	string	COMMENT '指标单位',
# MAGIC level1_sort	bigint	COMMENT 'pbi展示指标第一层排序',
# MAGIC level2_sort	bigint	COMMENT 'pbi展示指标第二层排序',
# MAGIC sort	bigint	COMMENT 'pbi展示指标第三层排序',
# MAGIC index_union_key	string	COMMENT '组合mapping键',
# MAGIC index_type_level1_code	string	COMMENT '源数据指标第一层编码',
# MAGIC index_type_level1_name	string	COMMENT '源数据指标第一层名称',
# MAGIC index_type_level2_code	string	COMMENT '源数据指标第二层编码',
# MAGIC index_type_level2_name	string	COMMENT '源数据指标第二层名称',
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
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_sort_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_sort_mapping
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi指标排序展示dim配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_sort_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'dim_index_sort'
# MAGIC );