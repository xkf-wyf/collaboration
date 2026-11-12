# Databricks notebook source
# MAGIC %sql
# MAGIC  -- adb sql
# MAGIC -- **********************************************************************
# MAGIC -- hc_product_line_group_mf接口
# MAGIC -- v1.0 wu.bingling@unilever-china.com 2026-03-03
# MAGIC -- **********************************************************************
# MAGIC
# MAGIC drop table if exists ${spark.var.catalog.dim}.fin.dim_hc_product_line_group_mf;
# MAGIC create table if not exists ${spark.var.catalog.dim}.fin.dim_hc_product_line_group_mf
# MAGIC (
# MAGIC 	bu_code 					        string COMMENT 'BU编码'
# MAGIC    ,bu_name 					        string COMMENT 'BU名称'   
# MAGIC    ,category_code 		    		    string COMMENT '品类编码'
# MAGIC    ,category_name 			    	    string COMMENT '品类名称'
# MAGIC    ,subbrand_code 			    	    string COMMENT '子品牌编码'
# MAGIC    ,subbrand_name 			    	    string COMMENT '子品牌名称'
# MAGIC    ,product_line_group_code 	        string COMMENT '产品线组编码'
# MAGIC    ,product_line_group 	    	        string COMMENT '产品线组名称'
# MAGIC    ,create_by 				      	    string comment '创建人'
# MAGIC    ,dw_create_time                      timestamp comment '创建时间'
# MAGIC    ,dw_last_update_time                 timestamp comment '最后更新时间'
# MAGIC    ,dw_batch_num                        bigint comment '批次号'
# MAGIC )
# MAGIC using delta
# MAGIC partitioned by (dt string comment '天分区')
# MAGIC comment 'dim_hc_product_line_group_mf,HC产品线组维度表'
# MAGIC ;
# MAGIC
# MAGIC alter table ${spark.var.catalog.dim}.fin.dim_hc_product_line_group_mf set owner to `${spark.var.table.owner}`;
# MAGIC
# MAGIC
# MAGIC
# MAGIC alter table ${spark.var.catalog.ads}.fin_cpt.ads_pfm_spending_mf
# MAGIC set TAGS (
# MAGIC 'project' = 'CPT',
# MAGIC 'datasetgroupname' = 'hc_product_line_group',
# MAGIC 'datasetname' = 'dim_hc_product_line_group'
# MAGIC );