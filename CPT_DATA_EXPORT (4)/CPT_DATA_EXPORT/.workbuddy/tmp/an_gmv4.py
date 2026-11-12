import csv, collections, os
D='checks'
def rd(f):
    with open(os.path.join(D,f),encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))
def num(x):
    if x in (None,'','null','\\N'): return 0.0
    try: return float(x)
    except: return 0.0
r7=rd('GMV_c07_0.csv')
# 校验恒等式
bad=0; gap_sum=0
for x in r7:
    ig=num(x['item_gmv']); sg=num(x['sku_gmv']); g=num(x['item_sku_gap'])
    gap_sum+=g
    if abs((ig-sg)-g)>0.02: bad+=1
print("恒等式不成立行数",bad,"/",len(r7),"; sum(gap)",round(gap_sum,2))
print()
# 分月
m=collections.defaultdict(lambda:[0,0,0,0,0])
for x in r7:
    k=x['month']
    m[k][0]+=num(x['item_gmv']); m[k][1]+=num(x['sku_gmv'])
    m[k][2]+=num(x['both_gmv']); m[k][3]+=num(x['jz_gmv']); m[k][4]+=num(x['ul_sku_gmv'])
print(f"{'month':8}{'item_gmv(CPT)':>16}{'sku_gmv(源)':>16}{'差':>15}{'差%':>8}{'both':>15}{'jz':>14}{'ul_sku':>14}")
for k in sorted(m):
    a,b,c,d,e=m[k]
    print(f"{k:8}{a:16,.0f}{b:16,.0f}{a-b:15,.0f}{(a-b)/b*100 if b else 0:7.2f}%{c:15,.0f}{d:14,.0f}{e:14,.0f}")
print()
# product_line_group 是否 null
n=collections.defaultdict(lambda:[0,0,0])
for x in r7:
    k='NULL' if x['product_line_group'] in ('null','','NULL') else '有值'
    n[k][0]+=num(x['item_gmv']); n[k][1]+=num(x['sku_gmv']); n[k][2]+=num(x['both_gmv'])
for k,v in n.items():
    print(f"plg={k}: item={v[0]:,.0f} sku={v[1]:,.0f} both={v[2]:,.0f} item-sku={v[0]-v[1]:,.0f}")
