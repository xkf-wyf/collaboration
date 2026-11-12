# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf (
# MAGIC period	string	COMMENT '月份',
# MAGIC ll1	string	COMMENT '客户编码（local level 1）',
# MAGIC cc_report_fcst	string	COMMENT 'Site名称',
# MAGIC customer_group	string	COMMENT '客户组名称',
# MAGIC ph8	string	COMMENT '产品层级L8（product hierarchy L8）',
# MAGIC bu	string	COMMENT 'bu',
# MAGIC category	string	COMMENT '品类',
# MAGIC brand	string	COMMENT '品牌',
# MAGIC product_line	string	COMMENT '品线',
# MAGIC item_code	string	COMMENT '指标编码',
# MAGIC item_name	string	COMMENT '指标名称',
# MAGIC amount	decimal(20,2)	COMMENT '指标值-未税金额(RMB 元)',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC etl_time	Timestamp	COMMENT '数据更新时间'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf
# MAGIC SET TBLPROPERTIES ('comment' = '取自上游数据库的源数据ods表');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'ods_rawdata'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf;
# MAGIC
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf (
# MAGIC period	string	COMMENT '月份',
# MAGIC ll1	string	COMMENT '客户编码（local level 1）',
# MAGIC cc_report_fcst	string	COMMENT 'Site名称',
# MAGIC customer_group	string	COMMENT '客户组名称',
# MAGIC ph8	string	COMMENT '产品层级L8（product hierarchy L8）',
# MAGIC bu	string	COMMENT 'bu',
# MAGIC category	string	COMMENT '品类',
# MAGIC brand	string	COMMENT '品牌',
# MAGIC product_line	string	COMMENT '品线',
# MAGIC item_code	string	COMMENT '指标编码',
# MAGIC item_name	string	COMMENT '指标名称',
# MAGIC amount	decimal(20,2)	COMMENT '指标值-未税金额(RMB 元)',
# MAGIC dw_create_time	Timestamp	COMMENT '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT '最后更新时间',
# MAGIC etl_time	Timestamp	COMMENT '数据更新时间'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC ALTER TABLE ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf
# MAGIC SET TBLPROPERTIES ('comment' = '取自上游数据库的源数据ods表_2025年手工数据');
# MAGIC
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'cc_report',
# MAGIC 'datasetname' = 'ods_rawdata'
# MAGIC );