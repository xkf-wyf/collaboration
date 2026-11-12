# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf (
# MAGIC data_type	string	COMMENT '数据类型,目前只取P&L和Budget Planning',
# MAGIC type	string	COMMENT '类型,Actual/FCST',
# MAGIC plan_cycle	string	COMMENT '计划周期',
# MAGIC bu_code	string	COMMENT 'bu编码',
# MAGIC bu_name	string	COMMENT 'bu名称',
# MAGIC site_code	string	COMMENT 'site编码',
# MAGIC site_name	string	COMMENT 'site名称',
# MAGIC store_code	string	COMMENT 'store编码',
# MAGIC store_name	string	COMMENT 'store名称',
# MAGIC category_code	string	COMMENT 'category编码',
# MAGIC category_name	string	COMMENT 'category名称',
# MAGIC brand_code	string	COMMENT 'brand_编码',
# MAGIC brand_name	string	COMMENT 'brand名称',
# MAGIC product_line_group_code	string	COMMENT 'product_line_group编码',
# MAGIC product_line_group_name	string	COMMENT 'product_line_group名称',
# MAGIC index_type_level1_code	string	COMMENT 'PBI展示一级指标编码',
# MAGIC index_type_level1_name	string	COMMENT 'PBI展示一级指标名称',
# MAGIC index_type_level2_code	string	COMMENT 'PBI展示子指标编码',
# MAGIC index_type_level2_name	string	COMMENT 'PBI展示子指标名称',
# MAGIC month	string	COMMENT '月份',
# MAGIC value	decimal(38,18)	COMMENT '指标数值',
# MAGIC create_by	String	COMMENT '创建人',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC dw_batch_num	string	COMMENT '日期格式的批次号,20260527'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi看板 ads结果表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'ads_planning'
# MAGIC );