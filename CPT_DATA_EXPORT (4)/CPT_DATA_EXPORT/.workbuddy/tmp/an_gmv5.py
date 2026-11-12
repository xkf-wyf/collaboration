import csv, collections, os
D='checks'
def rd(f):
    with open(os.path.join(D,f),encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))
def num(x):
    if x in (None,'','null','\\N'): return 0.0
    try: return float(x)
    except: return 0.0

r6=rd('GMV_c06_0.csv')
print("c06 行数",len(r6));print("列:",list(r6[0].keys())[:40])
ms=[f'mth{i:02d}' for i in range(1,11)]
print()
# 分月总 gap
tot=collections.defaultdict(float)
for x in r6:
    for k in ms: tot[k]+=num(x[k+'_gap_absolute'])
print("分月 gap_absolute 合计:")
for k in ms: print(f"  {k}: {tot[k]:>16,.2f}")
print(f"  YTD 合计: {sum(tot.values()):>16,.2f}")
print()
# 分店
st=collections.defaultdict(float)
for x in r6:
    st[(x['store_name'],x['bu'])]+=sum(num(x[k+'_gap_absolute']) for k in ms)
print("按 store 汇总 gap（前 15）:")
for (s,b),v in sorted(st.items(),key=lambda t:-abs(t[1]))[:15]:
    print(f"  {s:28} {b:18} {v:>16,.0f}")
print()
# 正负方向
pos=sum(v for v in st.values() if v>0); neg=sum(v for v in st.values() if v<0)
print(f"正 gap 合计 {pos:,.0f}   负 gap 合计 {neg:,.0f}   净 {pos+neg:,.0f}")
