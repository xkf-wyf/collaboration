# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_sec_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_sec_mf (
# MAGIC section	string	COMMENT '模块归属：P&L / Golden Formula',
# MAGIC bu	string	COMMENT '业务单元',
# MAGIC category	string	COMMENT '品类',
# MAGIC site	string	COMMENT '渠道',
# MAGIC store_type  string	COMMENT '门店类型，门店名称以CBE结尾的门店归为CBE，其他归为LEC',
# MAGIC brand	string	COMMENT '品牌',
# MAGIC period	string	COMMENT '月度 Jan~Dec 或季度 Q1~Q4',
# MAGIC period_sort_no	int	COMMENT '周期排序号：Jan=1 … Dec=12，Q1=13 … Q4=16',
# MAGIC kpi_name	string	COMMENT 'kpi名称',
# MAGIC kpi_unit	string	COMMENT 'kpi单位：K RMB / 千人 / % / RMB 等',
# MAGIC actual	decimal(38,3)	COMMENT '实际值（允许负数）',
# MAGIC plan	decimal(38,3)	COMMENT '计划值（允许负数）',
# MAGIC prior_year	decimal(38,3)	COMMENT '去年同期值（允许负数）',
# MAGIC kpi_parent	string	COMMENT 'kpi父级分组名',
# MAGIC kpi_parent_sort_no	int	COMMENT 'kpi父级排序号 1-14',
# MAGIC kpi_sort_no	int	COMMENT 'kpi子级分段排序号',
# MAGIC year	int	COMMENT '年份',
# MAGIC create_by	string	COMMENT '创建人',
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
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_sec_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_sec_mf
# MAGIC SET TBLPROPERTIES ('comment' = 'cpt planning pbi看板二期 ads结果表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_sec_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'ads_planning_sec'
# MAGIC );