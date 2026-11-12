# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_cpt_ec_pnl_mi;
# MAGIC CREATE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_cpt_ec_pnl_mi (
# MAGIC month	String	COMMENT  '月份',
# MAGIC bu_code	String	COMMENT  'BU编码',
# MAGIC bu_name	String	COMMENT  'BU名称',
# MAGIC category_code	String	COMMENT  '品类编码',
# MAGIC category_name	String	COMMENT  '品类名称',
# MAGIC brand_code	String	COMMENT  '品牌编码',
# MAGIC brand_name	String	COMMENT  '品牌名称',
# MAGIC product_line_group_code	String	COMMENT  '品线编码',
# MAGIC product_line_group_name	String	COMMENT  '品线名称',
# MAGIC business_type	String	COMMENT  'Business Type',
# MAGIC sold_to_code	String	COMMENT  'Sold To编码',
# MAGIC sold_to_name	String	COMMENT  'Sold To名称',
# MAGIC site_code	String	COMMENT  'Site编码',
# MAGIC site_name	String	COMMENT  'Site名称',
# MAGIC store_code	String	COMMENT  'Store编码',
# MAGIC store_name	String	COMMENT  'Store名称',
# MAGIC index_type	string	COMMENT  '账单指标名称',
# MAGIC amount	decimal(20,2)	COMMENT  '指标结果',
# MAGIC create_by	string	COMMENT  '创建人',
# MAGIC dw_create_time	Timestamp	COMMENT  '创建时间',
# MAGIC dw_last_update_time	Timestamp	COMMENT  '最后更新时间',
# MAGIC etl_time	Timestamp	COMMENT  '入库时间',
# MAGIC etl_flag	string COMMENT '数据当月更新批次标志,取当月的月份,比如2025年11月份跑的数,批次标志就是202511'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_ec_pnl_mi set owner to `${spark.var.table.owner}`;