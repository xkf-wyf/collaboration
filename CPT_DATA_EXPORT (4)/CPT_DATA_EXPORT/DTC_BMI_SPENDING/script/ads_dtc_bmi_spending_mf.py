# Databricks notebook source
# MAGIC %sql
# MAGIC -- dst 20260903 淘客联盟：替换新表 prod_ods.int_hologres.ods_tm_cps_trd_item_sales_di，唯品会itemid不保留，且修改关联dim_prd_item 的关联条件；热浪引擎：退前gmv计算逻辑更新

# COMMAND ----------

# DBTITLE 1,strat
import csv
import datetime
import hashlib
import time
import calendar
import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from pyspark.sql import functions as fn
from pyspark.sql.types import StringType
import datetime
from dateutil.relativedelta import relativedelta
 

catalog_dws = spark.conf.get("spark.var.catalog.dws")
catalog_dwd = spark.conf.get("spark.var.catalog.dwd")
catalog_ods = spark.conf.get("spark.var.catalog.ods")
catalog_dim = spark.conf.get("spark.var.catalog.dim")
catalog_tmp = spark.conf.get("spark.var.catalog.tmp")


# COMMAND ----------

# DBTITLE 1,参数窗口设置
dbutils.widgets.text("start_mth", "2025-01")
dbutils.widgets.text("end_mth", "2026-03")
dbutils.widgets.text("export_mth", "2026-03-04")
dbutils.widgets.text("dt", "2026-03-05")

# COMMAND ----------

# DBTITLE 1,确定时间参数
start_mth = dbutils.widgets.get("start_mth")
end_mth = dbutils.widgets.get("end_mth")
export_mth = dbutils.widgets.get("export_mth")
dt = dbutils.widgets.get("dt")
print(f"start_mth: {start_mth}")
print(f"end_mth: {end_mth}")
print(f"export_mth: {export_mth}")
print(f"dt: {dt}")

# COMMAND ----------

# DBTITLE 1,取TMFGS和VIP-弃
# MAGIC %skip
# MAGIC query_sql=f"""
# MAGIC SELECT left(period_key,7) as Month,
# MAGIC         item_id,
# MAGIC         max(item_name) item_name,
# MAGIC         '' as product_line_group,
# MAGIC         brand,
# MAGIC         category,
# MAGIC         bu,
# MAGIC         A.platform,
# MAGIC         b.customer,
# MAGIC         sum(gmv_before_refund) as gmv_before_refund
# MAGIC         ,sum(gmv) as gmv_after_refund
# MAGIC  FROM {catalog_tmp}.fin.tmp_trd_total_item_sales_all a
# MAGIC  left join {catalog_dim}.ddm.dim_store B on A.shop_id=b.shop_id
# MAGIC where  
# MAGIC left(a.period_key,7) <= '{end_mth}'
# MAGIC and flag = 1 and nvl(sku_code,'') <> '' 
# MAGIC and nvl(item_name,'') <>''         --20260609，iris新增逻辑,避免item_name为空时，关联cps表导致数据发散
# MAGIC and (a.platform like "%TMALL FGS%" or a.platform like "%VIP%")
# MAGIC   group BY
# MAGIC   left(period_key,7),
# MAGIC         item_id,
# MAGIC         brand,
# MAGIC         category,
# MAGIC         bu,
# MAGIC         A.platform,
# MAGIC         b.customer
# MAGIC """
# MAGIC
# MAGIC df = spark.sql(query_sql)
# MAGIC df.createOrReplaceTempView("tmp_gmv")
# MAGIC

# COMMAND ----------

# DBTITLE 1,spending-弃
# MAGIC %skip
# MAGIC query_sql=f"""
# MAGIC select
# MAGIC     replace(substr(t1.period_key,1,7),'-','')     as month
# MAGIC     ,t3.customer                                  as store_name 
# MAGIC     ,t2.bu                                        as bu  
# MAGIC     ,t2.category                                  as category_name   
# MAGIC     ,t2.brand                                     as brand_name                                     
# MAGIC     ,t2.product_line_group                        as product_line_group
# MAGIC     ,t2.item_id
# MAGIC     ,t2.item_name
# MAGIC     ,'Paid Media-CPS'                             as index_type           
# MAGIC     ,round(sum(spending),2)                       as value      
# MAGIC from {catalog_tmp}.fin.tmp_cps_spending t1
# MAGIC left join (
# MAGIC   select *
# MAGIC   from {catalog_dim}.ddm.dim_prd_item
# MAGIC   where is_current = 1
# MAGIC   and end_time='9999-12-31'   --20260609，iris新增逻辑，保证item数据唯一，避免数据发散
# MAGIC ) t2
# MAGIC on t1.item_id = t2.item_id
# MAGIC and t1.period_key >= t2.start_time and t1.period_key <= t2.end_time
# MAGIC left join (
# MAGIC   select *
# MAGIC   from {catalog_dim}.ddm.dim_store
# MAGIC   where status = 1
# MAGIC ) t3
# MAGIC on t2.shop_id = t3.shop_id
# MAGIC where substr(t1.period_key,1,7) between '{start_mth}' and '{end_mth}'
# MAGIC and t3.customer is not null
# MAGIC and (t3.customer_group like "%TMALL FGS%" or t3.customer_group like "%VIP%")
# MAGIC group by substr(t1.period_key,1,7),t3.customer,t2.category,t2.brand,t2.product_line_group,t3.customer,t2.item_id,t2.item_name,t2.bu
# MAGIC """
# MAGIC
# MAGIC df=spark.sql(query_sql)
# MAGIC df.createOrReplaceTempView("tmp_spending")

# COMMAND ----------

# DBTITLE 1,淘客联盟

# DBTITLE 1,淘客联盟（数据源改为 ods_tm_cps_trd_item_sales_di） -- 20260903
# 退前GMV = payment_amount；佣金结算(spending) = settlement_expenses_cost；退后GMV = settlement_amount
query_sql=f"""
select
    replace(substr(t1.date_time, 1, 7), '-', '')                          as month,
    ''                                                                   as bu_code,
    t2.bu                                                                as bu_name,
    ''                                                                   as store_code,
    t3.customer                                                          as store_name,
    ''                                                                   as category_code,
    t2.category                                                          as category_name,
    ''                                                                   as brand_code,
    t2.brand                                                             as brand_name,
    ''                                                                   as product_line_group_code,
    t2.product_line_group                                                as product_line_group,
    t1.product_id                                                        as item_id,
    max(nvl(t2.item_name,t1.product_name))                                    as item_name,
    cast(sum(t1.payment_amount) as decimal(38, 8))                       as gmv_before_refund,
    cast(sum(t1.settlement_amount) as decimal(38, 8))                    as gmv_after_refund,
    cast(sum(t1.settlement_expenses_cost) as decimal(38, 8))             as cps_spending,
    cast(sum(t1.settlement_expenses_cost) / nullif(sum(t1.settlement_amount), 0) as decimal(38, 8)) as cps_ratio,
    '淘客联盟'                                                            as source,
    'Automatic'                                                          as create_by,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time,
    cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
from {catalog_ods}.int_hologres.ods_tm_cps_trd_item_sales_di t1
left join (
    select item_id, bu, category, brand, product_line_group, item_name, shop_id,start_time,end_time
    from {catalog_dim}.ddm.dim_prd_item
    where is_current = 1
    -- and end_time = '9999-12-31' --20260609，iris新增逻辑，保证item数据唯一，避免数据发散
) t2 on t1.product_id = t2.item_id 
    -- and t1.date_time >= t2.start_time and t1.date_time <= t2.end_time  --避免一个itemid一个月有多个维度
and replace(last_day( date_format(to_date(t1.date_time, 'yyyy-MM-dd'), 'yyyy-MM-dd') ) , '-', '') >=  replace(t2.start_time, '-', '')
and replace(last_day( date_format(to_date(t1.date_time, 'yyyy-MM-dd'), 'yyyy-MM-dd') ) , '-', '') <=  replace(t2.end_time, '-', '') 
left join (
    select distinct shop_id,shop_name, customer, customer_group
    from {catalog_dim}.ddm.dim_store
    where status = 1
    and customer_group  ='TMALL FGS' and customer is not null
) t3 on t1.shop_name = t3.shop_name
where t1.plan_name <> '全部推广类型'
  and t1.period = '日'
  and substr(t1.date_time, 1, 7) between '{start_mth}' and '{end_mth}'
  and t3.customer is not null
  and (t3.customer_group like "%TMALL FGS%")
group by all;
    """

df=spark.sql(query_sql)
df.createOrReplaceTempView("tmp_tklm")

# COMMAND ----------

# DBTITLE 1,精选联盟
query_sql=f"""
select
    replace(substr(t1.confirm_time, 1, 7), '-', '')                       as month,
    ''                                                                   as bu_code,
    t2.bu                                                                as bu_name,
    ''                                                                   as store_code,
    t3.customer                                                          as store_name,
    ''                                                                   as category_code,
    t2.category                                                          as category_name,
    ''                                                                   as brand_code,
    t2.brand                                                             as brand_name,
    ''                                                                   as product_line_group_code,
    t2.product_line_group                                                as product_line_group,
    t2.item_id                                                           as item_id,
    t2.item_name                                                         as item_name,
    cast(sum(t1.pay_goods_amount/ 100) as decimal(38, 8))                as gmv_before_refund,
    cast(sum(t1.settled_goods_amount / 100) as decimal(38, 8))           as gmv_after_refund,
    cast(sum(t1.shop_real_commission / 100) as decimal(38, 8))              as cps_spending,
    cast(sum(t1.shop_real_commission / 100)/sum(t1.settled_goods_amount / 100) as decimal(38, 8)) as cps_ratio,
    '精选联盟'                                                             as source,
    'Automatic'                                                          as create_by,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time,
    cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)     as dw_batch_num
from {catalog_dwd}.ddm.dwd_dyxd_alliance_trd_df t1
left join (
    select  
        item_id,
        bu,
        category,
        brand,
        product_line_group,
        item_name,
        shop_name
    from {catalog_dim}.ddm.dim_prd_item
    where is_current = 1 and end_time='9999-12-31'
    group by item_id,
        bu,
        category,
        brand,
        product_line_group,
        item_name,
        shop_name
) t2 on t2.item_id = t1.product_id and t1.shop_name=t2.shop_name
left join (
    select  DISTINCT 
        shop_name,
        customer
    from {catalog_dim}.ddm.dim_store
    where status = 1 and is_current =1 and customer like "%DOUYIN%"
) t3 on t1.shop_name = t3.shop_name
where substr(t1.confirm_time, 1, 7) between '{start_mth}' and '{end_mth}'
  and t1.shop_real_commission > 0
  and t1.flow_point = 'SETTLE'
group by
    replace(substr(t1.confirm_time, 1, 7), '-', ''),
    t2.bu,
    t1.shop_name,
    t3.customer,
    t2.category,
    t2.brand,
    t2.product_line_group,
    t2.item_id,
    t2.item_name;
    """
df=spark.sql(query_sql)
df.createOrReplaceTempView("tmp_jxlm")

# COMMAND ----------

# DBTITLE 1,热浪引擎
query_sql=f"""
select 
    replace(left(t.bill_term, 7), 'M', '')                             as month,
    ''                                                                 as bu_code,
    t.bu                                                               as bu_name,
    ''                                                                 as store_code,
    t.shop_name                                                        as shop_name,
    t.customer                                                         as store_name,
    ''                                                                 as category_code,
    t.category                                                         as category_name,
    ''                                                                 as brand_code,
    t.brand                                                            as brand_name,
    ''                                                                 as product_line_group_code,
    t.product_line_group                                               as product_line_group,
    t.item_id                                                          as item_id,
    t.item_name                                                        as item_name,
    cast(sum(t.gmv_before_refund_amt) as decimal(38, 8))               as gmv_before_refund,
    cast(sum(t.gmv_after_refund_amt) as decimal(38, 8))                as gmv_after_refund,
    cast(sum(t.fee_amt) as decimal(38, 8))                             as cps_spending,
    cast(sum(t.fee_amt) / nullif(sum(t.gmv_after_refund_amt), 0) as decimal(38, 8)) as cps_ratio,
    '热浪引擎'                                                           as source,
    'Automatic'                                                         as create_by,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_create_time,
    cast(date_format(from_utc_timestamp(current_timestamp, 'Asia/Shanghai'), 'yyyy-MM-dd HH:mm:ss') as timestamp) as dw_last_update_time,
    cast(date_format(from_utc_timestamp(current_timestamp(), 'Asia/Shanghai'), 'yyyyMMddHHmmss') as bigint)   as dw_batch_num
from (
    select 
        t1.bill_term,
        t1.shop_name,
        if(flow_type='佣金退款',t1.actual_pay_amt - t1.rfd_ord_amt,t1.actual_pay_amt)  as gmv_before_refund_amt,  --20260903
        t1.actual_pay_amt                  as gmv_after_refund_amt,
        t1.comm_pay                        as fee_amt,
        t2.bu,
        t2.category,
        t2.brand,
        t2.product_line_group,
        t2.item_id,
        t2.item_name,
        t3.customer
    from {catalog_dwd}.ddm.dwd_tm_rlyq_comm_fee_mf t1
    left join (
        select item_id, bu, category, brand, product_line_group, item_name, shop_id
        from {catalog_dim}.ddm.dim_prd_item
        where is_current = 1 and end_time = '9999-12-31'
    ) t2 on t1.item_id = t2.item_id
    left join (
        select shop_id, customer
        from {catalog_dim}.ddm.dim_store
        where status = 1
    ) t3 on t2.shop_id = t3.shop_id
    where t1.bill_term is not null and t1.bill_term <> ''
    and replace(left(t1.bill_term, 7), 'M', '') between replace('{start_mth}','-','') and replace('{end_mth}','-','')

    union all

    -- 第二部分：服务费数据 (dwd_tm_rlyq_serv_fee_mf)
    select 
        t1.bill_term,
        t1.shop_name,
        if(flow_type='佣金退款',t1.actual_pay_amt - t1.rfd_ord_amt,t1.actual_pay_amt)  as gmv_before_refund_amt, --20260903
        t1.actual_pay_amt                  as gmv_after_refund_amt,
        t1.serv_fee_pay                    as fee_amt,
        t2.bu,
        t2.category,
        t2.brand,
        t2.product_line_group,
        t2.item_id,
        t2.item_name,
        t3.customer
    from {catalog_dwd}.ddm.dwd_tm_rlyq_serv_fee_mf t1
    left join (
        select item_id, bu, category, brand, product_line_group, item_name, shop_id
        from {catalog_dim}.ddm.dim_prd_item
        where is_current = 1 and end_time = '9999-12-31'
    ) t2 on t1.item_id = t2.item_id
    left join (
        select shop_id, customer
        from {catalog_dim}.ddm.dim_store
        where status = 1
    ) t3 on t2.shop_id = t3.shop_id
    where t1.bill_term is not null and t1.bill_term <> ''
    and replace(left(t1.bill_term, 7), 'M', '') between replace('{start_mth}','-','') and replace('{end_mth}','-','')
) t
group by
    replace(left(t.bill_term, 7), 'M', ''),
    t.bu,
    t.shop_name,
    t.customer,
    t.category,
    t.brand,
    t.product_line_group,
    t.item_id,
    t.item_name;
    """
df=spark.sql(query_sql)
df.createOrReplaceTempView("tmp_rlyq")
df.display()

# COMMAND ----------

# DBTITLE 1,合并结果
# MAGIC %sql
# MAGIC -- 设置动态分区覆盖模式
# MAGIC set spark.sql.sources.partitionOverwriteMode=dynamic;
# MAGIC
# MAGIC -- 插入数据到目标表（动态分区覆盖）
# MAGIC insert overwrite table ${spark.var.catalog.ads}.fin_cpt.ads_dtc_bmi_spending_mf partition(dt)
# MAGIC (
# MAGIC     month,
# MAGIC     bu_code,
# MAGIC     bu_name,
# MAGIC     store_code,
# MAGIC     store_name,
# MAGIC     category_code,
# MAGIC     category_name,
# MAGIC     brand_code,
# MAGIC     brand_name,
# MAGIC     product_line_group_code,
# MAGIC     product_line_group,
# MAGIC     item_id,
# MAGIC     item_name,
# MAGIC     gmv_before_refund,
# MAGIC     gmv_after_refund,
# MAGIC     cps_spending,
# MAGIC     cps_ratio,
# MAGIC     source,
# MAGIC     create_by,
# MAGIC     dw_create_time,
# MAGIC     dw_last_update_time,
# MAGIC     dw_batch_num,
# MAGIC     dt
# MAGIC )
# MAGIC select 
# MAGIC     month,
# MAGIC     bu_code,
# MAGIC     bu_name,
# MAGIC     store_code,
# MAGIC     store_name,
# MAGIC     category_code,
# MAGIC     category_name,
# MAGIC     brand_code,
# MAGIC     brand_name,
# MAGIC     product_line_group_code,
# MAGIC     product_line_group,
# MAGIC     item_id,
# MAGIC     item_name,
# MAGIC     gmv_before_refund,
# MAGIC     gmv_after_refund,
# MAGIC     cps_spending,
# MAGIC     cps_ratio,
# MAGIC     source,
# MAGIC     create_by,
# MAGIC     dw_create_time,
# MAGIC     dw_last_update_time,
# MAGIC     dw_batch_num,
# MAGIC     '$dt' as dt
# MAGIC from tmp_tklm  -- 20260903
# MAGIC union all 
# MAGIC select 
# MAGIC     month,
# MAGIC     bu_code,
# MAGIC     bu_name,
# MAGIC     store_code,
# MAGIC     store_name,
# MAGIC     category_code,
# MAGIC     category_name,
# MAGIC     brand_code,
# MAGIC     brand_name,
# MAGIC     product_line_group_code,
# MAGIC     product_line_group,
# MAGIC     item_id,
# MAGIC     item_name,
# MAGIC     gmv_before_refund,
# MAGIC     gmv_after_refund,
# MAGIC     cps_spending,
# MAGIC     cps_ratio,
# MAGIC     source,
# MAGIC     create_by,
# MAGIC     dw_create_time,
# MAGIC     dw_last_update_time,
# MAGIC     dw_batch_num,
# MAGIC     '$dt' as dt
# MAGIC from tmp_rlyq 
# MAGIC     union all 
# MAGIC     select 
# MAGIC         month,
# MAGIC         bu_code,
# MAGIC         bu_name,
# MAGIC         store_code,
# MAGIC         store_name,
# MAGIC         category_code,
# MAGIC         category_name,
# MAGIC         brand_code,
# MAGIC         brand_name,
# MAGIC         product_line_group_code,
# MAGIC         product_line_group,
# MAGIC         item_id,
# MAGIC         item_name,
# MAGIC         gmv_before_refund,
# MAGIC         gmv_after_refund,
# MAGIC         cps_spending,
# MAGIC         cps_ratio,
# MAGIC         source,
# MAGIC         create_by,
# MAGIC         dw_create_time,
# MAGIC         dw_last_update_time,
# MAGIC         dw_batch_num,
# MAGIC         '$dt' as dt
# MAGIC     from tmp_jxlm
# MAGIC     ;