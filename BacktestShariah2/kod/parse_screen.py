"""Parse fail keputusan quote_stock_screen (JSON) -> CSV harian: ticker,open,high,low,close,volume,floatcap"""
import json,sys,csv
KOD={2202:'open',2204:'high',2205:'low',2201:'close'}
def parse(path):
    txt=open(path).read(); d=json.loads(txt)
    if isinstance(d,list): d=json.loads(d[0]['text'])
    out=[]
    for it in d['data']['items']:
        r={'ticker':it['code'].split('.',1)[1],'nama':it.get('name','')}
        for x in it['results']:
            k=list(x.keys())[0]; v=x[k]
            p=v['property']['name']; val=v['res'].get('ival', v['res'].get('sval'))
            if val is None: continue
            if k=='simple_property_result' and p in KOD: r[KOD[p]]=int(val)/1000
            elif k=='cumulative_property_result' and p==3104: r['volume']=int(val)
            elif k=='financial_property_result' and p==4903: r['floatcap']=int(val)/1000
        out.append(r)
    return out, d.get('pagination',{})
if __name__=='__main__':
    rows=[];
    for p in sys.argv[2:]:
        o,pg=parse(p); rows+=o; print(p,len(o),pg,file=sys.stderr)
    w=csv.DictWriter(open(sys.argv[1],'w'),fieldnames=['ticker','nama','open','high','low','close','volume','floatcap']); w.writeheader(); w.writerows(rows)
    print(len(rows))
