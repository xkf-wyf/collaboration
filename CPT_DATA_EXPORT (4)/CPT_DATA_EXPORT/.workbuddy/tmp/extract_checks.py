import json, os, re, csv, html

BASE = r"F:/NW-诺唯/协作/CPT_DATA_EXPORT (4)/校验"
OUT = r"F:/NW-诺唯/协作/CPT_DATA_EXPORT (4)/CPT_DATA_EXPORT/.workbuddy/tmp/checks"
os.makedirs(OUT, exist_ok=True)


def parse_table(h):
    """解析 Databricks <table class='table-result'>，返回 (headers, rows)"""
    rows = []
    # 逐行抓 <tr>...</tr>
    for tr in re.findall(r"<tr>(.*?)</tr>", h, re.S):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells]
        if cells:
            rows.append(cells)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def process(fn, tag):
    nb = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
    index = []
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        for j, o in enumerate(c.get("outputs", [])):
            d = o.get("data", {})
            if "text/html" not in d:
                continue
            h = "".join(d["text/html"])
            hdr, rows = parse_table(h)
            if not hdr:
                continue
            name = f"{tag}_c{i:02d}_{j}"
            path = os.path.join(OUT, name + ".csv")
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(hdr)
                w.writerows(rows)
            first_line = next((l for l in src.split("\n") if l.strip() and not l.strip().startswith("%")), "")
            index.append((name, len(rows), len(hdr), first_line[:100]))
    return index


allidx = []
allidx += process("正式脚本_03_机制GMV Check.ipynb", "GMV")
allidx += process("正式脚本_04_BMI Spending Check.ipynb", "BMI")

print(f"{'table':22} {'rows':>6} {'cols':>5}  desc")
for n, r, c, d in allidx:
    print(f"{n:22} {r:6} {c:5}  {d}")
print(f"\ntotal tables: {len(allidx)}")
