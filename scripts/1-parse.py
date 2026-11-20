import re, json, sys
def rec(s):
    d={}
    for m in re.finditer(r'COL (\w+) VAL (.*?)(?= COL |$)', s.strip()):
        d[m.group(1)]=m.group(2).strip()
    return d
out={}
for ds in ['Walmart-Amazon','Abt-Buy']:
    out[ds]={}
    for sp in ['train','valid','test']:
        rows=[]
        for line in open(f'{ds}/{sp}.txt'):
            a,b,y=line.rstrip('\n').split('\t'); rows.append([rec(a),rec(b),int(y)])
        out[ds][sp]=rows
json.dump(out,open('pairs.json','w'))
print({ds:{sp:len(v) for sp,v in out[ds].items()} for ds in out}); print(out['Walmart-Amazon']['test'][3]); print(out['Abt-Buy']['test'][0][0].keys())
titles=set()
for ds in out:
    k='title' if ds=='Walmart-Amazon' else 'name'
    for sp in out[ds]:
        for a,b,y in out[ds][sp]: titles.add(a.get(k,'')); titles.add(b.get(k,''))
titles=sorted(t for t in titles if t)
json.dump(titles,open('titles.json','w')); print(len(titles))
