# Databricks notebook source
sparksql01 = f'''
SELECT DISTINCT email
FROM (
    SELECT admin AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE admin IS NOT NULL AND admin != ''
    UNION ALL
    SELECT function_owner_1 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE function_owner_1 IS NOT NULL AND function_owner_1 != ''
    UNION ALL
    SELECT function_owner_2 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE function_owner_2 IS NOT NULL AND function_owner_2 != ''
    UNION ALL
    SELECT function_owner_3 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE function_owner_3 IS NOT NULL AND function_owner_3 != ''
    UNION ALL
    SELECT function_owner_4 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE function_owner_4 IS NOT NULL AND function_owner_4 != ''
    UNION ALL
    SELECT function_owner_5 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE function_owner_5 IS NOT NULL AND function_owner_5 != ''
    UNION ALL
    SELECT fin_bp_1 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE fin_bp_1 IS NOT NULL AND fin_bp_1 != ''
    UNION ALL
    SELECT fin_bp_2 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE fin_bp_2 IS NOT NULL AND fin_bp_2 != ''
    UNION ALL
    SELECT fin_bp_3 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE fin_bp_3 IS NOT NULL AND fin_bp_3 != ''
    UNION ALL
    SELECT fin_bp_4 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE fin_bp_4 IS NOT NULL AND fin_bp_4 != ''
    UNION ALL
    SELECT fin_bp_5 AS email FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_mapping_table_df WHERE fin_bp_5 IS NOT NULL AND fin_bp_5 != ''
) AS all_emails
WHERE email IS NOT NULL AND email != '';
'''
spark_df01 = spark.sql(sparksql01)
# 2. 批量邮箱拼接 英文逗号分隔 标准邮件格式
email_list = [row.email for row in spark_df01.collect()]
recipients_str = ",".join(email_list)

# 打印校验结果
print("最终收件人逗号拼接格式：", recipients_str)

dbutils.notebook.exit(recipients_str)
