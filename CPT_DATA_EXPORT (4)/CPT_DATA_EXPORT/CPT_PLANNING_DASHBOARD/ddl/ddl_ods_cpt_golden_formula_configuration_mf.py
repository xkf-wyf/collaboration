# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cpt_golden_formula_configuration_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_golden_formula_configuration_mf (
# MAGIC id	bigint	COMMENT '自增ID',
# MAGIC period_code	string	COMMENT '周期',
# MAGIC encode	string	COMMENT '编码',
# MAGIC formula_type	string	COMMENT '公式类型（planning/actual）',
# MAGIC index_type_code	string	COMMENT '一级指标编码',
# MAGIC index_type	string	COMMENT '一级指标名称',
# MAGIC package_item_sub_type_code	string	COMMENT '二级指标编码',
# MAGIC package_item_sub_type	string	COMMENT '二级指标名称',
# MAGIC formula_code	string	COMMENT '具体公式—编码',
# MAGIC formula_name	string	COMMENT '具体公式—名称',
# MAGIC state	bigint	COMMENT '有效状态（1有效 0无效）',
# MAGIC delete_flag	bigint	COMMENT '删除标识（1已删除 0未删除）',
# MAGIC create_by	string	COMMENT '创建人',
# MAGIC create_date	timestamp	COMMENT '创建时间',
# MAGIC update_by	double	COMMENT '更新人',
# MAGIC update_date	double	COMMENT '更新时间',
# MAGIC period_name	string	COMMENT '周期名称',
# MAGIC three_level_classification_code	string	COMMENT '三级指标编码',
# MAGIC three_level_classification_name	string	COMMENT '三级指标名称',
# MAGIC four_level_classification_code	string	COMMENT '四级指标编码',
# MAGIC four_level_classification_name	string	COMMENT '四级指标名称',
# MAGIC revenue_stream_code	string	COMMENT 'Revenue Stream编码',
# MAGIC revenue_stream_name	string	COMMENT 'Revenue Stream名称',
# MAGIC kol_tier_code	string	COMMENT '达人层级编码（仅达播）',
# MAGIC kol_tier_name	string	COMMENT '达人层级名称（仅达播）',
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
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_golden_formula_configuration_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_golden_formula_configuration_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi指标计算公式ods配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_golden_formula_configuration_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'ods_formula'
# MAGIC );