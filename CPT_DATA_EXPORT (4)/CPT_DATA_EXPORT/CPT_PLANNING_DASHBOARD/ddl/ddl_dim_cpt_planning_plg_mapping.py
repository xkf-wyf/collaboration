# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_cpt_planning_plg_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_plg_mapping (
# MAGIC bu_name	string	COMMENT 'bu名称',
# MAGIC site_name	string	COMMENT 'site名称',
# MAGIC store_name	string	COMMENT '门店名称',
# MAGIC category_name	string	COMMENT 'category名称',
# MAGIC brand_name	string	COMMENT 'brand名称',
# MAGIC product_line_group_name	string	COMMENT '产品线名称',
# MAGIC plg_union_key	string	COMMENT '组合mapping键',
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
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_plg_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_plg_mapping
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi产品线维度配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_plg_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'dim_plg'
# MAGIC );