-- Databricks notebook source
-- adb sql
-- **********************************************************************
-- BMI Spending Actual-Order Time接口
-- 版本：v1.0
-- 作者：eddie.liang@systex.com.cn
-- 修改时间：2026-02-05
-- 描述：每月第4个工作日回传M-1月BMI Spending Actual
-- 存储格式：Delta Lake
-- 分区字段：dt(日期分区，格式yyyy-MM-dd)
-- 所属层级：ADS层 财务主题
-- **********************************************************************
-- 变量说明：
-- ${spark.var.catalog.ads}：ADS层目录名称
-- ${spark.var.table.owner}：表归属用户/服务主体
-- **********************************************************************

drop table if exists ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf;

create table if not exists ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf
(
     month                         string comment '会计月份，格式：yyyyMM'
    ,bu_code                       string comment '业务单元编码'
    ,bu_name                       string comment '业务单元名称'
    ,customer_type_code            string comment '客户类型编码'
    ,customer_type                 string comment '客户类型名称'
    ,site_code                     string comment '站点编码'
    ,site_name                     string comment '站点名称'
    ,store_code                    string comment '门店编码'
    ,store_name                    string comment '门店名称'
    ,category_code                 string comment '品类编码'
    ,category_name                 string comment '品类名称'
    ,brand_code                    string comment '品牌编码'
    ,brand_name                    string comment '品牌名称'
    ,product_line_group_code       string comment '产品线组编码'
    ,product_line_group            string comment '产品线组名称'
    ,index_type                    string comment '指标类型/指标名称'
    ,value                         decimal(38,2) comment '指标数值'
    ,value_taxed                   decimal(38,2) comment '结果,不除税'
    ,create_by                     string comment '创建人/处理程序标识'
    ,dw_create_time                timestamp comment '创建时间'
    ,dw_last_update_time           timestamp comment '最后更新时间'
    ,dw_batch_num                  bigint comment '批次号'
)
using delta
partitioned by (dt string comment '天分区')
comment 'ADS层财务主题表 - BMI Spending Actual-Order Time接口数据，每月第4个工作日回传上月数据'
tblproperties (
    'delta.autoOptimize.optimizeWrite' = 'true', 
    'delta.autoOptimize.autoCompact' = 'true',  
    'delta.columnMapping.mode' = 'name',        
    'created.by' = 'haolong.wu@chiefclouds.com', 
    'version' = 'v1.0'                          
);

alter table ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf set owner to `${spark.var.table.owner}`;

alter table ${spark.var.catalog.ads}.fin_cpt.ads_bmi_spending_mf set tblproperties ('comment' = 'ADS层财务主题表 - BMI Spending Actual-Order Time接口数据，每月第4个工作日回传上月数据');