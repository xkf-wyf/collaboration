# Databricks notebook source
pip install openpyxl 

# COMMAND ----------

import pandas as pd

catalog_ods = spark.conf.get("spark.var.catalog.ods")

file_path = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/fin/SAP CPP actual.xlsx"

df_pd = pd.read_excel(file_path, header=0, sheet_name=0)

df = spark.createDataFrame(df_pd)

df_renamed = df \
    .withColumnRenamed("Business Unit", "business_unit") \
    .withColumnRenamed("Local Level 01", "local_level_01") \
    .withColumnRenamed("Level 3", "level3") \
    .withColumnRenamed("Product", "product") \
    .withColumnRenamed("Record Type", "record_type") \
    .withColumnRenamed("Sold-to Group", "sold_to_group") \
    .withColumnRenamed("Period/Year", "period_year") \
    .withColumnRenamed("Level 1", "level1") \
    .withColumnRenamed("Level 4", "level4") \
    .withColumnRenamed("Level 5", "level5") \
    .withColumnRenamed("Level 7", "level7") \
    .withColumnRenamed("Level 8", "level8") \
    .withColumnRenamed("Profitability Unit", "profitability_unit") \
    .withColumnRenamed("Level 2", "level2") \
    .withColumnRenamed("Level 9", "level9") \
    .withColumnRenamed("@ GSV", "gsv") \
    .withColumnRenamed("@ TTS", "tts") \
    .withColumnRenamed("@ EOT", "eot") \
    .withColumnRenamed("@ BBT", "bbt") \
    .withColumnRenamed("@ BB Price", "bb_price") \
    .withColumnRenamed("@ OT", "ot") \
    .withColumnRenamed("@TURNOVER", "turnover") \
    .withColumnRenamed("@Ttl SCC", "ttl_scc") \
    .withColumnRenamed("@ GP", "gp") \
    .withColumnRenamed("@ BMI", "bmi") \
    .withColumnRenamed("@ Adv Expe", "adv_expe") \
    .withColumnRenamed("@ Ass Cr O", "ass_cr_o") \
    .withColumnRenamed("@ AdvProdT", "adv_prod_t") \
    .withColumnRenamed("AdvPrd C.T", "adv_prdc_t") \
    .withColumnRenamed("@ AdvFee T", "adv_fee_t") \
    .withColumnRenamed("Ch.Ag. Fee", "ch_ag_fee") \
    .withColumnRenamed("Adv.Ag.Com", "adv_ag_com") \
    .withColumnRenamed("@ AdvPro D", "adv_pro_d") \
    .withColumnRenamed("Adv.PC Dig", "adv_pc_dig") \
    .withColumnRenamed("@ AdvFee D", "advfee_d") \
    .withColumnRenamed("Adv Fee Dg", "adv_fee_dg") \
    .withColumnRenamed("@ Ass Dep", "ass_dep") \
    .withColumnRenamed("@ Medi C T", "medi_c_t") \
    .withColumnRenamed("Media Trd.", "media_trd") \
    .withColumnRenamed("@ Medi C D", "medicd") \
    .withColumnRenamed("MedCst-Dig", "medcst_dig") \
    .withColumnRenamed("@ Public R", "public_r") \
    .withColumnRenamed("@ Earned M", "earned_m") \
    .withColumnRenamed("Ear Med Tr", "ear_med_tr") \
    .withColumnRenamed("Ear MedCon", "ear_med_con") \
    .withColumnRenamed("@ Con EngC", "con_engc") \
    .withColumnRenamed("Cons EngCe", "cons_engce") \
    .withColumnRenamed("All.Ch.-Ad", "all_ch_ad") \
    .withColumnRenamed("@ Promo Ex", "promo_ex") \
    .withColumnRenamed("@ Pro PckM", "pro_pckm") \
    .withColumnRenamed("T-Pck&Mfg", "t_pck_mfg") \
    .withColumnRenamed("C-Pck&Mfg", "c_pck_mfg") \
    .withColumnRenamed("@ ProComMa", "pro_com_ma") \
    .withColumnRenamed("T-Comm Mat", "t_comm_mat") \
    .withColumnRenamed("C-Comm Mat", "c_comm_mat") \
    .withColumnRenamed("@ ProSamGi", "pro_sam_gi") \
    .withColumnRenamed("T-SmpleGif", "t_smplegif") \
    .withColumnRenamed("C-SmpleGif", "c_smplegif") \
    .withColumnRenamed("@ ProTeaCo", "pro_tea_co") \
    .withColumnRenamed("T-TeamCost", "t_team_cost") \
    .withColumnRenamed("C-TeamCost", "c_team_cost") \
    .withColumnRenamed("@ ProAgeFe", "pro_age_fe") \
    .withColumnRenamed("T-AgncyFee", "t_agncyfee") \
    .withColumnRenamed("C-AgncyFee", "c_agncyfee") \
    .withColumnRenamed("@ POS", "pos") \
    .withColumnRenamed("Cus S.Eqp.", "cus_s_eqp") \
    .withColumnRenamed("@ Merchand", "merchand") \
    .withColumnRenamed("Merch Trad", "merch_trad") \
    .withColumnRenamed("Merch Cons", "merch_cons") \
    .withColumnRenamed("@ PBI", "pbi") \
    .withColumnRenamed("@TOTAL IND", "total_ind") \
    .withColumnRenamed("@ MR", "mr") \
    .withColumnRenamed("MR-Trade", "mr_trade") \
    .withColumnRenamed("MR-Cons", "mr_cons") \
    .withColumnRenamed("@ Devlopmn", "devlopmn") \
    .withColumnRenamed("Prod. Dvl.", "prod_dvl") \
    .withColumnRenamed("Mrkt.Dvl.", "mrkt_dvl") \
    .withColumnRenamed("Mark.Activ", "mark_activ") \
    .withColumnRenamed("Sales Ind.", "sales_ind") \
    .withColumnRenamed("General In", "general_in") \
    .withColumnRenamed("Stock Opt.", "stock_opt") \
    .withColumnRenamed("OTI`s", "oti_s") \
    .withColumnRenamed("Restr.", "restr") \
    .withColumnRenamed("All.Ch-Res", "all_ch_res") \
    .withColumnRenamed("ERD Cred.", "erd_cred") \
    .withColumnRenamed("All.Ch.-In", "all_ch_in") \
    .withColumnRenamed("@ COP", "cop") \
    .withColumnRenamed("App.Oneoff", "app_oneoff") \
    .withColumnRenamed("M&A rl.act", "m_a_rl_act") \
    .withColumnRenamed("Impairment", "impairment") \
    .withColumnRenamed("P/L on Dsp", "p_l_on_dsp") \
    .withColumnRenamed("@ Op Pr", "op_pr") \
    .withColumnRenamed("Sales qty", "sales_qty") \
    .withColumnRenamed("SCM-MUpNT", "scm_mupnt") \
    .withColumnRenamed("NTMkupIntr", "ntmkupintr") \
    .withColumnRenamed("CrssChange", "crsschange") \
    .withColumnRenamed("Qty SUoM", "qty_suom") \
    .withColumnRenamed("NIV", "niv") \
    .withColumnRenamed("CC", "cc") \
    .withColumnRenamed("Mrk Up", "mrk_up") \
    .withColumnRenamed("Mrkup Cost", "mrkup_cost") \
    .withColumnRenamed("FG W-off", "fg_w_off")

df_renamed.createOrReplaceTempView("result")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC delete from ${spark.var.catalog.ods}.int_manual.ods_cpt_ke30_sap_cpp_actual_mi 
# MAGIC where 1 = 1
# MAGIC and etl_flag = date_format(current_date(), 'yyyyMM')
# MAGIC -- and etl_flag = '202601'
# MAGIC ;
# MAGIC
# MAGIC insert into ${spark.var.catalog.ods}.int_manual.ods_cpt_ke30_sap_cpp_actual_mi(
# MAGIC  local_level_01
# MAGIC ,business_unit
# MAGIC ,record_type
# MAGIC ,level3
# MAGIC ,product
# MAGIC ,sold_to_group
# MAGIC ,period_year
# MAGIC ,level1
# MAGIC ,level4
# MAGIC ,level5
# MAGIC ,level7
# MAGIC ,level8
# MAGIC ,profitability_unit
# MAGIC ,level2
# MAGIC ,level9
# MAGIC ,gsv
# MAGIC ,tts
# MAGIC ,eot
# MAGIC ,bbt
# MAGIC ,bb_price
# MAGIC ,ot
# MAGIC ,turnover
# MAGIC ,ttl_scc
# MAGIC ,gp
# MAGIC ,bmi
# MAGIC ,adv_expe
# MAGIC ,ass_cr_o
# MAGIC ,adv_prod_t
# MAGIC ,adv_prdc_t
# MAGIC ,adv_fee_t
# MAGIC ,ch_ag_fee
# MAGIC ,adv_ag_com
# MAGIC ,adv_pro_d
# MAGIC ,adv_pc_dig
# MAGIC ,advfee_d
# MAGIC ,adv_fee_dg
# MAGIC ,ass_dep
# MAGIC ,medi_c_t
# MAGIC ,media_trd
# MAGIC ,medicd
# MAGIC ,medcst_dig
# MAGIC ,public_r
# MAGIC ,earned_m
# MAGIC ,ear_med_tr
# MAGIC ,ear_med_con
# MAGIC ,con_engc
# MAGIC ,cons_engce
# MAGIC ,all_ch_ad
# MAGIC ,promo_ex
# MAGIC ,pro_pckm
# MAGIC ,t_pck_mfg
# MAGIC ,c_pck_mfg
# MAGIC ,pro_com_ma
# MAGIC ,t_comm_mat
# MAGIC ,c_comm_mat
# MAGIC ,pro_sam_gi
# MAGIC ,t_smplegif
# MAGIC ,c_smplegif
# MAGIC ,pro_tea_co
# MAGIC ,t_team_cost
# MAGIC ,c_team_cost
# MAGIC ,pro_age_fe
# MAGIC ,t_agncyfee
# MAGIC ,c_agncyfee
# MAGIC ,pos
# MAGIC ,cus_s_eqp
# MAGIC ,merchand
# MAGIC ,merch_trad
# MAGIC ,merch_cons
# MAGIC ,pbi
# MAGIC ,total_ind
# MAGIC ,mr
# MAGIC ,mr_trade
# MAGIC ,mr_cons
# MAGIC ,devlopmn
# MAGIC ,prod_dvl
# MAGIC ,mrkt_dvl
# MAGIC ,mark_activ
# MAGIC ,sales_ind
# MAGIC ,general_in
# MAGIC ,stock_opt
# MAGIC ,oti_s
# MAGIC ,restr
# MAGIC ,all_ch_res
# MAGIC ,erd_cred
# MAGIC ,all_ch_in
# MAGIC ,cop
# MAGIC ,app_oneoff
# MAGIC ,m_a_rl_act
# MAGIC ,impairment
# MAGIC ,p_l_on_dsp
# MAGIC ,op_pr
# MAGIC ,sales_qty
# MAGIC ,scm_mupnt
# MAGIC ,ntmkupintr
# MAGIC ,crsschange
# MAGIC ,qty_suom
# MAGIC ,niv
# MAGIC ,cc
# MAGIC ,mrk_up
# MAGIC ,mrkup_cost
# MAGIC ,fg_w_off
# MAGIC ,dw_create_time
# MAGIC ,dw_last_update_time
# MAGIC ,etl_time
# MAGIC ,etl_flag
# MAGIC )
# MAGIC select 
# MAGIC  local_level_01
# MAGIC ,business_unit
# MAGIC ,record_type
# MAGIC ,level3
# MAGIC ,product
# MAGIC ,sold_to_group
# MAGIC ,period_year
# MAGIC ,level1
# MAGIC ,level4
# MAGIC ,level5
# MAGIC ,level7
# MAGIC ,level8
# MAGIC ,profitability_unit
# MAGIC ,level2
# MAGIC ,level9
# MAGIC ,gsv
# MAGIC ,tts
# MAGIC ,eot
# MAGIC ,bbt
# MAGIC ,bb_price
# MAGIC ,ot
# MAGIC ,turnover
# MAGIC ,ttl_scc
# MAGIC ,gp
# MAGIC ,bmi
# MAGIC ,adv_expe
# MAGIC ,ass_cr_o
# MAGIC ,adv_prod_t
# MAGIC ,adv_prdc_t
# MAGIC ,adv_fee_t
# MAGIC ,ch_ag_fee
# MAGIC ,adv_ag_com
# MAGIC ,adv_pro_d
# MAGIC ,adv_pc_dig
# MAGIC ,advfee_d
# MAGIC ,adv_fee_dg
# MAGIC ,ass_dep
# MAGIC ,medi_c_t
# MAGIC ,media_trd
# MAGIC ,medicd
# MAGIC ,medcst_dig
# MAGIC ,public_r
# MAGIC ,earned_m
# MAGIC ,ear_med_tr
# MAGIC ,ear_med_con
# MAGIC ,con_engc
# MAGIC ,cons_engce
# MAGIC ,all_ch_ad
# MAGIC ,promo_ex
# MAGIC ,pro_pckm
# MAGIC ,t_pck_mfg
# MAGIC ,c_pck_mfg
# MAGIC ,pro_com_ma
# MAGIC ,t_comm_mat
# MAGIC ,c_comm_mat
# MAGIC ,pro_sam_gi
# MAGIC ,t_smplegif
# MAGIC ,c_smplegif
# MAGIC ,pro_tea_co
# MAGIC ,t_team_cost
# MAGIC ,c_team_cost
# MAGIC ,pro_age_fe
# MAGIC ,t_agncyfee
# MAGIC ,c_agncyfee
# MAGIC ,pos
# MAGIC ,cus_s_eqp
# MAGIC ,merchand
# MAGIC ,merch_trad
# MAGIC ,merch_cons
# MAGIC ,pbi
# MAGIC ,total_ind
# MAGIC ,mr
# MAGIC ,mr_trade
# MAGIC ,mr_cons
# MAGIC ,devlopmn
# MAGIC ,prod_dvl
# MAGIC ,mrkt_dvl
# MAGIC ,mark_activ
# MAGIC ,sales_ind
# MAGIC ,general_in
# MAGIC ,stock_opt
# MAGIC ,oti_s
# MAGIC ,restr
# MAGIC ,all_ch_res
# MAGIC ,erd_cred
# MAGIC ,all_ch_in
# MAGIC ,cop
# MAGIC ,app_oneoff
# MAGIC ,m_a_rl_act
# MAGIC ,impairment
# MAGIC ,p_l_on_dsp
# MAGIC ,op_pr
# MAGIC ,sales_qty
# MAGIC ,scm_mupnt
# MAGIC ,ntmkupintr
# MAGIC ,crsschange
# MAGIC ,qty_suom
# MAGIC ,niv
# MAGIC ,cc
# MAGIC ,mrk_up
# MAGIC ,mrkup_cost
# MAGIC ,fg_w_off
# MAGIC ,NOW() + INTERVAL 8 HOUR as dw_create_time
# MAGIC ,NOW() + INTERVAL 8 HOUR as dw_last_update_time
# MAGIC ,NOW() + INTERVAL 8 HOUR as etl_time
# MAGIC ,date_format(current_date(), 'yyyyMM') as etl_flag
# MAGIC -- ,'202601' as etl_flag
# MAGIC from result a 
# MAGIC ;

# COMMAND ----------

import pandas as pd 
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

catalog_ods = spark.conf.get("spark.var.catalog.ods")

src_dir = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/fin"

src_file = f"{src_dir}/SAP CPP actual.xlsx"

tgt_dir = f"/Volumes/{catalog_ods}/int_manual/vol_cpt_inbound_manual/fin/backup"

# today_str = datetime.now().strftime("%Y%m%d")
current_date = datetime.now()
last_month_date = current_date - relativedelta(months = 1)
mth = last_month_date.strftime("%Y%m") 

tgt_file = f"{tgt_dir}/SAP CPP actual_{mth}.csv"

dbutils.fs.cp(src_file, tgt_file)