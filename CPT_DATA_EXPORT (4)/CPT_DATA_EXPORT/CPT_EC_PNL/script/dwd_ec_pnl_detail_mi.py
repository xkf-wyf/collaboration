# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC delete from ${spark.var.catalog.dwd}.fin.dwd_ec_pnl_detail_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;
# MAGIC
# MAGIC with tmp_product as (
# MAGIC select 
# MAGIC  bu
# MAGIC ,category
# MAGIC ,brand
# MAGIC ,product_line_group 
# MAGIC ,sku_code
# MAGIC from (
# MAGIC select 
# MAGIC -- division_short as bu
# MAGIC  division as bu  --20250105修改，使用bu全称
# MAGIC ,category_short as category
# MAGIC ,cg_sub_brand as brand
# MAGIC ,national_ex42 as product_line_group
# MAGIC ,sku_code
# MAGIC ,etl_date
# MAGIC ,row_number() over(partition by sku_code order by etl_date desc) rn
# MAGIC from ${spark.var.catalog.dim}.cd.dim_product t
# MAGIC ) a
# MAGIC where rn=1
# MAGIC )
# MAGIC ,
# MAGIC
# MAGIC tmp_customer as (
# MAGIC -- select distinct 
# MAGIC --  key_cust5_cd
# MAGIC -- ,soldto_code as soldto_code
# MAGIC -- ,soldto_name as soldto_name
# MAGIC -- ,account_group_en as site
# MAGIC -- ,banner_en as store_name
# MAGIC -- from ${spark.var.catalog.dim}.cd.dim_customer 
# MAGIC -- where bu_type = 'BPC'
# MAGIC
# MAGIC -- 2026-07-31 iris修改,应marvin要求，补充HC、PC的店铺维度信息
# MAGIC select distinct 
# MAGIC  key_cust5_cd                          
# MAGIC ,soldto_code       as soldto_code      
# MAGIC ,soldto_name       as soldto_name      
# MAGIC ,account_group_en  as site             
# MAGIC ,banner_en         as store_name       
# MAGIC from ${spark.var.catalog.dim}.cd.dim_customer   
# MAGIC where (
# MAGIC -- 业务说明：BPC字段对应的范围是B&W和PC的非ORAL店，HC就是HC，PC的Oral取得是PC
# MAGIC -- 条件1：BPC 业务类型的客户，全部纳入
# MAGIC (bu_type = 'BPC' 
# MAGIC -- 条件2：凡是属于 PC 业务下、且不含 REGENERATE / ZHONGHUA 字样的 banner，
# MAGIC -- 其对应客户全部纳入（即 PC 业务的普通 banner）
# MAGIC or banner_en in (
# MAGIC select distinct banner_en 
# MAGIC from ${spark.var.catalog.dim}.cd.dim_customer  
# MAGIC where bu_type = 'PC' 
# MAGIC and (banner_en not like '%REGENERATE%' 
# MAGIC and banner_en not like '%ZHONGHUA%'))
# MAGIC )
# MAGIC -- 条件3：HC 业务类型的客户，全部纳入
# MAGIC or bu_type = 'HC'
# MAGIC -- 条件4：PC 业务下，banner 名含 REGENERATE 或 ZHONGHUA 的特殊 banner 客户
# MAGIC or (bu_type = 'PC' 
# MAGIC and (banner_en like '%REGENERATE%' 
# MAGIC or banner_en like '%ZHONGHUA%'))
# MAGIC )
# MAGIC )
# MAGIC
# MAGIC insert into ${spark.var.catalog.dwd}.fin.dwd_ec_pnl_detail_mi
# MAGIC select 
# MAGIC  t.customer_code
# MAGIC ,t.customer_name
# MAGIC ,t.business_unit_code
# MAGIC ,t.business_unit_name
# MAGIC ,t.record_type_code
# MAGIC ,t.record_type_name
# MAGIC ,t.level3_code
# MAGIC ,t.level3_name
# MAGIC ,t.product_code
# MAGIC ,t.product_name
# MAGIC ,t.sold_to_group_code
# MAGIC ,t.sold_to_group_name
# MAGIC ,t.period
# MAGIC ,t.year
# MAGIC ,t.month
# MAGIC ,t.mth
# MAGIC ,t.level1_code
# MAGIC ,t.level1_name
# MAGIC ,t.level4_code
# MAGIC ,t.level4_name
# MAGIC ,t.level5_code
# MAGIC ,t.level5_name
# MAGIC ,t.level7_code
# MAGIC ,t.level7_name
# MAGIC ,t.level8_code
# MAGIC ,t.level8_name
# MAGIC ,t.profitability_unit_code
# MAGIC ,t.profitability_unit_name
# MAGIC ,t.level2_code
# MAGIC ,t.level2_name
# MAGIC ,t.level9_code
# MAGIC ,t.level9_name
# MAGIC ,t1.bu as bu_name
# MAGIC ,t1.category as category_name
# MAGIC ,t1.brand as brand_name
# MAGIC ,t1.product_line_group as product_line_group_name
# MAGIC ,'2C' as business_type
# MAGIC ,t2.soldto_code as sold_to_code
# MAGIC ,t2.soldto_name as sold_to_name
# MAGIC ,t2.site as site_name
# MAGIC ,t2.store_name
# MAGIC ,t.gsv
# MAGIC ,t.tts
# MAGIC ,t.eot
# MAGIC ,t.bbt
# MAGIC ,t.bb_price
# MAGIC ,t.ot
# MAGIC ,t.turnover
# MAGIC ,t.ttl_scc
# MAGIC ,t.gp
# MAGIC ,t.bmi
# MAGIC ,t.adv_expe
# MAGIC ,t.ass_cr_o
# MAGIC ,t.adv_prod_t
# MAGIC ,t.adv_prdc_t
# MAGIC ,t.adv_fee_t
# MAGIC ,t.ch_ag_fee
# MAGIC ,t.adv_ag_com
# MAGIC ,t.adv_pro_d
# MAGIC ,t.adv_pc_dig
# MAGIC ,t.advfee_d
# MAGIC ,t.adv_fee_dg
# MAGIC ,t.ass_dep
# MAGIC ,t.medi_c_t
# MAGIC ,t.media_trd
# MAGIC ,t.medicd
# MAGIC ,t.medcst_dig
# MAGIC ,t.public_r
# MAGIC ,t.earned_m
# MAGIC ,t.ear_med_tr
# MAGIC ,t.ear_med_con
# MAGIC ,t.con_engc
# MAGIC ,t.cons_engce
# MAGIC ,t.all_ch_ad
# MAGIC ,t.promo_ex
# MAGIC ,t.pro_pckm
# MAGIC ,t.t_pck_mfg
# MAGIC ,t.c_pck_mfg
# MAGIC ,t.pro_com_ma
# MAGIC ,t.t_comm_mat
# MAGIC ,t.c_comm_mat
# MAGIC ,t.pro_sam_gi
# MAGIC ,t.t_smplegif
# MAGIC ,t.c_smplegif
# MAGIC ,t.pro_tea_co
# MAGIC ,t.t_team_cost
# MAGIC ,t.c_team_cost
# MAGIC ,t.pro_age_fe
# MAGIC ,t.t_agncyfee
# MAGIC ,t.c_agncyfee
# MAGIC ,t.pos
# MAGIC ,t.cus_s_eqp
# MAGIC ,t.merchand
# MAGIC ,t.merch_trad
# MAGIC ,t.merch_cons
# MAGIC ,t.pbi
# MAGIC ,t.total_ind
# MAGIC ,t.mr
# MAGIC ,t.mr_trade
# MAGIC ,t.mr_cons
# MAGIC ,t.devlopmn
# MAGIC ,t.prod_dvl
# MAGIC ,t.mrkt_dvl
# MAGIC ,t.mark_activ
# MAGIC ,t.sales_ind
# MAGIC ,t.general_in
# MAGIC ,t.stock_opt
# MAGIC ,t.oti_s
# MAGIC ,t.restr
# MAGIC ,t.all_ch_res
# MAGIC ,t.erd_cred
# MAGIC ,t.all_ch_in
# MAGIC ,t.cop
# MAGIC ,t.app_oneoff
# MAGIC ,t.m_a_rl_act
# MAGIC ,t.impairment
# MAGIC ,t.p_l_on_dsp
# MAGIC ,t.op_pr
# MAGIC ,t.sales_qty
# MAGIC ,t.scm_mupnt
# MAGIC ,t.ntmkupintr
# MAGIC ,t.crsschange
# MAGIC ,t.qty_suom
# MAGIC ,t.niv
# MAGIC ,t.cc
# MAGIC ,t.mrk_up
# MAGIC ,t.mrkup_cost
# MAGIC ,t.fg_w_off
# MAGIC ,NOW() + INTERVAL 8 HOUR dw_create_time
# MAGIC ,NOW() + INTERVAL 8 HOUR dw_last_update_time
# MAGIC ,NOW() + INTERVAL 8 HOUR etl_time
# MAGIC ,t.etl_flag
# MAGIC from ${spark.var.catalog.tmp}.fin.tmp_ec_pnl_detail_mi t
# MAGIC left join tmp_product t1 
# MAGIC on t.product_code = t1.sku_code
# MAGIC left join tmp_customer t2 
# MAGIC on t.customer_code = t2.key_cust5_cd
# MAGIC where 1 = 1
# MAGIC and t.etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and t.etl_flag = '202601'
# MAGIC -- and t.product_code <> 'Not'
# MAGIC and t.product_code not in ('Not','未分配的')   --ryan修改
# MAGIC ;