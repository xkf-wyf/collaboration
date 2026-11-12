# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC delete from ${spark.var.catalog.tmp}.fin.tmp_ec_pnl_detail_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;
# MAGIC
# MAGIC insert into ${spark.var.catalog.tmp}.fin.tmp_ec_pnl_detail_mi
# MAGIC SELECT
# MAGIC     -- 1. 拆分 local_level_01：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(local_level_01, ' ', 1)) AS local_level_01_code,
# MAGIC     TRIM(SUBSTRING(local_level_01, LENGTH(SPLIT_PART(local_level_01, ' ', 1)) + 1)) AS local_level_01_name,
# MAGIC
# MAGIC     -- 2. 拆分 business_unit：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(business_unit, ' ', 1)) AS business_unit_code,
# MAGIC     TRIM(SUBSTRING(business_unit, LENGTH(SPLIT_PART(business_unit, ' ', 1)) + 1)) AS business_unit_name,
# MAGIC
# MAGIC     -- 3. 拆分 record_type：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(record_type, ' ', 1)) AS record_type_code,
# MAGIC     TRIM(SUBSTRING(record_type, LENGTH(SPLIT_PART(record_type, ' ', 1)) + 1)) AS record_type_name,
# MAGIC
# MAGIC     -- 4. 拆分 level3：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level3, ' ', 1)) AS level3_code,
# MAGIC     TRIM(SUBSTRING(level3, LENGTH(SPLIT_PART(level3, ' ', 1)) + 1)) AS level3_name,
# MAGIC
# MAGIC     -- 5. 拆分 product：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(product, ' ', 1)) AS product_code,
# MAGIC     TRIM(SUBSTRING(product, LENGTH(SPLIT_PART(product, ' ', 1)) + 1)) AS product_name,
# MAGIC
# MAGIC     -- 6. 拆分 sold_to_group：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(sold_to_group, ' ', 1)) AS sold_to_group_code,
# MAGIC     TRIM(SUBSTRING(sold_to_group, LENGTH(SPLIT_PART(sold_to_group, ' ', 1)) + 1)) AS sold_to_group_name,
# MAGIC
# MAGIC     -- 7. 拆分 period_year：第一个空格前=period；去空格后前4字符=year；第一个空格后-第二个空格前=month
# MAGIC     TRIM(SPLIT_PART(period_year, ' ', 1)) AS period,
# MAGIC     TRIM(SUBSTRING(TRIM(period_year), 1, 4)) AS year,
# MAGIC     TRIM(REPLACE(SPLIT_PART(SPLIT_PART(period_year, ' ', 2), ' ', 1), '.', '')) AS month,
# MAGIC     CONCAT_WS('', TRIM(SUBSTRING(TRIM(period_year), 1, 4)), TRIM(substring(SPLIT_PART(SPLIT_PART(period_year, ' ', 1), '.', 2),2))) AS mth,
# MAGIC
# MAGIC     -- 8. 拆分 level1：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level1, ' ', 1)) AS level1_code,
# MAGIC     TRIM(SUBSTRING(level1, LENGTH(SPLIT_PART(level1, ' ', 1)) + 1)) AS level1_name,
# MAGIC
# MAGIC     -- 9. 拆分 level4：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level4, ' ', 1)) AS level4_code,
# MAGIC     TRIM(SUBSTRING(level4, LENGTH(SPLIT_PART(level4, ' ', 1)) + 1)) AS level4_name,
# MAGIC
# MAGIC     -- 10. 拆分 level5：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level5, ' ', 1)) AS level5_code,
# MAGIC     TRIM(SUBSTRING(level5, LENGTH(SPLIT_PART(level5, ' ', 1)) + 1)) AS level5_name,
# MAGIC
# MAGIC     -- 11. 拆分 level7：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level7, ' ', 1)) AS level7_code,
# MAGIC     TRIM(SUBSTRING(level7, LENGTH(SPLIT_PART(level7, ' ', 1)) + 1)) AS level7_name,
# MAGIC
# MAGIC     -- 12. 拆分 level8：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level8, ' ', 1)) AS level8_code,
# MAGIC     TRIM(SUBSTRING(level8, LENGTH(SPLIT_PART(level8, ' ', 1)) + 1)) AS level8_name,
# MAGIC
# MAGIC     -- 13. 拆分 profitability_unit：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(profitability_unit, ' ', 1)) AS profitability_unit_code,
# MAGIC     TRIM(SUBSTRING(profitability_unit, LENGTH(SPLIT_PART(profitability_unit, ' ', 1)) + 1)) AS profitability_unit_name,
# MAGIC
# MAGIC     -- 14. 拆分 level2：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level2, ' ', 1)) AS level2_code,
# MAGIC     TRIM(SUBSTRING(level2, LENGTH(SPLIT_PART(level2, ' ', 1)) + 1)) AS level2_name,
# MAGIC
# MAGIC     -- 15. 拆分 level9：第一个空格前为code，后面为name
# MAGIC     TRIM(SPLIT_PART(level9, ' ', 1)) AS level9_code,
# MAGIC     TRIM(SUBSTRING(level9, LENGTH(SPLIT_PART(level9, ' ', 1)) + 1)) AS level9_name,
# MAGIC
# MAGIC     -- 保留不处理的数值字段
# MAGIC     gsv,
# MAGIC     tts,
# MAGIC     eot,
# MAGIC     bbt,
# MAGIC     bb_price,
# MAGIC     ot,
# MAGIC     turnover,
# MAGIC     ttl_scc,
# MAGIC     gp,
# MAGIC     bmi,
# MAGIC     adv_expe,
# MAGIC     ass_cr_o,
# MAGIC     adv_prod_t,
# MAGIC     adv_prdc_t,
# MAGIC     adv_fee_t,
# MAGIC     ch_ag_fee,
# MAGIC     adv_ag_com,
# MAGIC     adv_pro_d,
# MAGIC     adv_pc_dig,
# MAGIC     advfee_d,
# MAGIC     adv_fee_dg,
# MAGIC     ass_dep,
# MAGIC     medi_c_t,
# MAGIC     media_trd,
# MAGIC     medicd,
# MAGIC     medcst_dig,
# MAGIC     public_r,
# MAGIC     earned_m,
# MAGIC     ear_med_tr,
# MAGIC     ear_med_con,
# MAGIC     con_engc,
# MAGIC     cons_engce,
# MAGIC     all_ch_ad,
# MAGIC     promo_ex,
# MAGIC     pro_pckm,
# MAGIC     t_pck_mfg,
# MAGIC     c_pck_mfg,
# MAGIC     pro_com_ma,
# MAGIC     t_comm_mat,
# MAGIC     c_comm_mat,
# MAGIC     pro_sam_gi,
# MAGIC     t_smplegif,
# MAGIC     c_smplegif,
# MAGIC     pro_tea_co,
# MAGIC     t_team_cost,
# MAGIC     c_team_cost,
# MAGIC     pro_age_fe,
# MAGIC     t_agncyfee,
# MAGIC     c_agncyfee,
# MAGIC     pos,
# MAGIC     cus_s_eqp,
# MAGIC     merchand,
# MAGIC     merch_trad,
# MAGIC     merch_cons,
# MAGIC     pbi,
# MAGIC     total_ind,
# MAGIC     mr,
# MAGIC     mr_trade,
# MAGIC     mr_cons,
# MAGIC     devlopmn,
# MAGIC     prod_dvl,
# MAGIC     mrkt_dvl,
# MAGIC     mark_activ,
# MAGIC     sales_ind,
# MAGIC     general_in,
# MAGIC     stock_opt,
# MAGIC     oti_s,
# MAGIC     restr,
# MAGIC     all_ch_res,
# MAGIC     erd_cred,
# MAGIC     all_ch_in,
# MAGIC     cop,
# MAGIC     app_oneoff,
# MAGIC     m_a_rl_act,
# MAGIC     impairment,
# MAGIC     p_l_on_dsp,
# MAGIC     op_pr,
# MAGIC     sales_qty,
# MAGIC     scm_mupnt,
# MAGIC     ntmkupintr,
# MAGIC     crsschange,
# MAGIC     qty_suom,
# MAGIC     niv,
# MAGIC     cc,
# MAGIC     mrk_up,
# MAGIC     mrkup_cost,
# MAGIC     fg_w_off,
# MAGIC     NOW() + INTERVAL 8 HOUR dw_create_time,
# MAGIC     NOW() + INTERVAL 8 HOUR dw_last_update_time,
# MAGIC     NOW() + INTERVAL 8 HOUR etl_time,
# MAGIC     etl_flag
# MAGIC FROM ${spark.var.catalog.ods}.int_manual.ods_cpt_ke30_sap_cpp_actual_mi
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;