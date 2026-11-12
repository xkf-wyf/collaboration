# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC with tmp_store_index_spending as (
# MAGIC select 
# MAGIC bu_name,
# MAGIC store_name,
# MAGIC bmi_spend_type,
# MAGIC replace(start_month,'-','') as start_month
# MAGIC from (
# MAGIC select distinct bu_name,store_name,bmi_spend_type,start_month
# MAGIC from ${spark.var.catalog.dim}.fin.dim_store_finance_spending_source_mapping 
# MAGIC where 1 = 1
# MAGIC and start_month is not null
# MAGIC ) a
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC var_max_dt as (
# MAGIC select max(dt) as max_dt
# MAGIC from ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_spending_detail as (
# MAGIC select 
# MAGIC t1.month,
# MAGIC t1.bu_name,
# MAGIC t1.category_name,
# MAGIC t1.brand_name,
# MAGIC t1.product_line_group as product_line_group_name,
# MAGIC t1.site_name,
# MAGIC t1.store_name,
# MAGIC t2.output_index_type,
# MAGIC t1.value,
# MAGIC t1.value_taxed
# MAGIC from (
# MAGIC select a.* 
# MAGIC from ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf a
# MAGIC inner join var_max_dt b 
# MAGIC on a.dt = b.max_dt
# MAGIC where 1 = 1
# MAGIC and a.bu_name in ('BEAUTY&WELLBEING','HOME CARE','PERSONAL CARE')
# MAGIC -- select * 
# MAGIC -- from ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf
# MAGIC -- where dt in ('2026-04-03')
# MAGIC -- and bu_name in ('BEAUTY&WELLBEING','HOME CARE','PERSONAL CARE')
# MAGIC ) t1 
# MAGIC inner join (
# MAGIC select a.bu_name,a.store_name,b.source_index_type,b.output_index_type,a.start_month
# MAGIC from tmp_store_index_spending a
# MAGIC inner join ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping b
# MAGIC on upper(a.bmi_spend_type) = upper(b.bmi_spend_type)
# MAGIC and b.source = 'bmi_spending'
# MAGIC ) t2
# MAGIC on upper(t1.bu_name) = upper(t2.bu_name)
# MAGIC and upper(t1.store_name) = upper(t2.store_name)
# MAGIC and upper(t1.index_type) = upper(t2.source_index_type)
# MAGIC and t1.month >= t2.start_month
# MAGIC where 1 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_store_index as (
# MAGIC select 
# MAGIC bu_name,
# MAGIC store_name,
# MAGIC bmi_spend_type,
# MAGIC replace(coalesce(start_month,'9999-01'),'-','') as start_month
# MAGIC from (
# MAGIC select distinct bu_name,store_name,bmi_spend_type,start_month
# MAGIC from ${spark.var.catalog.dim}.fin.dim_store_finance_spending_source_mapping 
# MAGIC where 1 = 1
# MAGIC and (start_month > '2025-01'
# MAGIC or start_month is null)
# MAGIC ) a 
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_bill_detail as (
# MAGIC select 
# MAGIC t1.month,
# MAGIC t1.bu_name,
# MAGIC t1.category_name,
# MAGIC t1.brand_name,
# MAGIC t1.product_line_group_name,
# MAGIC t1.site_name,
# MAGIC t1.store_name,
# MAGIC t2.output_index_type,
# MAGIC t1.amount_untaxed as value,
# MAGIC t1.amount_taxed as value_taxed
# MAGIC from (
# MAGIC select * 
# MAGIC from ${spark.var.catalog.ads}.fin_cpt.ads_ec_platform_bill_mi 
# MAGIC where month >= '202512' 
# MAGIC and bu_name in ('BEAUTY&WELLBEING','HOME CARE','PERSONAL CARE')
# MAGIC ) t1 
# MAGIC inner join (
# MAGIC select a.bu_name,a.store_name,b.source_index_type,b.output_index_type,a.start_month
# MAGIC from tmp_store_index a
# MAGIC inner join ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping b
# MAGIC on upper(a.bmi_spend_type) = upper(b.bmi_spend_type)
# MAGIC and b.source = 'platform_bill'
# MAGIC and b.source_index_type <> '无'
# MAGIC ) t2
# MAGIC on upper(t1.bu_name) = upper(t2.bu_name)
# MAGIC and upper(t1.store_name) = upper(t2.store_name)
# MAGIC and upper(t1.spending_type_fin) = upper(t2.source_index_type)
# MAGIC and t1.month >= '202501'
# MAGIC and t1.month < t2.start_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_target_v1 as (
# MAGIC select 
# MAGIC month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC value,
# MAGIC value_taxed,
# MAGIC 'bmi_spending' as source
# MAGIC from tmp_spending_detail
# MAGIC union all 
# MAGIC select 
# MAGIC month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC value,
# MAGIC value_taxed,
# MAGIC 'platform_bill' as source
# MAGIC from tmp_bill_detail
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_cfg_v2 as (
# MAGIC select 
# MAGIC bu_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC min(month) as min_month,
# MAGIC max(month) as max_moth
# MAGIC from tmp_target_v1
# MAGIC group by 
# MAGIC bu_name,
# MAGIC store_name,
# MAGIC output_index_type
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_cc_report_detail as (
# MAGIC select 
# MAGIC t1.month,
# MAGIC t1.bu_name,
# MAGIC t1.category_name,
# MAGIC t1.brand_name,
# MAGIC t1.product_line_group_name,
# MAGIC t1.site_name,
# MAGIC t1.store_name,
# MAGIC t2.output_index_type,
# MAGIC t1.value_untaxed as value
# MAGIC from ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi t1 
# MAGIC inner join (
# MAGIC select a.bu_name,a.store_name,b.source_index_type,b.output_index_type,a.start_month
# MAGIC from tmp_store_index a
# MAGIC inner join ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping b
# MAGIC on upper(a.bmi_spend_type) = upper(b.bmi_spend_type)
# MAGIC and b.source = 'cc_report'
# MAGIC and b.source_index_type <> '无'
# MAGIC ) t2
# MAGIC on upper(t1.bu_name) = upper(t2.bu_name)
# MAGIC and upper(t1.store_name) = upper(t2.store_name)
# MAGIC and upper(t1.index_type) = upper(t2.source_index_type)
# MAGIC and t1.month >= '202501'
# MAGIC and t1.month < t2.start_month
# MAGIC where 1 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_cc_v1 as (
# MAGIC select 
# MAGIC t1.month,
# MAGIC t1.bu_name,
# MAGIC t1.category_name,
# MAGIC t1.brand_name,
# MAGIC t1.product_line_group_name,
# MAGIC t1.site_name,
# MAGIC t1.store_name,
# MAGIC t1.output_index_type,
# MAGIC t1.value
# MAGIC from tmp_cc_report_detail t1
# MAGIC inner join tmp_cfg_v2 t2
# MAGIC on upper(t1.bu_name) = upper(t2.bu_name)
# MAGIC and upper(t1.store_name) = upper(t2.store_name)
# MAGIC and upper(t1.output_index_type) = upper(t2.output_index_type)
# MAGIC and t1.month < t2.min_month
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_cc_v2 as (
# MAGIC select 
# MAGIC t1.month,
# MAGIC t1.bu_name,
# MAGIC t1.category_name,
# MAGIC t1.brand_name,
# MAGIC t1.product_line_group_name,
# MAGIC t1.site_name,
# MAGIC t1.store_name,
# MAGIC t1.output_index_type,
# MAGIC t1.value
# MAGIC from tmp_cc_report_detail t1
# MAGIC left join tmp_cfg_v2 t2
# MAGIC on upper(t1.bu_name) = upper(t2.bu_name)
# MAGIC and upper(t1.store_name) = upper(t2.store_name)
# MAGIC and upper(t1.output_index_type) = upper(t2.output_index_type)
# MAGIC where 1 = 1
# MAGIC and t2.store_name is null 
# MAGIC and t2.output_index_type is null
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_cc_v3 as (
# MAGIC select 
# MAGIC t1.month,
# MAGIC t1.bu_name,
# MAGIC t1.category_name,
# MAGIC t1.brand_name,
# MAGIC t1.product_line_group_name,
# MAGIC t1.site_name,
# MAGIC t1.store_name,
# MAGIC t2.output_index_type,
# MAGIC t1.value_untaxed as value
# MAGIC from ${spark.var.catalog.dws}.fin.dws_ec_cc_report_mi t1 
# MAGIC inner join (
# MAGIC select a.bu_name,a.store_name,b.source_index_type,b.output_index_type
# MAGIC from (
# MAGIC select distinct bu_name,store_name
# MAGIC from ${spark.var.catalog.dim}.fin.dim_store_finance_spending_source_mapping
# MAGIC ) a
# MAGIC cross join (
# MAGIC select *
# MAGIC from ${spark.var.catalog.dim}.fin.dim_finance_index_source_mapping
# MAGIC where source = 'cc_report'
# MAGIC and bmi_spend_type in ('品牌新享','CRM','KOL Livestream')
# MAGIC ) b
# MAGIC ) t2
# MAGIC on upper(t1.bu_name) = upper(t2.bu_name)
# MAGIC and upper(t1.store_name) = upper(t2.store_name)
# MAGIC and upper(t1.index_type) = upper(t2.source_index_type)
# MAGIC where 1 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_target_v2 as (
# MAGIC select 
# MAGIC month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC value,
# MAGIC value_taxed,
# MAGIC source
# MAGIC from tmp_target_v1
# MAGIC union all 
# MAGIC select 
# MAGIC month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC value,
# MAGIC null as value_taxed,
# MAGIC 'cc_report' as source
# MAGIC from tmp_cc_v1
# MAGIC union all
# MAGIC select 
# MAGIC month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC value,
# MAGIC null as value_taxed,
# MAGIC 'cc_report' as source
# MAGIC from tmp_cc_v2
# MAGIC union all
# MAGIC select 
# MAGIC month,
# MAGIC bu_name,
# MAGIC category_name,
# MAGIC brand_name,
# MAGIC product_line_group_name,
# MAGIC site_name,
# MAGIC store_name,
# MAGIC output_index_type,
# MAGIC value,
# MAGIC null as value_taxed,
# MAGIC 'cc_report' as source
# MAGIC from tmp_cc_v3
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dws}.fin.dws_pfm_spending_mf(
# MAGIC month,
# MAGIC bu_code,
# MAGIC bu_name,
# MAGIC category_code,
# MAGIC category_name,
# MAGIC brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC site_code,
# MAGIC site_name,
# MAGIC store_code,
# MAGIC store_name,
# MAGIC bmi_spend_type,
# MAGIC index_type,
# MAGIC value_untaxed,
# MAGIC value_taxed,
# MAGIC source,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC month,
# MAGIC bu_name as bu_code,
# MAGIC bu_name,
# MAGIC category_name as category_code,
# MAGIC category_name,
# MAGIC brand_name as brand_code,
# MAGIC brand_name,
# MAGIC product_line_group_name as product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC site_name as site_code,
# MAGIC site_name,
# MAGIC store_name as store_code,
# MAGIC store_name,
# MAGIC output_index_type as bmi_spend_type,
# MAGIC output_index_type as index_type,
# MAGIC value as value_untaxed,
# MAGIC value_taxed,
# MAGIC source,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from tmp_target_v2
# MAGIC ;