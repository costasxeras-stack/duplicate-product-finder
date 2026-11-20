import json, numpy as np
res=np.load('res.npy',allow_pickle=True).item(); P=json.load(open('pairs.json'))
out={}
for ds in res:
    k='title' if ds=='Walmart-Amazon' else 'name'
    r=res[ds]; s=r['S']['test']; y=r['Y']['test']; F=r['feat']['test']
    v,yv=r['S']['valid'],r['Y']['valid']
    hi=float(min(t for t in np.linspace(0.3,0.99,70) if (yv[v>=t].mean() if (v>=t).sum()>=10 else 0)>=0.95))
    lo=float(max(t for t in np.linspace(0.005,0.5,100) if yv[v>=t].sum()/yv.sum()>=0.95))
    rows=[]
    for i,(a,b,lab) in enumerate(P[ds]['test']):
        f=F[0][i]
        rows.append(dict(a=a.get(k,''),b=b.get(k,''),am=a.get('modelno',''),bm=b.get('modelno',''),ab=a.get('brand',''),bb=b.get('brand',''),
          ap=a.get('price',''),bp=b.get('price',''),y=int(lab),s=round(float(s[i]),4),rule=int(r['rule']['test'][i]),
          sig=dict(title=round(float(f[0]),3),ai=round(float(f[1]),3),model=('same' if f[2] else 'partial' if f[7] else 'different' if f[3] else 'missing'),price=(round(float(f[5]),2) if not f[6] else None))))
    out[ds]=dict(hi=round(hi,2),lo=round(lo,3),pairs=rows)
json.dump(out,open('../data/app-data.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print(os.path.getsize('../data/app-data.json'), {d:(out[d]['hi'],out[d]['lo']) for d in out})

# Method comparison on test, thresholds chosen on validation (best F1)
from sklearn.metrics import precision_recall_fscore_support, average_precision_score
def prf(y,p):
    a,b,c,_=precision_recall_fscore_support(y,p,average='binary',zero_division=0); return [round(float(a),3),round(float(b),3),round(float(c),3)]
for ds in res:
    r=res[ds]; F=r['feat']; Y=r['Y']; S=r['S']
    def best(col_valid):
        return max(np.linspace(0.01,0.99,99),key=lambda t:prf(Y['valid'],col_valid>=t)[2])
    M={}
    M['rule']=prf(Y['test'],r['rule']['test'])+[None]
    t=best(F['valid'][0][:,0]); M['title']=prf(Y['test'],F['test'][0][:,0]>=t)+[round(float(average_precision_score(Y['test'],F['test'][0][:,0])),3)]
    t=best(F['valid'][0][:,1]); M['ai']=prf(Y['test'],F['test'][0][:,1]>=t)+[round(float(average_precision_score(Y['test'],F['test'][0][:,1])),3)]
    t=best(S['valid']); M['combined']=prf(Y['test'],S['test']>=t)+[round(float(average_precision_score(Y['test'],S['test'])),3)]
    out[ds]['methods']=M; out[ds]['counts']=dict(train=int(len(Y['train'])),valid=int(len(Y['valid'])),test=int(len(Y['test'])),test_dups=int(Y['test'].sum()))
    print(ds,M)
json.dump(out,open('../data/app-data.json','w'),ensure_ascii=False,separators=(',',':'))
