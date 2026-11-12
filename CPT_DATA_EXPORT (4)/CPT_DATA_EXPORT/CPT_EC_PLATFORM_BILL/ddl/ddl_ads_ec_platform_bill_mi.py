# Databricks notebook source
# MAGIC %sql
# MAGIC drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_ec_platform_bill_mi;
# MAGIC CREATE TABLE ${spark.var.catalog.ads}.fin_cpt.ads_ec_platform_bill_mi (
# MAGIC     month STRING COMMENT '账单月份',
# MAGIC     bu_code STRING COMMENT 'BU编码',
# MAGIC     bu_name STRING COMMENT 'BU名称',
# MAGIC     category_code STRING COMMENT '品类编码',
# MAGIC     category_name STRING COMMENT '品类名称',
# MAGIC     brand_code STRING COMMENT '品牌编码',
# MAGIC     brand_name STRING COMMENT '品牌名称',
# MAGIC     product_line_group_code STRING COMMENT '品线编码',
# MAGIC     product_line_group_name STRING COMMENT '品线名称',
# MAGIC     business_type STRING COMMENT 'Business Type',
# MAGIC     site_code STRING COMMENT 'Site编码',
# MAGIC     site_name STRING COMMENT 'Site名称',
# MAGIC     store_code STRING COMMENT 'Store编码',
# MAGIC     store_name STRING COMMENT 'Store名称',
# MAGIC     spending_type_fin STRING COMMENT '账单指标名称',
# MAGIC     amount_taxed DECIMAL(20,2) COMMENT '指标结果-含税金额',
# MAGIC     amount_untaxed DECIMAL(20,2) COMMENT '指标结果-未税金额',
# MAGIC     create_by STRING COMMENT '创建人',
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
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_ec_platform_bill_mi set owner to `${spark.var.table.owner}`;