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


h, rs = load("GMV_c07_0")
I = {k: i for i, k in enumerate(h)}


def show(store, month=None, n=30):
    sel = [r for r in rs if r[I["store_name"]] == store and (month is None or r[I["month"]] == month)]
    sel = sorted(sel, key=lambda r: -(abs(f2(r[I["item_sku_gap"]]) or 0)))
    print(f"\n### {store}" + (f" / {month}" if month else "") + f"  ({len(sel)} rows)")
    print(f"{'mth':8}{'bu':18}{'cat':8}{'brand':10}{'plg':16}"
          f"{'item_gmv':>14}{'src_gmv':>14}{'both':>14}{'ul_sku':>14}{'gap':>14}")
    for r in sel[:n]:
        print(f"{r[I['month']]:8}{r[I['bu']][:17]:18}{r[I['category_name']][:7]:8}{r[I['brand_name']][:9]:10}"
              f"{r[I['product_line_group']][:15]:16}"
              f"{(f2(r[I['item_gmv']]) or 0):14,.0f}{(f2(r[I['sku_gmv']]) or 0):14,.0f}"
              f"{(f2(r[I['both_gmv']]) or 0):14,.0f}{(f2(r[I['ul_sku_gmv']]) or 0):14,.0f}"
              f"{(f2(r[I['item_sku_gap']]) or 0):14,.0f}")


show("TMALL SUPER", "202606", 15)
show("PDD - AHC DTC", None, 12)
show("VIP - UL", "202606", 10)

print("\n\n=== GMV: TMALL SUPER vs TMALL SUPER - UL 月度 jz 覆盖率 ===")
h4, r4 = load("GMV_c04_0")
J = {k: i for i, k in enumerate(h4)}
mc = [i for i, x in enumerate(h4) if x.startswith("mth") and x.endswith("_jz_gmv_coverage")]
print(f"{'store':26}{'bu':20}" + "".join(f"{h4[i][3:5]:>7}" for i in mc))
for r in r4:
    if "TMALL SUPER" in r[0] or "VIP" in r[0]:
        print(f"{r[0]:26}{r[1][:19]:20}" + "".join(f"{(f2(r[i]) if f2(r[i]) is not None else -1):7.3f}" for i in mc))

print("\n=== BMI RTB 差异非零明细 Top25（原因待查）===")
hb, rb = load("BMI_c09_0")
K = {k: i for i, k in enumerate(hb)}
bad = [r for r in rb if r[K["reason"]] == "原因待查"]
bad.sort(key=lambda r: -abs(f2(r[K["gap_absolute"]]) or 0))
print(f"{'month':8}{'store':24}{'bu':18}{'cat':8}{'brand':10}{'plg':14}{'cpt':>12}{'golden':>12}{'gap':>12}")
for r in bad[:25]:
    print(f"{r[K['month']]:8}{r[K['store_name']][:23]:24}{r[K['bu']][:17]:18}{r[K['category_name']][:7]:8}"
          f"{r[K['brand_name']][:9]:10}{r[K['product_line_group']][:13]:14}"
          f"{(f2(r[K['rtb_spending_cpt']]) or 0):12,.0f}{(f2(r[K['rtb_spending_golden']]) or 0):12,.0f}"
          f"{(f2(r[K['gap_absolute']]) or 0):12,.0f}")
print(f"\n原因待查合计: {sum(f2(r[K['gap_absolute']]) or 0 for r in bad):,.0f}  行数 {len(bad)}")
stores = {}
for r in bad:
    stores[r[K["store_name"]]] = stores.get(r[K["store_name"]], 0) + (f2(r[K["gap_absolute"]]) or 0)
print("\n按店铺:")
for s, v in sorted(stores.items(), key=lambda x: -abs(x[1])):
    print(f"  {s:28}{v:14,.0f}")
