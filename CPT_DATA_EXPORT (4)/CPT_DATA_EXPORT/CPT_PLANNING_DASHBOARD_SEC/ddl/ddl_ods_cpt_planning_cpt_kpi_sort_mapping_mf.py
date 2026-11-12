# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_sort_mapping_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_sort_mapping_mf (
# MAGIC kpi_sort_no	int	COMMENT 'kpi排序号',
# MAGIC kpi_name	string	COMMENT 'KPI名称',
# MAGIC kpi_parent_name	string	COMMENT '上级kpi名称',
# MAGIC kpi_unit	string	COMMENT 'kpi单位',
# MAGIC kpi_source	string	COMMENT 'kpi来源',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC dw_batch_num	string	COMMENT '批次号，20260527',
# MAGIC data_source	string	COMMENT '数据来源，manual或者其他来源'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_sort_mapping_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_sort_mapping_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning cpt数据kpi排序配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_planning_cpt_kpi_sort_mapping_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'ods_cpt_kpi_sort'
# MAGIC );