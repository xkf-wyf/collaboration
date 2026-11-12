# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC with raw_data as (
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC period,
# MAGIC to_date(concat(period, '-01'), 'yyyy-MM-dd') as dt,
# MAGIC kpi_level_2 as kpi,
# MAGIC kpi_level_1 as unit,
# MAGIC cast(actual as decimal(38,3)) as actural,
# MAGIC cast(target as decimal(38,3)) as target
# MAGIC from ${spark.var.catalog.ads}.ddm_dset.ads_ec_pso_kpi_fact_limit_mf
# MAGIC where 1 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC add_py_data as (
# MAGIC select 
# MAGIC a.bu,
# MAGIC a.category,
# MAGIC a.site,
# MAGIC a.brand,
# MAGIC a.period,
# MAGIC a.dt,
# MAGIC a.kpi,
# MAGIC a.unit,
# MAGIC a.actural,
# MAGIC a.target,
# MAGIC b.actural as prior_year
# MAGIC from raw_data as a
# MAGIC left join raw_data as b
# MAGIC on a.bu = b.bu
# MAGIC and a.category = b.category 
# MAGIC and a.site = b.site 
# MAGIC and a.brand = b.brand 
# MAGIC and a.kpi = b.kpi
# MAGIC and a.unit = b.unit
# MAGIC and add_months(a.dt, -12) = b.dt
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC base_data as (
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC date_format(dt, 'MMM') as period,
# MAGIC concat('Q', quarter(dt)) as quarter,
# MAGIC substring(period,1,4) as year,
# MAGIC kpi,
# MAGIC unit,
# MAGIC actural,
# MAGIC target,
# MAGIC prior_year
# MAGIC from add_py_data
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC super_link_q_data as (
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC quarter as period,
# MAGIC kpi,
# MAGIC unit,
# MAGIC max(actural) as actural,
# MAGIC max(target) as target,
# MAGIC max(prior_year) as prior_year
# MAGIC from base_data 
# MAGIC where 1 = 1
# MAGIC and kpi = 'Super Link'
# MAGIC group by 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC quarter,
# MAGIC kpi,
# MAGIC unit
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC else_q_data as (
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC quarter as period,
# MAGIC kpi,
# MAGIC unit,
# MAGIC avg(actural) as actural,
# MAGIC avg(target) as target,
# MAGIC avg(prior_year) as prior_year 
# MAGIC from base_data 
# MAGIC where 1 = 1
# MAGIC and kpi not in ('Super Link')
# MAGIC group by 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC quarter,
# MAGIC kpi,
# MAGIC unit
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC aq_data as (
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC period,
# MAGIC case when kpi = 'SOS' then 'Share of search'
# MAGIC      else kpi 
# MAGIC       end as kpi,
# MAGIC unit,
# MAGIC actural,
# MAGIC target,
# MAGIC prior_year
# MAGIC from (
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC period,
# MAGIC kpi,
# MAGIC unit,
# MAGIC actural,
# MAGIC target,
# MAGIC prior_year
# MAGIC from base_data
# MAGIC union all
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC period,
# MAGIC kpi,
# MAGIC unit,
# MAGIC actural,
# MAGIC target,
# MAGIC prior_year
# MAGIC from super_link_q_data
# MAGIC union all
# MAGIC select 
# MAGIC bu,
# MAGIC category,
# MAGIC site,
# MAGIC brand,
# MAGIC year,
# MAGIC period,
# MAGIC kpi,
# MAGIC unit,
# MAGIC actural,
# MAGIC target,
# MAGIC prior_year
# MAGIC from else_q_data
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC target_data as (
# MAGIC select 
# MAGIC 'Perfect Store' as section,
# MAGIC case when a.bu = 'B&W' then 'BEAUTY&WELLBEING'
# MAGIC      when a.bu = 'HC' then 'HOME CARE'
# MAGIC      when a.bu = 'PC' then 'PERSONAL CARE'
# MAGIC       end as bu,
# MAGIC a.category,
# MAGIC a.site,
# MAGIC a.brand,
# MAGIC a.period,
# MAGIC case when a.period not in ('Q1','Q2','Q3','Q4')
# MAGIC      then month(to_date(concat('01-',a.period,'-2000'),'dd-MMM-yyyy')) 
# MAGIC      when a.period = 'Q1' then 13
# MAGIC      when a.period = 'Q2' then 14
# MAGIC      when a.period = 'Q3' then 15
# MAGIC      when a.period = 'Q4' then 16
# MAGIC       end as period_sort_no,
# MAGIC a.kpi,
# MAGIC a.unit,
# MAGIC a.actural as actual,
# MAGIC a.target,
# MAGIC a.prior_year,
# MAGIC 'Perfect Store' as kpi_parent,
# MAGIC 1 as kpi_parent_sort_no,
# MAGIC b.kpi_sort_no as kpi_sort_no,
# MAGIC a.year
# MAGIC from aq_data a  
# MAGIC left join ${spark.var.catalog.dim}.fin.dim_cpt_planning_ddm_kpi_sort_mapping b
# MAGIC on a.kpi = b.kpi_name
# MAGIC -- and a.unit = b.unit
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_ddm_mf(
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
# MAGIC target,
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
# MAGIC 'LEC' as store_type,
# MAGIC brand,
# MAGIC period,
# MAGIC period_sort_no,
# MAGIC kpi,
# MAGIC case when kpi in ('CTR','NSR','Share of search') then '%'
# MAGIC      when kpi = 'Super Link' then '个数'
# MAGIC      when kpi = 'Basket size' then 'RMB'
# MAGIC      when kpi = 'Search Volume' then '搜索人数'
# MAGIC      else null end as unit,
# MAGIC actual,
# MAGIC target,
# MAGIC prior_year,
# MAGIC kpi_parent,
# MAGIC kpi_parent_sort_no,
# MAGIC kpi_sort_no,
# MAGIC year,
# MAGIC 'Automatic' as create_by,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num 
# MAGIC from target_data
# MAGIC ;