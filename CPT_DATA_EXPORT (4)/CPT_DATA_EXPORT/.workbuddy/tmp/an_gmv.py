import csv, os

OUT = r"F:/NW-诺唯/协作/CPT_DATA_EXPORT (4)/CPT_DATA_EXPORT/.workbuddy/tmp/checks"


def load(name):
    with open(os.path.join(OUT, name + ".csv"), encoding="utf-8-sig") as f:
        r = list(csv.reader(f))
    return r[0], r[1:]


def f2(x):
    try:
        return float(x)
    except:
        return None


hdr, rows = load("GMV_c04_0")
iy = hdr.index("ytd_both_gmv_coverage")
jy = hdr.index("ytd_jz_gmv_coverage")
uy = hdr.index("ytd_ul_sku_gmv_coverage")

print("=== GMV ytd 覆盖率排序（both / jz / ul_sku）===")
print(f"{'store':30} {'bu':22} {'both':>8} {'jz':>8} {'ul_sku':>8}")
recs = []
for r in rows:
    b, j, u = f2(r[iy]), f2(r[jy]), f2(r[uy])
    recs.append((r[0], r[1], b, j, u))
recs.sort(key=lambda x: (x[2] is not None, x[2] if x[2] is not None else 9))
for s, bu, b, j, u in recs:
    print(f"{s:30} {bu:22} {'' if b is None else f'{b:.4f}':>8} {'' if j is None else f'{j:.4f}':>8} {'' if u is None else f'{u:.4f}':>8}")

print("\n=== 月度 both 覆盖率 < 0.9 的格子（按缺口大小）===")
mcols = [i for i, h in enumerate(hdr) if h.endswith("_both_gmv_coverage") and h.startswith("mth")]
bad = []
for r in rows:
    for i in mcols:
        v = f2(r[i])
        if v is not None and v < 0.9 and v > 0:
            bad.append((v, r[0], r[1], hdr[i][3:5], v))
bad.sort()
for _, s, bu, m, v in bad[:30]:
    print(f"  2026-{m}  {s:28} {bu:22} {v:.4f}")

print(f"\n合计低覆盖格数: {len(bad)}")
