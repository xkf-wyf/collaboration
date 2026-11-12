# Databricks notebook source
# MAGIC %sql 
# MAGIC
# MAGIC with tmp_mdhub as (
# MAGIC select distinct level8_long_code,sku_code
# MAGIC from ${spark.var.catalog.dim}.sc.dim_mdhub_product_wide_df
# MAGIC where 1 = 1
# MAGIC and COALESCE(sku_code, '') <> ''
# MAGIC and COALESCE(level8_long_code, '') <> ''
# MAGIC and level1_name in (
# MAGIC 'BEAUTY & WELLBEING',
# MAGIC 'HOME CARE',
# MAGIC 'PERSONAL CARE'
# MAGIC )
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_sku as (
# MAGIC select 
# MAGIC sku_code,
# MAGIC division,
# MAGIC category_short,
# MAGIC cg_sub_brand,
# MAGIC national_ex42
# MAGIC from (
# MAGIC select 
# MAGIC sku_code,
# MAGIC division,
# MAGIC category_short,
# MAGIC cg_sub_brand,
# MAGIC national_ex42,
# MAGIC row_number() over(partition by sku_code order by etl_date desc) rn
# MAGIC from (
# MAGIC select distinct sku_code,division,category_short,cg_sub_brand,national_ex42,etl_date
# MAGIC from ${spark.var.catalog.dim}.cd.dim_product
# MAGIC where 1 = 1
# MAGIC --and is_current = 1
# MAGIC and COALESCE(sku_code, '') <> ''
# MAGIC and COALESCE(national_ex42, '') <> ''
# MAGIC and COALESCE(division, '') <> ''
# MAGIC and COALESCE(category_short, '') <> ''
# MAGIC and COALESCE(cg_sub_brand, '') <> ''
# MAGIC ) a
# MAGIC ) b 
# MAGIC where rn = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_mdhub_product_mid as (
# MAGIC select 
# MAGIC t1.level8_long_code as l8_code,
# MAGIC t1.sku_code,
# MAGIC t2.division as bu,
# MAGIC t2.category_short as category,
# MAGIC t2.cg_sub_brand as brand,
# MAGIC t2.national_ex42 as product_line
# MAGIC from tmp_mdhub t1 
# MAGIC inner join tmp_sku t2 
# MAGIC on t1.sku_code = t2.sku_code
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_mdhub_product as (
# MAGIC select 
# MAGIC l8_code,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line
# MAGIC from (
# MAGIC select 
# MAGIC l8_code,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC row_number() over(partition by l8_code order by cast(sku_code as bigint) desc) rn
# MAGIC from tmp_mdhub_product_mid
# MAGIC ) a 
# MAGIC where rn = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_product_old as (
# MAGIC select 
# MAGIC l8_code,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line
# MAGIC from (
# MAGIC select 
# MAGIC l8_code,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC row_number() over(partition by l8_code order by cast(sku_code as bigint) desc) rn_2
# MAGIC from (
# MAGIC select 
# MAGIC l8_code,
# MAGIC bu,
# MAGIC category,
# MAGIC brand,
# MAGIC product_line,
# MAGIC sku_code,
# MAGIC row_number() over(partition by l8_code,sku_code order by etl_date desc) rn_1
# MAGIC from (
# MAGIC select distinct
# MAGIC global_l8_subbrand_code as l8_code,
# MAGIC division as bu,
# MAGIC category_short as category,
# MAGIC cg_sub_brand as brand,
# MAGIC national_ex42 as product_line,
# MAGIC sku_code,
# MAGIC etl_date
# MAGIC from ${spark.var.catalog.dim}.cd.dim_product
# MAGIC where 1 = 1
# MAGIC --and is_current = 1
# MAGIC and COALESCE(global_l8_subbrand_code, '') <> ''
# MAGIC and COALESCE(national_ex42, '') <> ''
# MAGIC and COALESCE(division, '') <> ''
# MAGIC and COALESCE(category_short, '') <> ''
# MAGIC and COALESCE(cg_sub_brand, '') <> ''
# MAGIC ) a
# MAGIC ) b 
# MAGIC where rn_1 = 1
# MAGIC ) c 
# MAGIC where rn_2 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_product_master as (
# MAGIC select 
# MAGIC COALESCE(t1.l8_code,t2.l8_code) as l8_code,
# MAGIC COALESCE(t1.bu,t2.bu) as bu,
# MAGIC COALESCE(t1.category,t2.category) as category,
# MAGIC COALESCE(t1.brand,t2.brand) as brand,
# MAGIC COALESCE(t1.product_line,t2.product_line) as product_line
# MAGIC from tmp_product_old t1
# MAGIC full join tmp_mdhub_product t2 
# MAGIC on t1.l8_code = t2.l8_code
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_product_org as (
# MAGIC select 
# MAGIC t1.ph8,
# MAGIC case when t1.bu = 'B&W' then 'BEAUTY&WELLBEING'
# MAGIC      when t1.bu = 'PC' then 'PERSONAL CARE'
# MAGIC      when t1.bu = 'HC' then 'HOME CARE'
# MAGIC      else t1.bu 
# MAGIC       end bu,
# MAGIC upper(t1.category) as category,
# MAGIC upper(t1.brand) as brand,
# MAGIC upper(t1.product_line_group) as product_line_group
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_ph8_mapping_adhoc t1
# MAGIC where product_line_group is not null
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_product as (
# MAGIC select 
# MAGIC COALESCE(t1.l8_code,t2.ph8) as l8_code,
# MAGIC COALESCE(t1.bu,t2.bu) as bu,
# MAGIC COALESCE(t1.category,t2.category) as category,
# MAGIC COALESCE(t1.brand,t2.brand) as brand,
# MAGIC COALESCE(t1.product_line,t2.product_line_group) as product_line
# MAGIC from tmp_product_master t1 
# MAGIC full join tmp_product_org t2 
# MAGIC on t1.l8_code = t2.ph8
# MAGIC where 1 = 1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_store as (
# MAGIC select customer_group,store_name
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_store_mapping
# MAGIC where 1 = 1
# MAGIC --and cpt_scope = 'Y'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_index_2026 as (
# MAGIC select item_code,item_name,cpt_index_mapping
# MAGIC from ${spark.var.catalog.dim}.fin.dim_cpt_cc_report_index_mapping
# MAGIC where 1 = 1
# MAGIC --and cpt_scope = 'Y'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_index_2025 as (
# MAGIC select item_code,item_name,cpt_index_mapping
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cc_report_cpt_index_mapping_v2025_adhoc
# MAGIC where 1 = 1
# MAGIC --and cpt_scope = 'Y'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_index as (
# MAGIC select 
# MAGIC COALESCE(t1.item_code,t2.item_code) as item_code,
# MAGIC COALESCE(t1.item_name,t2.item_name) as item_name,
# MAGIC COALESCE(t1.cpt_index_mapping,t2.cpt_index_mapping) as cpt_index_mapping
# MAGIC from tmp_index_2026 t1
# MAGIC full join tmp_index_2025 t2 
# MAGIC on t1.item_code = t2.item_code
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_site as (
# MAGIC select 
# MAGIC national_ex25 as store_name,
# MAGIC max(national_ex3) as site_name
# MAGIC from ${spark.var.catalog.dim}.cd.dim_store    
# MAGIC where national_ex1 = 'ONLINE'                         --20260513，新增过滤条件
# MAGIC and national_ex4 not like '%POP%'
# MAGIC and national_ex4 not in ('REDBOOK FGS','SPECIAL WS','SHEIN FGS')
# MAGIC group by national_ex25
# MAGIC union all 
# MAGIC select 
# MAGIC '拼多多分销-间供直送' as store_name,
# MAGIC 'PDD' as site_name
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_dwd_2026 as (
# MAGIC select 
# MAGIC  t1.period as month
# MAGIC --,case when t1.bu = 'B&W' then 'BEAUTY&WELLBEING' else null end as bu_name
# MAGIC ,t2.bu as bu_name
# MAGIC ,t2.category as category_name
# MAGIC ,t2.brand as brand_name
# MAGIC ,t2.product_line as product_line_group_name
# MAGIC ,t5.site_name as site_name
# MAGIC ,t3.store_name
# MAGIC ,t4.cpt_index_mapping as index_type
# MAGIC ,t1.amount as value_untaxed
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_mf t1
# MAGIC left join tmp_product t2
# MAGIC on t1.ph8 = t2.l8_code
# MAGIC left join tmp_store t3 
# MAGIC on upper(t1.customer_group) = upper(t3.customer_group)
# MAGIC left join tmp_index t4 
# MAGIC on upper(t1.item_code) = upper(t4.item_code)
# MAGIC left join tmp_site t5 
# MAGIC on upper(t3.store_name) = upper(t5.store_name)
# MAGIC where 1 = 1
# MAGIC and t1.period >= '2026-01'
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_dwd_2025 as (
# MAGIC select 
# MAGIC  t1.period as month
# MAGIC --,case when t1.bu = 'B&W' then 'BEAUTY&WELLBEING' else null end as bu_name
# MAGIC ,t2.bu as bu_name
# MAGIC ,t2.category as category_name
# MAGIC ,t2.brand as brand_name
# MAGIC ,t2.product_line as product_line_group_name
# MAGIC ,t5.site_name as site_name
# MAGIC ,t3.store_name
# MAGIC ,t4.cpt_index_mapping as index_type
# MAGIC ,t1.amount as value_untaxed
# MAGIC from ${spark.var.catalog.ods}.int_manual.ods_cpt_finbit_dm_tf_ddm_cc_output_v2025_mf t1
# MAGIC left join tmp_product t2
# MAGIC on t1.ph8 = t2.l8_code
# MAGIC left join tmp_store t3 
# MAGIC on upper(t1.customer_group) = upper(t3.customer_group)
# MAGIC left join tmp_index t4 
# MAGIC on upper(t1.item_code) = upper(t4.item_code)
# MAGIC left join tmp_site t5 
# MAGIC on upper(t3.store_name) = upper(t5.store_name)
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_dwd as (
# MAGIC select 
# MAGIC  t1.month
# MAGIC ,t1.bu_name
# MAGIC ,t1.category_name
# MAGIC ,t1.brand_name
# MAGIC ,t1.product_line_group_name
# MAGIC ,t1.site_name
# MAGIC ,t1.store_name
# MAGIC ,t1.index_type
# MAGIC ,t1.value_untaxed
# MAGIC from tmp_dwd_2025 t1
# MAGIC union all 
# MAGIC select 
# MAGIC  t2.month
# MAGIC ,t2.bu_name
# MAGIC ,t2.category_name
# MAGIC ,t2.brand_name
# MAGIC ,t2.product_line_group_name
# MAGIC ,t2.site_name
# MAGIC ,t2.store_name
# MAGIC ,t2.index_type
# MAGIC ,t2.value_untaxed
# MAGIC from tmp_dwd_2026 t2
# MAGIC )
# MAGIC
# MAGIC insert overwrite table ${spark.var.catalog.dwd}.fin.dwd_ec_cc_report_mi(
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
# MAGIC index_type,
# MAGIC value_untaxed,
# MAGIC dw_create_time,
# MAGIC dw_last_update_time,
# MAGIC etl_time
# MAGIC )
# MAGIC select 
# MAGIC replace(month,'-','') as month,
# MAGIC null as bu_code,
# MAGIC bu_name,
# MAGIC null as category_code,
# MAGIC category_name,
# MAGIC null as brand_code,
# MAGIC brand_name,
# MAGIC null as product_line_group_code,
# MAGIC product_line_group_name,
# MAGIC null as site_code,
# MAGIC site_name,
# MAGIC null as store_code,
# MAGIC store_name,
# MAGIC index_type,
# MAGIC value_untaxed,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_create_time,
# MAGIC NOW() + INTERVAL 8 HOUR as dw_last_update_time,
# MAGIC NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC from tmp_dwd
# MAGIC ;