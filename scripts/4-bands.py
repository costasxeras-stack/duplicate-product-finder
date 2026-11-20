import json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_recall_fscore_support
res=np.load('res.npy',allow_pickle=True).item(); P=json.load(open('pairs.json'))
for ds in res:
    r=res[ds]; F=r['feat']; Y=r['Y']
    for name,cols in [('all',list(range(9))),('no embedding',[0,2,3,4,5,6,7,8]),('only title+model',[0,2,3,7,8])]:
        lr=LogisticRegression(max_iter=2000).fit(F['train'][0][:,cols],Y['train']); s=lr.predict_proba(F['test'][0][:,cols])[:,1]
        print(ds,name,'AP %.3f'%average_precision_score(Y['test'],s))
    S=r['S']
    # bands from valid: hi = lowest t with valid precision>=0.95 ; lo = highest t keeping >=98% of valid dups above it
    v,yv=S['valid'],Y['valid']
    hi=min(t for t in np.linspace(0.3,0.99,70) if (yv[v>=t].mean() if (v>=t).sum()>=10 else 0)>=0.95)
    lo=max(t for t in np.linspace(0.005,0.5,100) if yv[v>=t].sum()/yv.sum()>=0.95)
    s,y=S['test'],Y['test']; n=len(y)
    m=s>=hi; k=s<lo; rv=~m&~k
    print(f"  bands hi={hi:.2f} lo={lo:.2f} | auto-merge {m.sum()} ({y[m].mean()*100:.1f}% right, {(~y[m].astype(bool)).sum()} wrong) | review {rv.sum()} ({rv.mean()*100:.0f}% of pairs, {y[rv].sum()} dups) | keep separate {k.sum()} (missed dups {y[k].sum()} of {y.sum()})")
    # rule false positives sample
    mi=np.array([x['mmiss'] for x in r['feat']['test'][1]],bool)
    print('   review band: share with a missing model number %.0f%%, all pairs %.0f%%'%(mi[rv].mean()*100, mi.mean()*100), ' precision of auto-merge on pairs with both model numbers', round(y[m&~mi].mean(),3), (m&~mi).sum(), 'with missing', (m&mi).sum())
    if False:
        rule=r['rule']['test']; fp=np.where((rule==1)&(y==0))[0][:6]
        for i in fp:
            a,b,_=P[ds]['test'][i]; print('   FP:',a['title'][:70],'|',a.get('modelno'),'||',b['title'][:70],'|',b.get('modelno'))
