# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_ddm_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_ddm_mf (
# MAGIC section	string	COMMENT '固定为 Perfect Store',
# MAGIC bu	string	COMMENT '业务单元',
# MAGIC category	string	COMMENT '品类',
# MAGIC site	string	COMMENT '渠道',
# MAGIC store_type  string	COMMENT '门店类型，这里统一归为LEC',
# MAGIC brand	string	COMMENT '品牌',
# MAGIC period	string	COMMENT '月度名称Jan~Dec',
# MAGIC period_sort_no	int	COMMENT '月度排序1 - 12',
# MAGIC kpi_name	string	COMMENT 'kpi名称',
# MAGIC kpi_unit	string	COMMENT '单位',
# MAGIC actual	decimal(38,3)	COMMENT '实际值',
# MAGIC target	decimal(38,3)	COMMENT '目标值（TGT）',
# MAGIC prior_year	decimal(38,3)	COMMENT '去年同期值',
# MAGIC kpi_parent	string	COMMENT '最上层kpi名称，固定为Perfect Store',
# MAGIC kpi_parent_sort_no	int	COMMENT '最上层kpi排序，固定1',
# MAGIC kpi_sort_no	int	COMMENT 'kpi排序1 - 9',
# MAGIC year	int	COMMENT '2026',
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
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_ddm_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_ddm_mf
# MAGIC SET TBLPROPERTIES (
# MAGIC   'cond_review_violate_rule' = 'ads_cpt_planning_ddm_mf跨项目依赖DDM ads_ec_pso_kpi_fact_limit_mf',
# MAGIC   'cond_review_time' = '2026-09-16',
# MAGIC   'cond_fix_status' = 'pending', 
# MAGIC   'cond_finish_time' = '',
# MAGIC   'cond_fix_note' = '跨项目协调周期较长，项目上线时间紧迫，，延后整改',
# MAGIC   'comment' = 'cpt planning pbi看板二期ddm数据 ads结果表'
# MAGIC );
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_ddm_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'planning',
# MAGIC 'datasetname' = 'ads_planning_ddm'
# MAGIC );