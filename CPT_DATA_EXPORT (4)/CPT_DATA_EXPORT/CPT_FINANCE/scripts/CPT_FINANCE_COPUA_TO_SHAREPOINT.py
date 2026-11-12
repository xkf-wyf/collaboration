# Databricks notebook source
# 访问sharepoint依赖
%pip install UnileverDatalakeToolkits ${PYPI_URL}
# Excel文件写入依赖
%pip install openpyxl
# 重启python环境
dbutils.library.restartPython()

# COMMAND ----------

import os
from pyspark.sql import SparkSession
import pandas as pd
import shutil
from datetime import datetime, timedelta
from UnileverDatalakeToolkits.sharepoint import SharepointOperator

# 配置参数
# 邮件发送sitename
site_name = "ChinaFinanceReport-OVHPOdashboard"
# sharepoint archive路径
# sharepoint_base_path = "Shared Documents/OVH Raw_data_archive"
# sharepoint 输出路径
sharepoint_path = "Shared Documents/OVH Raw_data"
# 输出文件路径，生产测试需调整
outpath_blob = "/Volumes/" + spark.conf.get("spark.var.catalog.ods") + "/int_manual/vol_cpt_inbound_manual/"
# 参数接收
folder_name = dbutils.widgets.get("dir")                      # 文件输出路径
filename = dbutils.widgets.get("filename")                        # 输出后的文件名
dt = dbutils.widgets.get("dt")                                    # 分区字段

# # 测试参数
# dt = "2026-04-10"
outpath = outpath_blob + folder_name + dt                                  #blob输出路径
# filename = "Copua_Order_Data.xlsx"

sparksql01 = f'''
SELECT
    t.accountassignmentcode,
    t.accountassignmentsequentialnumber,
    t.accountassignmentsplitpercentage,
    t.assetnumber,
    t.bdlflag,
    t.bdlloadtimestamp,
    t.bdlupdatetimestamp,
    t.businessareacode,
    t.buyingchannelname,
    t.cancelleddate,
    t.committypename,
    t.companycode,
    t.contractdescription,
    t.contractnumber,
    t.costcentrecode,
    t.creationdate,
    t.dcisourcingcode,
    t.documentcurrencyamount,
    t.documentcurrencycode,
    t.glaccountnumber,
    t.goodsreceiptdate,
    t.goodsreceiptdocumentcurrencyamount,
    t.goodsreceiptlocalcurrencyamount,
    t.goodsreceiptquantity,
    t.goodsreceiptreportingcurrencyeuroamount,
    t.goodsreceiptreportingcurrencyusdamount,
    t.handlinggroupname,
    t.incotermscode,
    t.internalordernumber,
    t.latestgoodsreceiptsubmitteddate,
    t.localcurrencyamount,
    t.localcurrencycode,
    t.market,
    t.materialnumber,
    t.needbydate,
    t.paymenttermcode,
    t.plantcode,
    t.preferredsupplierstatus2name,
    t.preferredsupplierstatusname,
    t.profitcentrecode,
    t.purchasecommoditycode,
    t.purchaseorderlinedescription,
    t.purchaseorderlinenumber,
    t.purchaseorderlinestatusname,
    t.purchaseorderlineversionnumber,
    t.purchaseordernumber,
    t.purchaseordersentmethodname,
    t.purchaseorderstatusname,
    t.purchaseordertypecode,
    t.purchaseorderversionnumber,
    t.purchaseorganisationcode,
    t.purchasequantity,
    t.purchaserequisitionapprovedbyloginname,
    t.purchaserequisitioncreationdate,
    t.purchaserequisitiondescription,
    t.purchaserequisitionnumber,
    t.purchaserequisitiononbehalfofname,
    t.purchaserequisitionrequestername,
    t.purchaserequisitionsubmitteddate,
    t.purchaserequisitiontypename,
    t.purchasesuppliercode,
    t.regionid,
    t.reportingcurrencyeuroamount,
    t.reportingcurrencyusdamount,
    t.serviceindicator,
    t.sourcesystemname,
    t.startdate,
    t.storagelocationcode,
    t.substoragelocationcode,
    t.supplierauxiliarypartnumber,
    t.supplierpartnumber,
    t.tagslisttext,
    t.taxcode,
    t.unitofmeasurecode,
    t.unitpriceamount,
    t.wbselementcode,
    t.workordernumber,
    -- CA 列：PO creation year
    year(t.creationdate) AS po_creation_year,
    -- CB 列：Days since PO creation
    datediff(current_date(), t.creationdate) AS days_since_po_creation,
    -- CC 列：Aging group
    CASE
        WHEN datediff(current_date(), t.creationdate) < 90  THEN 'less than 90'
        WHEN datediff(current_date(), t.creationdate) <= 180 THEN '90D-180D'
        WHEN datediff(current_date(), t.creationdate) <= 360 THEN '180D-360D'
        ELSE 'Over 360'
    END AS aging_group,
    -- CD 列：PO remaining amount
    CASE
        WHEN t.purchaseorderlinestatusname IN ('cancelled','soft_closed_for_invoicing')
        THEN 0
        ELSE nvl(t.localcurrencyamount, 0) - nvl(t.goodsreceiptlocalcurrencyamount, 0)
    END AS po_remaining_amount,
    -- CE 列：GR%
    CASE
        WHEN t.purchaseorderlinestatusname IN ('cancelled','soft_closed_for_invoicing')
        THEN 0
        WHEN nvl(t.localcurrencyamount, 0) = 0
        THEN 0
        ELSE round(nvl(t.goodsreceiptlocalcurrencyamount, 0) / t.localcurrencyamount, 6)
    END AS gr_percentage,
    -- CF 列：GOVH/SCOVH
    m.govh_scovh,
    -- CG 列：BU/National
    m.bu_national,
    -- CH 列：Function
    m.bu_national_2
FROM ${{spark.var.catalog.ods}}.int_bdl_sc.ods_bdl_vwcoupapurchaseorderu2k2_di t
INNER JOIN ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df m
ON regexp_replace(cast(t.costcentrecode AS string), '^0+', '') = m.costcentrecode
WHERE t.dt='{dt}'
AND t.creationdate >='2025-01-01'
;
'''
spark_df01 = spark.sql(sparksql01)
# 转换为pandas DataFrame
pandas_df01 = spark_df01.toPandas()

############################ 文件处理

def adjust_column_len(worksheet,pandas_df):
    """
    调整输出sheet的列宽
    param worksheet: 目标sheet
    param pandas_df: 来源df
    注意：需确保列名不重复
    """
    # openpyxl 的行列索引从 ‌1‌ 开始（与 Excel 原生坐标一致）
    for idx, col in enumerate(pandas_df.columns,start=1):
        # 获取每列数据最大长度
        data_len = pandas_df[col].astype(str).map(len).max()
        # 如果为空则最大长度为0
        data_max_len = 0 if pd.isna(data_len) else data_len
        # 取标题和data的最大长度
        max_len = max(data_max_len,len(col)) + 2
        # 调整对应字段最大长度
        worksheet.column_dimensions[worksheet.cell(row=1, column=idx).column_letter].width = max_len * 1.2

# 将内容写入excel文件
tmp_excel_path = "/tmp/" + filename
with pd.ExcelWriter(tmp_excel_path, engine="openpyxl") as writer: 
    print("开始进行文件写入...")
    pandas_df01.to_excel(writer, sheet_name='Mapping_data', index=False, header=True)
    print("开始调整列宽...")
    adjust_column_len(writer.sheets['Mapping_data'],pandas_df01)
print(f"文件已生成：{tmp_excel_path}")

export_path = outpath + "/" + filename
# export_path_ed = edpath + "/" + filename
dbutils.fs.cp("file://" + tmp_excel_path, export_path)
print(f"已完成文件复制：{export_path}")
# dbutils.fs.cp("file://" + tmp_excel_path, export_path_ed)
# print(f"已完成文件复制：{export_path_ed}")

# 删除tmp目录
dbutils.fs.rm(tmp_excel_path,True)
print(f"临时目录：{tmp_excel_path}已删除")

################################################### 开始将文件上传至sharepoint ###################################################

# 初始化SharePoint操作对象
s = SharepointOperator(site_name)

# 检查文件夹是否存在，不存在则创建
# archive路径
# target_folder_path = f"{sharepoint_base_path}/{dt}"
# if not s.is_sharepoint_folder_exists(target_folder_path):
#     print(f"创建目标文件夹: {target_folder_path}")
#     s.create_sharepoint_folder(target_folder_path)
# else:
#     print(f"文件夹已存在: {target_folder_path}")

# sharepoint 输出路径
target_folder_path2 = f"{sharepoint_path}"
if not s.is_sharepoint_folder_exists(target_folder_path2):
    print(f"创建目标文件夹: {target_folder_path2}")
    s.create_sharepoint_folder(target_folder_path2)
else:
    print(f"文件夹已存在: {target_folder_path2}")

# 上传文件到目标文件夹
# archive
local_file_path = f"{outpath}/{filename}"
# sharepoint_file_path = f"{target_folder_path}"
sharepoint_file_path2 = f"{target_folder_path2}"


print(f"\n上传文件到SharePoint: {sharepoint_file_path2}")
# s.upload_file_to_sharepoint_folder(local_file_path, sharepoint_file_path)
s.upload_file_to_sharepoint_folder(local_file_path, sharepoint_file_path2)

print("文件上传成功")