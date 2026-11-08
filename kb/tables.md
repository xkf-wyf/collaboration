# CPT 上游表知识库（tables.md)

> 来源：CPT-涉及上游表清单.xlsx（本地快照 2026-11-08，云端为准）

## DouYin（39 张上游表，按接口分组）

### Actual GSV By Store By Revenue 接口

| 表 | 说明 |
|----|------|
| cd.dim_product | 产品主数据模型层 |
| cd_bi.ads_omni_base_monthly_fix_mf | 进销存月结-HIERARCHY月表 |
| cd.dim_store | 门店UC模型层 |
| ddm.dim_prd_sku | |
| ddm.dim_sku_pack_size | |
| int_hologres.ods_dy_trd_item_sales_week_month_di | |
| ddm.dim_prd_item | |

### Actual logistic cost & 平台费接口

| 表 | 说明 |
|----|------|
| sc_dtc.ads_dtc_spending_bi_mi | |
| ddm.dws_dtc_oms_prd_detail_scd_di | |
| cd.dim_product_pcecost | |
| ddm.dws_dy_live_product_mi | |
| sc.dwd_dtc_latest_oms_order_header_di | |
| sc.dwd_dtc_latest_oms_order_detail_di | |
| cd.dim_product_listprice | |
| cd.dim_sku_matching | |
| cd.dim_store_matching | |
| cd.dim_customer | |
| cd.dim_store_scope | |
| sc.dwd_dtc_shopcost_di | |

### Actual Spending by 自商短接口

> 重复使用相同 dws（同上组）

### 自播 by 号 building block actual 接口

| 表 | 说明 |
|----|------|
| ddm.dwd_dy_self_livestream_di | |
| ddm.dws_dy_self_live_sales_mi | |
| ddm.dim_store | |
| ads_dy_gmv_second_gsv_mf | |
| cd_bi.ads_omni_base_monthly_fix_mf | |
| ads_dy_gmv_second_gsv_author_mf | |
| ddm.dws_dtc_oms_prd_detail_scd_di | |
| ddm.dim_sku_pack_size | |
| cd.dim_product_pcecost | |
| ddm.dws_dy_live_product_mi | |
| ddm.dim_store | |

## HCPC（92 张上游表，按产物分组）

| 产物 | 上游表 |
|------|--------|
| ads_bmi_golden_mf | ddm_dset.ads_ec_g_fomular_ndy_traffic_fact、ddm_dset.ads_ec_g_fomular_dim_traffic_metric_cfg |
| ads_bmi_spending_mf | ddm.dws_pfm_total_item_df、ddm.dim_jd_cps_mapping、ddm.dim_prd_item、ddm.dim_store |
| dim_core_pack_mf | ddm.dim_sku_pack_size |
| dim_core_pack_item_mf | ddm.dim_sku_pack_size、ddm.dim_store、cd.dim_product、cd.dim_product_listprice、cd.dwd_primary_sales_bdl |
| dim_core_pack_variant_mapping_mf | int_manual.ods_core_pack_variant_mapping_mf |
| CPT_EC_CC_REPORT | sc.dim_mdhub_product_wide_df、cd.dim_product |
| ads_ec_platform_bill_mi | ddm.dws_tmall_super_bill_mi、ddm.dws_pdd_bill_mi、cd.dim_product |
| dim_customer_2c_mf | cd.dim_customer |
| ads_dtc_bmi_spending_mf | ddm.dim_store、ddm.dim_prd_item、ddm.dwd_tm_rlyq_comm_fee_mf、ddm.dwd_tm_rlyq_serv_fee_mf |
| ads_omni_gsv_mf | cd_bi.ads_omni_base_monthly_fix_mf、cd.dim_product |
| ads_omni_stock_mf | ddm.dim_sku_pack_size、ddm.dim_store、cd_bi.ads_omni_base |
| ads_omni_stock_total_mf | cd_bi.ads_omni_base、cd.dim_product、ddm_dset.ads_ec_daily_sales_fact_sales、ddm_dset.ads_ec_daily_sales_dim_product、cd.dim_cpp_adjustment |
| dim_hc_product_line_group_mf | cd.dim_product_full |
| ads_second_total_sales_mf | （清单至第61行截断，待云端更新补全） |

## 备注

- 表名即全限定引用名（catalog/schema 前缀以清单原文为准，脚本变量 `${spark.var.catalog.*}` 在运行时注入）。
- `int_manual.ods_core_pack_variant_mapping_mf` 是人工上传的手工表（特殊香型机制匹配），更新时需按代码字段/路径要求人工上传。
- 清单在本地抽取时 HCPC 组第 62 行以后被截断，以云端完整版为准，更新时由人类审核方补全本文件。
