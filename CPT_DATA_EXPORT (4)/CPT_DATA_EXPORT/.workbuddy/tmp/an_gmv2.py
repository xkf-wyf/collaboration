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


# ---------- 1. PDD - AHC / DTC 在 raw 里的匹配情况 ----------
hdr, rows = load("GMV_c07_0")
print("=== raw 表列 ===")
print(hdr)
ip = hdr.index("item_sku_gap")
stores = {}
for r in rows:
    s = r[hdr.index("store_name")]
    g = f2(r[ip])
    if s not in stores:
        stores[s] = [0, 0.0, 0.0]
    stores[s][0] += 1
    if g:
        stores[s][1] += g
    v = f2(r[hdr.index("sku_gmv")])
    if v:
        stores[s][2] += v

print("\n=== 按 store 汇总（行数 / item_sku_gap 合计 / 源 GMV 合计）===")
print(f"{'store':30} {'rows':>6} {'gap_sum':>16} {'sku_gmv_sum':>16} {'gap%':>8}")
for s, (n, gap, base) in sorted(stores.items(), key=lambda x: -abs(x[1][1])):
    pct = gap / base if base else None
    print(f"{s:30} {n:6} {gap:16,.0f} {base:16,.0f} {'' if pct is None else f'{pct:.2%}':>8}")

# ---------- 2. gap 明细 Top20 ----------
hdr6, rows6 = load("GMV_c06_0")
print("\n=== 明细表列 ===")
print(hdr6)
iy = hdr6.index("ytd_absolute")
rr = sorted(rows6, key=lambda r: -abs(f2(r[iy]) or 0))
print("\n=== item vs sku gap Top 20（绝对值）===")
print(f"{'store':26} {'bu':20} {'category':10} {'brand':14} {'ytd_gap':>14}")
for r in rr[:20]:
    print(f"{r[0]:26} {r[1]:20} {r[2]:10} {r[3]:14} {(f2(r[iy]) or 0):14,.0f}")
