# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping (
# MAGIC kpi_parent_sort_no	int	COMMENT '上级kpi排序号',
# MAGIC kpi_parent_name	string	COMMENT '上级kpi名称',
# MAGIC kpi_list	string	COMMENT '上级kpi包含的下级kpi清单',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC dw_batch_num	string	COMMENT '批次号，20260527'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning cpt数据上级kpi排序配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'dim_cpt_kpi_parent_sort'
# MAGIC );