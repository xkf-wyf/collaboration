# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_cpt_planning_cycle_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_cycle_mapping (
# MAGIC idx	bigint	COMMENT '唯一序号',
# MAGIC type	string	COMMENT '类型，Actual/FCST',
# MAGIC cycle_en	string	COMMENT '计划周期英文格式，如2026Mar',
# MAGIC cycle_filter	string	COMMENT '计划周期(用于报表过滤)',
# MAGIC cycle_fact	string	COMMENT '实际计划周期',
# MAGIC month	string	COMMENT '计划周期包含的月份',
# MAGIC remark	string	COMMENT '备注',
# MAGIC cycle_union_key	string	COMMENT '关联键',
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
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_cycle_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_cycle_mapping
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi计划周期配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_cycle_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'dim_cycle'
# MAGIC );