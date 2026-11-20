import json, re, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support, average_precision_score
P=json.load(open('pairs.json')); T=json.load(open('titles.json')); idx={t:i for i,t in enumerate(T)}
E=np.fromfile('titles.f32','<f4').reshape(len(T),512); E/=np.linalg.norm(E,axis=1,keepdims=True)
norm=lambda s:re.sub(r'[^a-z0-9]','',str(s).lower())
def model_tokens(t): return {norm(w) for w in re.findall(r'[a-z0-9\-/]+',t.lower()) if re.search(r'\d',w) and re.search(r'[a-z]',w) and len(norm(w))>=4}
def feats(ds,rows,tf):
    k='title' if ds=='Walmart-Amazon' else 'name'
    X=[];R=[]
    A=tf.transform([a.get(k,'') for a,b,y in rows]); B=tf.transform([b.get(k,'') for a,b,y in rows])
    tfcos=np.asarray(A.multiply(B).sum(1)).ravel()
    for i,(a,b,y) in enumerate(rows):
        ta,tb=a.get(k,''),b.get(k,'')
        emb=float(E[idx[ta]]@E[idx[tb]]) if ta and tb else 0.0
        ma=model_tokens(ta)|({norm(a['modelno'])} if a.get('modelno') else set()); mb=model_tokens(tb)|({norm(b['modelno'])} if b.get('modelno') else set())
        mm=1.0 if ma&mb else 0.0
        mpart=1.0 if (not mm and any((x in z or z in x) for x in ma for z in mb if min(len(x),len(z))>=5)) else 0.0
        mmiss=1.0 if not(ma and mb) else 0.0
        mconf=1.0 if (ma and mb and not mm and not mpart) else 0.0
        ba,bb=norm(a.get('brand','')),norm(b.get('brand',''))
        brand=1.0 if ba and bb and (ba in bb or bb in ba) else (0.5 if not(ba and bb) else 0.0)
        try: pa,pb=float(a.get('price') or 0),float(b.get('price') or 0)
        except: pa=pb=0
        pr=min(pa,pb)/max(pa,pb) if pa>0 and pb>0 else -1
        X.append([tfcos[i],emb,mm,mconf,brand,max(pr,0),1.0 if pr<0 else 0.0,mpart,mmiss]); R.append(dict(mm=mm,brand=brand,mmiss=mmiss))
    return np.array(X),R
res={}
for ds in ['Walmart-Amazon','Abt-Buy']:
    k='title' if ds=='Walmart-Amazon' else 'name'
    tf=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),sublinear_tf=True).fit([r[0].get(k,'') for r in P[ds]['train']]+[r[1].get(k,'') for r in P[ds]['train']])
    D={sp:feats(ds,P[ds][sp],tf) for sp in ['train','valid','test']}; Y={sp:np.array([r[2] for r in P[ds][sp]]) for sp in D}
    lr=LogisticRegression(max_iter=2000,C=1.0).fit(D['train'][0],Y['train'])
    S={sp:lr.predict_proba(D[sp][0])[:,1] for sp in D}
    def prf(y,p): pr,rc,f,_=precision_recall_fscore_support(y,p,average='binary',zero_division=0); return round(pr,3),round(rc,3),round(f,3)
    # rule
    rule={sp:np.array([1 if r['mm'] and r['brand']>=0.5 else 0 for r in D[sp][1]]) for sp in D}
    # title tfidf threshold best F1 on valid
    tv=D['valid'][0][:,0]; best=max(np.linspace(0.1,0.95,86),key=lambda t:prf(Y['valid'],tv>=t)[2])
    tlr=max(np.linspace(0.05,0.95,91),key=lambda t:prf(Y['valid'],S['valid']>=t)[2])
    print(ds,'test pairs',len(Y['test']),'dups',Y['test'].sum())
    print('  rule            ',prf(Y['test'],rule['test']))
    print('  title sim  t=%.2f'%best,prf(Y['test'],D['test'][0][:,0]>=best))
    print('  embed only AP %.3f'%average_precision_score(Y['test'],D['test'][0][:,1]))
    print('  combined   t=%.2f'%tlr,prf(Y['test'],S['test']>=tlr),'AP %.3f'%average_precision_score(Y['test'],S['test']))
    print('  coef',np.round(lr.coef_,2))
    res[ds]=dict(S=S,Y=Y,rule=rule,feat=D)
np.save('res.npy',res,allow_pickle=True)
