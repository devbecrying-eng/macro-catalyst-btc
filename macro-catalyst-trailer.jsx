import { useState, useEffect, useRef } from "react";
const TL=[{t:0,ph:"BEAR",lb:"BREAKING",oil:94,vix:24,btc:70000,gold:4400,y:4.28,bias:"NEUTRAL",bs:0},{t:3,ph:"BEAR",lb:"ESCALATION",oil:98,vix:27,btc:68500,gold:4550,y:4.35,bias:"LEAN RISK-OFF",bs:-3},{t:6,ph:"BEAR",lb:"HORMUZ THREATENED",oil:108,vix:32,btc:64000,gold:4800,y:4.48,bias:"RISK-OFF",bs:-8},{t:10,ph:"BEAR",lb:"OIL CRISIS",oil:118,vix:38,btc:58000,gold:5100,y:4.62,bias:"RISK-OFF",bs:-12},{t:13,ph:"BEAR",lb:"CRISIS ZONE",oil:125,vix:42,btc:52000,gold:5400,y:4.75,bias:"RISK-OFF",bs:-16},{t:16,ph:"BEAR",lb:"CAPITULATION",oil:130,vix:45,btc:48000,gold:5600,y:4.85,bias:"RISK-OFF",bs:-18},{t:20,ph:"PIVOT",lb:"CEASEFIRE TALKS",oil:122,vix:40,btc:50000,gold:5300,y:4.70,bias:"RISK-OFF",bs:-14},{t:23,ph:"PIVOT",lb:"DE-ESCALATION",oil:110,vix:33,btc:55000,gold:4900,y:4.50,bias:"LEAN RISK-OFF",bs:-6},{t:27,ph:"BULL",lb:"STRAIT REOPENS",oil:95,vix:25,btc:62000,gold:4500,y:4.30,bias:"NEUTRAL",bs:0},{t:30,ph:"BULL",lb:"OIL FLUSHING",oil:82,vix:20,btc:70000,gold:4100,y:4.10,bias:"LEAN RISK-ON",bs:5},{t:34,ph:"BULL",lb:"RELIEF RALLY",oil:75,vix:17,btc:78000,gold:3800,y:3.90,bias:"RISK-ON",bs:10},{t:37,ph:"BULL",lb:"MACRO TAILWIND",oil:72,vix:15,btc:85000,gold:3500,y:3.75,bias:"RISK-ON",bs:14},{t:40,ph:"BULL",lb:"BTC BREAKOUT",oil:70,vix:14,btc:92000,gold:3300,y:3.60,bias:"RISK-ON",bs:16},{t:44,ph:"BULL",lb:"PRICE DISCOVERY",oil:68,vix:13,btc:98000,gold:3100,y:3.50,bias:"RISK-ON",bs:18},{t:48,ph:"END",lb:"MACRO CATALYST",oil:68,vix:13,btc:98000,gold:3100,y:3.50,bias:"RISK-ON",bs:18}];
const EC=[
{t:0,dur:2.8,icon:"\u{1F6E2}\uFE0F",title:"Ultimatum Expires",body:"Trump's 48-hour Hormuz deadline passes. Iran refuses to comply.",detail:"20% of global oil transits the Strait",c:"#ef4444"},
{t:3,dur:2.8,icon:"\u{1F4C8}",title:"Oil Enters STRESS Zone",body:"Oil breaks $95. Historically, 4 of 5 shocks above this level preceded recession.",detail:"Every $10 above $95 = +0.3% CPI",c:"#ef4444"},
{t:6,dur:3.5,icon:"\u{1F6A2}",title:"Hormuz Closure Threat",body:"Iran threatens full Strait closure. Shipping insurers halt coverage. Tanker traffic frozen.",detail:"20M barrels/day at risk",c:"#ef4444"},
{t:10,dur:2.8,icon:"\u{1F4CA}",title:"VIX Explodes Past 35",body:"Institutional panic. Forced liquidations cascade across all leveraged positions.",detail:"VIX >35 = extreme fear — top 5% historically",c:"#ef4444"},
{t:13,dur:2.8,icon:"\u{1F947}",title:"Gold Surges to $5,400",body:"Extreme flight to safety. Capital fleeing all risk assets into gold and treasuries.",detail:"Gold/BTC divergence at historic extreme",c:"#f59e0b"},
{t:16,dur:3.5,icon:"\u{20BF}",title:"BTC Capitulation: -31%",body:"Bitcoin drops from $70K to $48K. Macro headwind overwhelming. Crypto-equity correlation spikes to 0.9.",detail:"$2.4B liquidated in 48 hours",c:"#ef4444"},
{t:20,dur:2.8,icon:"\u{1F54A}\uFE0F",title:"Diplomatic Channels Open",body:"Back-channel negotiations through Oman. Both sides signal willingness to talk. Markets hold breath.",detail:"First de-escalation signal in 3 weeks",c:"#f59e0b"},
{t:23,dur:3,icon:"\u{2705}",title:"Ceasefire Agreement Signed",body:"Formal ceasefire. Iran agrees to keep Strait open. US pauses strikes on energy infrastructure.",detail:"Oil futures gap down 8% overnight",c:"#10b981"},
{t:27,dur:2.8,icon:"\u{1F6E2}\uFE0F",title:"Oil Flushes Below $95",body:"Supply fear premium unwinding rapidly. Tanker traffic resuming. Oil exits crisis zone.",detail:"Fastest oil drop since COVID recovery",c:"#10b981"},
{t:30,dur:2.8,icon:"\u{1F4C9}",title:"VIX Drops Below 20",body:"Fear gauge normalizes. Institutional hedges unwinding. Capital rotating back to risk assets.",detail:"Falling VIX = strongest risk-on signal in macro",c:"#10b981"},
{t:34,dur:2.8,icon:"\u{1F3E6}",title:"Fed Signals Flexibility",body:"Fed hints at rate flexibility now that oil-driven inflation pressure is easing. Yields dropping fast.",detail:"10Y yield: 4.85% \u2192 3.90%",c:"#10b981"},
{t:37,dur:2.8,icon:"\u{1F4B0}",title:"Liquidity Returns to Markets",body:"Lower yields + easing VIX = liquidity flowing back. Money rotating from gold into risk assets.",detail:"Gold drops $1,800 from peak — risk rotation",c:"#10b981"},
{t:40,dur:3,icon:"\u{20BF}",title:"BTC Reclaims $92,000",body:"All macro catalysts aligned: oil stable, VIX low, yields falling. Bitcoin surges past bull structure.",detail:"Oil-BTC correlation confirmed the entire move",c:"#10b981"},
{t:44,dur:3,icon:"\u{1F680}",title:"Price Discovery: $98,000",body:"BTC approaches all-time highs. Macro not fighting you — full tailwind environment activated.",detail:"From $48K capitulation to $98K. Macro drove it all.",c:"#10b981"},
];
const NAR=[{t:0,tx:"March 23 — Trump's Hormuz ultimatum expires"},{t:3,tx:"Iran refuses. Oil crosses $95 into STRESS"},{t:6,tx:"Strait of Hormuz closure threatened"},{t:10,tx:"Oil $118, VIX 38 — full crisis mode"},{t:13,tx:"Stagflation fears. Gold surges. BTC collapses"},{t:16,tx:"BTC -31%. Capitulation."},{t:20,tx:"Diplomatic channels reopen through Oman"},{t:23,tx:"Ceasefire agreement. De-escalation begins"},{t:27,tx:"Strait reopens. Oil flushing — relief signal"},{t:30,tx:"VIX normalizes. Risk-on ignites"},{t:34,tx:"Fed signals flexibility. Yields dropping"},{t:37,tx:"Liquidity returning. Gold-to-risk rotation"},{t:40,tx:"BTC breaks $90K. All catalysts green"},{t:44,tx:"Price discovery. Full macro tailwind"}];
function lerp(a,b,t){return a+(b-a)*t}
function getData(s){let p=TL[0],n=TL[0];for(let i=0;i<TL.length-1;i++){if(s>=TL[i].t&&s<TL[i+1].t){p=TL[i];n=TL[i+1];break}if(i===TL.length-2){p=n=TL[i+1]}}const r=n.t-p.t||1,f=Math.min(1,Math.max(0,(s-p.t)/r)),e=f<.5?2*f*f:1-Math.pow(-2*f+2,2)/2;return{oil:lerp(p.oil,n.oil,e),vix:lerp(p.vix,n.vix,e),btc:lerp(p.btc,n.btc,e),gold:lerp(p.gold,n.gold,e),y:lerp(p.y,n.y,e),bias:n.bias,bs:Math.round(lerp(p.bs,n.bs,e)),ph:n.ph,lb:n.lb}}
function getNar(s){let c=NAR[0];for(const n of NAR)if(s>=n.t)c=n;return c.tx}
function getCards(s){return EC.filter(c=>s>=c.t&&s<c.t+c.dur)}

function EvCard({card,elapsed}){
  const age=elapsed-card.t,fi=Math.min(1,age/.3),fo=Math.max(0,1-Math.max(0,age-(card.dur-.4))/.4),op=Math.min(fi,fo),sl=(1-fi)*20;
  return(<div style={{position:"fixed",left:"50%",top:"50%",transform:`translate(-50%,calc(-50% + ${sl}px))`,width:460,zIndex:200,opacity:op,
    background:`linear-gradient(135deg,${card.c}15,rgba(13,38,38,0.92) 35%)`,backdropFilter:"blur(30px)",WebkitBackdropFilter:"blur(30px)",
    border:`1px solid ${card.c}35`,borderRadius:18,padding:"18px 22px",boxShadow:`0 16px 60px rgba(0,0,0,0.6),0 0 40px ${card.c}10`}}>
    <div style={{position:"absolute",top:-1,left:-1,width:80,height:80,background:`radial-gradient(circle at top left,${card.c}22,transparent 70%)`,borderRadius:"18px 0 0 0",pointerEvents:"none"}}/>
    <div style={{position:"absolute",bottom:-1,right:-1,width:60,height:60,background:`radial-gradient(circle at bottom right,${card.c}12,transparent 70%)`,borderRadius:"0 0 18px 0",pointerEvents:"none"}}/>
    <div style={{display:"flex",alignItems:"flex-start",gap:14,position:"relative"}}>
      <div style={{fontSize:"1.8rem",width:44,height:44,display:"flex",alignItems:"center",justifyContent:"center",background:`${card.c}15`,borderRadius:12,flexShrink:0}}>{card.icon}</div>
      <div style={{flex:1}}>
        <div style={{fontSize:".75rem",fontWeight:800,color:card.c,marginBottom:3,letterSpacing:".03em"}}>CATALYST EVENT</div>
        <div style={{fontSize:"1.05rem",fontWeight:900,color:"#f0fdf4",marginBottom:5,lineHeight:1.25}}>{card.title}</div>
        <div style={{fontSize:".82rem",fontWeight:500,color:"#d1fae5",lineHeight:1.45,marginBottom:8}}>{card.body}</div>
        <div style={{fontSize:".72rem",fontWeight:700,color:card.c,padding:"4px 10px",background:`${card.c}10`,borderRadius:10,display:"inline-block",border:`1px solid ${card.c}20`}}>{card.detail}</div>
      </div>
    </div>
  </div>)
}

function MC({history,color,label,fmt,h=65}){
  const w=240,pad=4;if(history.length<2)return null;const vals=history.map(v=>v.val),mn=Math.min(...vals)*.98,mx=Math.max(...vals)*1.02,rng=mx-mn||1;
  const pts=vals.map((v,i)=>`${pad+(i/(vals.length-1))*(w-pad*2)},${h-pad-((v-mn)/rng)*(h-pad*2)}`).join(" ");
  const fill=`${pad},${h-pad} ${pts} ${w-pad},${h-pad}`,last=vals[vals.length-1],ly=h-pad-((last-mn)/rng)*(h-pad*2);
  const id=label.replace(/\s/g,"");
  return(<div><div style={{display:"flex",justifyContent:"space-between",alignItems:"baseline",marginBottom:2}}>
    <span style={{fontSize:".78rem",fontWeight:800,color:"#6ee7b7"}}>{label}</span>
    <span style={{fontSize:"1.05rem",fontWeight:900,color,transition:"color .5s"}}>{fmt(last)}</span></div>
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{width:"100%"}}><defs><linearGradient id={`f${id}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={color} stopOpacity=".22"/><stop offset="100%" stopColor={color} stopOpacity="0"/></linearGradient></defs>
    <polygon points={fill} fill={`url(#f${id})`}/><polyline points={pts} fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx={w-pad} cy={ly} r="4" fill={color} opacity=".7"><animate attributeName="r" values="4;6;4" dur="1.5s" repeatCount="indefinite"/></circle><circle cx={w-pad} cy={ly} r="2" fill="#fff"/></svg></div>)
}

function BG({score,mx,verdict,color}){
  const pct=Math.max(2,Math.min(98,(score/mx)*50+50));
  return(<div>
    <div style={{textAlign:"center",fontSize:"1.6rem",fontWeight:900,color,textShadow:`0 0 20px ${color}40`,transition:"color .5s"}}>{verdict}</div>
    <div style={{position:"relative",height:10,background:"rgba(10,26,26,.8)",borderRadius:5,margin:"6px 0",border:"1px solid rgba(16,185,129,.08)"}}>
      <div style={{position:"absolute",left:0,top:0,width:"30%",height:"100%",background:"rgba(239,68,68,.08)",borderRadius:"5px 0 0 5px"}}/>
      <div style={{position:"absolute",right:0,top:0,width:"30%",height:"100%",background:"rgba(16,185,129,.08)",borderRadius:"0 5px 5px 0"}}/>
      <div style={{position:"absolute",left:"50%",width:1,height:"100%",background:"rgba(16,185,129,.12)"}}/>
      <div style={{position:"absolute",left:`${pct}%`,top:-3,width:5,height:16,background:color,borderRadius:3,transform:"translateX(-2px)",boxShadow:`0 0 12px ${color}`,transition:"left .5s ease-out"}}/></div>
    <div style={{display:"flex",justifyContent:"space-between",fontSize:".6rem",fontWeight:700}}>
      <span style={{color:"#ef4444"}}>Risk-Off</span><span style={{color:"#6ee7b7"}}>Neutral</span><span style={{color:"#10b981"}}>Risk-On</span></div>
    <div style={{textAlign:"center",marginTop:3,fontSize:".85rem",fontWeight:900,color,transition:"color .5s"}}>Score: {score>0?"+":""}{score} / {mx}</div>
  </div>)
}

export default function Trailer(){
  const[el,setEl]=useState(-1),[pl,setPl]=useState(false),[hi,setHi]=useState({oil:[],vix:[],btc:[],gold:[],y:[]});
  const rf=useRef(null),total=50;
  useEffect(()=>{if(!pl)return;rf.current=setInterval(()=>{setEl(p=>{if(p>=total){setPl(false);clearInterval(rf.current);return total}return p+.1})},100);return()=>clearInterval(rf.current)},[pl]);
  useEffect(()=>{if(el<0)return;const d=getData(el);setHi(p=>({oil:[...p.oil.slice(-80),{t:el,val:d.oil}],vix:[...p.vix.slice(-80),{t:el,val:d.vix}],btc:[...p.btc.slice(-80),{t:el,val:d.btc}],gold:[...p.gold.slice(-80),{t:el,val:d.gold}],y:[...p.y.slice(-80),{t:el,val:d.y}]}))},[Math.floor(el*5)]);
  const d=el>=0?getData(Math.max(0,el)):getData(0),nar=el>=0?getNar(el):"",cards=el>=0?getCards(el):[],prog=Math.max(0,el/total)*100;
  const bc=d.bias.includes("RISK-ON")?"#10b981":d.bias==="NEUTRAL"?"#f59e0b":"#ef4444",pc=d.ph==="BEAR"?"#ef4444":d.ph==="BULL"?"#10b981":"#f59e0b";
  const gc="linear-gradient(135deg,rgba(16,185,129,.08),rgba(13,38,38,.65) 30%)";

  return(<div style={{minHeight:"100vh",background:"#0a1a1a",color:"#f0fdf4",fontFamily:"'Inter',system-ui,sans-serif",position:"relative",overflow:"hidden"}}>
    <div style={{position:"fixed",inset:0,pointerEvents:"none",background:`radial-gradient(ellipse 80% 50% at 20% 0%,${pc}06,transparent 70%),radial-gradient(ellipse 60% 40% at 80% 100%,rgba(6,182,212,.03),transparent 60%)`,transition:"background 2s"}}/>
    
    {/* Header */}
    <div style={{padding:"12px 24px",display:"flex",justifyContent:"space-between",alignItems:"center",position:"relative",zIndex:10}}>
      <div><span style={{fontSize:"1.4rem",fontWeight:900}}>Macro Catalyst</span><span style={{fontSize:".8rem",fontWeight:600,color:"#6ee7b7",marginLeft:10}}>Scenario Simulation</span></div>
      <div style={{fontSize:".72rem",fontWeight:800,color:pc,padding:"4px 14px",background:`${pc}12`,border:`1px solid ${pc}30`,borderRadius:20,transition:"all .5s"}}>● {d.ph==="END"?"COMPLETE":d.ph}</div>
    </div>
    
    {/* Progress */}
    <div style={{height:3,background:"rgba(16,185,129,.06)",position:"relative",zIndex:10}}>
      <div style={{height:"100%",width:`${prog}%`,background:"linear-gradient(90deg,#ef4444,#f59e0b 50%,#10b981)",transition:"width .1s linear",borderRadius:2}}/></div>
    
    {/* Narration */}
    <div style={{textAlign:"center",padding:"10px 24px 8px",position:"relative",zIndex:10,opacity:el>=0?1:0,transition:"opacity .5s"}}>
      <div style={{fontSize:".65rem",fontWeight:800,color:pc,letterSpacing:1.5,marginBottom:2}}>{d.lb}</div>
      <div style={{fontSize:"1.1rem",fontWeight:800,color:"#d1fae5"}}>{nar}</div>
    </div>
    
    {/* Main grid — wider sides, narrower center */}
    <div style={{display:"grid",gridTemplateColumns:"300px 1fr 280px",gap:10,padding:"0 24px",position:"relative",zIndex:10}}>
      
      {/* LEFT: Bias + Threats (bigger) */}
      <div style={{background:gc,backdropFilter:"blur(24px)",border:"1px solid rgba(16,185,129,.1)",borderRadius:16,padding:16,boxShadow:"0 8px 32px rgba(0,0,0,.4)"}}>
        <div style={{fontSize:".78rem",fontWeight:800,color:"#6ee7b7",marginBottom:8,display:"flex",alignItems:"center",gap:6}}>
          <div style={{width:6,height:6,borderRadius:"50%",background:bc,boxShadow:`0 0 10px ${bc}`}}/>Confluence Bias</div>
        <BG score={d.bs} mx={18} verdict={d.bias} color={bc}/>
        <div style={{marginTop:10,borderTop:"1px solid rgba(16,185,129,.08)",paddingTop:8}}>
          <div style={{fontSize:".65rem",fontWeight:800,color:"#6ee7b7",marginBottom:5}}>Threat Status</div>
          {[{k:"OIL",v:`$${d.oil.toFixed(0)}`,dn:d.oil>95,sf:d.oil<78},{k:"VIX",v:d.vix.toFixed(1),dn:d.vix>25,sf:d.vix<20},{k:"10Y",v:`${d.y.toFixed(2)}%`,dn:d.y>4.5,sf:d.y<3.8},{k:"GOLD",v:`$${Math.round(d.gold).toLocaleString()}`,dn:d.gold>4000,sf:d.gold<2800},{k:"BTC",v:`$${Math.round(d.btc).toLocaleString()}`,dn:d.btc<55000,sf:d.btc>72000}].map(i=>{
            const st=i.dn?"DANGER":i.sf?"SAFE":"CAUTION",sc=i.dn?"#ef4444":i.sf?"#10b981":"#f59e0b";
            return(<div key={i.k} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"3px 0",borderBottom:"1px solid rgba(16,185,129,.05)"}}>
              <span style={{fontSize:".72rem",fontWeight:800,color:"#6ee7b7"}}>{i.k}</span>
              <span style={{fontSize:".78rem",fontWeight:900,color:sc,transition:"color .5s"}}>{i.v}</span>
              <span style={{fontSize:".58rem",fontWeight:800,color:sc,padding:"2px 7px",background:`${sc}12`,borderRadius:10,border:`1px solid ${sc}22`}}>{st}</span>
            </div>)
          })}
        </div>
      </div>
      
      {/* CENTER: BTC chart (narrower) */}
      <div style={{background:"linear-gradient(135deg,rgba(16,185,129,.06),rgba(13,38,38,.6) 30%)",backdropFilter:"blur(24px)",border:"1px solid rgba(16,185,129,.1)",borderRadius:16,padding:14,boxShadow:"0 8px 32px rgba(0,0,0,.4)"}}>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:6}}>
          <div><span style={{fontSize:".78rem",fontWeight:800,color:"#6ee7b7"}}>Bitcoin</span>
          <span style={{fontSize:"1.8rem",fontWeight:900,color:d.btc>=70000?"#10b981":"#ef4444",marginLeft:10,transition:"color .5s"}}>${Math.round(d.btc).toLocaleString()}</span></div>
          <span style={{fontSize:".85rem",fontWeight:900,color:d.btc>=70000?"#10b981":"#ef4444",padding:"3px 12px",background:d.btc>=70000?"rgba(16,185,129,.12)":"rgba(239,68,68,.12)",borderRadius:20,transition:"all .5s"}}>{((d.btc-70000)/70000*100).toFixed(1)}%</span>
        </div>
        {hi.btc.length>1&&(()=>{const vals=hi.btc.map(v=>v.val),w=420,h=180,pad=5,mn=Math.min(...vals)*.97,mx=Math.max(...vals)*1.03,rng=mx-mn||1;
        const pts=vals.map((v,i)=>`${pad+(i/(vals.length-1))*(w-pad*2)},${h-pad-((v-mn)/rng)*(h-pad*2)}`).join(" ");
        const fill=`${pad},${h-pad} ${pts} ${w-pad},${h-pad}`,col=d.btc>=70000?"#10b981":"#ef4444",ly=h-pad-((vals[vals.length-1]-mn)/rng)*(h-pad*2);
        return(<svg width="100%" viewBox={`0 0 ${w} ${h}`}><defs><linearGradient id="bG" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={col} stopOpacity=".18"/><stop offset="100%" stopColor={col} stopOpacity="0"/></linearGradient></defs>
        <polygon points={fill} fill="url(#bG)"/><polyline points={pts} fill="none" stroke={col} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
        <circle cx={w-pad} cy={ly} r="5" fill={col} opacity=".6"><animate attributeName="r" values="5;8;5" dur="1.5s" repeatCount="indefinite"/></circle><circle cx={w-pad} cy={ly} r="2.5" fill="#fff"/></svg>)})()}
      </div>
      
      {/* RIGHT: Mini charts (bigger) */}
      <div style={{background:gc,backdropFilter:"blur(24px)",border:"1px solid rgba(16,185,129,.1)",borderRadius:16,padding:16,boxShadow:"0 8px 32px rgba(0,0,0,.4)",display:"flex",flexDirection:"column",gap:6}}>
        <MC history={hi.oil} color={d.oil>95?"#ef4444":d.oil>78?"#f59e0b":"#10b981"} label="WTI Crude Oil" fmt={v=>`$${v.toFixed(0)}`}/>
        <MC history={hi.vix} color={d.vix>25?"#ef4444":d.vix>20?"#f59e0b":"#10b981"} label="VIX Fear Index" fmt={v=>v.toFixed(1)}/>
        <MC history={hi.gold} color={d.gold>4000?"#ef4444":"#f59e0b"} label="Gold" fmt={v=>`$${Math.round(v).toLocaleString()}`}/>
        <MC history={hi.y} color={d.y>4.5?"#ef4444":d.y>3.8?"#f59e0b":"#10b981"} label="10Y Treasury" fmt={v=>`${v.toFixed(2)}%`}/>
      </div>
    </div>
    
    {/* Bottom ticker */}
    <div style={{margin:"10px 24px 0",background:"linear-gradient(135deg,rgba(16,185,129,.05),rgba(13,38,38,.4))",backdropFilter:"blur(16px)",border:"1px solid rgba(16,185,129,.06)",borderRadius:12,padding:"8px 16px",display:"flex",justifyContent:"space-between",alignItems:"center",position:"relative",zIndex:10}}>
      {[{k:"OIL",v:`$${d.oil.toFixed(0)}`,c:d.oil>95?"#ef4444":d.oil>78?"#f59e0b":"#10b981"},{k:"VIX",v:d.vix.toFixed(1),c:d.vix>25?"#ef4444":d.vix>20?"#f59e0b":"#10b981"},{k:"10Y",v:`${d.y.toFixed(2)}%`,c:d.y>4.5?"#ef4444":d.y>3.8?"#f59e0b":"#10b981"},{k:"GOLD",v:`$${Math.round(d.gold).toLocaleString()}`,c:d.gold>4000?"#ef4444":"#f59e0b"},{k:"S&P",v:"—",c:"#6ee7b7"},{k:"BTC",v:`$${Math.round(d.btc).toLocaleString()}`,c:d.btc>=70000?"#10b981":"#ef4444"}].map(i=>(<div key={i.k} style={{textAlign:"center"}}>
        <div style={{fontSize:".65rem",fontWeight:800,color:"#6ee7b7"}}>{i.k}</div>
        <div style={{fontSize:".95rem",fontWeight:900,color:i.c,transition:"color .5s"}}>{i.v}</div></div>))}
      <div style={{fontSize:".75rem",fontWeight:900,color:bc,padding:"4px 14px",background:`${bc}12`,border:`1px solid ${bc}25`,borderRadius:20,transition:"all .5s"}}>{d.bias}</div>
    </div>
    
    {/* EVENT CARDS — centered overlay */}
    {cards.map((c,i)=><EvCard key={`${c.t}-${i}`} card={c} elapsed={el}/>)}
    
    {/* Play overlay */}
    {!pl&&el<1&&(<div style={{position:"fixed",inset:0,display:"flex",alignItems:"center",justifyContent:"center",background:"rgba(10,26,26,.93)",backdropFilter:"blur(14px)",zIndex:300,cursor:"pointer"}} onClick={()=>{setPl(true);setEl(0);setHi({oil:[],vix:[],btc:[],gold:[],y:[]})}}>
      <div style={{textAlign:"center"}}>
        <div style={{fontSize:"2.4rem",fontWeight:900}}>Macro Catalyst</div>
        <div style={{fontSize:".95rem",fontWeight:600,color:"#6ee7b7",marginBottom:24}}>What if the worst happened — and then it didn't?</div>
        <div style={{width:72,height:72,borderRadius:"50%",background:"rgba(16,185,129,.12)",border:"2px solid rgba(16,185,129,.35)",display:"flex",alignItems:"center",justifyContent:"center",margin:"0 auto",transition:"all .3s"}}>
          <div style={{width:0,height:0,borderTop:"14px solid transparent",borderBottom:"14px solid transparent",borderLeft:"22px solid #10b981",marginLeft:4}}/></div>
        <div style={{fontSize:".7rem",color:"#6ee7b7",marginTop:12,opacity:.5}}>Click to play · 50 seconds</div>
      </div></div>)}
    
    {/* End screen */}
    {el>=total&&(<div style={{position:"fixed",inset:0,display:"flex",alignItems:"center",justifyContent:"center",background:"rgba(10,26,26,.94)",backdropFilter:"blur(14px)",zIndex:300}}>
      <div style={{textAlign:"center"}}>
        <div style={{fontSize:"2.2rem",fontWeight:900,color:"#10b981",textShadow:"0 0 30px rgba(16,185,129,.3)"}}>Macro Catalyst</div>
        <div style={{fontSize:".85rem",fontWeight:600,color:"#6ee7b7",marginBottom:6}}>Intelligence Terminal</div>
        <div style={{fontSize:".75rem",color:"#6ee7b7",opacity:.4,marginBottom:18}}>Real data · Real signals · No speculation</div>
        <div style={{padding:"7px 22px",background:"rgba(16,185,129,.12)",border:"1px solid rgba(16,185,129,.3)",borderRadius:20,cursor:"pointer",fontSize:".72rem",fontWeight:800,color:"#10b981",display:"inline-block"}} onClick={()=>{setEl(-1);setPl(false);setHi({oil:[],vix:[],btc:[],gold:[],y:[]})}}>Replay</div>
      </div></div>)}
  </div>)
}
