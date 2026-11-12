# Databricks notebook source
# MAGIC %pip install UnileverDatalakeToolkits ${PYPI_URL}
# MAGIC # 重启python环境
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from UnileverDatalakeToolkits import mail
import pandas as pd
import base64
import os

# dt_date='20260417'
dt_date = dbutils.widgets.get("dt")
subject = dbutils.widgets.get("subject")
recipients = dbutils.widgets.get("recipients")
cc = dbutils.widgets.get("cc")
dir_img = dbutils.widgets.get("img_bg")

# 设置主题匹配月份
month_abbr = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
}
# 提取月份和年份
year = dt_date[:4]
month = dt_date[4:6]
month_name = month_abbr.get(month, 'Month') 
# 从目标表匹配邮件正文日期
query_sql = f"""
    SELECT close_date_display
    FROM ${{spark.var.catalog.ods}}.int_manual.ods_finance_calendar_date_df
    WHERE regexp_replace(email_send_date, '/|-', '') = '{dt_date}'
"""
df_calendar = spark.sql(query_sql)
if df_calendar.count() > 0:
    close_date = df_calendar.collect()[0]["close_date_display"]
    close_date_formatted = str(close_date).replace("-", "/")
else:
    close_date = "未設定關賬日期"
    close_date_formatted = close_date

try:
    dbutils
except NameError:
    dbutils = None

def send_mail():
    # 转成列表
    recipients_list = [e.strip() for e in recipients.split(",") if e.strip()]
    # 多个抄送 → 转成 []
    if cc.strip() == "":
        cc_list = []
    else:
        cc_list = [e.strip() for e in cc.split(",") if e.strip()]
    
    subject_final = f"{subject} - {month_name} {year}"

    # 1. 读取图片并转 Base64
    # 注意：确保路径正确，这里假设 dir_img 只是文件名或者相对路径
    # 如果 dir_img 包含路径，请根据实际情况调整
    background_image_path = f"/Volumes/{spark.conf.get('spark.var.catalog.ods')}/int_manual/vol_cpt_inbound_manual/{dir_img}"
    background_image_base64 = ""
    
    try:
        with open(background_image_path, "rb") as f:
            image_data = f.read()
        background_image_base64 = base64.b64encode(image_data).decode('utf-8')
        background_image_base64 = background_image_base64.replace('\n', '').replace('\r', '')
        print(f"成功读取图片，长度: {len(background_image_base64)}")
    except FileNotFoundError:
        print(f"找不到图片: {background_image_path}")

    bg_src = f"data:image/png;base64,{background_image_base64}"
    
    # 获取 Notebook 路径
    try:
        notebook_path = (
            dbutils.notebook.entry_point.getDbutils()
            .notebook()
            .getContext()
            .notebookPath()
            .get()
        )
    except Exception:
        notebook_path = "Local Environment"

    # 2. 修改 HTML 结构
    # 去掉了 body 的背景图，改为白色背景
    # 在 mail-card 底部添加了右对齐的图片表格
    html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 40px 30px;
            font-family: "Century Gothic", Arial, sans-serif;
            font-size: 11pt;
            color: #0c64c0;
            line-height: 1.6;
            background-color: #ffffff; /* 改为白色背景 */
        }}
        .mail-card {{
            max-width: 900px;
            margin: 0 auto;
            background: transparent !important;
            border: none !important;
            padding: 0;
        }}
        h2 {{
            margin: 0 0 30px;
            text-align: center;
            font-size: 18pt;
            color: #0c64c0;
            font-weight: 700;
        }}
        p {{
            margin: 0 0 16px;
            font-size: 11pt;
            color: #0c64c0;
        }}
        a {{
            color: #0c64c0;
            text-decoration: underline;
            font-weight: bold;
        }}
        
        /* 隐藏可能的页脚/免责声明元素 (保留你原有的逻辑) */
        body > div:last-child,
        body > p:last-of-type,
        .MsoNormal:last-child {{ 
            display: none !important; 
            visibility: hidden !important;
            height: 0 !important;
            font-size: 0 !important;
        }}
    </style>
    </head>

    <body>
        <div class="mail-card">
            <h2>OVH Open PO Dashboard</h2>
            
            <p>Dear colleagues,</p>
            <p>This is a reminder that Coupa GR cutoff date for this month is <strong style="text-decoration: underline;">{close_date_formatted}</strong>. If your goods or services have been received and meet the standards, please make sure the GR process is completed before cutoff.</p>

            <p>For latest PO details and GR status, please access <a href="https://app.powerbi.com/groups/be375e5e-330f-46d5-a457-24ff7feddc53/reports/bcb590b9-d31e-4da3-b2e1-8de3e99d77e9/defaa3fdb6cd26d22ec2?experience=power-bi">OVH Open PO Dashboard</a>.</p>

            <p style="font-style: italic;">This dashboard is refreshed daily and provides comprehensive overview of Overheads PO list, GR status, and amounts.</p>
        
            <p>For questions or specific report requests, please contact: <a href="mailto:Sherry.Ke@unilever.com">Sherry.Ke@unilever.com</a>.</p>

            <!-- 新增：右下角落款图片 -->
            <!-- 使用表格布局确保在邮件客户端中右对齐最稳定 -->
            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="margin-top: 40px;">
                <tr>
                    <td align="right">
                        <img src="{bg_src}" style="max-width: 300px; height: auto; display: block;" />
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
    m = mail.M365Mail()
    
    # 发送邮件
    m.send_mail(
        recipients=recipients_list,
        cc_recipients=cc_list,
        subject=subject_final,
        body=html
    )
    
    print("邮件发送成功！")

if __name__ == "__main__":
    send_mail()
