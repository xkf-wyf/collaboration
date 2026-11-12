import csv, collections, os
D='checks'
def rd(f):
    with open(os.path.join(D,f),encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))
def num(x):
    if x in (None,'','null','\\N'): return 0.0
    try: return float(x)
    except: return 0.0
ms=[f'mth{i:02d}' for i in range(1,11)]

# c05 分店分品类覆盖率
r5=rd('GMV_c05_0.csv')
print("=== TMALL SUPER 分品类覆盖率 ===")
print(f"{'category':14}{'bu':18}"+''.join(f'{k[3:]:>7}' for k in ms))
for x in r5:
    if x['store_name']=='TMALL SUPER':
        print(f"{x['category_name']:14}{x['bu']:18}"+''.join(f"{num(x[k+'_both_gmv_coverage'])*100:6.1f}%" for k in ms))

# c07 分店分月 接口 vs 源
print("\n=== c07 分店分月（item=接口侧 sku=源侧）===")
r7=rd('GMV_c07_0.csv')
agg=collections.defaultdict(lambda:[0,0])
for x in r7:
    agg[(x['store_name'],x['month'])][0]+=num(x['item_gmv'])
    agg[(x['store_name'],x['month'])][1]+=num(x['sku_gmv'])
stores=['TMALL SUPER','TMALL SUPER - UL','VIP - UL','JD - UL','PDD - UL','VIP - AHC']
for s in stores:
    print(f"-- {s}")
    for k in ms:
        a,b=agg.get((s,k),[0,0])
        print(f"   {k}  item={a:>14,.0f}  sku={b:>14,.0f}  gap={a-b:>14,.0f}  {(a-b)/b*100 if b else 0:>7.1f}%")
