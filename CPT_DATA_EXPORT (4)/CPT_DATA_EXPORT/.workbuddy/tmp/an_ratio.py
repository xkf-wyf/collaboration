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
months = sorted({r[I["month"]] for r in rs if r[I["month"]]})

print("=== 各店铺 月度 CPT/源 比值（>1 CPT多出, <1 CPT少出）===")
focus = ["TMALL SUPER", "TMALL SUPER - UL", "VIP - UL", "VIP - AHC", "VIP - AHC CBE",
         "JD - UL", "PDD - UL", "PDD - VSL", "TMALL FGS - BPC", "PDD - AHC DTC", "PDD - AHC"]
print(f"{'store':22}" + "".join(f"{m[4:]:>7}" for m in months))
for s in focus:
    line = f"{s:22}"
    for m in months:
        it = sum(f2(r[I["item_gmv"]]) or 0 for r in rs if r[I["store_name"]] == s and r[I["month"]] == m)
        sc = sum(f2(r[I["sku_gmv"]]) or 0 for r in rs if r[I["store_name"]] == s and r[I["month"]] == m)
        line += f"{(it/sc if sc else -1):7.2f}"
    print(line)

print("\n=== TMALL SUPER: plg 为 null 的行占比 ===")
for s in ["TMALL SUPER", "TMALL SUPER - UL", "VIP - UL", "JD - UL"]:
    tot = sum(f2(r[I["sku_gmv"]]) or 0 for r in rs if r[I["store_name"]] == s and r[I["month"]].startswith("2026"))
    nul = sum(f2(r[I["sku_gmv"]]) or 0 for r in rs if r[I["store_name"]] == s
              and r[I["month"]].startswith("2026") and r[I["product_line_group"]] == "")
    cptnul = sum(f2(r[I["item_gmv"]]) or 0 for r in rs if r[I["store_name"]] == s
                 and r[I["month"]].startswith("2026") and r[I["product_line_group"]] == "")
    print(f"{s:22} 源GMV={tot:14,.0f}  其中plg空={nul:12,.0f} ({nul/tot:5.1%})  该组CPT出={cptnul:12,.0f}")

print("\n=== 全量：CPT 侧 vs 源侧 总量（2026 全年）===")
A = sum(f2(r[I["item_gmv"]]) or 0 for r in rs if r[I["month"]].startswith("2026"))
B = sum(f2(r[I["sku_gmv"]]) or 0 for r in rs if r[I["month"]].startswith("2026"))
print(f"CPT={A:,.0f}  源={B:,.0f}  差={A-B:,.0f}  ({(A-B)/B:.2%})")
print(f"其中源侧 plg 空的行: {sum(f2(r[I['sku_gmv']]) or 0 for r in rs if r[I['month']].startswith('2026') and r[I['product_line_group']]=='') :,.0f}")
print(f"其中源侧无 SKU mapping(ul_sku=0) 的行: {sum(f2(r[I['sku_gmv']]) or 0 for r in rs if r[I['month']].startswith('2026') and (f2(r[I['ul_sku_gmv']]) or 0)==0):,.0f}")
