# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC delete from ${spark.var.catalog.dws}.fin.dws_ec_pnl_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;
# MAGIC
# MAGIC with t_agg as (
# MAGIC select 
# MAGIC mth as month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC business_type,
# MAGIC sold_to_code,
# MAGIC sold_to_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC etl_flag,
# MAGIC sum(nvl(gsv,0)) gsv,
# MAGIC sum(nvl(tts,0)) tts,
# MAGIC sum(nvl(turnover,0)) turnover
# MAGIC from ${spark.var.catalog.dwd}.fin.dwd_ec_pnl_detail_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC group by 
# MAGIC mth,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC business_type,
# MAGIC sold_to_code,
# MAGIC sold_to_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC etl_flag
# MAGIC )
# MAGIC
# MAGIC insert into ${spark.var.catalog.dws}.fin.dws_ec_pnl_mi
# MAGIC select 
# MAGIC month,
# MAGIC null as bu_code,
# MAGIC bu_name,
# MAGIC null as category_code,
# MAGIC category_name,
# MAGIC null as brand_code,
# MAGIC brand_name,
# MAGIC null as product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC business_type,
# MAGIC sold_to_code,
# MAGIC sold_to_name,
# MAGIC null as site_code,
# MAGIC site_name,
# MAGIC null as store_code,
# MAGIC store_name,
# MAGIC null as spending_type_fin_sort,
# MAGIC idx.index_type as spending_type_fin,
# MAGIC case idx.index_type
# MAGIC when 'Secondary GSV' then gsv
# MAGIC when 'CPP' then tts
# MAGIC when 'GMV' then turnover
# MAGIC when 'Bill CPP%' then IF(gsv = 0, 0, t.tts/t.gsv)
# MAGIC end as amount,
# MAGIC NOW() + INTERVAL 8 HOUR dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR etl_time,
# MAGIC etl_flag
# MAGIC from t_agg t
# MAGIC -- 笛卡尔积生成4种指标类型，替代原4个UNION ALL分支
# MAGIC CROSS JOIN (
# MAGIC     SELECT 'Secondary GSV' AS index_type UNION ALL
# MAGIC     SELECT 'CPP' UNION ALL
# MAGIC     SELECT 'GMV' UNION ALL
# MAGIC     SELECT 'Bill CPP%'
# MAGIC ) idx
# MAGIC ;