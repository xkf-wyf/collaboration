# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ods}.int_manual.ods_platform_finance_spending_mapping;
# MAGIC CREATE TABLE ${spark.var.catalog.ods}.int_manual.ods_platform_finance_spending_mapping (
# MAGIC     platform_name STRING COMMENT '平台',
# MAGIC     fee_type_platform STRING COMMENT '原始账单费用类型（来自 PDD/TMALL 账单）',
# MAGIC     spending_type_fin STRING COMMENT 'UL财务费用类型',
# MAGIC     dw_create_time TIMESTAMP COMMENT '创建时间',
# MAGIC     dw_last_update_time TIMESTAMP COMMENT '最后更新时间',
# MAGIC     etl_time TIMESTAMP COMMENT '数据加载时间'
# MAGIC )
# MAGIC TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.autoCompact' = 'true',
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'true'
# MAGIC )
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC alter table ${spark.var.catalog.ods}.int_manual.ods_platform_finance_spending_mapping set owner to `${spark.var.table.owner}`;