# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf (
# MAGIC id	bigint	COMMENT '自增ID',
# MAGIC period_code	bigint	COMMENT '周期',
# MAGIC indicator_type	string	COMMENT '指标类型',
# MAGIC index_type_code	string	COMMENT 'Index Type （一级）编码',
# MAGIC index_type	string	COMMENT 'Index Type （一级）',
# MAGIC package_item_sub_type_code	string	COMMENT 'Package Item Sub Type （二级）编码',
# MAGIC package_item_sub_type	string	COMMENT 'Package Item Sub Type （二级）',
# MAGIC three_level_classification_code	string	COMMENT '三级编码',
# MAGIC three_level_classification_name	string	COMMENT '三级名称',
# MAGIC unit	string	COMMENT '单位',
# MAGIC data_source	string	COMMENT '指标类型标识（Input/Import/Calculate）',
# MAGIC actual_item_mapping	string	COMMENT '对应实际数指标名称',
# MAGIC parent_id	string	COMMENT '报表折叠对应的父级编码',
# MAGIC sort	double	COMMENT '排序字段',
# MAGIC state	bigint	COMMENT '有效状态（1有效 0无效）',
# MAGIC delete_flag	bigint	COMMENT '删除标识（1已删除 0未删除）',
# MAGIC create_by	string	COMMENT '创建人',
# MAGIC create_date	timestamp	COMMENT '创建时间',
# MAGIC update_by	double	COMMENT '更新人',
# MAGIC update_date	double	COMMENT '更新时间',
# MAGIC period_name	string	COMMENT '周期名称',
# MAGIC detail_report_mapping	string	COMMENT 'Detail报表映射指标code',
# MAGIC is_show	double	COMMENT '是否展示（1是 0否）',
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
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi指标ods配置表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_plan_template_configuration_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'ods_index'
# MAGIC );