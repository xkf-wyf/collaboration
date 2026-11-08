# CPT 接口知识库（interfaces.md）

> 来源：CPT运维SOP.docx（本地快照 2026-11-08，云端为准）

## 接口总览

| # | 接口 | trigger 管道 | Check 脚本 | 对数文件 |
|---|------|-------------|-----------|----------|
| 01 | 机制主数据 | PL_PAR_DIM_CORE_PACK_ITEM_MONTHLY | 01_机制主数据 Check | cpt数据Check追踪（第2页 sheet 记录修复） |
| 02 | GMV大数 | PL_PAR_ADS_SECOND_TOTAL_SALES_MONTHLY | 02_GMV大数 Check | GMV by PLG VS 日销看板对数_yyyymmdd |
| 03 | 机制GMV | PL_PAR_ADS_SECONDARY_GSV_GMV_MONTHLY | 03_机制GMV Check | 机制GMV check_yyyymmdd |
| 04 | BMI Spending | PL_PAR_ADS_BMI_SPENDING_MONTHLY | 04_BMI Spending Check | BMI Spending check_yyyymmdd |
| 05 | 期初理论库存 | PL_PAR_ADS_OMNI_STOCK_MONTHLY | 05_期初理论库存 Check | 期初理论库存 check_yyyymmdd |
| 06 | PDD GSV大数（人工导数） | （手动脚本） | 06_PDD GSV大数人工导数脚本 | 导出 csv 给下游（志鹏） |

推数阶段手动 trigger 所有接口父管道，**例外：PL_PAR_DIM_CORE_PACK_VARIANT_MAPPING_MANUAL**（特殊香型机制匹配手工表，需按代码里的字段与路径要求人工上传后跑脚本）。

## 01 机制主数据接口

- **流程**：trigger 管道（逻辑有变动时，需把生产脚本拉到本地手动改逻辑跑数）→ 等 DDM 打机制标（祝梅）完成并跑到 ADB → 按校验脚本 01 逐步校验（先不跑最后拉小样 List 的代码）→ 问题输出发祝梅修复 → 修复并跑到 ADB 后重新校验，循环至无问题 → 祝梅提供修复记录贴入【cpt数据Check追踪】第二页 sheet。
- **校验对象**：机制打标表 `prod_dim.ddm.dim_sku_pack_size`
- **拉小样清单**：第一步问题修复后（紧张时可同步），跑脚本最后两段代码，导出 Excel 发 Josie & Marvin，Marvin 转祝梅修复，修复后复查。

## 02 GMV大数接口

- **Check 参数**（脚本 02）：
  - `dt`：跑完的数所在分区，一般为当天日期
  - `start_mth` / `end_mth`：校验月份范围，须与跑数范围一致
  - `store`：校验店铺（第一段 python 代码可增删店铺）
- **输出**：结果或 raw data 贴入对数文件对应 sheet；null 替换为空，格式刷统一格式，gap 大的标红。
- **例外**：gap=100% 需确认是否因日销看板过滤，是则不标红。
- **Sheet 结构**：Sheet1 = CPT GMV大数接口 vs 日销看板 By Brand 对数；Sheet2 = 对数 raw data。
- **问题处理**：按校验代码逻辑查 CPT 接口表与校验对象表找原因，必要时对到更细粒度；逻辑改动或 DDM 数据问题及时反馈业务；问题/原因/方案/状态记录到【cpt数据Check追踪】。

## 03 机制GMV接口

- **Sheet 结构**：
  - Sheet1：机制打标、sku mapping 缺失分别导致的过滤 coverage，及 both_coverage，粒度 store
  - Sheet2：coverage，粒度 store+category
  - Sheet3：机制GMV 接口用的 sku 粒度销售表 vs 日销大数用的 item 粒度销售表，粒度 store+category+brand
  - Sheet4：raw data

## 04 BMI Spending 接口

- **Sheet 结构**：
  - Sheet1：CPT spending RTB vs 黄金公式看板 RTB 的 gap，粒度 store+category+brand
  - Sheet2：同上 gap，粒度 store+category+brand+plg
  - Sheet3：raw data
  - Sheet4：CPT PFM Spending vs 取数底表的 gap，粒度 store+category+brand
  - Sheet5：CPT CPS Spending vs 取数底表的 gap，粒度 store+site

## 05 期初理论库存接口

- **Sheet 结构**：
  - Sheet1：CPT 库存数字 vs 进销存看板库存的 gap（CPT 会过滤没有机制打标的），粒度 store+category
  - Sheet2：raw data

## 06 PDD GSV大数（推数阶段）

- 所有 Actual 校验完毕、下游确认推数时间后（一般晚于自动调度时间）执行。
- 手动 trigger 所有接口父管道（除 PL_PAR_DIM_CORE_PACK_VARIANT_MAPPING_MANUAL）。
- 手动执行【06_PDD GSV大数人工导数脚本】，改代码里的月份，导出 csv 给下游（志鹏）。
- 全部 trigger 完毕后通知下游（志鹏）。
- 最终 Check 结果输出【1-11月 Actual Check_yyyymmdd】和【cpt数据Check追踪-yyyymm】，邮件发业务（Robin、Josie、Winnie）。

## 对接人速查

| 事项 | 对接人 |
|------|--------|
| 机制打标表（DDM） | 祝梅（打标/修复）、Teresa（ddm 表开发逻辑） |
| cd 表 | Lvlin |
| 小样问题流转 | Josie & Marvin（Marvin 转祝梅） |
| PDD GSV / 下游通知 | 志鹏 |
| 最终 Check 邮件 | Robin、Josie、Winnie |
| 特殊香型机制手工表 | 人工按代码字段/路径要求上传 |
