# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC  -- adb sql
# MAGIC -- **********************************************************************
# MAGIC -- ods_store_brand_scope_detailed_planning_mapping 接口
# MAGIC -- v1.0 iris.iris 2026-04-29
# MAGIC -- 描述：每个月不定时更新该mapping表。by bu+store+category+brand 的粒度，去定义detailed_planning的内容。对接人：polly
# MAGIC -- **********************************************************************
# MAGIC
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_store_brand_scope_detailed_planning_mapping_adhoc;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_store_brand_scope_detailed_planning_mapping_adhoc (
# MAGIC bu	String	COMMENT 'bu名称',
# MAGIC store	String	COMMENT 'store名称',
# MAGIC category	String	COMMENT 'category名称',
# MAGIC brand	String	COMMENT 'brand名称',
# MAGIC detailed_planning	String	COMMENT '是否做明细计划或计划类型',
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
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_store_brand_scope_detailed_planning_mapping_adhoc set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_store_brand_scope_detailed_planning_mapping_adhoc
# MAGIC SET TBLPROPERTIES ('comment' = 'core_pack_check的scope_detailed_planning_mapping表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_store_brand_scope_detailed_planning_mapping_adhoc
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'core_pack_check',
# MAGIC 'datasetname' = 'ods_core_pack_check'
# MAGIC );