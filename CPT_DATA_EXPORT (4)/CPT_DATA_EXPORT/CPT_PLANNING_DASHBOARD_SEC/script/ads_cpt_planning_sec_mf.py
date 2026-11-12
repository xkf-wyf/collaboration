# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual_sec
# MAGIC with dim_site as (
# MAGIC select distinct 
# MAGIC national_ex25 as store_name,
# MAGIC national_ex3 as cpt_site_name,
# MAGIC national_ex4 as pbi_site_name
# MAGIC from ${spark.var.catalog.dim}.cd.dim_store a 
# MAGIC where national_ex3 = 'TMALL'
# MAGIC and a.national_ex2 in ('EC','SOCIAL')
# MAGIC and a.national_ex4  not like '%POP%' 
# MAGIC and a.national_ex4  not in ('REDBOOK FGS','SPECIAL WS','SHEIN FGS') --20260509-新增筛选条件
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC t_cpt_planning_rawdata as (
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
# MAGIC case when a.site_code = 'TMALL' then b.pbi_site_name
# MAGIC      else a.site_code
# MAGIC       end as site_code,
# MAGIC case when a.site_name = 'TMALL' then b.pbi_site_name
# MAGIC      else a.site_name
# MAGIC       end as site_name,
# MAGIC a.store_code,	
# MAGIC a.store_name,	
# MAGIC case when a.store_name like '%CBE' then 'CBE' else 'LEC' end as store_type, 
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
# MAGIC left join dim_site b 
# MAGIC on upper(a.store_name) = upper(b.store_name)
# MAGIC and upper(a.site_name) = upper(b.cpt_site_name)
# MAGIC where 1 = 1
# MAGIC and a_month < date_format(current_date(), 'yyyyMM')
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec
# MAGIC with dim_site as (
# MAGIC select distinct 
# MAGIC national_ex25 as store_name,
# MAGIC national_ex3 as cpt_site_name,
# MAGIC national_ex4 as pbi_site_name
# MAGIC from ${spark.var.catalog.dim}.cd.dim_store a 
# MAGIC where national_ex3 = 'TMALL'
# MAGIC and a.national_ex2 in ('EC','SOCIAL')
# MAGIC and a.national_ex4  not like '%POP%' 
# MAGIC and a.national_ex4  not in ('REDBOOK FGS','SPECIAL WS','SHEIN FGS') --20260509-新增筛选条件
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC t_cpt_planning_rawdata as (
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
# MAGIC case when a.site_code = 'TMALL' then c.pbi_site_name
# MAGIC      else a.site_code
# MAGIC       end as site_code,
# MAGIC case when a.site_name = 'TMALL' then c.pbi_site_name
# MAGIC      else a.site_name
# MAGIC       end as site_name,
# MAGIC a.store_code,	
# MAGIC a.store_name,
# MAGIC case when a.store_name like '%CBE' then 'CBE' else 'LEC' end as store_type, 
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
# MAGIC left join dim_site c
# MAGIC on upper(a.store_name) = upper(c.store_name)
# MAGIC and upper(a.site_name) = upper(c.cpt_site_name)
# MAGIC ;

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_pl_sec
# MAGIC with max_plan_cycle_formula as (
# MAGIC select max(period_code) as period_code
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_planning_formula_mapping
# MAGIC where 1 = 1
# MAGIC and formula_type = 'detail_secondary_pl'
# MAGIC and package_item_sub_type_code in (
# MAGIC 'formula-0083',
# MAGIC 'formula-0085',
# MAGIC 'formula-0087',
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
# MAGIC 'formula-0087',
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
# MAGIC actual_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC to_date(concat(a.a_month, '01'), 'yyyyMMdd') AS dt,
# MAGIC a.a_value
# MAGIC from (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual_sec a
# MAGIC where data_type = 'P&L'
# MAGIC and index_type_level1_code = 'formula-0141'
# MAGIC group by 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC max_actual_month as (
# MAGIC select max(a_month) as a_month from actual_data
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC plan_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a
# MAGIC where data_type = 'P&L'
# MAGIC and index_type_level1_code = 'formula-0141'
# MAGIC and (a.plan_cycle like '%12'
# MAGIC  or a.plan_cycle like '%03'
# MAGIC  or a.plan_cycle like '%06'
# MAGIC  or a.plan_cycle like '%09')
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a
# MAGIC where data_type = 'P&L'
# MAGIC and index_type_level1_code = 'formula-0141'
# MAGIC and site_name = 'DOUYIN'
# MAGIC and plan_cycle = '202604'
# MAGIC and bu_name = 'BEAUTY&WELLBEING'
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC max_plan_cycle as (
# MAGIC select 
# MAGIC distinct plan_cycle
# MAGIC from (
# MAGIC select 
# MAGIC plan_cycle,
# MAGIC a_month,
# MAGIC row_number() over(partition by a_month order by plan_cycle desc) as rn
# MAGIC from (
# MAGIC select distinct plan_cycle,a.a_month
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a 
# MAGIC inner join max_actual_month b 
# MAGIC on a.a_month > b.a_month 
# MAGIC and a.a_month <= date_format(NOW() + INTERVAL 8 HOUR, 'yyyyMM')
# MAGIC and a.data_type = 'P&L' 
# MAGIC ) b
# MAGIC ) c
# MAGIC where rn = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC latest_plan_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC to_date(concat(a.a_month, '01'), 'yyyyMMdd') AS dt,
# MAGIC a.a_value
# MAGIC from (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a
# MAGIC inner join max_actual_month c  
# MAGIC on a.a_month > c.a_month
# MAGIC and a.a_month <= date_format(NOW() + INTERVAL 8 HOUR, 'yyyyMM')
# MAGIC and a.data_type = 'P&L'
# MAGIC and a.index_type_level1_code = 'formula-0141'
# MAGIC and a.plan_cycle in (select plan_cycle from max_plan_cycle)
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC py_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value as actual_value,
# MAGIC b.a_value as py_value
# MAGIC from actual_data a
# MAGIC left join actual_data b
# MAGIC on a.site_name = b.site_name 
# MAGIC and a.store_type = b.store_type
# MAGIC and a.bu_name = b.bu_name
# MAGIC and a.category_name = b.category_name 
# MAGIC and a.brand_name = b.brand_name 
# MAGIC and a.index_type_level2_code = b.index_type_level2_code
# MAGIC and add_months(a.dt, -12) = b.dt
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC latest_plan_py_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value as actual_value,
# MAGIC b.a_value as py_value
# MAGIC from latest_plan_data a
# MAGIC left join actual_data b
# MAGIC on a.site_name = b.site_name 
# MAGIC and a.store_type = b.store_type
# MAGIC and a.bu_name = b.bu_name
# MAGIC and a.category_name = b.category_name 
# MAGIC and a.brand_name = b.brand_name 
# MAGIC and a.index_type_level2_code = b.index_type_level2_code
# MAGIC and add_months(a.dt, -12) = b.dt
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC latest_py_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.actual_value,
# MAGIC a.py_value
# MAGIC from py_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.actual_value,
# MAGIC a.py_value
# MAGIC from latest_plan_py_data a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC pl_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.actual_value,
# MAGIC 0 as plan_value,
# MAGIC a.py_value
# MAGIC from latest_py_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC 0 as actual_value,
# MAGIC a.a_value as plan_value,
# MAGIC 0 as py_value
# MAGIC from plan_data a
# MAGIC ) a 
# MAGIC group by 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,		
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC solo_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0078',
# MAGIC 'formula-0079',
# MAGIC 'formula-0117','formula-0063','formula-0131','formula-0251','formula-0250','formula-0249',
# MAGIC 'formula-0066','formula-0067',
# MAGIC 'formula-0064','formula-0065'
# MAGIC )
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC agg_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC b.index_code as index_type_level2_code,	       
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from pl_data a
# MAGIC inner join formula_mapping b 
# MAGIC on a.index_type_level2_code = b.index_str
# MAGIC where 1 = 1
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC b.index_code,	       
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_01 as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC 'Sample+GWP' as index_type_level2_code,	    
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0117','formula-0063','formula-0131','formula-0251','formula-0250','formula-0249'
# MAGIC )
# MAGIC group by 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,		    
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_02 as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC 'TP' as index_type_level2_code,	    
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0066','formula-0067'
# MAGIC )
# MAGIC group by 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,		    
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_03 as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC 'OP' as index_type_level2_code,	    
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from pl_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0064','formula-0065'
# MAGIC )
# MAGIC group by 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,		    
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC union_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from solo_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from agg_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from new_data_01 a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from new_data_02 a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level2_code,	    
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from new_data_03 a
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC case when a.index_type_level2_code = 'formula-0078' then 'GMV'
# MAGIC      when a.index_type_level2_code = 'formula-0079' then 'Offtake GSV'
# MAGIC      when a.index_type_level2_code = 'formula-0117' then 'UL Premium'
# MAGIC      when a.index_type_level2_code = 'formula-0063' then 'Non-UL Premium'
# MAGIC      when a.index_type_level2_code = 'formula-0131' then 'Sold Bundle Pack'
# MAGIC      when a.index_type_level2_code = 'formula-0251' then 'Instore Agency'
# MAGIC      when a.index_type_level2_code = 'formula-0250' then 'POSM'
# MAGIC      when a.index_type_level2_code = 'formula-0249' then 'Digital Premium'
# MAGIC      when a.index_type_level2_code = 'formula-0066' then 'EC TP-自播'
# MAGIC      when a.index_type_level2_code = 'formula-0067' then 'EC TP-非自播'
# MAGIC      when a.index_type_level2_code = 'formula-0064' then 'Transportation'
# MAGIC      when a.index_type_level2_code = 'formula-0065' then 'Promotion Package & Repacking'
# MAGIC      when a.index_type_level2_code = 'formula-0083' then 'TO'
# MAGIC      when a.index_type_level2_code = 'formula-0085' then 'GP'
# MAGIC      when a.index_type_level2_code = 'formula-0087' then 'PFM'
# MAGIC      when a.index_type_level2_code = 'formula-0089' then 'Channel PBO'
# MAGIC      when a.index_type_level2_code = 'Sample+GWP' then 'Sample+GWP'
# MAGIC      when a.index_type_level2_code = 'TP' then 'TP'
# MAGIC      when a.index_type_level2_code = 'OP' then 'OP'
# MAGIC       end as kpi_name,
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from union_data a
# MAGIC ;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create or replace table ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_budget_sec
# MAGIC with scope_actual as (
# MAGIC select 
# MAGIC distinct 
# MAGIC a.site_name,	
# MAGIC a.store_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,		
# MAGIC a.a_month
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual_sec a
# MAGIC where a.data_type = 'Budget Planning'
# MAGIC and a.index_type_level1_code = 'formula-0003'
# MAGIC and a.index_type_level2_code = 'formula-0032'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC rawdata_actual as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual_sec a
# MAGIC inner join scope_actual b
# MAGIC on a.site_name = 	b.site_name
# MAGIC and a.store_name = b.store_name
# MAGIC and a.store_type = b.store_type
# MAGIC and a.bu_name = b.bu_name
# MAGIC and a.category_name = b.category_name
# MAGIC and a.brand_name = b.brand_name
# MAGIC and a.a_month = b.a_month
# MAGIC and a.data_type = 'Budget Planning'
# MAGIC and a.index_type_level1_code = 'formula-0129'
# MAGIC and a.index_type_level2_code = 'formula-0129'
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_actual_sec a
# MAGIC where a.data_type = 'Budget Planning'
# MAGIC and a.index_type_level1_code not in ('formula-0129')
# MAGIC and a.index_type_level2_code not in ('formula-0129') 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC scope_fcst as (
# MAGIC select 
# MAGIC distinct 
# MAGIC a.plan_cycle,
# MAGIC a.site_name,	
# MAGIC a.store_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,		
# MAGIC a.a_month
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a
# MAGIC where data_type = 'Budget Planning'
# MAGIC and a.index_type_level1_code = 'formula-0003'
# MAGIC and a.index_type_level2_code = 'formula-0032'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC rawdata_fcst as (
# MAGIC select 
# MAGIC a.plan_cycle,
# MAGIC a.site_name,	
# MAGIC a.store_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a
# MAGIC inner join scope_fcst b
# MAGIC on a.plan_cycle = b.plan_cycle
# MAGIC and a.site_name = b.site_name
# MAGIC and a.store_name = b.store_name
# MAGIC and a.store_type = b.store_type
# MAGIC and a.bu_name = b.bu_name
# MAGIC and a.category_name = b.category_name
# MAGIC and a.brand_name = b.brand_name
# MAGIC and a.a_month = b.a_month
# MAGIC and a.data_type = 'Budget Planning'
# MAGIC and a.index_type_level1_code = 'formula-0129'
# MAGIC and a.index_type_level2_code = 'formula-0129'
# MAGIC union all 
# MAGIC select 
# MAGIC a.plan_cycle,
# MAGIC a.site_name,	
# MAGIC a.store_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_rawdata_fcst_sec a
# MAGIC where a.data_type = 'Budget Planning'
# MAGIC and a.index_type_level1_code not in ('formula-0129')
# MAGIC and a.index_type_level2_code not in ('formula-0129') 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC actual_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC to_date(concat(a.a_month, '01'), 'yyyyMMdd') AS dt,
# MAGIC a.a_value
# MAGIC from (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from rawdata_actual a
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC max_actual_month as (
# MAGIC select max(a_month) as a_month from actual_data
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC plan_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from rawdata_fcst a
# MAGIC where 1 = 1
# MAGIC and (a.plan_cycle like '%12'
# MAGIC  or a.plan_cycle like '%03'
# MAGIC  or a.plan_cycle like '%06'
# MAGIC  or a.plan_cycle like '%09')
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from rawdata_fcst a
# MAGIC where 1 = 1
# MAGIC and site_name = 'DOUYIN'
# MAGIC and plan_cycle = '202604'
# MAGIC and bu_name = 'BEAUTY&WELLBEING'
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC max_plan_cycle as (
# MAGIC select 
# MAGIC distinct plan_cycle
# MAGIC from (
# MAGIC select 
# MAGIC plan_cycle,
# MAGIC a_month,
# MAGIC row_number() over(partition by a_month order by plan_cycle desc) as rn
# MAGIC from (
# MAGIC select distinct plan_cycle,a.a_month
# MAGIC from rawdata_fcst a 
# MAGIC inner join max_actual_month b 
# MAGIC on a.a_month > b.a_month 
# MAGIC and a.a_month <= date_format(NOW() + INTERVAL 8 HOUR, 'yyyyMM')
# MAGIC ) b
# MAGIC ) c
# MAGIC where rn = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC latest_plan_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC to_date(concat(a.a_month, '01'), 'yyyyMMdd') AS dt,
# MAGIC a.a_value
# MAGIC from (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.a_value) as a_value
# MAGIC from rawdata_fcst a
# MAGIC inner join max_actual_month c  
# MAGIC on a.a_month > c.a_month
# MAGIC and a.a_month <= date_format(NOW() + INTERVAL 8 HOUR, 'yyyyMM')
# MAGIC and a.plan_cycle in (select plan_cycle from max_plan_cycle)
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC py_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value as actual_value,
# MAGIC b.a_value as py_value
# MAGIC from actual_data a
# MAGIC left join actual_data b
# MAGIC on a.site_name = b.site_name 
# MAGIC and a.store_type = b.store_type
# MAGIC and a.bu_name = a.bu_name
# MAGIC and a.category_name = b.category_name 
# MAGIC and a.brand_name = b.brand_name 
# MAGIC and a.index_type_level1_code = b.index_type_level1_code 
# MAGIC and a.index_type_level2_code = b.index_type_level2_code
# MAGIC and add_months(a.dt, -12) = b.dt
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC latest_plan_py_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.a_value as actual_value,
# MAGIC b.a_value as py_value
# MAGIC from latest_plan_data a
# MAGIC left join actual_data b
# MAGIC on a.site_name = b.site_name 
# MAGIC and a.store_type = b.store_type
# MAGIC and a.bu_name = a.bu_name
# MAGIC and a.category_name = b.category_name 
# MAGIC and a.brand_name = b.brand_name 
# MAGIC and a.index_type_level1_code = b.index_type_level1_code 
# MAGIC and a.index_type_level2_code = b.index_type_level2_code
# MAGIC and add_months(a.dt, -12) = b.dt
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC latest_py_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.actual_value,
# MAGIC a.py_value
# MAGIC from py_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.actual_value,
# MAGIC a.py_value
# MAGIC from latest_plan_py_data a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC budget_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC a.actual_value,
# MAGIC 0 as plan_value,
# MAGIC a.py_value
# MAGIC from latest_py_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month,
# MAGIC 0 as actual_value,
# MAGIC a.a_value as plan_value,
# MAGIC 0 as py_value
# MAGIC from plan_data a
# MAGIC ) a 
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.index_type_level2_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC solo_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from budget_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in (
# MAGIC 'formula-0007','formula-0005','formula-0003','formula-0009','formula-0129','formula-0012'
# MAGIC )
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0033','formula-0032','formula-0034','formula-0129','formula-0036'
# MAGIC )
# MAGIC group by 
# MAGIC a.site_name,
# MAGIC a.store_type,	
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_base as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,month,
# MAGIC (case when actual_value_0007 = 0 then 0 else actual_value_0005 / actual_value_0007 end)          as actual_A,    -- CVR%
# MAGIC (case when actual_value_0005 = 0 then 0 else actual_value_0003 / actual_value_0005 end)          as actual_B,    -- 客单价
# MAGIC actual_value_0129                   as actual_C,    -- 退后GMV
# MAGIC (case when actual_value_0003 = 0 then 0 else 1 - actual_value_0129 / actual_value_0003 end)     as actual_D,    -- 退货率
# MAGIC (case when actual_value_0007 = 0 then 0 else actual_value_0009 / actual_value_0007 end)        as actual_E,    -- UV去重系数
# MAGIC (case when actual_value_0009 = 0 then 0 else actual_value_0012 / actual_value_0009 end)        as actual_F,    -- Free占比
# MAGIC
# MAGIC (case when plan_value_0007 = 0 then 0 else plan_value_0005 / plan_value_0007 end)          as plan_A,    -- CVR%
# MAGIC (case when plan_value_0005 = 0 then 0 else plan_value_0003 / plan_value_0005 end)          as plan_B,    -- 客单价
# MAGIC plan_value_0129                   as plan_C,    -- 退后GMV
# MAGIC (case when plan_value_0003 = 0 then 0 else 1 - plan_value_0129 / plan_value_0003 end)     as plan_D,    -- 退货率
# MAGIC (case when plan_value_0007 = 0 then 0 else plan_value_0009 / plan_value_0007 end)        as plan_E,    -- UV去重系数
# MAGIC (case when plan_value_0009 = 0 then 0 else plan_value_0012 / plan_value_0009 end)        as plan_F,    -- Free占比
# MAGIC
# MAGIC (case when py_value_0007 = 0 then 0 else py_value_0005 / py_value_0007 end)          as py_A,    -- CVR%
# MAGIC (case when py_value_0005 = 0 then 0 else py_value_0003 / py_value_0005 end)          as py_B,    -- 客单价
# MAGIC py_value_0129                   as py_C,    -- 退后GMV
# MAGIC (case when py_value_0003 = 0 then 0 else 1 - py_value_0129 / py_value_0003 end)     as py_D,    -- 退货率
# MAGIC (case when py_value_0007 = 0 then 0 else py_value_0009 / py_value_0007 end)        as py_E,    -- UV去重系数
# MAGIC (case when py_value_0009 = 0 then 0 else py_value_0012 / py_value_0009 end)        as py_F    -- Free占比
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.index_type_level1_code,a.month,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when index_type_level1_code = 'formula-0003' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as actual_value_0003,
# MAGIC max(case when index_type_level1_code = 'formula-0003' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as plan_value_0003,
# MAGIC max(case when index_type_level1_code = 'formula-0003' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as py_value_0003,
# MAGIC max(case when index_type_level1_code = 'formula-0005' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as actual_value_0005,
# MAGIC max(case when index_type_level1_code = 'formula-0005' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as plan_value_0005,
# MAGIC max(case when index_type_level1_code = 'formula-0005' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as py_value_0005,
# MAGIC max(case when index_type_level1_code = 'formula-0007' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as actual_value_0007,
# MAGIC max(case when index_type_level1_code = 'formula-0007' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as plan_value_0007,
# MAGIC max(case when index_type_level1_code = 'formula-0007' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as py_value_0007,
# MAGIC max(case when index_type_level1_code = 'formula-0009' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as actual_value_0009,
# MAGIC max(case when index_type_level1_code = 'formula-0009' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as plan_value_0009,
# MAGIC max(case when index_type_level1_code = 'formula-0009' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as py_value_0009,
# MAGIC max(case when index_type_level1_code = 'formula-0012' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as actual_value_0012,
# MAGIC max(case when index_type_level1_code = 'formula-0012' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as plan_value_0012,
# MAGIC max(case when index_type_level1_code = 'formula-0012' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as py_value_0012,
# MAGIC max(case when index_type_level1_code = 'formula-0129' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as actual_value_0129,
# MAGIC max(case when index_type_level1_code = 'formula-0129' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as plan_value_0129,
# MAGIC max(case when index_type_level1_code = 'formula-0129' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,month) as py_value_0129
# MAGIC from solo_data a
# MAGIC where 1 = 1
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_01 as (
# MAGIC select site_name,store_type,bu_name,category_name,brand_name,'index_0001' as index_type_level1_code,month,
# MAGIC case when actual_A = 0 then 0
# MAGIC      when actual_B = 0 then 0
# MAGIC      when (1 - actual_D) = 0 then 0
# MAGIC      else (((actual_C / (1 - actual_D)) / actual_B) / actual_A) * actual_E * actual_F
# MAGIC       end as actual_value,
# MAGIC case when plan_A = 0 then 0
# MAGIC      when plan_B = 0 then 0
# MAGIC      when (1 - plan_D) = 0 then 0
# MAGIC      else (((plan_C / (1 - plan_D)) / plan_B) / plan_A) * plan_E * plan_F
# MAGIC       end as plan_value,
# MAGIC case when py_A = 0 then 0
# MAGIC      when py_B = 0 then 0
# MAGIC      when (1 - py_D) = 0 then 0
# MAGIC      else (((py_C / (1 - py_D)) / py_B) / py_A) * py_E * py_F
# MAGIC       end as py_value
# MAGIC from new_data_base
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_02 as (
# MAGIC select site_name,store_type,bu_name,category_name,brand_name,'index_0002' as index_type_level1_code,month,
# MAGIC case when actual_A = 0 then 0
# MAGIC      when actual_B = 0 then 0
# MAGIC      when (1 - actual_D) = 0 then 0
# MAGIC      else (((actual_C / (1 - actual_D)) / actual_B) / actual_A) * actual_E * (1 - actual_F)
# MAGIC       end as actual_value,
# MAGIC case when plan_A = 0 then 0
# MAGIC      when plan_B = 0 then 0
# MAGIC      when (1 - plan_D) = 0 then 0
# MAGIC      else (((plan_C / (1 - plan_D)) / plan_B) / plan_A) * plan_E * (1 - plan_F)
# MAGIC       end as plan_value,
# MAGIC case when py_A = 0 then 0
# MAGIC      when py_B = 0 then 0
# MAGIC      when (1 - py_D) = 0 then 0
# MAGIC      else (((py_C / (1 - py_D)) / py_B) / py_A) * py_E * (1 - py_F)
# MAGIC       end as py_value
# MAGIC from new_data_base
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC agg_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.a_month as month,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from budget_data a
# MAGIC where 1 = 1
# MAGIC and a.index_type_level1_code in (
# MAGIC 'formula-0020','formula-0021','formula-0016','formula-0017'
# MAGIC )
# MAGIC and a.index_type_level2_code in (
# MAGIC 'formula-0037','formula-0038','formula-0039','formula-0040',
# MAGIC 'formula-0042','formula-0043','formula-0044','formula-0045','formula-0046','formula-0047','formula-0048'
# MAGIC )
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.a_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC union_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from solo_data a
# MAGIC where index_type_level1_code in ('formula-0007','formula-0005','formula-0003')
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from agg_data a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from new_data_01 a
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.index_type_level1_code,	
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from new_data_02 a
# MAGIC )
# MAGIC
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC case when a.index_type_level1_code = 'formula-0020' then 'GMV Free'
# MAGIC      when a.index_type_level1_code = 'formula-0021' then 'GMV Paid'
# MAGIC      when a.index_type_level1_code = 'formula-0007' then 'UV'
# MAGIC      when a.index_type_level1_code = 'index_0001' then 'Free UV'
# MAGIC      when a.index_type_level1_code = 'index_0002' then 'Paid UV'
# MAGIC      when a.index_type_level1_code = 'formula-0005' then 'Shopper'
# MAGIC      when a.index_type_level1_code = 'formula-0016' then 'Free shopper'
# MAGIC      when a.index_type_level1_code = 'formula-0017' then 'Paid shopper'
# MAGIC      when a.index_type_level1_code = 'formula-0003' then '退前GMV'
# MAGIC       end as kpi_name,
# MAGIC a.month,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from union_data a
# MAGIC ;

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC with raw_data as (
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.kpi_name,
# MAGIC a.month,
# MAGIC date_format(to_date(concat(a.month,'01'),'yyyyMMdd'),'MMM') as period,
# MAGIC substring(a.month,1,4) as year,
# MAGIC case when period in ('Jan','Feb','Mar') then 'Q1'
# MAGIC      when period in ('Apr','May','Jun') then 'Q2'
# MAGIC      when period in ('Jul','Aug','Sep') then 'Q3'
# MAGIC      when period in ('Oct','Nov','Dec') then 'Q4'
# MAGIC       end as quarter,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_budget_sec a   
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,
# MAGIC a.store_type,
# MAGIC a.bu_name,		
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.kpi_name,
# MAGIC a.month,
# MAGIC date_format(to_date(concat(a.month,'01'),'yyyyMMdd'),'MMM') as period,
# MAGIC substring(a.month,1,4) as year,
# MAGIC case when period in ('Jan','Feb','Mar') then 'Q1'
# MAGIC      when period in ('Apr','May','Jun') then 'Q2'
# MAGIC      when period in ('Jul','Aug','Sep') then 'Q3'
# MAGIC      when period in ('Oct','Nov','Dec') then 'Q4'
# MAGIC       end as quarter,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_cpt_planning_result_pl_sec a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC aq_data as (
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.kpi_name,
# MAGIC a.year,
# MAGIC a.period,
# MAGIC a.actual_value,
# MAGIC a.plan_value,
# MAGIC a.py_value
# MAGIC from raw_data a 
# MAGIC union all 
# MAGIC select 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.kpi_name,
# MAGIC a.year,
# MAGIC a.quarter as period,
# MAGIC sum(a.actual_value) as actual_value,
# MAGIC sum(a.plan_value) as plan_value,
# MAGIC sum(a.py_value) as py_value
# MAGIC from raw_data a
# MAGIC group by 
# MAGIC a.site_name,	
# MAGIC a.store_type,
# MAGIC a.bu_name,	
# MAGIC a.category_name,	
# MAGIC a.brand_name,	
# MAGIC a.kpi_name,
# MAGIC a.year,
# MAGIC a.quarter
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC -- new_data_01 as (
# MAGIC -- select 
# MAGIC -- a.site_name,	
# MAGIC -- a.category_name,	
# MAGIC -- a.brand_name,	
# MAGIC -- a.year,
# MAGIC -- a.period,
# MAGIC -- case when a.kpi_name = 'Offtake GSV' then 'GSV GR%'
# MAGIC --      when a.kpi_name = 'TO' then 'USG%'
# MAGIC --       end as kpi_name,
# MAGIC -- case when a.py_value = 0 then 100 else (a.actual_value/a.py_value-1)*100 end as actual_value,
# MAGIC -- case when a.py_value = 0 then 100 else (a.plan_value/a.py_value-1)*100 end as plan_value,
# MAGIC -- null as py_value
# MAGIC -- from aq_data a 
# MAGIC -- where 1 = 1
# MAGIC -- and kpi_name in ('Offtake GSV','TO')
# MAGIC -- )
# MAGIC -- ,
# MAGIC
# MAGIC new_data_02 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Channel PBO% TO' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'Channel PBO' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'TO' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'Channel PBO' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'TO' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'Channel PBO' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'TO' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('Channel PBO','TO')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_03 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'PFM% GMV' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'PFM' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'GMV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'PFM' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'GMV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'PFM' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'GMV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('PFM','GMV')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_04 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'CVR' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'Shopper' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'UV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'Shopper' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'UV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'Shopper' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'UV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('Shopper','UV')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_05 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Free CVR' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'Free shopper' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'Free UV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'Free shopper' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'Free UV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'Free shopper' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'Free UV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('Free shopper','Free UV')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_06 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Paid CVR' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'Paid shopper' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'Paid UV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'Paid shopper' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'Paid UV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'Paid shopper' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'Paid UV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('Paid shopper','Paid UV')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_07 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'BZ' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = '退前GMV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'Shopper' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = '退前GMV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'Shopper' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = '退前GMV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'Shopper' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('退前GMV','Shopper')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_08 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Free BZ' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'GMV Free' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'Free shopper' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'GMV Free' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'Free shopper' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'GMV Free' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'Free shopper' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('GMV Free','Free shopper')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_09 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Paid BZ' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else num_actual/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else num_plan/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else num_py/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'GMV Paid' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'Paid shopper' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'GMV Paid' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'Paid shopper' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'GMV Paid' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'Paid shopper' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('GMV Paid','Paid shopper')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_10 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Cost per UV' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else -num_actual*1000/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else -num_plan*1000/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else -num_py*1000/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'PFM' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'UV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'PFM' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'UV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'PFM' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'UV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('PFM','UV')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC new_data_11 as (
# MAGIC select distinct 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,
# MAGIC 'Paid Cost per UV' as kpi_name,
# MAGIC case when den_actual = 0 then 0 else -num_actual*1000/den_actual end as actual_value,
# MAGIC case when den_plan = 0 then 0 else -num_plan*1000/den_plan end as plan_value,
# MAGIC case when den_py = 0 then 0 else -num_py*1000/den_py end as py_value
# MAGIC from (
# MAGIC select
# MAGIC a.site_name,a.store_type,a.bu_name,a.category_name,a.brand_name,a.year,a.period,a.kpi_name,
# MAGIC a.actual_value,a.plan_value,a.py_value,
# MAGIC max(case when kpi_name = 'PFM' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_actual,
# MAGIC max(case when kpi_name = 'Paid UV' then actual_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_actual,
# MAGIC max(case when kpi_name = 'PFM' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_plan,
# MAGIC max(case when kpi_name = 'Paid UV' then plan_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_plan,
# MAGIC max(case when kpi_name = 'PFM' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as num_py,
# MAGIC max(case when kpi_name = 'Paid UV' then py_value end) 
# MAGIC over(partition by site_name,store_type,bu_name,category_name,brand_name,year,period) as den_py
# MAGIC from aq_data a
# MAGIC where 1 = 1
# MAGIC and kpi_name in ('PFM','Paid UV')
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC union_data as (
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from aq_data
# MAGIC -- union all 
# MAGIC -- select 
# MAGIC -- site_name,category_name,brand_name,year,period,kpi_name,
# MAGIC -- actual_value,plan_value,py_value
# MAGIC -- from new_data_01
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_02
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_03
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_04
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_05
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_06
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_07
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_08
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_09
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_10
# MAGIC union all 
# MAGIC select 
# MAGIC site_name,store_type,bu_name,category_name,brand_name,year,period,kpi_name,
# MAGIC actual_value,plan_value,py_value
# MAGIC from new_data_11
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC mid_data as (
# MAGIC select 
# MAGIC case when kpi_name in (
# MAGIC 'GMV',
# MAGIC 'GMV Free',
# MAGIC 'GMV Paid',
# MAGIC 'Offtake GSV',
# MAGIC 'TO',
# MAGIC 'GP',
# MAGIC 'PFM',
# MAGIC 'Sample+GWP',
# MAGIC 'TP',
# MAGIC 'OP',
# MAGIC 'Channel PBO',
# MAGIC 'Channel PBO% TO',
# MAGIC 'PFM% GMV',
# MAGIC 'POSM',
# MAGIC 'UL Premium',
# MAGIC 'Non-UL Premium',
# MAGIC 'Sold Bundle Pack',
# MAGIC 'Instore Agency',
# MAGIC 'Digital Premium',
# MAGIC 'EC TP-自播',
# MAGIC 'EC TP-非自播',
# MAGIC 'Transportation',
# MAGIC 'Promotion Package & Repacking'
# MAGIC )
# MAGIC then 'P&L'
# MAGIC else 'Golden Formula' 
# MAGIC end as section,
# MAGIC bu_name,category_name,site_name,store_type,brand_name,year,period,
# MAGIC kpi_name,actual_value,plan_value,py_value
# MAGIC from union_data 
# MAGIC where 1 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC target_data as (
# MAGIC select 
# MAGIC a.section,
# MAGIC a.bu_name as bu,
# MAGIC a.category_name as category,
# MAGIC a.site_name as site,
# MAGIC a.store_type,
# MAGIC a.brand_name as brand,
# MAGIC a.period,
# MAGIC case when a.period not in ('Q1','Q2','Q3','Q4')
# MAGIC      then month(to_date(concat('01-',a.period,'-2000'),'dd-MMM-yyyy')) 
# MAGIC      when a.period = 'Q1' then 13
# MAGIC      when a.period = 'Q2' then 14
# MAGIC      when a.period = 'Q3' then 15
# MAGIC      when a.period = 'Q4' then 16
# MAGIC       end as period_order,
# MAGIC a.kpi_name,
# MAGIC b.kpi_unit,
# MAGIC a.actual_value as actual,
# MAGIC a.plan_value as plan,
# MAGIC a.py_value as prior_year,
# MAGIC b.kpi_parent_name,
# MAGIC c.kpi_parent_sort_no,
# MAGIC b.kpi_sort_no,
# MAGIC a.year
# MAGIC from mid_data a 
# MAGIC left join ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_sort_mapping b 
# MAGIC on a.kpi_name = b.kpi_name
# MAGIC left join ${spark.var.catalog.dim}.fin.dim_cpt_planning_cpt_kpi_parent_sort_mapping c 
# MAGIC on b.kpi_parent_name = c.kpi_parent_name
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_sec_mf(
# MAGIC section,
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC store_type,
# MAGIC brand,
# MAGIC period,
# MAGIC period_sort_no,
# MAGIC kpi_name,
# MAGIC kpi_unit,
# MAGIC actual,
# MAGIC plan,
# MAGIC prior_year,
# MAGIC kpi_parent,
# MAGIC kpi_parent_sort_no,
# MAGIC kpi_sort_no,
# MAGIC year,
# MAGIC create_by,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC section,
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC store_type,
# MAGIC brand,
# MAGIC period,
# MAGIC period_order,
# MAGIC kpi_name,
# MAGIC kpi_unit,
# MAGIC actual,
# MAGIC plan,
# MAGIC prior_year,
# MAGIC kpi_parent_name,
# MAGIC kpi_parent_sort_no,
# MAGIC kpi_sort_no,
# MAGIC year,
# MAGIC 'Automatic' as create_by,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from target_data
# MAGIC ;