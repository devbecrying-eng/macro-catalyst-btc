"""
╔══════════════════════════════════════════════════════════════╗
║  MACRO CATALYST INTELLIGENCE TERMINAL — V6                   ║
║  UI: ChainX-inspired deep teal glass-morphism                ║
║  Data: Oil·VIX·10Y·Gold·S&P·BTC — Hyperliquid + Yahoo       ║
╚══════════════════════════════════════════════════════════════╝
"""
import streamlit as st,pandas as pd,numpy as np,plotly.graph_objects as go
from datetime import datetime,timedelta,date
import requests,time

try:
    import yfinance as yf;HAS_YF=True
except ImportError:HAS_YF=False
try:
    from streamlit_autorefresh import st_autorefresh;HAS_AR=True
except ImportError:HAS_AR=False

# ═══════════════════════════════════════════════════════
#  DESIGN — Deep teal glass-morphism (ChainX style)
# ═══════════════════════════════════════════════════════
CSS="""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
:root{
  --bg:#0a1a1a;--bg2:#0d2626;--card:rgba(16,46,46,0.65);--card2:rgba(20,56,56,0.5);
  --border:rgba(16,185,129,0.12);--border2:rgba(16,185,129,0.25);
  --accent:#10b981;--accent2:#34d399;--accent-dim:#059669;--accent-glow:rgba(16,185,129,0.2);
  --red:#ef4444;--amber:#f59e0b;--cyan:#06b6d4;
  --white:#f0fdf4;--text:#d1fae5;--sub:#6ee7b7;--muted:#064e3b;
}
[data-testid="stAppViewContainer"]{background:var(--bg)!important;font-family:'Inter',sans-serif;color:var(--white);}
[data-testid="stAppViewContainer"]::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(ellipse 80% 50% at 20% 0%,rgba(16,185,129,0.06),transparent 70%),
  radial-gradient(ellipse 60% 40% at 80% 100%,rgba(6,182,212,0.04),transparent 60%);}
[data-testid="stHeader"],[data-testid="stToolbar"],#MainMenu,footer{display:none!important;}
.block-container{padding:0.5rem 1rem!important;max-width:100%!important;position:relative;z-index:1;}
section[data-testid="stSidebar"]{display:none!important;}
[data-testid="column"]{padding:0 0.15rem!important;}
div[data-testid="stVerticalBlock"]>div{gap:0.08rem!important;}

/* Glass cards — frosted with corner gradient glow + pulse + shadow */
.gc{
  background:linear-gradient(135deg,rgba(16,185,129,0.08) 0%,rgba(16,46,46,0.55) 30%,rgba(13,38,38,0.65) 100%);
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border:1px solid rgba(16,185,129,0.1);border-radius:16px;padding:0.7rem 0.85rem;margin-bottom:0.35rem;
  box-shadow:0 8px 32px rgba(0,0,0,0.4),0 2px 8px rgba(0,0,0,0.2);
  position:relative;overflow:hidden;
  animation:cardPulse 4s ease-in-out infinite;
}
.gc::after{content:'';position:absolute;top:-1px;right:-1px;width:80px;height:80px;
  background:radial-gradient(circle at top right,rgba(16,185,129,0.12),transparent 70%);
  border-radius:0 16px 0 0;pointer-events:none;}
@keyframes cardPulse{0%,100%{border-color:rgba(16,185,129,0.1);box-shadow:0 8px 32px rgba(0,0,0,0.4),0 2px 8px rgba(0,0,0,0.2);}
50%{border-color:rgba(16,185,129,0.18);box-shadow:0 8px 32px rgba(0,0,0,0.4),0 0 15px rgba(16,185,129,0.06);}}
.gc:hover{border-color:rgba(16,185,129,0.25);box-shadow:0 8px 32px rgba(0,0,0,0.4),0 0 20px rgba(16,185,129,0.1);}
.gc-title{font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;color:var(--sub);margin-bottom:0.45rem;display:flex;align-items:center;gap:0.4rem;}
.gc-dot{width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 10px var(--accent);}
/* Intel blocks — same glass treatment */
.ib{background:linear-gradient(135deg,rgba(16,185,129,0.05) 0%,rgba(20,56,56,0.45) 100%);
  backdrop-filter:blur(16px);border:1px solid rgba(16,185,129,0.08);border-radius:12px;
  padding:0.55rem 0.7rem;margin-bottom:0.25rem;border-left:none;
  box-shadow:0 4px 16px rgba(0,0,0,0.25);transition:border-color 0.2s;}
.ib:hover{border-color:rgba(16,185,129,0.2);}

/* Pills */
.pill{font-family:'Inter',sans-serif;font-size:0.6rem;font-weight:700;padding:0.15rem 0.55rem;border-radius:20px;display:inline-block;}
.pill-safe{background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);}
.pill-warn{background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);}
.pill-danger{background:rgba(239,68,68,0.15);color:#f87171;border:1px solid rgba(239,68,68,0.3);}
.pill-neutral{background:rgba(16,185,129,0.08);color:var(--sub);border:1px solid var(--border);}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{gap:4px;background:var(--card);border-radius:12px;padding:3px;border:1px solid var(--border);backdrop-filter:blur(20px);}
.stTabs [data-baseweb="tab"]{font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;color:var(--sub);
  background:transparent;border-radius:10px;padding:0.5rem 1.5rem;transition:all 0.2s;}
.stTabs [aria-selected="true"]{background:var(--accent)!important;color:#022c22!important;box-shadow:0 0 15px rgba(16,185,129,0.3);}
.stTabs [data-baseweb="tab-highlight"]{display:none;}
.stTabs [data-baseweb="tab-border"]{display:none;}

/* Select boxes */
div[data-baseweb="select"]>div{background:var(--card2)!important;border-color:var(--border)!important;color:var(--accent)!important;font-family:'Inter'!important;font-size:0.75rem!important;border-radius:10px!important;}
div[data-baseweb="popover"] ul{background:rgba(16,46,46,0.95)!important;backdrop-filter:blur(20px)!important;border:1px solid var(--border)!important;border-radius:10px!important;}
div[data-baseweb="popover"] li{color:var(--text)!important;font-family:'Inter'!important;font-size:0.8rem!important;}
div[data-baseweb="popover"] li:hover{background:var(--accent-glow)!important;}

/* Scrollbar */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--muted);border-radius:2px;}
</style>"""

# ═══════════════════════════════════════════════════════
#  ZONES (same logic, new colors mapped)
# ═══════════════════════════════════════════════════════
OIL_Z={"DEPRESSED":{"mn":0,"mx":58,"c":"#06b6d4","b":-1,"l":"DEPRESSED","d":"Demand destruction"},
"STABLE":{"mn":58,"mx":78,"c":"#10b981","b":2,"l":"STABLE","d":"Growth-supportive"},
"ELEVATED":{"mn":78,"mx":95,"c":"#f59e0b","b":0,"l":"ELEVATED","d":"Inflation pressure"},
"STRESS":{"mn":95,"mx":115,"c":"#ef4444","b":-1,"l":"STRESS","d":"Supply disruption"},
"CRISIS":{"mn":115,"mx":999,"c":"#ef4444","b":-2,"l":"CRISIS","d":"Stagflation risk"}}
VIX_Z={"LOW":{"mn":0,"mx":15,"c":"#10b981","b":2,"l":"LOW FEAR","d":"Risk-on"},
"NORMAL":{"mn":15,"mx":20,"c":"#06b6d4","b":1,"l":"NORMAL","d":"Standard"},
"ELEVATED":{"mn":20,"mx":25,"c":"#f59e0b","b":0,"l":"ELEVATED","d":"Caution"},
"HIGH":{"mn":25,"mx":35,"c":"#ef4444","b":-1,"l":"HIGH FEAR","d":"Correction likely"},
"EXTREME":{"mn":35,"mx":999,"c":"#ef4444","b":-2,"l":"EXTREME","d":"Panic"}}
YLD_Z={"ACCOM":{"mn":0,"mx":3.0,"c":"#10b981","b":2,"l":"ACCOMMODATIVE","d":"Favor risk"},
"NEUTRAL":{"mn":3.0,"mx":3.8,"c":"#06b6d4","b":1,"l":"NEUTRAL","d":"Manageable"},
"TIGHT":{"mn":3.8,"mx":4.5,"c":"#f59e0b","b":0,"l":"TIGHTENING","d":"Growth pressure"},
"RESTRICT":{"mn":4.5,"mx":5.0,"c":"#ef4444","b":-1,"l":"RESTRICTIVE","d":"Tight liquidity"},
"CRISIS":{"mn":5.0,"mx":99,"c":"#ef4444","b":-2,"l":"CRISIS","d":"Severe"}}
GOLD_Z={"LOW":{"mn":0,"mx":1800,"c":"#10b981","b":1,"l":"LOW","d":"Risk appetite strong"},
"NORMAL":{"mn":1800,"mx":2200,"c":"#06b6d4","b":0,"l":"NORMAL","d":"Standard"},
"ELEVATED":{"mn":2200,"mx":2800,"c":"#f59e0b","b":-1,"l":"ELEVATED","d":"Safe-haven rising"},
"HIGH":{"mn":2800,"mx":4000,"c":"#ef4444","b":-1,"l":"HIGH","d":"Flight to safety"},
"EXTREME":{"mn":4000,"mx":99999,"c":"#ef4444","b":-2,"l":"EXTREME","d":"Crisis hedging"}}
SPX_Z={"BEAR":{"mn":0,"mx":4200,"c":"#ef4444","b":-2,"l":"BEAR","d":"Deep correction"},
"WEAK":{"mn":4200,"mx":4800,"c":"#f59e0b","b":-1,"l":"WEAK","d":"Below trend"},
"NEUTRAL":{"mn":4800,"mx":5400,"c":"#06b6d4","b":0,"l":"NEUTRAL","d":"Range-bound"},
"BULL":{"mn":5400,"mx":6200,"c":"#10b981","b":1,"l":"BULL","d":"Risk appetite"},
"EUPHORIA":{"mn":6200,"mx":99999,"c":"#10b981","b":2,"l":"EUPHORIA","d":"Peak risk-on"}}
BTC_Z={"DEEP_BEAR":{"mn":0,"mx":40000,"c":"#ef4444","b":-2,"l":"DEEP BEAR","d":"Capitulation"},
"BEAR":{"mn":40000,"mx":55000,"c":"#f59e0b","b":-1,"l":"BEAR","d":"Below key MAs"},
"NEUTRAL":{"mn":55000,"mx":72000,"c":"#06b6d4","b":0,"l":"NEUTRAL","d":"Consolidation"},
"BULL":{"mn":72000,"mx":95000,"c":"#10b981","b":1,"l":"BULL","d":"Trending up"},
"EUPHORIA":{"mn":95000,"mx":999999,"c":"#10b981","b":2,"l":"EUPHORIA","d":"Price discovery"}}

CATS={"OIL":{"n":"Crude Oil","s":"CL=F","u":"$/bbl","z":OIL_Z,"f":"${:.2f}"},
"VIX":{"n":"VIX","s":"^VIX","u":"pts","z":VIX_Z,"f":"{:.2f}"},
"10Y":{"n":"10Y Yield","s":"^TNX","u":"%","z":YLD_Z,"f":"{:.2f}%"},
"GOLD":{"n":"Gold","s":"GC=F","u":"$/oz","z":GOLD_Z,"f":"${:,.0f}"},
"S&P":{"n":"S&P 500","s":"^GSPC","u":"pts","z":SPX_Z,"f":"{:,.0f}"},
"BTC":{"n":"Bitcoin","s":"BTC-USD","u":"USD","z":BTC_Z,"f":"${:,.0f}"}}

THREAT_CFG={
"OIL":{"safe":[58,78],"caution":[78,95],"danger":[95,999],"sn":"No inflation pressure from energy","cn":"Inflation pressure building","dn":"Recession risk rising, BTC under pressure","inv":False,"label":"WTI CRUDE"},
"VIX":{"safe":[0,20],"caution":[20,25],"danger":[25,999],"sn":"Fear low, risk appetite healthy","cn":"Elevated BTC volatility likely","dn":"Institutional fear driving sell pressure","inv":False,"label":"VIX"},
"10Y":{"safe":[0,3.8],"caution":[3.8,4.5],"danger":[4.5,99],"sn":"Liquidity conditions supportive","cn":"Borrowing costs pressuring growth","dn":"Tight liquidity draining risk assets","inv":False,"label":"10Y YIELD"},
"GOLD":{"safe":[0,2800],"caution":[2800,4000],"danger":[4000,99999],"sn":"Capital available for risk","cn":"Capital shifting defensive","dn":"Capital locked in defensive assets","inv":False,"label":"GOLD"},
"S&P":{"safe":[5400,99999],"caution":[4800,5400],"danger":[0,4800],"sn":"Broad risk appetite strong","cn":"Mixed signals for crypto","dn":"Risk-off weighing on all assets","inv":True,"label":"S&P 500"},
"BTC":{"safe":[72000,999999],"caution":[55000,72000],"danger":[0,55000],"sn":"Bull structure intact","cn":"Waiting for direction","dn":"Below key support","inv":True,"label":"BTC"},
}

SPEED_TH={"24h":{"n":3,"x":5},"3d":{"n":6,"x":10},"7d":{"n":10,"x":15}}
TFC={"1H":{"p":"5d","i":"1h","l":"1H"},"4H":{"p":"30d","i":"1h","l":"4H"},"1D":{"p":"1y","i":"1d","l":"1D"},"1W":{"p":"5y","i":"1wk","l":"1W"},"1M":{"p":"max","i":"1mo","l":"1M"}}
REFRESH=120

ECON_CAL=[
{"dt":"2026-03-23","ev":"DEADLINE","t":"Trump 48hr Hormuz Ultimatum","ctx":"Binary event for oil. All risk assets hinge on this.","imp":"EXTREME"},
{"dt":"2026-03-24","ev":"PMI","t":"March PMIs","ctx":"First hard data on war impact. Services below 50 = recession.","imp":"HIGH"},
{"dt":"2026-03-25","ev":"DATA","t":"Durable Goods","ctx":"Business capex gauge.","imp":"MED"},
{"dt":"2026-03-26","ev":"DATA","t":"Jobless Claims","ctx":"Spike above 250K = layoff cycle.","imp":"MED"},
{"dt":"2026-03-27","ev":"DATA","t":"Feb PCE + UMich","ctx":"Fed's preferred inflation + consumer confidence.","imp":"HIGH"},
{"dt":"2026-04-03","ev":"NFP","t":"Mar Jobs","ctx":"Strong = Fed tight. Weak = cut hopes.","imp":"HIGH"},
{"dt":"2026-04-10","ev":"CPI","t":"Mar CPI","ctx":"Oil pass-through. If oil >$90, expect hot.","imp":"HIGH"},
{"dt":"2026-05-06","ev":"FOMC","t":"Fed Decision","ctx":"First post-crisis meeting.","imp":"EXTREME"},
{"dt":"2026-06-17","ev":"FOMC","t":"Fed + Dot Plot","ctx":"Rate path for rest of year.","imp":"EXTREME"},
{"dt":"2026-07-29","ev":"FOMC","t":"Fed Decision","ctx":"Summer rate decision.","imp":"EXTREME"},
]

# ═══════════════════════════════════════════════════════
#  DATA + CALCS (unchanged logic)
# ═══════════════════════════════════════════════════════
def gz(p,z):
    if p is None: return list(z.values())[2]
    for v in z.values():
        if v["mn"]<=p<v["mx"]: return v
    return list(z.values())[-1]

@st.cache_data(ttl=REFRESH)
def hl_price():
    try:
        r=requests.post("https://api.hyperliquid.xyz/info",json={"type":"allMids"},headers={"Content-Type":"application/json"},timeout=10)
        if r.status_code==200:
            ms=r.json()
            for t in["xyz:CL","xyz:OIL","xyz:USOIL","xyz:WTI"]:
                if t in ms:return float(ms[t]),t
            for k,v in ms.items():
                if any(x in k.upper() for x in["CL","OIL","WTI","CRUDE"]):return float(v),k
    except:pass
    return None,None

@st.cache_data(ttl=REFRESH)
def yfd(sym,period="1y",interval="1d"):
    if not HAS_YF:return None
    try:
        df=yf.Ticker(sym).history(period=period,interval=interval)
        if df is not None and len(df)>0:
            df.reset_index(inplace=True)
            if "Datetime" in df.columns:df.rename(columns={"Datetime":"Date"},inplace=True)
            df["Date"]=pd.to_datetime(df["Date"])
            if df["Date"].dt.tz is not None:df["Date"]=df["Date"].dt.tz_localize(None)
            return df
    except:pass
    return None

def latest(sym):
    df=yfd(sym,"5d","1h")
    return float(df["Close"].iloc[-1]) if df is not None and len(df)>0 else None

def calc_speed(df):
    if df is None or len(df)<2:return None
    cl=df["Close"].values;cur=cl[-1];ag=(df["Date"].iloc[-1]-df["Date"].iloc[0]).total_seconds()/max(len(df)-1,1)
    dy=ag>43200;ws={"24h":1,"3d":3,"7d":7} if dy else {"24h":24,"3d":72,"7d":168};o={}
    for k,lb in ws.items():
        if len(cl)>lb and cl[-(lb+1)]!=0:
            p=((cur-cl[-(lb+1)])/cl[-(lb+1)])*100;th=SPEED_TH[k];sv="EXTREME" if abs(p)>=th["x"] else("NOTABLE" if abs(p)>=th["n"] else "NORMAL")
            o[k]={"p":p,"s":sv,"d":"UP" if p>0 else "DOWN"}
        else:o[k]=None
    return o

def calc_rsi(df):
    if df is None or len(df)<15:return None
    c=df["Close"].copy();d=c.diff();g=d.where(d>0,0.0);l=(-d.where(d<0,0.0))
    ag=g.rolling(14,min_periods=14).mean();al=l.rolling(14,min_periods=14).mean()
    rs=ag/al.replace(0,np.nan);rsi=100-(100/(1+rs));v=rsi.iloc[-1]
    return float(v) if not pd.isna(v) else None

def calc_dir(df,lb=10):
    if df is None or len(df)<lb+1:return "FLAT",0.0
    c=df["Close"].values;p=((c[-1]-c[-(lb+1)])/c[-(lb+1)])*100
    return("RISING",p) if p>2 else(("FALLING",p) if p<-2 else("FLAT",p))

def calc_corr(d1,d2,w=30):
    if d1 is None or d2 is None or len(d1)<w or len(d2)<w:return None
    try:
        a=d1.set_index("Date")["Close"].resample("1D").last().dropna();b=d2.set_index("Date")["Close"].resample("1D").last().dropna()
        m=pd.DataFrame({"a":a,"b":b}).dropna()
        return float(m["a"].tail(w).corr(m["b"].tail(w))) if len(m)>=w else None
    except:return None

def calc_timeline(df,zones):
    if df is None or len(df)<2:return None,{}
    tl,zd=[],{}
    for _,r in df.iterrows():
        z=gz(r["Close"],zones);k=z["l"];zd[k]=zd.get(k,0)+1;tl.append({"dt":r["Date"],"p":r["Close"],"z":k,"c":z["c"]})
    return tl,zd

def zone_trans(df,zones,lb=5):
    if df is None or len(df)<lb+1:return None
    cz=gz(df["Close"].iloc[-1],zones)["l"];pz=gz(df["Close"].iloc[-(lb+1)],zones)["l"]
    return{"from":pz,"to":cz} if cz!=pz else None

# Bias
def add_sigs(sigs,key,price,df,zones):
    if price is not None:z=gz(price,zones);sigs.append({"cat":key,"sig":"Zone","st":z["l"],"sc":z["b"],"mx":2})
    spd=calc_speed(df)
    if spd:
        ss,sl=0,"Normal"
        for w in["24h","3d","7d"]:
            s=spd.get(w)
            if s and s["s"]=="EXTREME":
                if key in["VIX","GOLD"]:ss=-2 if s["d"]=="UP" else 2
                elif key in["10Y"]:ss=-1 if s["d"]=="UP" else 1
                elif key=="OIL":ss=2 if s["d"]=="DOWN" else -2
                else:ss=2 if s["d"]=="UP" else -2
                sl=f"Extreme {w}";break
            elif s and s["s"]=="NOTABLE":
                if key in["VIX","GOLD","OIL","10Y"]:ss=max(ss,1) if s["d"]=="DOWN" else min(ss,-1)
                else:ss=max(ss,1) if s["d"]=="UP" else min(ss,-1)
                sl=f"Notable {w}"
        if ss!=0:sigs.append({"cat":key,"sig":"Speed","st":sl,"sc":ss,"mx":2})
    tr=zone_trans(df,zones,5)
    if tr:
        zk=list(zones.keys());fi=next((i for i,k2 in enumerate(zk) if zones[k2]["l"]==tr["from"]),2);ti=next((i for i,k2 in enumerate(zk) if zones[k2]["l"]==tr["to"]),2)
        tsc=(1 if ti>fi else -1) if key in["S&P","BTC"] else(1 if ti<fi else -1)
        sigs.append({"cat":key,"sig":"Shift","st":f"{tr['from']}→{tr['to']}","sc":tsc,"mx":1})

def calc_bias(prices,dailys):
    sigs=[]
    for key in CATS:add_sigs(sigs,key,prices.get(key),dailys.get(key),CATS[key]["z"])
    tot=sum(s["sc"] for s in sigs);mp=sum(s["mx"] for s in sigs)
    if mp==0:return{"sigs":sigs,"tot":0,"mp":mp,"v":"NO DATA","vc":"#6ee7b7"}
    ra=tot/mp
    if ra>=0.5:v,vc="RISK-ON","#10b981"
    elif ra>=0.2:v,vc="LEAN RISK-ON","#34d399"
    elif ra>-0.2:v,vc="NEUTRAL","#f59e0b"
    elif ra>-0.5:v,vc="LEAN RISK-OFF","#ef4444"
    else:v,vc="RISK-OFF","#ef4444"
    return{"sigs":sigs,"tot":tot,"mp":mp,"v":v,"vc":vc}

# Threat status
def threat(key,price):
    if price is None:return None
    tc=THREAT_CFG[key];inv=tc["inv"];s,c,d=tc["safe"],tc["caution"],tc["danger"]
    if not inv:
        if s[0]<=price<s[1]:st2,note,col="SAFE",tc["sn"],"#10b981"
        elif c[0]<=price<c[1]:st2,note,col="CAUTION",tc["cn"],"#f59e0b"
        else:st2,note,col="DANGER",tc["dn"],"#ef4444"
        fmax=d[0]*1.3 if d[0]<1000 else d[0]+2000
        bar=max(2,min(98,((price-s[0])/(fmax-s[0]))*100))
        if st2=="SAFE":prox=f"{abs((c[0]-price)/price*100):.1f}% to caution"
        elif st2=="CAUTION":prox=f"{abs((d[0]-price)/price*100):.1f}% to danger"
        else:prox=f"In danger zone"
    else:
        if s[0]<=price:st2,note,col="SAFE",tc["sn"],"#10b981"
        elif c[0]<=price<c[1]:st2,note,col="CAUTION",tc["cn"],"#f59e0b"
        else:st2,note,col="DANGER",tc["dn"],"#ef4444"
        if key=="BTC":fmin,fmax=30000,120000
        elif key=="S&P":fmin,fmax=3500,7000
        else:fmin,fmax=0,s[0]*1.3
        bar=max(2,min(98,((price-fmin)/(fmax-fmin))*100))
        if st2=="SAFE":prox=f"{abs((price-s[0])/price*100):.1f}% above safe"
        elif st2=="CAUTION":prox=f"{abs((s[0]-price)/price*100):.1f}% to safe"
        else:prox=f"In danger zone"
    return{"st":st2,"note":note,"col":col,"prox":prox,"bar":bar}

# Intelligence
def gen_briefing(prices,dailys,bias,corrs):
    lines=[];op,vp,yp,gp,sp,bp=prices.get("OIL"),prices.get("VIX"),prices.get("10Y"),prices.get("GOLD"),prices.get("S&P"),prices.get("BTC")
    lines.append(("MACRO",f"Bias: {bias['v']} — Score {bias['tot']:+d}/{bias['mp']}",bias["vc"]))
    if op:
        oz=gz(op,OIL_Z)
        if oz["l"] in["STRESS","CRISIS"]:lines.append(("OIL",f"Oil ${op:.0f} in {oz['l']}. Supply disruption priced. Every $10 above $95 adds ~0.3% to CPI within 2 months.","#ef4444"))
        elif oz["l"]=="ELEVATED":lines.append(("OIL",f"Oil ${op:.0f} ELEVATED. Watch $95 for regime shift. This is where 2022 inflation accelerated.","#f59e0b"))
        else:lines.append(("OIL",f"Oil ${op:.0f} STABLE. No energy inflation pressure. Best macro for risk.","#10b981"))
    if vp:
        vz=gz(vp,VIX_Z);vd,vdp=calc_dir(dailys.get("VIX"),5)
        if vz["l"] in["EXTREME","HIGH FEAR"]:lines.append(("VIX",f"VIX {vp:.1f} — {vz['l']}. Institutional hedging heavy.","#ef4444"))
        elif vd=="FALLING" and vp>18:lines.append(("VIX",f"VIX {vp:.1f} falling ({vdp:.1f}% 5d). Fear subsiding — strong risk-on signal.","#10b981"))
    if gp and vp:
        gd,_=calc_dir(dailys.get("GOLD"),10);vd2,_=calc_dir(dailys.get("VIX"),10)
        if gd=="RISING" and vd2=="FALLING":lines.append(("SIGNAL",f"Gold rising + VIX falling. Institutions hedging geopolitical risk specifically, not broad fear.","#06b6d4"))
    if yp:
        yz=gz(yp,YLD_Z);yd,ydp=calc_dir(dailys.get("10Y"),10)
        if yz["l"] in["RESTRICTIVE","CRISIS"]:lines.append(("10Y",f"Yields {yp:.2f}% {yz['l']}. Liquidity drain active.","#ef4444"))
        elif yd=="RISING":lines.append(("10Y",f"Yields {yp:.2f}% rising. Tightening. Watch 4.5%.","#f59e0b"))
        elif yd=="FALLING":lines.append(("10Y",f"Yields {yp:.2f}% falling. Market pricing easing.","#10b981"))
    if bp:
        oc=corrs.get("OIL/BTC");sc=corrs.get("S&P/BTC")
        if oc and abs(oc)>0.4:lines.append(("BTC",f"Oil-BTC correlation {oc:+.2f}. Macro transmission active.","#06b6d4"))
        if sc and abs(sc)>0.4:lines.append(("BTC",f"S&P-BTC {sc:+.2f}. BTC moving {'with' if sc>0 else 'against'} equities.","#06b6d4"))
    return lines

def gen_scenarios(prices):
    op,vp=prices.get("OIL"),prices.get("VIX")
    bull,bear=[],[]
    if op and op>85:bull+=["Oil drops below $85 (ceasefire)","→ Inflation eases","→ Fed gets flexibility","→ Yields drop, liquidity improves","→ BTC rallies on risk rotation"]
    if vp and vp>20:bull+=["VIX below 20 (fear normalizing)","→ Hedges unwind, capital to risk"]
    if op and op>80:bear+=["Oil above $115 (Hormuz closure)","→ Inflation spikes, CPI hot","→ Fed forced restrictive","→ Liquidity drains","→ BTC tests lower supports"]
    if vp and vp>15:bear+=["VIX above 35 (systemic fear)","→ Forced liquidations","→ Everything sells"]
    return bull,bear

def gen_chains(prices):
    ch=[];op,vp,yp,gp=prices.get("OIL"),prices.get("VIX"),prices.get("10Y"),prices.get("GOLD")
    if op and op>90:ch.append({"t":"IRAN/HORMUZ","s":[f"Oil ${op:.0f}","→ Inflation rising","→ Fed boxed in","→ Yields high","→ BTC headwind"],"c":"#ef4444"})
    if vp and vp<20:ch.append({"t":"FEAR SUBSIDING","s":[f"VIX {vp:.1f}","→ Hedges unwinding","→ Capital to risk","→ BTC benefits"],"c":"#10b981"})
    if gp and gp>4000:ch.append({"t":"SAFE HAVEN","s":[f"Gold ${gp:,.0f}","→ Institutional fear","→ Defensive capital","→ Less crypto flow","→ Reversal = sharp risk-on"],"c":"#f59e0b"})
    if yp and yp>4.3:ch.append({"t":"RATE PRESSURE","s":[f"10Y {yp:.2f}%","→ Costs rising","→ Growth declining","→ Crypto pressure"],"c":"#ef4444"})
    return ch

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    st.set_page_config(page_title="Macro Catalyst",page_icon="📊",layout="wide",initial_sidebar_state="collapsed")
    st.markdown(CSS,unsafe_allow_html=True)
    if HAS_AR:st_autorefresh(interval=REFRESH*1000,key="ar")

    hlp,hltk=hl_price()
    prices={k:(hlp if k=="OIL" and hlp else latest(c["s"])) for k,c in CATS.items()}
    src="Hyperliquid 24/7" if hlp else "Yahoo Finance"
    dailys={k:yfd(c["s"],"1y","1d") for k,c in CATS.items()}
    bias=calc_bias(prices,dailys)
    corrs={f"{k}/BTC":calc_corr(dailys.get(k),dailys.get("BTC"),30) for k in["OIL","VIX","GOLD","S&P","10Y"]}

    # Header
    h1,h2=st.columns([5,1])
    with h1:
        st.markdown(f'<div style="font-family:Inter;font-size:1.5rem;font-weight:900;color:#f0fdf4">Macro Catalyst</div>'
            f'<div style="font-family:Inter;font-size:0.75rem;font-weight:500;color:#6ee7b7;margin-top:-4px">Intelligence Terminal</div>',unsafe_allow_html=True)
    with h2:
        st.markdown(f'<div style="text-align:right;padding-top:4px">'
            f'<span style="font-family:Inter;font-size:0.65rem;font-weight:600;color:#10b981;padding:3px 10px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);border-radius:20px">● Live: {src}</span></div>',unsafe_allow_html=True)

    tab1,tab2=st.tabs(["Command Center","Intelligence Briefing"])

    # ═══ TAB 1 ═══
    with tab1:
        r1a,r1b=st.columns([2,3])
        # Bias
        with r1a:
            vc=bias["vc"];sp=max(2,min(98,(bias["tot"]/bias["mp"]*50+50) if bias["mp"]>0 else 50))
            sh="".join(f'<div style="display:flex;align-items:center;gap:0.3rem;padding:0.25rem 0;border-bottom:1px solid rgba(16,185,129,0.08)">'
                f'<span style="font-size:0.7rem;font-weight:700;color:#6ee7b7;min-width:30px">{s["cat"]}</span>'
                f'<span style="font-size:0.75rem;font-weight:600;color:#d1fae5;flex:1">{s["st"]}</span>'
                f'<span style="font-size:0.65rem;color:#6ee7b7;min-width:45px">{s["sig"]}</span>'
                f'<span style="font-size:0.8rem;font-weight:800;color:{"#10b981" if s["sc"]>0 else("#ef4444" if s["sc"]<0 else "#6ee7b7")};min-width:28px;text-align:right">{s["sc"]:+d}</span></div>' for s in bias["sigs"])
            st.markdown(f"""<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:{vc};box-shadow:0 0 10px {vc}"></div>Macro Confluence Bias</div>
                <div style="text-align:center;padding:4px 0"><span style="font-size:1.4rem;font-weight:900;color:{vc}">{bias['v']}</span></div>
                <div style="position:relative;height:10px;background:rgba(10,26,26,0.8);border-radius:5px;margin:6px 0;border:1px solid rgba(16,185,129,0.1)">
                <div style="position:absolute;left:0;top:0;width:30%;height:100%;background:rgba(239,68,68,0.06);border-radius:5px 0 0 5px"></div>
                <div style="position:absolute;right:0;top:0;width:30%;height:100%;background:rgba(16,185,129,0.06);border-radius:0 5px 5px 0"></div>
                <div style="position:absolute;left:50%;width:1px;height:100%;background:rgba(16,185,129,0.15)"></div>
                <div style="position:absolute;left:{sp}%;top:-3px;width:5px;height:16px;background:{vc};border-radius:3px;transform:translateX(-2px);box-shadow:0 0 10px {vc}"></div></div>
                <div style="display:flex;justify-content:space-between;margin-bottom:6px"><span style="font-size:0.6rem;font-weight:600;color:#ef4444">Risk-Off</span><span style="font-size:0.6rem;color:#6ee7b7">Neutral</span><span style="font-size:0.6rem;font-weight:600;color:#10b981">Risk-On</span></div>
                <div style="text-align:center;margin-bottom:8px"><span style="font-size:0.75rem;color:#6ee7b7">Score</span><span style="font-size:1rem;font-weight:900;color:{vc}"> {bias['tot']:+d}</span><span style="font-size:0.75rem;color:rgba(16,185,129,0.3)"> / {bias['mp']}</span></div>
                <div style="border-top:1px solid rgba(16,185,129,0.1);padding-top:4px"><div style="font-size:0.65rem;font-weight:700;color:#6ee7b7;margin-bottom:4px">Signal Breakdown</div><div style="max-height:210px;overflow-y:auto">{sh}</div></div></div>""",unsafe_allow_html=True)

        # Threat Board
        with r1b:
            safe_c=sum(1 for k in CATS if threat(k,prices.get(k)) and threat(k,prices.get(k))["st"]=="SAFE")
            danger_c=sum(1 for k in CATS if threat(k,prices.get(k)) and threat(k,prices.get(k))["st"]=="DANGER")
            total_a=sum(1 for k in CATS if prices.get(k) is not None)
            sc2="#10b981" if safe_c>danger_c else("#ef4444" if danger_c>safe_c else "#f59e0b")
            st.markdown(f"""<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:{sc2};box-shadow:0 0 10px {sc2}"></div>Threat Board</div>
                <div style="text-align:center;margin-bottom:8px"><span style="font-size:0.85rem;font-weight:800;color:{sc2}">{safe_c} Safe · {total_a-safe_c-danger_c} Caution · {danger_c} Danger</span></div>""",unsafe_allow_html=True)
            for key in CATS:
                p=prices.get(key);ts=threat(key,p);tc=THREAT_CFG[key]
                if ts is None:continue
                dr,_=calc_dir(dailys.get(key),7)
                ps=CATS[key]["f"].format(p);inv=tc["inv"]
                # Direction arrow color
                if key in["S&P","BTC"]:dc="#10b981" if dr=="RISING" else("#ef4444" if dr=="FALLING" else "#6ee7b7")
                else:dc="#ef4444" if dr=="RISING" else("#10b981" if dr=="FALLING" else "#6ee7b7")
                arr="↑" if dr=="RISING" else("↓" if dr=="FALLING" else "→")
                # Bar segments
                if not inv:sp2,cp,dp=30,35,35
                else:dp,cp,sp2=30,35,35
                pcls="pill-safe" if ts["st"]=="SAFE" else("pill-danger" if ts["st"]=="DANGER" else "pill-warn")
                st.markdown(f"""<div style="display:flex;align-items:center;gap:0.5rem;padding:0.35rem 0.5rem;border-bottom:1px solid rgba(16,185,129,0.06)">
                    <div style="min-width:85px"><span style="font-size:0.7rem;font-weight:700;color:{ts['col']}">{key}</span><br>
                    <span style="font-size:0.95rem;font-weight:800;color:{ts['col']}">{ps}</span>
                    <span style="font-size:0.75rem;font-weight:700;color:{dc};margin-left:2px">{arr}</span></div>
                    <div style="flex:1"><div style="position:relative;height:12px;border-radius:6px;overflow:hidden;display:flex">
                    {'<div style="width:'+str(sp2)+'%;background:rgba(16,185,129,0.2)"></div><div style="width:'+str(cp)+'%;background:rgba(245,158,11,0.2)"></div><div style="width:'+str(dp)+'%;background:rgba(239,68,68,0.2)"></div>' if not inv else '<div style="width:'+str(dp)+'%;background:rgba(239,68,68,0.2)"></div><div style="width:'+str(cp)+'%;background:rgba(245,158,11,0.2)"></div><div style="width:'+str(sp2)+'%;background:rgba(16,185,129,0.2)"></div>'}
                    </div><div style="position:relative;margin-top:-12px;height:12px"><div style="position:absolute;left:{ts['bar']}%;top:-2px;width:5px;height:16px;background:{ts['col']};border-radius:3px;transform:translateX(-2px);box-shadow:0 0 8px {ts['col']}"></div></div>
                    <div style="font-size:0.65rem;font-weight:600;color:#6ee7b7;margin-top:2px">{ts['prox']}</div></div>
                    <span class="{pcls}">{ts['st']}</span></div>""",unsafe_allow_html=True)
            summary="Macro not fighting you" if safe_c>=4 else("Macro headwind active" if danger_c>=3 else "Mixed conditions")
            st.markdown(f'<div style="padding:0.4rem;font-size:0.75rem;font-weight:700;color:{sc2};border-top:1px solid rgba(16,185,129,0.1)">{summary}</div></div>',unsafe_allow_html=True)

        # Catalyst cards
        cs=st.columns(6)
        for i,(key,cat) in enumerate(CATS.items()):
            p=prices.get(key);z=gz(p,cat["z"]);df=dailys.get(key)
            ps=cat["f"].format(p) if p else "—";dr,dp=calc_dir(df,10) if df is not None else("FLAT",0);rsi=calc_rsi(df)
            dc="#10b981" if dr=="RISING" else("#ef4444" if dr=="FALLING" else "#6ee7b7")
            da="▲" if dr=="RISING" else("▼" if dr=="FALLING" else "—");rc="#10b981" if rsi and rsi<30 else("#ef4444" if rsi and rsi>70 else "#d1fae5")
            pcls="pill-safe" if z["b"]>0 else("pill-danger" if z["b"]<0 else "pill-neutral")
            with cs[i]:
                st.markdown(f"""<div class="gc"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.2rem">
                    <span style="font-size:0.75rem;font-weight:700;color:#6ee7b7">{key}</span><span class="{pcls}">{z['l']}</span></div>
                    <div><span style="font-size:1.2rem;font-weight:900;color:#34d399">{ps}</span></div>
                    <div style="display:flex;gap:0.6rem;margin-top:0.2rem">
                    <div><span style="font-size:0.55rem;color:#6ee7b7">Trend</span><br><span style="font-size:0.7rem;font-weight:700;color:{dc}">{da}{dr}</span></div>
                    <div><span style="font-size:0.55rem;color:#6ee7b7">Chg</span><br><span style="font-size:0.7rem;font-weight:700;color:{dc}">{dp:+.1f}%</span></div>
                    <div><span style="font-size:0.55rem;color:#6ee7b7">RSI</span><br><span style="font-size:0.7rem;font-weight:700;color:{rc}">{f"{rsi:.0f}" if rsi else "—"}</span></div></div></div>""",unsafe_allow_html=True)

        # Bottom row
        d1,d2,d3=st.columns([1.5,1.5,2])
        with d1:
            st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:#06b6d4;box-shadow:0 0 10px #06b6d4"></div>Correlations (30d)</div>',unsafe_allow_html=True)
            for pair,cv in corrs.items():
                if cv is None:continue
                cc="#10b981" if cv>0.3 else("#ef4444" if cv<-0.3 else "#6ee7b7");bw=max(5,min(95,abs(cv)*100))
                strength="Strong" if abs(cv)>0.6 else("Mod" if abs(cv)>0.3 else "Weak")
                st.markdown(f'<div style="padding:0.25rem 0;border-bottom:1px solid rgba(16,185,129,0.06)"><div style="display:flex;justify-content:space-between;margin-bottom:2px"><span style="font-size:0.75rem;font-weight:700;color:#d1fae5">{pair}</span><span style="font-size:0.8rem;font-weight:800;color:{cc}">{cv:+.2f}</span><span style="font-size:0.6rem;font-weight:700;color:{cc}">{strength}</span></div><div style="height:3px;background:rgba(10,26,26,0.8);border-radius:2px"><div style="height:100%;width:{bw}%;background:{cc};border-radius:2px"></div></div></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        with d2:
            odf=dailys.get("OIL")
            if odf is not None and len(odf)>10:
                tl,zd=calc_timeline(odf,OIL_Z);total=len(odf)
                if tl:
                    st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot"></div>Oil Regime — 12mo</div>',unsafe_allow_html=True)
                    active=[(k,zd.get(k,0)) for k in OIL_Z if zd.get(k,0)>0]
                    if active:
                        bc=st.columns([max(d2v,1) for _,d2v in active])
                        for i2,(zk,days) in enumerate(active):
                            zz=OIL_Z[zk]
                            with bc[i2]:st.markdown(f'<div style="background:{zz["c"]};border-radius:6px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.6rem;font-weight:700;color:#0a1a1a">{days}d</div>',unsafe_allow_html=True)
                    for zk in OIL_Z:
                        days=zd.get(zk,0)
                        if days==0:continue
                        zz=OIL_Z[zk]
                        st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.15rem 0;border-bottom:1px solid rgba(16,185,129,0.06)"><span style="font-size:0.7rem;font-weight:700;color:{zz["c"]}">{zz["l"]}</span><span style="font-size:0.7rem;color:#6ee7b7">{days}d ({days/total*100:.1f}%)</span></div>',unsafe_allow_html=True)
                    if len(tl)>=30:
                        mc=st.columns(30)
                        for i2,dd in enumerate(tl[-30:]):
                            with mc[i2]:st.markdown(f'<div style="background:{dd["c"]};height:8px;border-radius:3px;opacity:0.7"></div>',unsafe_allow_html=True)
                    st.markdown('</div>',unsafe_allow_html=True)
        with d3:
            today_d=date.today();upcoming=[e for e in ECON_CAL if datetime.strptime(e["dt"],"%Y-%m-%d").date()>=today_d][:6]
            st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:#f59e0b;box-shadow:0 0 10px #f59e0b"></div>Upcoming Catalysts</div>',unsafe_allow_html=True)
            for e in upcoming:
                ed=datetime.strptime(e["dt"],"%Y-%m-%d").date();du=(ed-today_d).days
                ec={"FOMC":"#10b981","CPI":"#f59e0b","NFP":"#06b6d4","PMI":"#06b6d4","DATA":"#6ee7b7","DEADLINE":"#ef4444"}.get(e["ev"],"#6ee7b7")
                urg="color:#ef4444;font-weight:800" if du<=3 else("color:#f59e0b;font-weight:700" if du<=7 else "color:#6ee7b7")
                ds="TODAY" if du==0 else("TMR" if du==1 else f"{du}d")
                st.markdown(f'<div style="padding:0.25rem 0.4rem;border-bottom:1px solid rgba(16,185,129,0.06)"><div style="display:flex;justify-content:space-between"><div style="display:flex;align-items:center;gap:5px"><div style="width:4px;height:4px;border-radius:50%;background:{ec};box-shadow:0 0 6px {ec}"></div><span style="font-size:0.65rem;font-weight:700;color:{ec}">{e["ev"]}</span></div><span style="font-size:0.7rem;{urg}">{ds} · {ed.strftime("%b %d")}</span></div><div style="font-size:0.75rem;font-weight:800;color:#d1fae5">{e["t"]}</div><div style="font-size:0.6rem;color:#6ee7b7">{e["ctx"]}</div></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

    # ═══ TAB 2 ═══
    with tab2:
        briefing=gen_briefing(prices,dailys,bias,corrs);bull,bear=gen_scenarios(prices);chains=gen_chains(prices)
        ib1,ib2=st.columns([3,2])
        with ib1:
            st.markdown(f'<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:{bias["vc"]};box-shadow:0 0 10px {bias["vc"]}"></div>Intelligence Briefing</div>',unsafe_allow_html=True)
            for cat,text,col in briefing:
                sz="0.9rem" if cat=="MACRO" else "0.75rem";wt="900" if cat=="MACRO" else "600"
                st.markdown(f'<div class="ib"><div style="display:flex;align-items:center;gap:6px;margin-bottom:3px"><div style="width:4px;height:4px;border-radius:50%;background:{col};box-shadow:0 0 6px {col}"></div><span style="font-size:0.65rem;font-weight:700;color:{col}">{cat}</span></div><span style="font-size:{sz};font-weight:{wt};color:#d1fae5;line-height:1.5">{text}</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
            st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:#10b981;box-shadow:0 0 10px #10b981"></div>Impact Chains</div>',unsafe_allow_html=True)
            for ch in chains:
                ch_h="<br>".join(f'<span style="font-size:0.75rem;font-weight:600;color:#d1fae5">{s}</span>' for s in ch["s"])
                st.markdown(f'<div class="ib"><div style="display:flex;align-items:center;gap:6px;margin-bottom:3px"><div style="width:4px;height:4px;border-radius:50%;background:{ch["c"]};box-shadow:0 0 6px {ch["c"]}"></div><span style="font-size:0.7rem;font-weight:800;color:{ch["c"]}">{ch["t"]}</span></div>{ch_h}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        with ib2:
            st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:#10b981;box-shadow:0 0 10px #10b981"></div>Bull Scenario</div>',unsafe_allow_html=True)
            for l in bull:
                cl="#10b981" if l.startswith("→") else "#d1fae5";st.markdown(f'<div style="padding:0.2rem 0.4rem;font-size:0.75rem;font-weight:{"600" if l.startswith("→") else "800"};color:{cl};border-bottom:1px solid rgba(16,185,129,0.06)">{l}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
            st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:#ef4444;box-shadow:0 0 10px #ef4444"></div>Bear Scenario</div>',unsafe_allow_html=True)
            for l in bear:
                cl="#ef4444" if l.startswith("→") else "#d1fae5";st.markdown(f'<div style="padding:0.2rem 0.4rem;font-size:0.75rem;font-weight:{"600" if l.startswith("→") else "800"};color:{cl};border-bottom:1px solid rgba(16,185,129,0.06)">{l}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
            today_d=date.today();upcoming=[e for e in ECON_CAL if datetime.strptime(e["dt"],"%Y-%m-%d").date()>=today_d][:10]
            st.markdown('<div class="gc"><div class="gc-title"><div class="gc-dot" style="background:#f59e0b;box-shadow:0 0 10px #f59e0b"></div>Full Calendar</div>',unsafe_allow_html=True)
            for e in upcoming:
                ed=datetime.strptime(e["dt"],"%Y-%m-%d").date();du=(ed-today_d).days
                ec={"FOMC":"#10b981","CPI":"#f59e0b","NFP":"#06b6d4","PMI":"#06b6d4","DATA":"#6ee7b7","DEADLINE":"#ef4444"}.get(e["ev"],"#6ee7b7")
                urg="color:#ef4444;font-weight:800" if du<=3 else("color:#f59e0b;font-weight:700" if du<=7 else "color:#6ee7b7")
                ds="TODAY" if du==0 else("TMR" if du==1 else f"{du}d")
                st.markdown(f'<div class="ib"><div style="display:flex;justify-content:space-between"><div style="display:flex;align-items:center;gap:5px"><div style="width:4px;height:4px;border-radius:50%;background:{ec};box-shadow:0 0 6px {ec}"></div><span style="font-size:0.65rem;font-weight:700;color:{ec}">{e["ev"]}</span></div><span style="font-size:0.7rem;{urg}">{ds} · {ed.strftime("%b %d")}</span></div><div style="font-size:0.75rem;font-weight:800;color:#d1fae5">{e["t"]}</div><div style="font-size:0.65rem;color:#6ee7b7">{e["ctx"]}</div></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.6rem;color:rgba(16,185,129,0.15);text-align:center;padding:10px 0;margin-top:10px">Macro Catalyst V6 · Intelligence Terminal · Refresh {REFRESH}s</div>',unsafe_allow_html=True)

if __name__=="__main__":main()
