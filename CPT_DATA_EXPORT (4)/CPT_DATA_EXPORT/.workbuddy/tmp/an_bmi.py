import csv, os
OUT = r"F:/NW-诺唯/协作/CPT_DATA_EXPORT (4)/CPT_DATA_EXPORT/.workbuddy/tmp/checks"


def load(n):
    with open(os.path.join(OUT, n + ".csv"), encoding="utf-8-sig") as f:
        r = list(csv.reader(f))
    return r[0], r[1:]


def f2(x):
    try:
        return float(x)
    except:
        return None


# ---------- RTB reason 分布 ----------
hdr, rows = load("BMI_c09_0")
print("=== RTB raw 列 ===")
print(hdr)
ri = hdr.index("reason")
gi = hdr.index("gap_absolute")
ci = hdr.index("rtb_spending_cpt")
reason = {}
for r in rows:
    k = r[ri] if len(r) > ri else ""
    k = k if k else "(gap=0)"
    d = reason.setdefault(k, [0, 0.0, 0.0])
    d[0] += 1
    d[1] += f2(r[gi]) or 0
    d[2] += f2(r[ci]) or 0
print("\n=== RTB 差异归因分布 ===")
print(f"{'reason':28} {'rows':>6} {'gap_sum':>16} {'cpt_sum':>16} {'gap%':>8}")
for k, (n, g, c) in sorted(reason.items(), key=lambda x: -abs(x[1][1])):
    print(f"{k:28} {n:6} {g:16,.0f} {c:16,.0f} {'' if not c else f'{g/c:8.2%}'}")

# ---------- 三张检查表的总量对比 ----------
for name, a, b, gcol, label in [
    ("BMI_c09_0", "rtb_spending_cpt", "rtb_spending_golden", "gap_absolute", "RTB (CPT vs 黄金公式看板)"),
    ("BMI_c10_0", "pfm_spending_cpt", "pfm_spending_source", "gap_amount", "PFM (CPT vs dws_pfm_total_item_df)"),
    ("BMI_c11_0", "cps_spending_cpt", "cps_pending_source", "gap_amount", "CPS (CPT vs tmp_cps_spending)"),
]:
    h, rs = load(name)
    if a not in h:
        print(f"\n{label}: 列不匹配 {h}")
        continue
    A = sum(f2(r[h.index(a)]) or 0 for r in rs)
    B = sum(f2(r[h.index(b)]) or 0 for r in rs)
    nz = sum(1 for r in rs if abs(f2(r[h.index(gcol)]) or 0) > 0.5)
    print(f"\n{label}")
    print(f"  CPT={A:,.0f}  源={B:,.0f}  差={A-B:,.0f}  ({(A-B)/B:.2%})   非零差异行={nz}/{len(rs)}")

# ---------- PFM 按 pfm_type ----------
h, rs = load("BMI_c10_0")
ti = h.index("pfm_type")
agg = {}
for r in rs:
    k = r[ti]
    d = agg.setdefault(k, [0.0, 0.0])
    d[0] += f2(r[h.index("pfm_spending_cpt")]) or 0
    d[1] += f2(r[h.index("pfm_spending_source")]) or 0
print("\n=== PFM 按类型 ===")
print(f"{'pfm_type':28} {'CPT':>16} {'源':>16} {'差':>16} {'gap%':>8}")
for k, (a, b) in sorted(agg.items(), key=lambda x: -abs(x[1][0] - x[1][1])):
    print(f"{k:28} {a:16,.0f} {b:16,.0f} {a-b:16,.0f} {'' if not b else f'{(a-b)/b:8.2%}'}")
