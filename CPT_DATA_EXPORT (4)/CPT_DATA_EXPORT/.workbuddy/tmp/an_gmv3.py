import csv, collections, os
D='checks'
def rd(f):
    with open(os.path.join(D,f),encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))
def num(x):
    try: return float(x)
    except: return 0.0

# ---------- GMV_c07: 源侧 vs 两侧都有的口径拆解 ----------
r7=rd('GMV_c07_0.csv')
print("c07 行数",len(r7))
cols=r7[0].keys()
print("列:",list(cols))
for c in ['item_gmv_after_refund','item_gmv','sku_gmv','both_gmv','jz_gmv','ul_sku_gmv','item_sku_gap']:
    print("  sum",c,round(sum(num(x[c]) for x in r7),2))
