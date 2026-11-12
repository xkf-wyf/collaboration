# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.dwd}.fin.dwd_cpt_planning_pl_target_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.dwd}.fin.dwd_cpt_planning_pl_target_mf (
# MAGIC section	string	COMMENT '固定 P&L',
# MAGIC bu	string	COMMENT '业务单元',
# MAGIC category	string	COMMENT '品类',
# MAGIC site	string	COMMENT '渠道',
# MAGIC store_type  string	COMMENT '门店类型，这里统一归为LEC',
# MAGIC brand	string	COMMENT '品牌',
# MAGIC period	string	COMMENT 'Jan~Dec',
# MAGIC kpi_name	string	COMMENT '客户手工填入的kpi名称',
# MAGIC target	decimal(38,3)	COMMENT '客户手工填入的KPI月度目标',
# MAGIC year	int	COMMENT '2026',
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
# MAGIC alter table ${spark.var.catalog.dwd}.fin.dwd_cpt_planning_pl_target_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.dwd}.fin.dwd_cpt_planning_pl_target_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'p&l目标数据手工配置数据dwd表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.dwd}.fin.dwd_cpt_planning_pl_target_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'dwd_cpt_pl_target'
# MAGIC );