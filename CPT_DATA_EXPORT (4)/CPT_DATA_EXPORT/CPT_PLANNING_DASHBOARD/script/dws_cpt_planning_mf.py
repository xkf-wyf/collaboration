# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual
# MAGIC with t_cpt_planning_rawdata as (
# MAGIC select 
# MAGIC 'Budget Planning' as data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC period_name,
# MAGIC bu_code,	
# MAGIC bu_name,	
# MAGIC channel_code,	
# MAGIC channel_name,	
# MAGIC site_code,	
# MAGIC site_name,	
# MAGIC store_code,	
# MAGIC store_name,	
# MAGIC category_code,	
# MAGIC category_name,	
# MAGIC brand_code,	
# MAGIC brand_name,	
# MAGIC product_line_group_code,	
# MAGIC product_line_group_name,	
# MAGIC index_type_code,	
# MAGIC index_type_name,	
# MAGIC package_item_sub_type_code,	
# MAGIC package_item_sub_type_name,	
# MAGIC third_level_index_code,	
# MAGIC third_level_index_name,	
# MAGIC fourth_level_index_code,	
# MAGIC fourth_level_index_name,
# MAGIC cpt_adjust_jan as A01,
# MAGIC cpt_adjust_feb as A02,
# MAGIC cpt_adjust_mar as A03,
# MAGIC cpt_adjust_apr as A04,
# MAGIC cpt_adjust_may as A05,
# MAGIC cpt_adjust_jun as A06,
# MAGIC cpt_adjust_jul as A07,
# MAGIC cpt_adjust_aug as A08,
# MAGIC cpt_adjust_sep as A09,
# MAGIC cpt_adjust_oct as A10,
# MAGIC cpt_adjust_nov as A11,
# MAGIC cpt_adjust_dec as A12
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_cpt_budget_planning_df
# MAGIC where 1 = 1
# MAGIC and type = 'Actual'
# MAGIC union all 
# MAGIC select 
# MAGIC 'P&L' as data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC period_name,
# MAGIC bu_code,	
# MAGIC bu_name,	
# MAGIC channel_code,	
# MAGIC channel_name,	
# MAGIC site_code,	
# MAGIC site_name,	
# MAGIC store_code,	
# MAGIC store_name,	
# MAGIC category_code,	
# MAGIC category_name,	
# MAGIC brand_code,	
# MAGIC brand_name,	
# MAGIC product_line_group_code,	
# MAGIC product_line_group_name,	
# MAGIC index_type_code,	
# MAGIC index_type_name,	
# MAGIC package_item_sub_type_code,	
# MAGIC package_item_sub_type_name,	
# MAGIC third_level_index_code,	
# MAGIC third_level_index_name,	
# MAGIC fourth_level_index_code,	
# MAGIC fourth_level_index_name,
# MAGIC cpt_adjust_jan as A01,
# MAGIC cpt_adjust_feb as A02,
# MAGIC cpt_adjust_mar as A03,
# MAGIC cpt_adjust_apr as A04,
# MAGIC cpt_adjust_may as A05,
# MAGIC cpt_adjust_jun as A06,
# MAGIC cpt_adjust_jul as A07,
# MAGIC cpt_adjust_aug as A08,
# MAGIC cpt_adjust_sep as A09,
# MAGIC cpt_adjust_oct as A10,
# MAGIC cpt_adjust_nov as A11,
# MAGIC cpt_adjust_dec as A12
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_cpt_p_and_l_df
# MAGIC where 1 = 1
# MAGIC and type = 'Actual'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC raw_data as (
# MAGIC select 
# MAGIC data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC period_name,
# MAGIC bu_code,	
# MAGIC bu_name,	
# MAGIC channel_code,	
# MAGIC channel_name,	
# MAGIC site_code,	
# MAGIC site_name,	
# MAGIC store_code,	
# MAGIC store_name,	
# MAGIC category_code,	
# MAGIC category_name,	
# MAGIC brand_code,	
# MAGIC brand_name,	
# MAGIC product_line_group_code,	
# MAGIC product_line_group_name,	
# MAGIC index_type_code,	
# MAGIC index_type_name,	
# MAGIC package_item_sub_type_code,	
# MAGIC package_item_sub_type_name,	
# MAGIC third_level_index_code,	
# MAGIC third_level_index_name,	
# MAGIC fourth_level_index_code,	
# MAGIC fourth_level_index_name,
# MAGIC A01,
# MAGIC A02,
# MAGIC A03,
# MAGIC A04,
# MAGIC A05,
# MAGIC A06,
# MAGIC A07,
# MAGIC A08,
# MAGIC A09,
# MAGIC A10,
# MAGIC A11,
# MAGIC A12
# MAGIC from t_cpt_planning_rawdata 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC mid_data as (
# MAGIC select
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.period_name,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_code,	
# MAGIC a.index_type_name,	
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,        
# MAGIC t.a_month,
# MAGIC t.a_value
# MAGIC from raw_data a    
# MAGIC LATERAL VIEW STACK(
# MAGIC   12,
# MAGIC   '01', A01,
# MAGIC   '02', A02,
# MAGIC   '03', A03,
# MAGIC   '04', A04,
# MAGIC   '05', A05,
# MAGIC   '06', A06,
# MAGIC   '07', A07,
# MAGIC   '08', A08,
# MAGIC   '09', A09,
# MAGIC   '10', A10,
# MAGIC   '11', A11,
# MAGIC   '12', A12
# MAGIC ) t AS a_month, a_value
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_data as (
# MAGIC select
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_code,	
# MAGIC a.index_type_name,	
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,        
# MAGIC a.period_name||a.a_month as a_month,
# MAGIC a.a_value
# MAGIC from mid_data a
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_code as index_type_level1_code,	
# MAGIC a.index_type_name as index_type_level1_name,	
# MAGIC a.package_item_sub_type_code,
# MAGIC a.package_item_sub_type_name,
# MAGIC a.third_level_index_code,
# MAGIC a.third_level_index_name,
# MAGIC a.fourth_level_index_code,
# MAGIC a.fourth_level_index_name,
# MAGIC substring_index(
# MAGIC regexp_replace(
# MAGIC nvl(a.index_type_code,'')||'|'||
# MAGIC nvl(a.package_item_sub_type_code,'')||'|'||
# MAGIC nvl(a.third_level_index_code,'')||'|'||
# MAGIC nvl(a.fourth_level_index_code,''),
# MAGIC '\\|+$', 
# MAGIC ''),
# MAGIC '|', 
# MAGIC -1) as index_type_level2_code,	
# MAGIC substring_index(
# MAGIC regexp_replace(
# MAGIC nvl(a.index_type_name,'')||'|'||
# MAGIC nvl(a.package_item_sub_type_name,'')||'|'||
# MAGIC nvl(a.third_level_index_name,'')||'|'||
# MAGIC nvl(a.fourth_level_index_name,''),
# MAGIC '\\|+$', 
# MAGIC ''),
# MAGIC '|', 
# MAGIC -1) as index_type_level2_name,        
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from tmp_data a
# MAGIC where 1 = 1
# MAGIC and a_month < date_format(current_date(), 'yyyyMM')
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst
# MAGIC with t_cpt_planning_rawdata as (
# MAGIC select 
# MAGIC 'Budget Planning' as data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC start_month,
# MAGIC end_month,
# MAGIC period_name,
# MAGIC bu_code,	
# MAGIC bu_name,	
# MAGIC channel_code,	
# MAGIC channel_name,	
# MAGIC site_code,	
# MAGIC site_name,	
# MAGIC store_code,	
# MAGIC store_name,	
# MAGIC category_code,	
# MAGIC category_name,	
# MAGIC brand_code,	
# MAGIC brand_name,	
# MAGIC product_line_group_code,	
# MAGIC product_line_group_name,	
# MAGIC index_type_code,	
# MAGIC index_type_name,	
# MAGIC package_item_sub_type_code,	
# MAGIC package_item_sub_type_name,	
# MAGIC third_level_index_code,	
# MAGIC third_level_index_name,	
# MAGIC fourth_level_index_code,	
# MAGIC fourth_level_index_name,
# MAGIC cpt_adjust_jan as A01,
# MAGIC cpt_adjust_feb as A02,
# MAGIC cpt_adjust_mar as A03,
# MAGIC cpt_adjust_apr as A04,
# MAGIC cpt_adjust_may as A05,
# MAGIC cpt_adjust_jun as A06,
# MAGIC cpt_adjust_jul as A07,
# MAGIC cpt_adjust_aug as A08,
# MAGIC cpt_adjust_sep as A09,
# MAGIC cpt_adjust_oct as A10,
# MAGIC cpt_adjust_nov as A11,
# MAGIC cpt_adjust_dec as A12,
# MAGIC cpt_reserve_adjust_jan as F01,
# MAGIC cpt_reserve_adjust_feb as F02,
# MAGIC cpt_reserve_adjust_mar as F03
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_cpt_budget_planning_df
# MAGIC where 1 = 1
# MAGIC and type = 'FCST'
# MAGIC union all 
# MAGIC select 
# MAGIC 'P&L' as data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC start_month,
# MAGIC end_month,
# MAGIC period_name,
# MAGIC bu_code,	
# MAGIC bu_name,	
# MAGIC channel_code,	
# MAGIC channel_name,	
# MAGIC site_code,	
# MAGIC site_name,	
# MAGIC store_code,	
# MAGIC store_name,	
# MAGIC category_code,	
# MAGIC category_name,	
# MAGIC brand_code,	
# MAGIC brand_name,	
# MAGIC product_line_group_code,	
# MAGIC product_line_group_name,	
# MAGIC index_type_code,	
# MAGIC index_type_name,	
# MAGIC package_item_sub_type_code,	
# MAGIC package_item_sub_type_name,	
# MAGIC third_level_index_code,	
# MAGIC third_level_index_name,	
# MAGIC fourth_level_index_code,	
# MAGIC fourth_level_index_name,
# MAGIC cpt_adjust_jan as A01,
# MAGIC cpt_adjust_feb as A02,
# MAGIC cpt_adjust_mar as A03,
# MAGIC cpt_adjust_apr as A04,
# MAGIC cpt_adjust_may as A05,
# MAGIC cpt_adjust_jun as A06,
# MAGIC cpt_adjust_jul as A07,
# MAGIC cpt_adjust_aug as A08,
# MAGIC cpt_adjust_sep as A09,
# MAGIC cpt_adjust_oct as A10,
# MAGIC cpt_adjust_nov as A11,
# MAGIC cpt_adjust_dec as A12,
# MAGIC cpt_reserve_adjust_jan as F01,
# MAGIC cpt_reserve_adjust_feb as F02,
# MAGIC cpt_reserve_adjust_mar as F03
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_cpt_p_and_l_df
# MAGIC where 1 = 1
# MAGIC and type = 'FCST'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC raw_data as (
# MAGIC select 
# MAGIC data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC period_name,
# MAGIC bu_code,	
# MAGIC bu_name,	
# MAGIC channel_code,	
# MAGIC channel_name,	
# MAGIC site_code,	
# MAGIC site_name,	
# MAGIC store_code,	
# MAGIC store_name,	
# MAGIC category_code,	
# MAGIC category_name,	
# MAGIC brand_code,	
# MAGIC brand_name,	
# MAGIC product_line_group_code,	
# MAGIC product_line_group_name,	
# MAGIC index_type_code,	
# MAGIC index_type_name,	
# MAGIC package_item_sub_type_code,	
# MAGIC package_item_sub_type_name,	
# MAGIC third_level_index_code,	
# MAGIC third_level_index_name,	
# MAGIC fourth_level_index_code,	
# MAGIC fourth_level_index_name,
# MAGIC A01,
# MAGIC A02,
# MAGIC A03,
# MAGIC A04,
# MAGIC A05,
# MAGIC A06,
# MAGIC A07,
# MAGIC A08,
# MAGIC A09,
# MAGIC A10,
# MAGIC A11,
# MAGIC A12,
# MAGIC F01,
# MAGIC F02,
# MAGIC F03
# MAGIC from t_cpt_planning_rawdata 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC mid_data as (
# MAGIC select
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.period_name,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_code,	
# MAGIC a.index_type_name,	
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,        
# MAGIC t.a_month,
# MAGIC t.a_value
# MAGIC from raw_data a    
# MAGIC LATERAL VIEW STACK(
# MAGIC   15,
# MAGIC   '01', A01,
# MAGIC   '02', A02,
# MAGIC   '03', A03,
# MAGIC   '04', A04,
# MAGIC   '05', A05,
# MAGIC   '06', A06,
# MAGIC   '07', A07,
# MAGIC   '08', A08,
# MAGIC   '09', A09,
# MAGIC   '10', A10,
# MAGIC   '11', A11,
# MAGIC   '12', A12,
# MAGIC   'F01', F01,
# MAGIC   'F02', F02,
# MAGIC   'F03', F03
# MAGIC ) t AS a_month, a_value
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_data as (
# MAGIC select
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_code,	
# MAGIC a.index_type_name,	
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,   
# MAGIC case when a.a_month like 'F%' 
# MAGIC      then cast((cast(substring(a.plan_cycle,1,4) as integer) + 1) as string)||substring(a.a_month,2,2)  
# MAGIC      else substring(a.plan_cycle,1,4)||a.a_month
# MAGIC       end as a_month,
# MAGIC a.a_value
# MAGIC from mid_data a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC plan_cycle_rawdata as (
# MAGIC select 
# MAGIC cast(plan_cycle as string) as plan_cycle,
# MAGIC cast(cast(start_month as integer) as string) as start_month,
# MAGIC cast(cast(end_month as integer) as string) as end_month
# MAGIC from (
# MAGIC select distinct plan_cycle,start_month,end_month
# MAGIC from t_cpt_planning_rawdata
# MAGIC ) 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC plan_mapping as (
# MAGIC select
# MAGIC plan_cycle,
# MAGIC date_format(add_month, 'yyyyMM') as a_month
# MAGIC from plan_cycle_rawdata
# MAGIC lateral view explode (
# MAGIC sequence (
# MAGIC to_date(concat(start_month, '01'), 'yyyyMMdd'),
# MAGIC to_date(concat(end_month, '01'), 'yyyyMMdd'),
# MAGIC interval 1 month
# MAGIC )
# MAGIC ) as add_month
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_code as index_type_level1_code,	
# MAGIC a.index_type_name as index_type_level1_name,
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,   
# MAGIC substring_index(
# MAGIC regexp_replace(
# MAGIC nvl(a.index_type_code,'')||'|'||
# MAGIC nvl(a.package_item_sub_type_code,'')||'|'||
# MAGIC nvl(a.third_level_index_code,'')||'|'||
# MAGIC nvl(a.fourth_level_index_code,''),
# MAGIC '\\|+$', 
# MAGIC ''),
# MAGIC '|', 
# MAGIC -1) as index_type_level2_code,	
# MAGIC substring_index(
# MAGIC regexp_replace(
# MAGIC nvl(a.index_type_name,'')||'|'||
# MAGIC nvl(a.package_item_sub_type_name,'')||'|'||
# MAGIC nvl(a.third_level_index_name,'')||'|'||
# MAGIC nvl(a.fourth_level_index_name,''),
# MAGIC '\\|+$', 
# MAGIC ''),
# MAGIC '|', 
# MAGIC -1) as index_type_level2_name,  
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from tmp_data a 
# MAGIC inner join plan_mapping b 
# MAGIC on a.plan_cycle = b.plan_cycle 
# MAGIC and a.a_month = b.a_month
# MAGIC where 1 = 1
# MAGIC and to_date(a.a_month, 'yyyyMM') >= add_months(date_trunc('quarter', date(NOW() + INTERVAL 8 HOUR)),-3)
# MAGIC and to_date(a.a_month, 'yyyyMM') < add_months(date_trunc('quarter', date(NOW() + INTERVAL 8 HOUR)),3)
# MAGIC ;

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_pl
# MAGIC with max_plan_cycle_formula as (
# MAGIC select max(period_code) as period_code
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_formula_mapping
# MAGIC where 1 = 1
# MAGIC and formula_type = 'detail_secondary_pl'
# MAGIC and package_item_sub_type_code in (
# MAGIC 'formula-0083',
# MAGIC 'formula-0085',
# MAGIC 'formula-0086',
# MAGIC 'formula-0087',
# MAGIC 'formula-0088',
# MAGIC 'formula-0089'
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_raw_data as (
# MAGIC select a.*
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_formula_mapping a 
# MAGIC inner join max_plan_cycle_formula b 
# MAGIC on a.period_code = b.period_code
# MAGIC where 1 = 1
# MAGIC and a.formula_type = 'detail_secondary_pl'
# MAGIC and a.package_item_sub_type_code in (
# MAGIC 'formula-0083',
# MAGIC 'formula-0085',
# MAGIC 'formula-0086',
# MAGIC 'formula-0087',
# MAGIC 'formula-0088',
# MAGIC 'formula-0089'
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_temp as (
# MAGIC select 
# MAGIC package_item_sub_type_code as index_code,
# MAGIC package_item_sub_type as index_name,
# MAGIC regexp_replace(
# MAGIC formula_code, 
# MAGIC '[()]', 
# MAGIC ''
# MAGIC ) as index_str
# MAGIC from formula_raw_data
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_mapping as (
# MAGIC select 
# MAGIC index_code,
# MAGIC index_name,
# MAGIC explode(split(index_str, '\\+')) as index_str
# MAGIC from formula_temp
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC max_plan_cycle_index as (
# MAGIC select max(period_code) as period_code
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping
# MAGIC where 1 = 1
# MAGIC and indicator_type = 'detail_report'
# MAGIC and index_type_code = 'formula-0141'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC index_mapping as (
# MAGIC select distinct a.package_item_sub_type_code,a.package_item_sub_type 
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping a 
# MAGIC inner join max_plan_cycle_index b 
# MAGIC on a.period_code = b.period_code
# MAGIC where 1 = 1
# MAGIC and a.indicator_type = 'detail_report'
# MAGIC and a.index_type_code = 'formula-0141'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC pl_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,   
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,  
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual a
# MAGIC where data_type = 'P&L'
# MAGIC and index_type_level1_code = 'formula-0141'
# MAGIC union all
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,   
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,  
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst a
# MAGIC where data_type = 'P&L'
# MAGIC and index_type_level1_code = 'formula-0141'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_solo_data_01 as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC b.package_item_sub_type as index_type_level2_name,       
# MAGIC a.a_month as month,
# MAGIC sum(a.a_value) as value
# MAGIC from pl_data a
# MAGIC left join index_mapping b
# MAGIC on a.index_type_level2_code = b.package_item_sub_type_code
# MAGIC where 1 = 1
# MAGIC -- and a.index_type_level2_code in ('formula-0078','formula-0079','formula-0137','formula-0113','formula-0111','formula-0112')
# MAGIC and a.index_type_level2_code in ('formula-0078','formula-0079')
# MAGIC group by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC b.package_item_sub_type, 
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_solo_data_02 as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC c.package_item_sub_type as index_type_level2_name,       
# MAGIC a.a_month as month,
# MAGIC sum(a.a_value) as value
# MAGIC from pl_data a
# MAGIC inner join (
# MAGIC select *
# MAGIC from formula_mapping
# MAGIC where index_code in ('formula-0087','formula-0088')
# MAGIC ) b 
# MAGIC on a.index_type_level2_code = b.index_str
# MAGIC left join index_mapping c
# MAGIC on a.index_type_level2_code = c.package_item_sub_type_code
# MAGIC where 1 = 1
# MAGIC group by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC c.package_item_sub_type, 
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_solo_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_solo_data_01 a
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_solo_data_02 a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_agg_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC b.index_code as index_type_level2_code,	
# MAGIC c.package_item_sub_type as index_type_level2_name,         
# MAGIC a.a_month as month,
# MAGIC sum(a.a_value) as value
# MAGIC from pl_data a
# MAGIC inner join (
# MAGIC select *
# MAGIC from formula_mapping
# MAGIC where index_code not in ('formula-0087','formula-0088') 
# MAGIC ) b 
# MAGIC on a.index_type_level2_code = b.index_str
# MAGIC left join index_mapping c
# MAGIC on b.index_code = c.package_item_sub_type_code
# MAGIC where 1 = 1
# MAGIC group by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC b.index_code,	
# MAGIC c.package_item_sub_type,
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC -- formula_new_data as (
# MAGIC -- select 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,	
# MAGIC -- a.index_type_level1_code,	
# MAGIC -- a.index_type_level1_name,	
# MAGIC -- 'index_formula_9001' as index_type_level2_code,	
# MAGIC -- 'Paid Others' as index_type_level2_name,       
# MAGIC -- a.a_month as month,
# MAGIC -- sum(a.a_value) as value
# MAGIC -- from pl_data a
# MAGIC -- where 1 = 1
# MAGIC -- and a.index_type_level2_code in (
# MAGIC -- 'formula-0069',
# MAGIC -- 'formula-0139',
# MAGIC -- 'formula-0110',
# MAGIC -- 'formula-0062',
# MAGIC -- 'formula-0140',
# MAGIC -- 'formula-0243',
# MAGIC -- 'formula-0244'
# MAGIC -- )
# MAGIC -- group by 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,	
# MAGIC -- a.index_type_level1_code,	
# MAGIC -- a.index_type_level1_name,	
# MAGIC -- a.a_month
# MAGIC -- )
# MAGIC -- ,
# MAGIC
# MAGIC target_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_solo_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_agg_data a
# MAGIC -- union all 
# MAGIC -- select 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,	
# MAGIC -- a.index_type_level1_code,	
# MAGIC -- a.index_type_level1_name,	
# MAGIC -- a.index_type_level2_code,	
# MAGIC -- a.index_type_level2_name,       
# MAGIC -- a.month,
# MAGIC -- a.value
# MAGIC -- from formula_new_data a
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from target_data a
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_budget
# MAGIC with max_plan_cycle_index as (
# MAGIC select max(period_code) as period_code
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping
# MAGIC where 1 = 1
# MAGIC and indicator_type = 'budget'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC index_mapping as (
# MAGIC select distinct index_code,index_name
# MAGIC from (
# MAGIC select distinct a.index_type_code as index_code,a.index_type as index_name
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping a 
# MAGIC inner join max_plan_cycle_index b 
# MAGIC on a.period_code = b.period_code
# MAGIC where 1 = 1
# MAGIC and a.indicator_type = 'budget'
# MAGIC union all
# MAGIC select distinct a.package_item_sub_type_code as index_code,a.package_item_sub_type as index_name
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_index_mapping a
# MAGIC inner join max_plan_cycle_index b 
# MAGIC on a.period_code = b.period_code
# MAGIC where 1 = 1
# MAGIC and a.indicator_type = 'budget'
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC pl_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,   
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,  
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual a
# MAGIC where data_type = 'Budget Planning'
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.channel_code,	
# MAGIC a.channel_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,
# MAGIC a.package_item_sub_type_code,	
# MAGIC a.package_item_sub_type_name,	
# MAGIC a.third_level_index_code,	
# MAGIC a.third_level_index_name,	
# MAGIC a.fourth_level_index_code,	
# MAGIC a.fourth_level_index_name,   
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,  
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst a
# MAGIC where data_type = 'Budget Planning'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_solo_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.a_month as month,
# MAGIC sum(a.a_value) as value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in (
# MAGIC 'formula-0009','formula-0005','formula-0007','formula-0003',
# MAGIC 'formula-0020','formula-0021','formula-0012','formula-0013',
# MAGIC 'formula-0008','formula-0029'
# MAGIC )
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0034','formula-0033','formula-0032','formula-0037','formula-0038',
# MAGIC 'formula-0042','formula-0047','formula-0045','formula-0044','formula-0008','formula-0056'
# MAGIC )
# MAGIC group by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_new_data_01 as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,		
# MAGIC 'index_formula_9002' as index_type_level2_code,	    
# MAGIC a.a_month as month,
# MAGIC sum(a.a_value) as value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in (
# MAGIC 'formula-0020','formula-0012'
# MAGIC )
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0039','formula-0040'
# MAGIC )
# MAGIC group by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC formula_new_data_02 as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,		
# MAGIC 'index_formula_9003' as index_type_level2_code,	     
# MAGIC a.a_month as month,
# MAGIC sum(a.a_value) as value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in (
# MAGIC 'formula-0021','formula-0013'
# MAGIC )
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0043','formula-0046','formula-0048'
# MAGIC )
# MAGIC group by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC target_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC b.index_name as index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC c.index_name as index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_solo_data a
# MAGIC left join index_mapping b
# MAGIC on a.index_type_level1_code = b.index_code
# MAGIC left join index_mapping c
# MAGIC on a.index_type_level2_code = c.index_code
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC b.index_name as index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC 'Free others' as index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_new_data_01 a
# MAGIC left join index_mapping b
# MAGIC on a.index_type_level1_code = b.index_code
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC b.index_name as index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC 'Paid Others' as index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from formula_new_data_02 a
# MAGIC left join index_mapping b
# MAGIC on a.index_type_level1_code = b.index_code
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_gmv_rawdata as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,		
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.value
# MAGIC from target_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in ('formula-0020','formula-0021','formula-0029')
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0037','formula-0038','formula-0042','formula-0047','formula-0045',
# MAGIC 'formula-0044','index_formula_9002','index_formula_9003','formula-0056')
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_gmv_01 as (
# MAGIC select
# MAGIC * except(a.index_type_level2_code, value),
# MAGIC a.index_type_level2_code,
# MAGIC value,
# MAGIC max(case when a.index_type_level2_code = 'formula-0056' then value end) 
# MAGIC over (partition by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	   
# MAGIC a.month
# MAGIC ) as formula_0056
# MAGIC from else_gmv_rawdata a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_gmv_02 as (
# MAGIC select *
# MAGIC from else_gmv_01
# MAGIC WHERE index_type_level2_code IN (
# MAGIC 'formula-0037','formula-0038','formula-0042','formula-0047','formula-0045',
# MAGIC 'formula-0044','index_formula_9002','index_formula_9003'
# MAGIC ) 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_gmv_03 as (
# MAGIC select 
# MAGIC case when index_type_level1_code = 'formula-0020' then 'index_formula-9004'
# MAGIC      when index_type_level1_code = 'formula-0021' then 'index_formula-9005'
# MAGIC      else index_type_level1_code 
# MAGIC       end as index_type_level1_code,
# MAGIC case when index_type_level1_code = 'formula-0020' then '去重后GMV-Free'
# MAGIC      when index_type_level1_code = 'formula-0021' then '去重后GMV-Paid'
# MAGIC      else index_type_level1_name 
# MAGIC       end as index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name
# MAGIC from (
# MAGIC select distinct
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name
# MAGIC from target_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in ('formula-0020','formula-0021')
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0037','formula-0038','formula-0042','formula-0047',
# MAGIC 'formula-0045','formula-0044','index_formula_9002','index_formula_9003')
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_gmv_result as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC b.index_type_level1_code,
# MAGIC b.index_type_level1_name,
# MAGIC a.index_type_level2_code,	
# MAGIC b.index_type_level2_name,    
# MAGIC a.month,
# MAGIC case when a.formula_0056 = 0 then 0 else a.value/a.formula_0056 end as value
# MAGIC from else_gmv_02 a
# MAGIC left join else_gmv_03 b 
# MAGIC on a.index_type_level2_code = b.index_type_level2_code
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_uv_rawdata as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,		
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.value
# MAGIC from target_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in ('formula-0012','formula-0013','formula-0008')
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0037','formula-0038','formula-0042','formula-0047','formula-0045',
# MAGIC 'formula-0044','index_formula_9002','index_formula_9003','formula-0008')
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_uv_01 as (
# MAGIC select
# MAGIC * except(a.index_type_level2_code, value),
# MAGIC a.index_type_level2_code,
# MAGIC value,
# MAGIC max(case when a.index_type_level2_code = 'formula-0008' then value end) 
# MAGIC over (partition by 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	   
# MAGIC a.month
# MAGIC ) as formula_0008
# MAGIC from else_uv_rawdata a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_uv_02 as (
# MAGIC select *
# MAGIC from else_uv_01
# MAGIC where index_type_level2_code in (
# MAGIC 'formula-0037','formula-0038','formula-0042','formula-0047','formula-0045',
# MAGIC 'formula-0044','index_formula_9002','index_formula_9003'
# MAGIC ) 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_uv_03 as (
# MAGIC select 
# MAGIC case when index_type_level1_code = 'formula-0012' then 'index_formula-9006'
# MAGIC      when index_type_level1_code = 'formula-0013' then 'index_formula-9007'
# MAGIC      else index_type_level1_code 
# MAGIC       end as index_type_level1_code,
# MAGIC case when index_type_level1_code = 'formula-0012' then '去重后UV-Free UV'
# MAGIC      when index_type_level1_code = 'formula-0013' then '去重后UV-Paid UV'
# MAGIC      else index_type_level1_name 
# MAGIC       end as index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name
# MAGIC from (
# MAGIC select distinct
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name
# MAGIC from target_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in ('formula-0012','formula-0013')
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0037','formula-0038','formula-0042','formula-0047',
# MAGIC 'formula-0045','formula-0044','index_formula_9002','index_formula_9003')
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_uv_result as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC b.index_type_level1_code,
# MAGIC b.index_type_level1_name,
# MAGIC a.index_type_level2_code,	
# MAGIC b.index_type_level2_name,    
# MAGIC a.month,
# MAGIC case when a.formula_0008 = 0 then 0 else a.value/a.formula_0008 end as value
# MAGIC from else_uv_02 a
# MAGIC left join else_uv_03 b 
# MAGIC on a.index_type_level2_code = b.index_type_level2_code
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC -- distinct_uv_rawdata as (
# MAGIC -- select 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,		
# MAGIC -- a.index_type_level2_code,	    
# MAGIC -- a.month,
# MAGIC -- a.value
# MAGIC -- from target_data a
# MAGIC -- where 1 = 1
# MAGIC -- and a.index_type_level1_code in ('formula-0009','formula-0008')
# MAGIC -- and a.index_type_level2_code in ('formula-0034','formula-0008')
# MAGIC -- )
# MAGIC -- ,
# MAGIC
# MAGIC -- distinct_uv_01 as (
# MAGIC -- select
# MAGIC -- * except(a.index_type_level2_code, value),
# MAGIC -- a.index_type_level2_code,
# MAGIC -- value,
# MAGIC -- max(case when a.index_type_level2_code = 'formula-0008' then value end) 
# MAGIC -- over (partition by 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,	   
# MAGIC -- a.month
# MAGIC -- ) as formula_0008
# MAGIC -- from distinct_uv_rawdata a
# MAGIC -- )
# MAGIC -- ,
# MAGIC
# MAGIC -- distinct_uv_02 as (
# MAGIC -- select *
# MAGIC -- from distinct_uv_01
# MAGIC -- where index_type_level2_code in ('formula-0034') 
# MAGIC -- )
# MAGIC -- ,
# MAGIC
# MAGIC -- distinct_uv_result as (
# MAGIC -- select 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,	
# MAGIC -- 'index_formula-9008' as index_type_level1_code,
# MAGIC -- 'UV_去重后' as index_type_level1_name,
# MAGIC -- 'index_formula-9009' as index_type_level2_code,	
# MAGIC -- 'Total去重后' as index_type_level2_name,    
# MAGIC -- a.month,
# MAGIC -- case when a.formula_0008 = 0 then 0 else a.value/a.formula_0008 end as value
# MAGIC -- from distinct_uv_02 a
# MAGIC -- )
# MAGIC -- ,
# MAGIC
# MAGIC else_cvr_result as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,		
# MAGIC 'index_formula_0002' as index_type_level1_code,
# MAGIC 'UV去重后计算CVR' as index_type_level1_name,
# MAGIC 'index_formula_0003' as index_type_level2_code,	
# MAGIC 'Total去重后计算CVR' as index_type_level2_name,      
# MAGIC a.month,
# MAGIC a.value
# MAGIC from target_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in ('formula-0007')
# MAGIC and a.index_type_level2_code in ('formula-0033')
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC bedget_result as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from target_data a
# MAGIC where a.index_type_level2_code not in ('formula-0008','formula-0056')
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from else_gmv_result a
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from else_uv_result a
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from else_cvr_result a
# MAGIC -- union all 
# MAGIC -- select 
# MAGIC -- a.data_type,
# MAGIC -- a.type,
# MAGIC -- a.plan_cycle,
# MAGIC -- a.bu_code,	
# MAGIC -- a.bu_name,	
# MAGIC -- a.site_code,	
# MAGIC -- a.site_name,	
# MAGIC -- a.store_code,	
# MAGIC -- a.store_name,	
# MAGIC -- a.category_code,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_code,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.product_line_group_code,	
# MAGIC -- a.product_line_group_name,	
# MAGIC -- a.index_type_level1_code,	
# MAGIC -- a.index_type_level1_name,	
# MAGIC -- a.index_type_level2_code,	
# MAGIC -- a.index_type_level2_name,       
# MAGIC -- a.month,
# MAGIC -- a.value
# MAGIC -- from distinct_uv_result a
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC a.plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from bedget_result a
# MAGIC ;

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC with union_data as (
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC case when a.type = 'Actual' then '/' else a.plan_cycle end as plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_budget a   
# MAGIC union all 
# MAGIC select 
# MAGIC a.data_type,
# MAGIC a.type,
# MAGIC case when a.type = 'Actual' then '/' else a.plan_cycle end as plan_cycle,
# MAGIC a.bu_code,	
# MAGIC a.bu_name,	
# MAGIC a.site_code,	
# MAGIC a.site_name,	
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC a.category_code,	
# MAGIC a.category_name,	
# MAGIC a.brand_code,	
# MAGIC a.brand_name,	
# MAGIC a.product_line_group_code,	
# MAGIC a.product_line_group_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level1_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.index_type_level2_name,       
# MAGIC a.month,
# MAGIC a.value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_pl a
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dws}.fin.dws_cpt_planning_mf(
# MAGIC data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC bu_code,
# MAGIC bu_name,
# MAGIC site_code,
# MAGIC site_name,
# MAGIC store_code,
# MAGIC store_name,
# MAGIC category_code,
# MAGIC category_name,
# MAGIC brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC index_type_level1_code,
# MAGIC index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name,
# MAGIC month,
# MAGIC value,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC data_type,
# MAGIC type,
# MAGIC plan_cycle,
# MAGIC bu_code,
# MAGIC bu_name,
# MAGIC site_code,
# MAGIC site_name,
# MAGIC store_code,
# MAGIC store_name,
# MAGIC category_code,
# MAGIC category_name,
# MAGIC brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC index_type_level1_code,
# MAGIC index_type_level1_name,
# MAGIC index_type_level2_code,
# MAGIC index_type_level2_name,
# MAGIC month,
# MAGIC value,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from union_data
# MAGIC ;