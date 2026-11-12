import csv, collections, os
D='checks'
def rd(f):
    with open(os.path.join(D,f),encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))
def num(x):
    if x in (None,'','null','\\N'): return 0.0
    try: return float(x)
    except: return 0.0
r4=rd('GMV_c04_0.csv')
print("c04 列:",list(r4[0].keys()))
print()
ms=[f'mth{i:02d}' for i in range(1,11)]
print(f"{'store':26}{'bu':18}"+''.join(f'{k[3:]:>7}' for k in ms))
for x in r4:
    if x['store_name'] in ('TMALL SUPER','TMALL SUPER - UL','VIP - UL','JD - UL','PDD - UL','VIP - AHC','PDD - AHC','PDD - AHC DTC','TMALL FGS - BPC','TMALL FGS - AHC','PDD - VSL'):
        print(f"{x['store_name']:26}{x['bu']:18}"+''.join(f"{num(x[k+'_both_gmv_coverage'])*100:6.1f}%" for k in ms))
