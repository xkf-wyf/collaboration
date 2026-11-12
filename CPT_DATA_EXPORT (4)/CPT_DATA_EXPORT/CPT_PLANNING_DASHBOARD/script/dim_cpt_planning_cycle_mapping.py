# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC with raw_data as (
# MAGIC select 
# MAGIC cast(plan_cycle as string) as plan_cycle,
# MAGIC cast(cast(start_month as integer) as string) as start_month,
# MAGIC cast(cast(end_month as integer) as string) as end_month
# MAGIC from (
# MAGIC select distinct plan_cycle,start_month,end_month
# MAGIC from (
# MAGIC select distinct plan_cycle,start_month,end_month
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_cpt_budget_planning_df
# MAGIC where 1 = 1
# MAGIC and type = 'FCST'
# MAGIC union all 
# MAGIC select distinct plan_cycle,start_month,end_month
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_cpt_p_and_l_df
# MAGIC where 1 = 1
# MAGIC and type = 'FCST'
# MAGIC ) 
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC normal_expanded as (
# MAGIC select
# MAGIC plan_cycle,
# MAGIC plan_cycle as plan_cycle_last,
# MAGIC date_format(add_month, 'yyyyMM') as month
# MAGIC from raw_data
# MAGIC lateral view explode (
# MAGIC sequence (
# MAGIC to_date(concat(start_month, '01'), 'yyyyMMdd'),
# MAGIC to_date(concat(end_month, '01'), 'yyyyMMdd'),
# MAGIC interval 1 month
# MAGIC )
# MAGIC ) as add_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC gap_data as (
# MAGIC select
# MAGIC plan_cycle,
# MAGIC date_format(add_months(to_date(concat(start_month, '01'), 'yyyyMMdd'), -1), 'yyyyMM') AS gap_month
# MAGIC from raw_data
# MAGIC where start_month > plan_cycle
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC gap_with_last AS (
# MAGIC select 
# MAGIC plan_cycle,
# MAGIC plan_cycle_last,
# MAGIC month
# MAGIC from (
# MAGIC select
# MAGIC g.plan_cycle,
# MAGIC m.plan_cycle as plan_cycle_last,
# MAGIC g.gap_month as month
# MAGIC from gap_data g
# MAGIC left join normal_expanded m 
# MAGIC on m.month = g.gap_month
# MAGIC qualify row_number() over (
# MAGIC partition by g.plan_cycle 
# MAGIC order by m.plan_cycle desc
# MAGIC ) = 1
# MAGIC )
# MAGIC where plan_cycle_last is not null
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC final as (
# MAGIC select * from normal_expanded
# MAGIC union all
# MAGIC select * from gap_with_last
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC fcst_data as (
# MAGIC select
# MAGIC 'FCST' as type,
# MAGIC date_format(to_date(concat(plan_cycle, '01'), 'yyyyMMdd'), 'yyyyMMM') as cycle_en,
# MAGIC plan_cycle as cycle_filter,
# MAGIC plan_cycle_last as cycle_fact,
# MAGIC month,
# MAGIC case when plan_cycle <> plan_cycle_last then '补充'
# MAGIC      else null end as remark,
# MAGIC 'FCST'||month||plan_cycle_last as cycle_union_key
# MAGIC from final
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC actual_data as (
# MAGIC select 
# MAGIC 'Actual' as type,
# MAGIC '/' as cycle_en,
# MAGIC '/' as cycle_filter,
# MAGIC '/' as cycle_fact,
# MAGIC month as month,
# MAGIC null as remark,
# MAGIC 'Actual'||month||'/' as cycle_union_key
# MAGIC from (
# MAGIC select distinct month
# MAGIC from ${spark.var.catalog.ads}.fin_cpt.ads_cpt_planning_mf 
# MAGIC where 1 = 1
# MAGIC and type = 'Actual'
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC target_data as (
# MAGIC select
# MAGIC type,
# MAGIC cycle_en,
# MAGIC cycle_filter,
# MAGIC cycle_fact,
# MAGIC month,
# MAGIC remark,
# MAGIC cycle_union_key
# MAGIC from actual_data
# MAGIC union all 
# MAGIC select
# MAGIC type,
# MAGIC cycle_en,
# MAGIC cycle_filter,
# MAGIC cycle_fact,
# MAGIC month,
# MAGIC remark,
# MAGIC cycle_union_key
# MAGIC from fcst_data
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dim}.fin.dim_cpt_planning_cycle_mapping(
# MAGIC idx,
# MAGIC type,
# MAGIC cycle_en,
# MAGIC cycle_filter,
# MAGIC cycle_fact,
# MAGIC month,
# MAGIC remark,
# MAGIC cycle_union_key,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC dw_batch_num
# MAGIC )
# MAGIC select 
# MAGIC row_number() over(order by cycle_union_key) as idx,
# MAGIC type,
# MAGIC cycle_en,
# MAGIC cycle_filter,
# MAGIC cycle_fact,
# MAGIC month,
# MAGIC remark,
# MAGIC cycle_union_key,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC date_format(current_date(), 'yyyyMMdd') as dw_batch_num
# MAGIC from target_data
# MAGIC order by cycle_filter,month;