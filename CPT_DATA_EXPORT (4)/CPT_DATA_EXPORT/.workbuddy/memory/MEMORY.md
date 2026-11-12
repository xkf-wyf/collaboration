# CPT_DATA_EXPORT 项目笔记

## 仓库性质
Unilever CPT（B2C）项目 Databricks 数据工厂出站接口脚本集。`CPT_DATA_EXPORT/` 下 23 个数据集目录、158 个文件（124 py + 34 sql）。

## 目录约定
每个数据集目录三段式：
- `ddl/ddl_<table>.sql|py` — Delta 建表，`partitioned by (dt)`，带 `set TAGS(project='CPT', datasetgroupname, datasetname)`
- `script/<table>.sql|py` — 主加工，`insert overwrite ... partition(dt)` 写入 `${catalog.ads}.fin_cpt.<table>`
- `script/<table>_csv.py|sql` — 出站导出，CSV 落到 `/Volumes/{ads}/fin_cpt/vol_cpt_outbound_cpt/...`，文件名 `cpt_<数据集>_{mth}.csv`（mth = dt 减 1 月）

统一参数：`dbutils.widgets` 的 `dt` / `start_mth` / `end_mth`。

## 分类
- 18 个对外接口（有 _csv 导出）：OMNI_GSV、SECONDARY_GSV、SECONDARY_GSV_GMV、SECONDARY_GSV_CLAIM、SECOND_TOTAL_SALES、OMNI_STOCK(2)、BMI_GOLDEN、BMI_SPENDING、DTC_BMI_SPENDING、CORE_PACK、CORE_PACK_ITEM、PRODUCT_HIERARCHY、PRODUCT_LINE_GROUP、CUSTOMER_HIERARCHY、STORE_MASTER、CPT_EC_PNL、CPT_EC_PFM、CPT_EC_CC_REPORT、CPT_EC_PLATFORM_BILL(3)
- 2 个内部看板（无出站）：CPT_PLANNING_DASHBOARD、CPT_PLANNING_DASHBOARD_SEC
- CPT_FINANCE 是入站链路（SharePoint 拉 Copua / OVH 发邮件），与出站无关

## 代码风格差异
`.py` 与 `.sql` 两种 notebook 混用；`.sql` 里的 Python 整段包在 `-- MAGIC %python` 注释中。
主脚本头部用 `-- v1.x 作者 日期 说明` 累积变更日志，是唯一的口径文档来源。

## 校验文件位置（重要）
不在 `CPT_DATA_EXPORT/` 内，而在**同级目录** `F:/NW-诺唯/协作/CPT_DATA_EXPORT (4)/校验/`：
- `正式脚本_03_机制GMV Check.ipynb`（16MB，21 cell）→ 对应 SECONDARY_GSV_GMV 接口
- `正式脚本_04_BMI Spending Check.ipynb`（11MB，40 cell）→ 对应 BMI_SPENDING 接口

仅覆盖 18 个接口中的 2 个。详见当日日志。
