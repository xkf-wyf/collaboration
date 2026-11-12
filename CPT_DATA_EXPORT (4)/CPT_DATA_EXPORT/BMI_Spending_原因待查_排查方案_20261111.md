# BMI Spending `原因待查` 异常排查方案

> **数据源**：`F:\NW-诺唯\CPT\HCPC\十一月月结输出\04_BMI Spending Check_20261111.xlsx` → sheet `raw data`（6,084 行，覆盖 202601–202610）
> **排查对象**：`reason = 原因待查` 共 **38 行**，差额绝对值合计 **562,967 元**
> **排查范围**：限定 `fin_cpt` / `cpt` schema
> **编制**：2026-11-11 ｜ 替代上一版（上一版基于 20261110 文件，仅 5 行 / 4,972 元，全部是本版 38 行的子集）

---

## 一、本期变化：为什么从 5 行变成 38 行

| 维度 | 20261110 | 20261111 | 变化 |
|---|---|---|---|
| raw data 行数 | 5,428 | 6,084 | +656 |
| 月份范围 | 202601–202609 | 202601–**202610** | 新增 202610（648 行） |
| 原因待查 | 5 行 / 4,972 元 | **38 行 / 562,967 元** | +33 行 / +55.8 万 |

拆分增量来源：

- **新增 202610 带来 25 行**，金额约 **51.2 万**（占本期总额 91%）
- **历史月份重跑带来 8 行**（202601 +2、202604 +1、202606 +1、202607 +1、202609 +3）
- 上一期的 `202608 / PDD - VSL / SKIN / VASELINE / OTHERS`（35,577 元）**本期已消失**，说明历史月份重跑后已对齐 —— 这类单月偶发差异具备自愈性，不必单独追

结论：**本期主要矛盾在 202610**，其余是持续性存量问题。

---

## 二、38 行按形态分组

| 组 | 形态特征 | 行数 | 差额（元） | 占比 | 性质判定 |
|---|---|---|---|---|---|
| **A** | JD - UL / HAIR / CLEAR / CORE，202604 起持续、比例型差异 | 7 | **337,480** | 59.9% | 口径漂移，**金额最大** |
| **B** | 202610 全月 DEO / LUX，5 店铺 golden 同时为 0 | 9 | **156,297** | 27.8% | 黄金公式侧月度维度缺失 |
| **D** | JD - UL / HHC / CIF，高比例差 | 2 | 34,227 | 6.1% | 小品类 item 级差异 |
| **E** | JD - UL / PW / LUX / OTHERS（202603） | 1 | 15,983 | 2.8% | OTHERS 桶错位 |
| **F** | JD - UL / SKIN / VASELINE / LIP&CUTTIE，全期持续 | 10 | 12,308 | 2.2% | 持续小额比例差 |
| **C** | 零星 golden=0（202601 / 202609） | 6 | 5,864 | 1.0% | 单月维度落点差异 |
| **G** | DERMA ↔ GWP/SAMPLE 配对 | 2 | 404 / −403 | ≈0 | **打标错位确证样本** |
| **H** | int() 截断假阳性 | 1 | −1 | — | 直接关闭 |

**A + B 两组占 87.7%**，是本次排查的主战场。D/E/F 属存量小额，G 是解 A 组的钥匙，H 无需处理。

---

## 三、关键观察（三条，直接决定排查方向）

### 观察 1：A 组存在明确的起始拐点 —— 202604

JD - UL / HAIR / CLEAR / CORE 这一组合，202601–202603 **完全对平**，从 202604 开始出现差异并持续放大：

| 月份 | gap（元） | gap% |
|---|---|---|
| 202601–202603 | 0 | 0 |
| 202604 | 8,705 | 0.43% |
| 202605 | 45,672 | 1.49% |
| 202606 | 27,788 | 0.77% |
| 202607 | 31,050 | 1.38% |
| 202608 | 43,152 | 1.46% |
| 202609 | 48,622 | 1.35% |
| 202610 | **132,491** | **3.14%** |

有起点、持续存在、比例逐步抬升 —— 这是**某次变更引入了系统性偏差**的典型特征，不是随机误差。排查应聚焦 202604 前后 CLEAR 品牌在 JD 渠道的什么变了（新品上线、组合装、打标表版本、店铺新增）。

### 观察 2：B 组是整月整品牌的集体缺失，不是单店问题

202610 的 DEO / LUX，**跨 5 个店铺、9 个维度组合，golden 侧一律为 0**：

| 店铺 | plg | cpt | golden |
|---|---|---:|---:|
| PDD - UL | DEO LOTION | 35,576.45 | 0 |
| PDD - UL | DEO LOTION MIST | 9,762.58 | 0 |
| TMALL FGS - LUX | DEO LOTION | 35,100.68 | 0 |
| TMALL FGS - LUX | OTHERS | 28,248.31 | 0 |
| JD - UL | DEO LOTION | 23,263.84 | 0 |
| JD - UL | DEO LOTION MIST | 16,916.46 | 0 |
| TMALL SUPER | OTHERS | 4,175.12 | 0 |
| TMALL FGS - BPC | DEO LOTION | 3,210.42 | 0 |
| TMALL FGS - BPC | OTHERS | 47.09 | 0 |

5 个不同渠道的店铺同时归零，**不可能用单店归店口径解释**。指向黄金公式侧在 202610 的品牌（或品类）维度映射缺失、或该月数据未完整回传。

### 观察 3：G 组是「品线组打标错位」的干净确证样本

202603 / JD - UL / SKIN / VASELINE：

| plg | CPT | golden | 差 |
|---|---:|---:|---:|
| DERMA | 158,200.56 | 157,796.65 | +403.91 |
| GWP/SAMPLE | 0.00 | 403.91 | −403.91 |

**同一笔 403.91 元，CPT 归到 `DERMA`，golden 归到 `GWP/SAMPLE`**，两侧合计完全相等（158,200.56 vs 158,200.56），差额为零。

这是 `pfm_product_line_group`（CPT 侧）与 `product_group`（golden 侧）打标不一致的**实锤**。A 组 33.7 万的差异，很可能也是同类机制 —— 只是量级大、且不完全对冲。

---

## 四、接口链路速查（RTB 分支）

`fin_cpt.ads_bmi_spending_mf`，`index_type = 'Paid Media-RTB'`

```
上游：dws.ddm.dws_pfm_total_item_df
  ├─ 分支① 能关联打标表（t2.bu is not null）
  │     join dim.ddm.dim_prd_item (is_current=1)
  │          on item_id + if(platform in('VIP','TMALL SUPER'),shop_id,platform)
  │          and period_key between start_time and end_time
  │         → category / brand / bu / product_line_group
  │     join dim.ddm.dim_store (status=1)
  │          on coalesce(dim_prd_item.shop_id, fact.shop_id) = dim_store.shop_id   ← 仅 shop_id
  │         → customer(=store_name) / channel(=customer_type) / platform(=site_name)
  │
  └─ 分支② 店铺维度（t2.bu is null 且 (item_id in ('0','-') 或 Package 且 item_id is null)）
        join dim_store on shop_id AND platform      ← v1.4 20260609 修正，仅此分支
        维度取事实表自带列：pfm_category / pfm_brand / pfm_bu / pfm_product_line_group
```

**PDD 归店硬编码**：

```sql
if(t1.period_key > '2025-10-16' and t2.shop_id = '621699362', 'PDD - VSL', t3.customer)
```

**落表口径**：`value_taxed = round(sum(pfm_spending),2)`（含税，校验用）｜`value = round(sum(pfm_spending)/1.06,2)`

**golden 侧**：`fin_cpt.ads_bmi_golden_mf`，`index_type='rtb_spending'`，`value` 字段；
维度全部直接取事实表自带列 `store_group / category / brand / product_group / bu / site`。

### 两侧维度来源差异（一切差异的源头）

| 维度 | CPT（RTB） | golden |
|---|---|---|
| `store_name` | `dim_store.customer` + 621699362 硬编码 | `fact.store_group` |
| `category` | `dim_prd_item.category` 或 `pfm_category` | `fact.category` |
| `brand` | `dim_prd_item.brand` 或 `pfm_brand` | `fact.brand` |
| `product_line_group` | `dim_prd_item.product_line_group` 或 `pfm_product_line_group` | `fact.product_group` |
| `bu` | `dim_prd_item.bu` 或 `pfm_bu` | `fact.bu` |
| `site_name` | `dim_store.platform` | `fact.site` |

---

## 五、排查 SQL

> 占位符：`{DT}` = `ads_bmi_spending_mf` 分区（校验的 `$dt`，对应 20261111 批次）；`{GDT}` = `ads_bmi_golden_mf` 分区。
> 统一用 `abs(gap) >= 0.01` 作阈值，规避 `int()` 截断造成的假阳性。

### S0-a 确认可用分区（第一步）

```sql
select 'bmi_spending' as tbl, dt, count(*) as cnt
     , min(month) as min_month, max(month) as max_month
from fin_cpt.ads_bmi_spending_mf
where index_type = 'Paid Media-RTB'
group by dt
union all
select 'bmi_golden', dt, count(*), min(month), max(month)
from fin_cpt.ads_bmi_golden_mf
where index_type = 'rtb_spending'
group by dt
order by tbl, dt desc;
```

**关注**：`bmi_golden` 是否有覆盖 202601–202610 的分区。若没有同期分区，先确认哪个分区装全了这 10 个月。

---

### S0-b 基准校准（必做，否则后续结论不可信）

**已知锚点**：202601 / PDD - UL / PW / LUX / OTHERS → golden = **177.19**

```sql
select month, store_name, category_name, brand_name
     , coalesce(product_line_group,'<NULL>') as plg
     , count(*) as row_cnt
     , round(sum(value),2) as golden_value
from fin_cpt.ads_bmi_golden_mf
where dt = '{GDT}'
  and index_type = 'rtb_spending'
  and store_name = 'PDD - UL'
  and category_name = 'PW' and brand_name = 'LUX'
  and month in ('202601','202602','202603')
group by month, store_name, category_name, brand_name
       , coalesce(product_line_group,'<NULL>')
order by month, plg;
```

**判断**：能查到 `177.19` → 镜像基准可用；查不到 → 镜像与原表不等价（大概率 `left join dim_store` 时 `national_ex25` 不唯一导致行放大），需先修基准再往下走。

---

### S1【A 组】JD - UL / HAIR / CLEAR / CORE 逐月趋势

**目的**：确认 202604 拐点，判断偏差是否随时间累积。

```sql
with cpt as (
    select month, round(sum(value_taxed),2) as amt
    from fin_cpt.ads_bmi_spending_mf
    where dt = '{DT}' and index_type = 'Paid Media-RTB'
      and store_name = 'JD - UL' and category_name = 'HAIR' and brand_name = 'CLEAR'
      and product_line_group = 'CORE'
      and month between '202601' and '202610'
    group by month
), gld as (
    select month, round(sum(value),2) as amt
    from fin_cpt.ads_bmi_golden_mf
    where dt = '{GDT}' and index_type = 'rtb_spending'
      and store_name = 'JD - UL' and category_name = 'HAIR' and brand_name = 'CLEAR'
      and product_line_group = 'CORE'
      and month between '202601' and '202610'
    group by month
)
select coalesce(c.month, g.month)                    as month
     , coalesce(c.amt, 0)                            as cpt_amt
     , coalesce(g.amt, 0)                            as golden_amt
     , round(coalesce(c.amt,0) - coalesce(g.amt,0), 2) as gap
     , round((coalesce(c.amt,0) - coalesce(g.amt,0))
             / nullif(coalesce(c.amt,0), 0) * 100, 2)  as gap_pct
from cpt c
full join gld g on c.month = g.month
order by month;
```

**判断**：202601–202603 应为 0，202604 起转正并扩大 → 确认拐点。

---

### S2【A 组】是否被挪到别的品线组（有无对冲）

**目的**：区分「真实多算」和「品线组错位」。若其他 plg 出现等额负差，即错位。

```sql
with cpt as (
    select month, coalesce(product_line_group,'<NULL>') as plg, sum(value_taxed) as v
    from fin_cpt.ads_bmi_spending_mf
    where dt = '{DT}' and index_type = 'Paid Media-RTB'
      and store_name = 'JD - UL' and category_name = 'HAIR' and brand_name = 'CLEAR'
      and month between '202604' and '202610'
    group by month, coalesce(product_line_group,'<NULL>')
), gld as (
    select month, coalesce(product_line_group,'<NULL>') as plg, sum(value) as v
    from fin_cpt.ads_bmi_golden_mf
    where dt = '{GDT}' and index_type = 'rtb_spending'
      and store_name = 'JD - UL' and category_name = 'HAIR' and brand_name = 'CLEAR'
      and month between '202604' and '202610'
    group by month, coalesce(product_line_group,'<NULL>')
)
select coalesce(c.month, g.month)   as month
     , coalesce(c.plg,   g.plg)     as plg
     , round(coalesce(c.v,0), 2)    as cpt_amt
     , round(coalesce(g.v,0), 2)    as golden_amt
     , round(coalesce(c.v,0) - coalesce(g.v,0), 2) as gap
from cpt c
full join gld g on c.month = g.month and c.plg = g.plg
where abs(coalesce(c.v,0) - coalesce(g.v,0)) >= 0.01
order by month, abs(coalesce(c.v,0) - coalesce(g.v,0)) desc;
```

**判断**
- 只有 `CORE` 一行有差、其他 plg 无反向 → **真实多算**，需查打标表与事实表的行放大
- 其他 plg 出现等额负差 → **品线组错位**，同 G 组机制

---

### S3【A 组】店铺级总额守恒

**目的**：判断差额是只在维度上错位，还是 JD - UL 整店总额真的多算。

```sql
with cpt as (
    select month, sum(value_taxed) as v
    from fin_cpt.ads_bmi_spending_mf
    where dt = '{DT}' and index_type = 'Paid Media-RTB'
      and store_name = 'JD - UL' and month between '202601' and '202610'
    group by month
), gld as (
    select month, sum(value) as v
    from fin_cpt.ads_bmi_golden_mf
    where dt = '{GDT}' and index_type = 'rtb_spending'
      and store_name = 'JD - UL' and month between '202601' and '202610'
    group by month
)
select coalesce(c.month, g.month)   as month
     , round(coalesce(c.v,0), 2)    as cpt_total
     , round(coalesce(g.v,0), 2)    as golden_total
     , round(coalesce(c.v,0) - coalesce(g.v,0), 2) as gap
     , round((coalesce(c.v,0) - coalesce(g.v,0))
             / nullif(coalesce(g.v,0),0) * 100, 4) as gap_pct
from cpt c full join gld g on c.month = g.month
order by month;
```

**判断**
- 整店 gap ≈ 0，但 A 组有 33.7 万差 → 说明被其它 category/brand 的反向差异抵消，**属维度切分问题，总量没错**
- 整店 gap 也约 33.7 万 → **真实多算**，转 S4 查行放大

---

### S4【A 组】行放大排查：site / customer_type 维度核查

**目的**：分支① 的 `dim_store` 关联只用了 `shop_id`（分支② 已在 v1.4 改为 `shop_id AND platform`）。若同一 `shop_id` 在 `dim_store` 中有多行，会 fan-out 放大金额。

```sql
select month, site_name, customer_type
     , count(*) as row_cnt
     , round(sum(value_taxed), 2) as amt
from fin_cpt.ads_bmi_spending_mf
where dt = '{DT}' and index_type = 'Paid Media-RTB'
  and store_name = 'JD - UL' and category_name = 'HAIR' and brand_name = 'CLEAR'
  and product_line_group = 'CORE'
  and month between '202601' and '202610'
group by month, site_name, customer_type
order by month, site_name;
```

**判断**：若 202604 起 `site_name` 或 `customer_type` 出现新取值 / 空值 / 同月多行 → `dim_store` 关联歧义，需把分支① 也改成 `shop_id AND platform`。

> 若要进一步确认是否 `dim_prd_item` 一对多（同 item 多个 current 版本导致费用被重复计入），需出 `fin_cpt` 查 `dim.ddm.dim_prd_item`，见第七节。

---

### S5【B 组】202610 全店铺 DEO / LUX 双侧对照

**目的**：一次性看清 5 个店铺 golden 是否全为 0，以及 CPT 侧的全貌。

```sql
select 'cpt' as src, store_name
     , coalesce(product_line_group,'<NULL>') as plg
     , count(*) as row_cnt
     , round(sum(value_taxed), 2) as amt
from fin_cpt.ads_bmi_spending_mf
where dt = '{DT}' and index_type = 'Paid Media-RTB'
  and month = '202610' and category_name = 'DEO' and brand_name = 'LUX'
group by store_name, coalesce(product_line_group,'<NULL>')
union all
select 'golden', store_name
     , coalesce(product_line_group,'<NULL>')
     , count(*)
     , round(sum(value), 2)
from fin_cpt.ads_bmi_golden_mf
where dt = '{GDT}' and index_type = 'rtb_spending'
  and month = '202610' and category_name = 'DEO' and brand_name = 'LUX'
group by store_name, coalesce(product_line_group,'<NULL>')
order by src, store_name, amt desc;
```

**判断**：golden 侧返回 0 行 → 确认整品牌缺失。

---

### S6【B 组】判定是「品牌级」还是「品类级」缺失

**目的**：区分是 LUX 这个品牌没映射上，还是整个 DEO 品类没进来。这是给上游提单的关键依据。

```sql
select 'cpt' as src, brand_name
     , count(*) as row_cnt
     , round(sum(value_taxed), 2) as amt
from fin_cpt.ads_bmi_spending_mf
where dt = '{DT}' and index_type = 'Paid Media-RTB'
  and month = '202610' and category_name = 'DEO'
group by brand_name
union all
select 'golden', brand_name, count(*), round(sum(value), 2)
from fin_cpt.ads_bmi_golden_mf
where dt = '{GDT}' and index_type = 'rtb_spending'
  and month = '202610' and category_name = 'DEO'
group by brand_name
order by src, amt desc;
```

**判断**
- golden 侧 DEO 下其他品牌（DOVE / REXONA）正常、仅 LUX 为 0 → **品牌级映射缺失**
- golden 侧 DEO 整品类为 0 → **品类级缺失，或 10 月数据未回传**

---

### S7【B 组】确认是否为 202610 新增缺失

```sql
select 'cpt' as src, month
     , round(sum(value_taxed), 2) as amt
from fin_cpt.ads_bmi_spending_mf
where dt = '{DT}' and index_type = 'Paid Media-RTB'
  and category_name = 'DEO' and brand_name = 'LUX'
  and month between '202601' and '202610'
group by month
union all
select 'golden', month, round(sum(value), 2)
from fin_cpt.ads_bmi_golden_mf
where dt = '{GDT}' and index_type = 'rtb_spending'
  and category_name = 'DEO' and brand_name = 'LUX'
  and month between '202601' and '202610'
group by month
order by src, month;
```

**判断**：202601–202609 golden 都有值、仅 202610 为 0 → **本期新增缺失**，优先找黄金公式侧确认 10 月回传与品牌映射配置。

---

### S8【G 组】DERMA ↔ GWP/SAMPLE 错位确证

```sql
select 'cpt' as src
     , product_line_group
     , count(*) as row_cnt
     , round(sum(value_taxed), 2) as amt
from fin_cpt.ads_bmi_spending_mf
where dt = '{DT}' and index_type = 'Paid Media-RTB'
  and store_name = 'JD - UL' and category_name = 'SKIN' and brand_name = 'VASELINE'
  and month = '202603'
  and product_line_group in ('DERMA','GWP/SAMPLE','CORE','OTHERS')
group by product_line_group
union all
select 'golden', product_line_group, count(*), round(sum(value), 2)
from fin_cpt.ads_bmi_golden_mf
where dt = '{GDT}' and index_type = 'rtb_spending'
  and store_name = 'JD - UL' and category_name = 'SKIN' and brand_name = 'VASELINE'
  and month = '202603'
  and product_line_group in ('DERMA','GWP/SAMPLE','CORE','OTHERS')
group by product_line_group
order by src, product_line_group;
```

**预期结果**：CPT 侧 `DERMA = 158,200.56 / GWP SAMPLE = 0`，golden 侧 `DERMA = 157,796.65 / GWP SAMPLE = 403.91`，两侧合计相等。
→ 确认 403.91 元是打标差异，非数据缺失。

---

### S9【G 组】GWP/SAMPLE 桶的全局系统性偏差

**目的**：若 CPT 侧 `GWP/SAMPLE` 系统性偏少、且差额能被其它 plg 的超出额对冲，说明这是全局性的打标口径问题，会污染多个品类。

```sql
select month, store_name, category_name, brand_name
     , round(sum(case when src = 'cpt'    then amt else 0 end), 2) as cpt_amt
     , round(sum(case when src = 'golden' then amt else 0 end), 2) as golden_amt
     , round(sum(case when src = 'cpt'    then amt else 0 end)
           - sum(case when src = 'golden' then amt else 0 end), 2) as gap
from (
    select 'cpt' as src, month, store_name, category_name, brand_name
         , value_taxed as amt
    from fin_cpt.ads_bmi_spending_mf
    where dt = '{DT}' and index_type = 'Paid Media-RTB'
      and product_line_group = 'GWP/SAMPLE'
      and month between '202601' and '202610'
    union all
    select 'golden', month, store_name, category_name, brand_name, value
    from fin_cpt.ads_bmi_golden_mf
    where dt = '{GDT}' and index_type = 'rtb_spending'
      and product_line_group = 'GWP/SAMPLE'
      and month between '202601' and '202610'
) u
group by month, store_name, category_name, brand_name
having abs(round(sum(case when src = 'cpt' then amt else 0 end)
              - sum(case when src = 'golden' then amt else 0 end), 2)) >= 0.01
order by abs(gap) desc;
```

---

### S10【D 组】JD - UL / HHC / CIF 高比例差

```sql
with cpt as (
    select month, round(sum(value_taxed),2) as amt
    from fin_cpt.ads_bmi_spending_mf
    where dt = '{DT}' and index_type = 'Paid Media-RTB'
      and store_name = 'JD - UL' and category_name = 'HHC' and brand_name = 'CIF'
      and month between '202601' and '202610'
    group by month
), gld as (
    select month, round(sum(value),2) as amt
    from fin_cpt.ads_bmi_golden_mf
    where dt = '{GDT}' and index_type = 'rtb_spending'
      and store_name = 'JD - UL' and category_name = 'HHC' and brand_name = 'CIF'
      and month between '202601' and '202610'
    group by month
)
select coalesce(c.month, g.month) as month
     , coalesce(c.amt, 0) as cpt_amt
     , coalesce(g.amt, 0) as golden_amt
     , round(coalesce(c.amt,0) - coalesce(g.amt,0), 2) as gap
     , round((coalesce(c.amt,0) - coalesce(g.amt,0))
             / nullif(coalesce(c.amt,0),0) * 100, 2) as gap_pct
from cpt c full join gld g on c.month = g.month
order by month;
```

**判断**：该品类总量小（月均 10 万级），少量 item 的口径差就会造成 16%–38% 的高比例。重点看 gap 是集中在 202609/202610 还是全期都有。

---

### S11【E / F 组】PW - LUX - OTHERS 与 VASELINE - LIP&CUTTIE 趋势

```sql
-- E 组：JD - UL / PW / LUX / OTHERS
select month
     , round(sum(case when src='cpt'    then amt else 0 end), 2) as cpt_amt
     , round(sum(case when src='golden' then amt else 0 end), 2) as golden_amt
     , round(sum(case when src='cpt'    then amt else 0 end)
           - sum(case when src='golden' then amt else 0 end), 2) as gap
from (
    select 'cpt' as src, month, value_taxed as amt
    from fin_cpt.ads_bmi_spending_mf
    where dt='{DT}' and index_type='Paid Media-RTB'
      and store_name='JD - UL' and category_name='PW' and brand_name='LUX'
      and product_line_group='OTHERS' and month between '202601' and '202610'
    union all
    select 'golden', month, value
    from fin_cpt.ads_bmi_golden_mf
    where dt='{GDT}' and index_type='rtb_spending'
      and store_name='JD - UL' and category_name='PW' and brand_name='LUX'
      and product_line_group='OTHERS' and month between '202601' and '202610'
) u
group by month
order by month;

-- F 组：JD - UL / SKIN / VASELINE / LIP&CUTTIE
select month
     , round(sum(case when src='cpt'    then amt else 0 end), 2) as cpt_amt
     , round(sum(case when src='golden' then amt else 0 end), 2) as golden_amt
     , round(sum(case when src='cpt'    then amt else 0 end)
           - sum(case when src='golden' then amt else 0 end), 2) as gap
from (
    select 'cpt' as src, month, value_taxed as amt
    from fin_cpt.ads_bmi_spending_mf
    where dt='{DT}' and index_type='Paid Media-RTB'
      and store_name='JD - UL' and category_name='SKIN' and brand_name='VASELINE'
      and product_line_group='LIP&CUTTIE' and month between '202601' and '202610'
    union all
    select 'golden', month, value
    from fin_cpt.ads_bmi_golden_mf
    where dt='{GDT}' and index_type='rtb_spending'
      and store_name='JD - UL' and category_name='SKIN' and brand_name='VASELINE'
      and product_line_group='LIP&CUTTIE' and month between '202601' and '202610'
) u
group by month
order by month;
```

**F 组判断**：10 个月全部存在、gap% 稳定在 0.3%–2.9% → 持续性小额比例差，典型成因是某类商品（赠品/小样/组合装）在一侧被剔除，属**已知口径差**，建议纳入 reason 白名单而非逐行追。

---

### S12【H 组】`int()` 截断假阳性全量清单

**目的**：一次清掉所有「真实差额 < 1 元、被 `int()` 放大成 1 元」的行（本期 1 行：202610 / PDD - UL / FEN / COMFORT / OTHERS，127.99 vs 128.00）。

```sql
select *
from (
    select month, store_name, category_name, brand_name
         , coalesce(product_line_group,'<NULL>') as plg
         , round(sum(case when src='cpt'    then amt else 0 end), 2) as cpt_amt
         , round(sum(case when src='golden' then amt else 0 end), 2) as golden_amt
         , round(sum(case when src='cpt'    then amt else 0 end)
               - sum(case when src='golden' then amt else 0 end), 2) as real_gap
    from (
        select 'cpt' as src, month, store_name, category_name, brand_name
             , product_line_group, value_taxed as amt
        from fin_cpt.ads_bmi_spending_mf
        where dt='{DT}' and index_type='Paid Media-RTB'
          and month between '202601' and '202610'
        union all
        select 'golden', month, store_name, category_name, brand_name
             , product_line_group, value
        from fin_cpt.ads_bmi_golden_mf
        where dt='{GDT}' and index_type='rtb_spending'
          and month between '202601' and '202610'
    ) u
    group by month, store_name, category_name, brand_name
           , coalesce(product_line_group,'<NULL>')
) t
where real_gap <> 0 and abs(real_gap) < 1
order by abs(real_gap) desc;
```

---

### S13【收口】用修正逻辑在 `fin_cpt` 内复跑全量对数

**这是本节最值得跑的一条** —— 替代原本跨 schema 的校验，一次拿到修正后的完整差异清单。

修正了两点：`round` 替代 `int`、`plg` 做 null-safe。

```sql
with cpt as (
    select month, bu_name, store_name, category_name, brand_name
         , coalesce(product_line_group,'<NULL>') as plg
         , sum(value_taxed) as v
    from fin_cpt.ads_bmi_spending_mf
    where dt = '{DT}' and index_type = 'Paid Media-RTB'
      and month between '202601' and '202610'
    group by month, bu_name, store_name, category_name, brand_name
           , coalesce(product_line_group,'<NULL>')
), gld as (
    select month, bu_name, store_name, category_name, brand_name
         , coalesce(product_line_group,'<NULL>') as plg
         , sum(value) as v
    from fin_cpt.ads_bmi_golden_mf
    where dt = '{GDT}' and index_type = 'rtb_spending'
      and month between '202601' and '202610'
    group by month, bu_name, store_name, category_name, brand_name
           , coalesce(product_line_group,'<NULL>')
)
select coalesce(c.month,        g.month)         as month
     , coalesce(c.bu_name,      g.bu_name)       as bu
     , coalesce(c.store_name,   g.store_name)    as store_name
     , coalesce(c.category_name,g.category_name) as category_name
     , coalesce(c.brand_name,   g.brand_name)    as brand_name
     , coalesce(c.plg,          g.plg)           as plg
     , round(coalesce(c.v,0), 2)                 as cpt_amt
     , round(coalesce(g.v,0), 2)                 as golden_amt
     , round(coalesce(c.v,0) - coalesce(g.v,0), 2) as gap
from cpt c
full join gld g
       on c.month         = g.month
      and c.bu_name       = g.bu_name
      and c.store_name    = g.store_name
      and c.category_name = g.category_name
      and c.brand_name    = g.brand_name
      and c.plg           = g.plg
where abs(coalesce(c.v,0) - coalesce(g.v,0)) >= 0.01
order by abs(coalesce(c.v,0) - coalesce(g.v,0)) desc;
```

**用法**：结果行数应与「待查 38 行」接近或略多（原脚本还有 4 类白名单会被过滤掉，差异行会多一些）。若出现原清单里没有的大额行，说明原脚本的 reason 规则掩盖了真实差异，需要重新审视分类逻辑。

---

## 六、执行顺序

| 步 | SQL | 目的 | 预期产出 |
|---|---|---|---|
| 1 | S0-a / S0-b | 确认分区、校准基准 | 建立可信基准 |
| 2 | S5 / S6 / S7 | **B 组优先**（28%，全店铺归零，最好定性） | 判定品牌级 or 品类级缺失，直接向上游提单 |
| 3 | S1 / S2 / S3 | **A 组**（60%，金额最大） | 确认 202604 拐点 + 是否真实多算 |
| 4 | S8 / S9 | G 组确证打标错位机制 | 为 A 组提供解释路径 |
| 5 | S4 / S10 / S11 | 行放大与存量小额 | 补齐细节 |
| 6 | S12 | 清假阳性 | H 组直接关闭 |
| 7 | S13 | 用修正逻辑全量复跑 | 最终收口清单 |

---

## 七、超出 `fin_cpt` 才能查的部分

若 S2/S3 证明 A 组是「真实多算」而非错位，需进一步查 dimension 一对多。以下表不在 `fin_cpt` / `cpt` 内，**需额外权限**：

| 表 | schema | 用途 |
|---|---|---|
| `dim_prd_item` | `dim.ddm` | 确认同 `item_id + platform` 是否有多个 `is_current=1` 且时间区间重叠的版本（会导致 `pfm_spending` 被重复计入） |
| `dim_store` | `dim.ddm` | 确认同 `shop_id` 是否有多个 platform/customer（分支① 只关联 shop_id，会 fan-out） |
| `dws_pfm_total_item_df` | `dws.ddm` | 拿到 item 级 `pfm_spending` / `pfm_product_line_group`，与 golden 的 `product_group` 逐 item 比对 |
| `ads_ec_g_fomular_ndy_traffic_fact` | `ads.ddm_dset` | 黄金公式侧原始流量事实表，确认 202610 DEO/LUX 是否真的没有数据 |

**行放大自查 SQL**（拿到 `dim` 权限后先跑这条）：

```sql
-- 检查 JD 渠道是否存在同一 item + platform 的多版本打标（会导致 RTB 费用被重复计入）
select item_id, platform
     , count(*) as version_cnt
     , collect_set(concat(start_time,'~',end_time)) as ranges
from dim.ddm.dim_prd_item
where is_current = 1
  and platform = 'JD'
group by item_id, platform
having count(*) > 1
order by version_cnt desc
limit 100;

-- 检查 dim_store 同 shop_id 多行（分支① 只关联 shop_id 的风险）
select shop_id, count(*) as cnt
     , collect_set(platform)  as platforms
     , collect_set(customer)  as customers
from dim.ddm.dim_store
where status = 1
group by shop_id
having count(*) > 1
order by cnt desc
limit 100;
```

---

## 八、校验脚本自身缺陷（建议本次一并修复）

| # | 缺陷 | 影响 | 修法 |
|---|---|---|---|
| 1 | `gap_absolute = int(cpt) - int(golden)` | 0.01 元尾差被放大成 1 元（H 组） | 改 `round(cpt - golden, 2)`，判定用 `abs(gap) >= 0.01` |
| 2 | RTB 的 join 用 `t1.product_line_group = t2.product_line_group` | 两侧同为 NULL 时 `NULL = NULL` 为 unknown，full join 拆成两条假差异 | 补 `or (both is null)`（PFM 分支已修，RTB 漏了） |
| 3 | 基准直接读 `ddm_dset` 原表 | 运维侧跨 schema 无权限，排查常卡住 | 改用 `fin_cpt.ads_bmi_golden_mf`（须先过 S0-b 校准） |
| 4 | 12 个月列名硬编码 `202601`–`202612` | 跨年失效（2027 年整套作废） | 改为动态月份列或长表输出 |
| 5 | F 组这类持续性小额口径差反复进入「待查」 | 噪音掩盖真实问题 | 把已知口径差（如 GWP/SAMPLE、LIP&CUTTIE 的赠品处理）纳入 reason 白名单 |

---

## 九、优先级建议

| 优先级 | 对象 | 金额 | 理由 |
|---|---|---|---|
| **P0** | B 组：202610 DEO / LUX 全线缺失 | 156,297 | 5 店铺同时归零，指向明确，最易定性，向上游提单即可 |
| **P0** | A 组：JD - UL / CLEAR / CORE 202604 起漂移 | 337,480 | 金额最大（60%），有明确拐点，大概率是 202604 前后某次变更 |
| P1 | G 组：DERMA ↔ GWP/SAMPLE 打标错位 | ≈0 | 已确证机制，可作为修打标逻辑的切入样本 |
| P2 | D 组：HHC / CIF | 34,227 | 小品类高比例，逐 item 查 |
| P2 | E / F 组 | 28,291 | 存量小额，建议白名单化 |
| P3 | C / H 组 | 5,863 | 单月偶发 + 校验假阳性，随 S12/S13 一并清掉 |

> 本期 562,967 元占 RTB 总量（约 5.28 亿）的 **0.107%**。虽然绝对额比上期（4,972 元）放大百倍，但主要来自 202610 首次入账，属「新增月份暴露存量问题」而非数据质量恶化。**建议按 P0 两条先推进，其余随脚本修复一并收口。**
