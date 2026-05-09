<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>anna CRM</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
html,body,#root{height:100%;font-family:'DM Sans',sans-serif;-webkit-font-smoothing:antialiased;}
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:#d4ccc7;border-radius:8px;}

/* Cards & hover */
.ch{transition:all .2s cubic-bezier(.4,0,.2,1)!important;}
.ch:hover{transform:translateY(-2px)!important;box-shadow:0 12px 32px rgba(162,106,37,.10),0 2px 8px rgba(0,0,0,.05)!important;}

/* Table rows */
.rh:hover td{background:#f8f5f2!important;}

/* Buttons */
.bp{transition:all .2s ease!important;letter-spacing:.3px;}
.bp:hover{background:#7a5018!important;transform:translateY(-1px);box-shadow:0 4px 12px rgba(162,106,37,.25)!important;}
.bg:hover{background:rgba(162,106,37,.06)!important;}

/* Rich text */
[contenteditable][data-ph]:empty:before{content:attr(data-ph);color:#a89f99;pointer-events:none;font-style:italic;}
.rich img{max-width:100%;border-radius:8px;}.rich a{color:#1e5fad;text-decoration:underline;}
.rich ul,.rich ol{padding-left:20px;margin:3px 0;}.rich p{margin:3px 0;line-height:1.7;}

/* Toolbar */
.tbe{width:26px;height:24px;border:0.5px solid #e0d9d4;border-radius:5px;cursor:pointer;background:none;color:#1a1410;display:inline-flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;transition:all .15s;}
.tbe:hover{background:#f0eeeb;border-color:#cfc5bd;}

/* Palette dots */
.pal:hover{transform:scale(1.35);transition:transform .15s;}

/* Inputs */
input[type=date],input[type=time]{color-scheme:light;}
select:focus,input:focus,textarea:focus{border-color:#a26a25!important;box-shadow:0 0 0 3px rgba(162,106,37,.08)!important;outline:none;}
input,select,textarea{font-family:'DM Sans',sans-serif;}

/* Nav button active indicator */
.nav-active{position:relative;}
.nav-active::after{content:'';position:absolute;bottom:-2px;left:50%;transform:translateX(-50%);width:16px;height:2px;background:#a26a25;border-radius:1px;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
// ════════════════════════════════════════════════════════════
// anna CRM – Supabase Edition
// ════════════════════════════════════════════════════════════

// ── KONFIGURATION ── Ersetze mit deinen Supabase-Zugangsdaten
const SUPABASE_URL  = 'https://fdlwjxyqivzrhmlxxrrq.supabase.co'
const SUPABASE_KEY  = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkbHdqeHlxaXZ6cmhtbHh4cnJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNTg1MjgsImV4cCI6MjA5MzgzNDUyOH0._Rhm03AMq0QEqvaR_TMQyVOV-SjTPdU51wJZl_wWQ9M'

// ── Supabase Client ──────────────────────────────────────────
const sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY, {
  auth: { persistSession: true, autoRefreshToken: true, storageKey: 'anna-crm' }
})

// ── React Hooks ──────────────────────────────────────────────
const { useState, useEffect, useRef } = React

// ── Theme ────────────────────────────────────────────────────
const C = {br:'#a26a25',brL:'#c4873a',brD:'#7a5018',wg:'#cfc5bd',be:'#ebe7e2',beL:'#f5f2ef',w:'#ffffff',s:'#1a1410',tL:'#8a7d74',bo:'#ddd5cd',ok:'#3d7a55',er:'#b5472a',okBg:'#eaf4ee',brBg:'#fff3e6'}
const CS = ['Strategiegespräch','Angebot unterbreitet','Follow up','Verloren']
const BS = ['Onboarding','1:1 Clients','Gruppenbegleitung','Online-Kurs']
const STAGE_C = { Verloren: C.er }
const ACTS = [{id:'call',l:'Anruf',e:'📞'},{id:'meeting',l:'Meeting',e:'👥'},{id:'followup',l:'Follow-up',e:'🔄'},{id:'task',l:'Aufgabe',e:'✅'},{id:'email',l:'E-Mail',e:'📧'},{id:'closing',l:'Closing',e:'🤝'},{id:'onboarding',l:'Onboarding',e:'🚀'},{id:'offboarding',l:'Offboarding',e:'📋'}]
const PAL = [{id:'braun',bg:'#fff3e6',tx:'#a26a25',bo:'#e8c59a'},{id:'gruen',bg:'#eaf4ee',tx:'#2d6e47',bo:'#8ecfa6'},{id:'blau',bg:'#e6effc',tx:'#1e5fad',bo:'#88b4ee'},{id:'lila',bg:'#f2eefb',tx:'#6d34c8',bo:'#bea8ee'},{id:'rosa',bg:'#fceef4',tx:'#b53472',bo:'#eeaacc'},{id:'tuerkis',bg:'#e4f5f3',tx:'#0f7268',bo:'#6ecfc8'},{id:'orange',bg:'#fff4e4',tx:'#c45710',bo:'#f5b470'},{id:'grau',bg:'#f0eeeb',tx:'#6a6460',bo:'#bdb8b4'}]
const DP = [{id:'cp1',name:'Passives Einkommen Kurs',price:1997,color:'braun'},{id:'cp2',name:'1:1 Coaching (6 Monate)',price:10000,color:'lila'},{id:'cp3',name:'Done-for-You Service',price:4797,color:'tuerkis'},{id:'cp4',name:'ELARA AI System',price:199,color:'blau'}]
const DW = [{id:'cw1',name:'6K Passives Einkommen',color:'gruen'},{id:'cw2',name:'KI für Fotografen',color:'blau'},{id:'cw3',name:'Ads für Fotografen',color:'orange'}]

const gc  = (id) => PAL.find(c => c.id === id) || PAL[0]
const uid = () => crypto.randomUUID()
const today = () => new Date().toLocaleDateString('de-DE')
const toDE  = s => { if (!s) return ''; const [y,m,d] = s.split('-'); return `${d}.${m}.${y}` }
const todayISO = () => new Date().toISOString().split('T')[0]
const IS = { flex:1, padding:'7px 10px', border:`1px solid ${C.bo}`, borderRadius:8, fontSize:12.5, background:C.w, outline:'none', color:C.s }

function isExp(s) {
  if (!s) return false
  try { const d = s.includes('-') ? new Date(s) : new Date(s.split('.').reverse().join('-')); return !isNaN(d) && d < new Date() } catch { return false }
}
function daysLeft(dateDE) {
  if (!dateDE) return null
  try {
    const parts = dateDE.split('.')
    if (parts.length !== 3) return null
    const d = new Date(+parts[2], +parts[1]-1, +parts[0])
    const t = new Date(); t.setHours(0,0,0,0)
    return Math.ceil((d - t) / (1000*60*60*24))
  } catch { return null }
}
function isUrgent(c) { const d = daysLeft(c.offboardingDate); return d !== null && d >= 0 && d <= 7 }
function hasOvd(c) { return (c.timeline||[]).some(e => e.type==='activity' && !e.completed && isExp(e.date)) }
function hasOff(c) { return c.offboardingDate && isExp(c.offboardingDate) }
function stripH(h) { return (h||'').replace(/<[^>]+>/g,'').trim() }

// ── DB Konvertierung ─────────────────────────────────────────
const fromDB = r => ({
  id: r.id, name: r.name||'', email: r.email||'', phone: r.phone||'',
  website: r.website||'', spezialisierung: r.spezialisierung||'',
  driveUrl: r.drive_url||'', gesprachsScore: r.gesprachs_score||null,
  kundenZiele: r.kunden_ziele||'',
  tags: r.tags||[],
  pipelines: r.pipelines||['closing'],
  closingStage: r.closing_stage||'Strategiegespräch',
  begleitungStage: r.begleitung_stage||null,
  offboardingDate: r.offboarding_date||null,
  labels: r.labels||[], products: r.products||[], webinars: r.webinars||[], timeline: r.timeline||[],
  createdAt: r.created_at ? new Date(r.created_at).toLocaleDateString('de-DE') : today(),
})
const toDB = c => ({
  id: c.id, name: c.name, email: c.email, phone: c.phone,
  website: c.website, spezialisierung: c.spezialisierung,
  drive_url: c.driveUrl||'', gesprachs_score: c.gesprachsScore||null,
  kunden_ziele: c.kundenZiele||'',
  tags: c.tags||[],
  pipelines: c.pipelines, closing_stage: c.closingStage,
  begleitung_stage: c.begleitungStage, offboarding_date: c.offboardingDate,
  labels: c.labels, products: c.products, webinars: c.webinars, timeline: c.timeline,
})

// ── DB Operationen ───────────────────────────────────────────
const DB = {
  async contacts() {
    const { data, error } = await sb.from('contacts').select('*').order('created_at', { ascending: false })
    if (error) throw error
    return (data||[]).map(fromDB)
  },
  async upsert(c) {
    const { data, error } = await sb.from('contacts').upsert(toDB(c)).select()
    if (error) throw error
    return data?.[0] ? fromDB(data[0]) : c
  },
  async del(id) { await sb.from('contacts').delete().eq('id', id) },
  async getSetting(key, def) {
    const { data } = await sb.from('settings').select('value').eq('key', key).single()
    return data?.value ?? def
  },
  async saveSetting(key, value) { await sb.from('settings').upsert({ key, value }) },
}

// ── Root (Auth Gate) ─────────────────────────────────────────
function Root() {
  const [session, setSession] = useState(undefined)
  useEffect(() => {
    sb.auth.getSession().then(({ data: { session } }) => setSession(session))
    const { data: { subscription } } = sb.auth.onAuthStateChange((_, s) => setSession(s))
    return () => subscription.unsubscribe()
  }, [])
  if (session === undefined) return <Loader />
  if (!session) return <LoginScreen />
  return <App session={session} />
}

// ── Login Screen ─────────────────────────────────────────────
function LoginScreen() {
  const [email, setEmail] = useState('')
  const [pass, setPass]   = useState('')
  const [err, setErr]     = useState('')
  const [busy, setBusy]   = useState(false)
  const login = async () => {
    if (!email||!pass) return setErr('Bitte E-Mail und Passwort eingeben')
    setBusy(true); setErr('')
    const { error } = await sb.auth.signInWithPassword({ email, password: pass })
    setBusy(false)
    if (error) setErr(error.message.includes('Invalid') ? 'Falsche E-Mail oder Passwort' : error.message)
  }
  return (
    <div style={{height:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:`linear-gradient(135deg, #f5f0eb 0%, #ede6de 100%)`}}>
      <div style={{background:C.w,borderRadius:20,padding:44,width:380,boxShadow:'0 24px 80px rgba(162,106,37,.12), 0 4px 24px rgba(0,0,0,.06)'}}>
        <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:32,fontWeight:600,color:C.br,textAlign:'center',marginBottom:4,letterSpacing:'.5px'}}>anna CRM</div>
        <div style={{fontSize:12,color:C.tL,textAlign:'center',marginBottom:32,letterSpacing:'.3px'}}>Bitte einloggen</div>
        <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="E-Mail"
          onKeyDown={e=>e.key==='Enter'&&login()} style={{...IS,display:'block',width:'100%',padding:'12px 16px',marginBottom:12,fontSize:14,borderRadius:10,border:`0.5px solid ${C.bo}`}}/>
        <input type="password" value={pass} onChange={e=>setPass(e.target.value)} placeholder="Passwort"
          onKeyDown={e=>e.key==='Enter'&&login()} style={{...IS,display:'block',width:'100%',padding:'12px 16px',marginBottom:10,fontSize:14,borderRadius:10,border:`0.5px solid ${C.bo}`}}/>
        {err && <div style={{color:C.er,fontSize:12,marginBottom:10,textAlign:'center'}}>{err}</div>}
        <button onClick={login} disabled={busy} className="bp"
          style={{width:'100%',padding:'13px',background:busy?C.wg:C.br,color:C.w,border:'none',borderRadius:10,cursor:busy?'wait':'pointer',fontSize:14,fontWeight:500,letterSpacing:'.4px',boxShadow:`0 4px 16px rgba(162,106,37,.25)`,transition:'all .2s'}}>
          {busy ? 'Wird geladen …' : 'Einloggen'}
        </button>
      </div>
    </div>
  )
}

// ── App ───────────────────────────────────────────────────────
function App({ session }) {
  const [contacts, setContacts] = useState([])
  const [prodCat, setProdCat]   = useState([])
  const [webCat, setWebCat]     = useState([])
  const [view, setView]         = useState('pipeline')
  const [pipeTab, setPipeTab]   = useState('closing')
  const [sel, setSel]           = useState(null)
  const [showAdd, setShowAdd]   = useState(false)
  const [showTidy, setShowTidy] = useState(false)
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    ;(async () => {
      try {
        const [c, p, w] = await Promise.all([DB.contacts(), DB.getSetting('product_catalog', DP), DB.getSetting('webinar_catalog', DW)])
        setContacts(c); setProdCat(p); setWebCat(w)
      } catch (e) { console.error(e) }
      setLoading(false)
    })()
    // Real-time sync – alle Teammitglieder sehen Änderungen sofort
    const ch = sb.channel('crm').on('postgres_changes', { event:'*', schema:'public', table:'contacts' }, (pl) => {
      if (pl.eventType === 'INSERT') setContacts(p => [fromDB(pl.new), ...p])
      if (pl.eventType === 'UPDATE') { const u = fromDB(pl.new); setContacts(p => p.map(c => c.id===u.id ? u : c)); setSel(p => p?.id===u.id ? u : p) }
      if (pl.eventType === 'DELETE') { setContacts(p => p.filter(c => c.id!==pl.old.id)); setSel(p => p?.id===pl.old.id ? null : p) }
    }).subscribe()
    return () => sb.removeChannel(ch)
  }, [])

  const updC = async (c) => { try { await DB.upsert(c) } catch (e) { console.error(e); setContacts(p => p.map(x => x.id===c.id ? c : x)); setSel(c) } }
  const addC = async (d) => { const nc = { ...d, id: uid(), pipelines:['closing'], closingStage:'Strategiegespräch', begleitungStage:null, offboardingDate:null, labels:[], products:[], webinars:[], timeline:[], website:'', spezialisierung:'' }; try { await DB.upsert(nc) } catch(e){console.error(e)} }
  const delC = async (id) => { setSel(null); try { await DB.del(id) } catch(e){console.error(e)} }
  const saveP = async (items) => { setProdCat(items); try { await DB.saveSetting('product_catalog', items) } catch(e){console.error(e)} }
  const saveW = async (items) => { setWebCat(items); try { await DB.saveSetting('webinar_catalog', items) } catch(e){console.error(e)} }

  const fromTidy = async (d) => {
    const tl = { id:uid(), type:'note', html:`<p>📅 <strong>TidyCal:</strong> ${d.note||'Strategiegespräch gebucht'}</p>`, date:today(), ts:new Date().toISOString() }
    const ex = contacts.find(c => c.email?.toLowerCase() === d.email?.toLowerCase())
    if (ex) await updC({ ...ex, pipelines:[...new Set([...ex.pipelines,'closing'])], closingStage:'Strategiegespräch', timeline:[...(ex.timeline||[]),tl] })
    else await addC({ name:d.name, email:d.email, phone:d.phone||'', timeline:[tl] })
    setPipeTab('closing'); setView('pipeline'); setShowTidy(false)
  }

  const live = sel ? contacts.find(c => c.id === sel.id) : null
  if (loading) return <Loader />

  return (
    <div style={{height:'100vh',display:'flex',flexDirection:'column',background:C.beL,fontFamily:"'DM Sans',sans-serif",color:C.s,overflow:'hidden'}}>
      <header style={{background:C.w,borderBottom:'none',boxShadow:'0 1px 0 rgba(0,0,0,.06), 0 2px 12px rgba(0,0,0,.04)',padding:'0 28px',display:'flex',alignItems:'center',gap:20,height:56,flexShrink:0,zIndex:10}}>
        <span style={{fontFamily:"'Cormorant Garamond',serif",fontSize:22,fontWeight:600,color:C.br,letterSpacing:'.5px'}}>anna CRM</span>
        <div style={{width:'1px',height:20,background:C.bo,opacity:.6}}/>
        <nav style={{display:'flex',gap:1}}>
          {[['dashboard','Dashboard'],['pipeline','Pipelines'],['contacts','Kontakte'],['catalog','Katalog']].map(([v,l]) => (
            <button key={v} className="bg" onClick={() => setView(v)}
              style={{padding:'6px 14px',border:'none',borderRadius:8,cursor:'pointer',fontSize:12.5,fontWeight:view===v?500:400,
                background:view===v?'rgba(162,106,37,.07)':'transparent',
                color:view===v?C.br:C.tL,transition:'all .15s',position:'relative',
                boxShadow:view===v?`inset 0 -2px 0 ${C.br}`:'none'}}>
              {l}
            </button>
          ))}
        </nav>
        <div style={{marginLeft:'auto',display:'flex',gap:8,alignItems:'center'}}>
          <span style={{fontSize:11,color:C.tL,maxWidth:160,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap',letterSpacing:'.1px'}}>{session.user.email}</span>
          <div style={{width:'1px',height:16,background:C.bo,opacity:.6}}/>
          <button onClick={() => setShowTidy(true)}
            style={{padding:'6px 14px',background:'transparent',color:C.br,border:`0.5px solid rgba(162,106,37,.3)`,borderRadius:8,cursor:'pointer',fontSize:12,fontWeight:500,letterSpacing:'.2px',transition:'all .15s'}}
            onMouseEnter={e=>{e.target.style.background=C.brBg}} onMouseLeave={e=>{e.target.style.background='transparent'}}>
            TidyCal
          </button>
          <button onClick={() => setShowAdd(true)} className="bp"
            style={{padding:'7px 18px',background:C.br,color:C.w,border:'none',borderRadius:8,cursor:'pointer',fontSize:12,fontWeight:500,letterSpacing:'.3px',boxShadow:'0 2px 8px rgba(162,106,37,.2)'}}>
            + Kontakt
          </button>
          <button onClick={() => sb.auth.signOut()} title="Ausloggen"
            style={{padding:'6px 10px',background:'none',border:`0.5px solid ${C.bo}`,borderRadius:8,cursor:'pointer',fontSize:13,color:C.tL,transition:'all .15s'}}
            onMouseEnter={e=>{e.target.style.borderColor=C.br;e.target.style.color=C.br}} onMouseLeave={e=>{e.target.style.borderColor=C.bo;e.target.style.color=C.tL}}>
            ↩
          </button>
        </div>
      </header>
      <div style={{flex:1,overflow:'hidden',display:'flex'}}>
        {view==='dashboard' && <DashboardView contacts={contacts} prodCat={prodCat} session={session} onSelectContact={(c)=>{setSel(c);setView('pipeline')}}/>}
        {view==='pipeline' && <PipelineView contacts={contacts} tab={pipeTab} setTab={setPipeTab} onSelect={setSel} selId={live?.id} prodCat={prodCat} webCat={webCat}/>}
        {view==='contacts' && <ContactsView contacts={contacts} onSelect={setSel} selId={live?.id} prodCat={prodCat} webCat={webCat} onImport={async (rows)=>{for(const r of rows){try{await DB.upsert(r)}catch(e){console.error(e)}}}}/>}
        {view==='catalog'  && <CatalogView prodCat={prodCat} webCat={webCat} onSaveP={saveP} onSaveW={saveW}/>}
        {live && <Akte contact={live} prodCat={prodCat} webCat={webCat} onUpdate={updC} onDelete={delC} onClose={() => setSel(null)} userEmail={session.user.email}/>}
      </div>
      {showAdd  && <AddModal onAdd={addC} onClose={() => setShowAdd(false)}/>}
      {showTidy && <TidyModal onAdd={fromTidy} onClose={() => setShowTidy(false)}/>}
    </div>
  )
}

// ── Dashboard ─────────────────────────────────────────────────
function DashboardView({ contacts, prodCat, session, onSelectContact }) {
  const userName = session.user.email.split('@')[0]
  const totalRev = contacts.reduce((s,c)=>s+c.products.reduce((ps,p)=>ps+p.price,0),0)

  // Monthly revenue last 6 months
  const now = new Date()
  const months = Array.from({length:6},(_,i)=>{
    const d=new Date(now.getFullYear(),now.getMonth()-5+i,1)
    return {label:d.toLocaleDateString('de-DE',{month:'short'}),year:d.getFullYear(),month:d.getMonth(),revenue:0}
  })
  contacts.forEach(c=>c.products.forEach(p=>{
    if(!p.date)return
    const pts=p.date.split('.')
    if(pts.length!==3)return
    const m=months.find(m=>m.year===+pts[2]&&m.month===+pts[1]-1)
    if(m)m.revenue+=p.price
  }))
  const maxRev = Math.max(...months.map(m=>m.revenue),1)

  // My open activities (all types)
  const myTasks = contacts.flatMap(c=>
    (c.timeline||[])
      .filter(e=>e.type==='activity'&&!e.completed&&(!e.assignee||e.assignee===userName||e.assignee===session.user.email))
      .map(e=>({...e,contactId:c.id,contactName:c.name}))
  ).sort((a,b)=>(a.date||'').localeCompare(b.date||''))

  // All open activities
  const allTasks = contacts.flatMap(c=>
    (c.timeline||[])
      .filter(e=>e.type==='activity'&&!e.completed)
      .map(e=>({...e,contactId:c.id,contactName:c.name}))
  ).sort((a,b)=>(a.date||'').localeCompare(b.date||''))

  // Upcoming offboardings
  const upcoming = contacts
    .filter(c=>c.offboardingDate&&!hasOff(c))
    .map(c=>({...c,days:daysLeft(c.offboardingDate)}))
    .filter(c=>c.days!==null&&c.days<=30&&c.days>=0)
    .sort((a,b)=>a.days-b.days)

  const openTasksForMe = myTasks.length
  const openTasksAll = allTasks.length

  return (
    <div style={{flex:1,overflowY:'auto',padding:24,display:'flex',flexDirection:'column',gap:20}}>
      {/* Greeting */}
      <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:24,fontWeight:600,color:C.s}}>
        Hallo, {userName}! <span style={{fontSize:16,color:C.tL,fontFamily:"'DM Sans',sans-serif",fontWeight:400}}>— {new Date().toLocaleDateString('de-DE',{weekday:'long',day:'numeric',month:'long'})}</span>
      </div>

      {/* Stats */}
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:12}}>
        {[
          {l:'Kontakte',v:contacts.length,c:C.br},
          {l:'In Closing',v:contacts.filter(c=>c.pipelines.includes('closing')).length,c:'#2563ad'},
          {l:'In Begleitung',v:contacts.filter(c=>c.pipelines.includes('begleitung')).length,c:C.ok},
          {l:'Offene Aufgaben',v:openTasksAll,c:openTasksAll>0?'#d97706':C.tL},
          {l:'Gesamtumsatz',v:totalRev.toLocaleString('de-DE')+' €',c:C.ok},
        ].map(s=>(
          <div key={s.l} style={{background:C.w,border:`0.5px solid rgba(0,0,0,.07)`,borderRadius:14,padding:'16px 20px',boxShadow:'0 2px 12px rgba(0,0,0,.04)'}}>
            <div style={{fontSize:10,textTransform:'uppercase',letterSpacing:1,color:C.tL,marginBottom:6}}>{s.l}</div>
            <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:28,fontWeight:600,color:s.c,lineHeight:1}}>{s.v}</div>
          </div>
        ))}
      </div>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:20}}>
        {/* Monthly Revenue Chart */}
        <div style={{background:C.w,border:`1px solid ${C.bo}`,borderRadius:12,padding:'18px 20px'}}>
          <div style={{fontSize:12,fontWeight:500,color:C.s,marginBottom:16,textTransform:'uppercase',letterSpacing:.5}}>Umsatz nach Monat</div>
          <div style={{display:'flex',gap:8,alignItems:'flex-end',height:120}}>
            {months.map(m=>(
              <div key={m.label} style={{flex:1,display:'flex',flexDirection:'column',alignItems:'center',gap:4}}>
                <div style={{fontSize:9.5,color:C.tL,fontWeight:500}}>{m.revenue>0?Math.round(m.revenue/1000)+'k':''}</div>
                <div style={{width:'100%',background:m.revenue>0?C.br:C.be,borderRadius:'4px 4px 0 0',
                  height:m.revenue>0?Math.max(8,Math.round((m.revenue/maxRev)*90))+'px':'4px',
                  transition:'height .3s'}}/>
                <div style={{fontSize:9.5,color:C.tL}}>{m.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* My Tasks */}
        <div style={{background:C.w,border:`1px solid ${C.bo}`,borderRadius:12,padding:'18px 20px',display:'flex',flexDirection:'column',gap:10}}>
          <div style={{fontSize:12,fontWeight:500,color:C.s,textTransform:'uppercase',letterSpacing:.5}}>
            Meine Aufgaben {openTasksForMe>0&&<span style={{background:'#2563ad',color:C.w,padding:'1px 8px',borderRadius:8,fontSize:10,marginLeft:6}}>{openTasksForMe}</span>}
          </div>
          <div style={{flex:1,overflowY:'auto',display:'flex',flexDirection:'column',gap:6}}>
            {myTasks.length===0 && <div style={{fontSize:13,color:C.tL,padding:'8px 0'}}>Keine offenen Aufgaben</div>}
            {myTasks.map(t=>(
              <div key={t.id} onClick={()=>onSelectContact(contacts.find(c=>c.id===t.contactId))}
                style={{display:'flex',gap:10,alignItems:'center',padding:'8px 10px',background:C.beL,borderRadius:7,cursor:'pointer'}}
                onMouseEnter={e=>e.currentTarget.style.background=C.be}
                onMouseLeave={e=>e.currentTarget.style.background=C.beL}>
                <div style={{flex:1,minWidth:0}}>
                  <div style={{fontSize:12.5,fontWeight:500,color:C.s,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{t.title}</div>
                  <div style={{fontSize:11,color:C.tL,marginTop:1}}>{t.contactName} · {t.date}</div>
                </div>
                {isExp(t.date)&&<span style={{fontSize:9,background:C.er,color:C.w,padding:'1px 6px',borderRadius:3,fontWeight:700,flexShrink:0}}>ÜBERFÄLLIG</span>}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming offboardings */}
      {upcoming.length>0 && (
        <div style={{background:C.w,border:`1px solid ${C.bo}`,borderRadius:12,padding:'18px 20px'}}>
          <div style={{fontSize:12,fontWeight:500,color:C.s,marginBottom:12,textTransform:'uppercase',letterSpacing:.5}}>Offboarding in den nächsten 30 Tagen</div>
          <div style={{display:'flex',gap:10,flexWrap:'wrap'}}>
            {upcoming.map(c=>(
              <div key={c.id} onClick={()=>onSelectContact(c)}
                style={{display:'flex',alignItems:'center',gap:10,padding:'8px 14px',background:c.days<=7?'#fff5f5':C.beL,border:`1px solid ${c.days<=7?C.er:C.bo}`,borderRadius:8,cursor:'pointer'}}>
                <div>
                  <div style={{fontSize:13,fontWeight:500}}>{c.name}</div>
                  <div style={{fontSize:11,color:C.tL}}>{c.offboardingDate}</div>
                </div>
                <span style={{fontSize:13,fontWeight:700,color:c.days<=7?C.er:'#d97706',marginLeft:8}}>{c.days}T</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// ── Pipeline View ─────────────────────────────────────────────
function PipelineView({ contacts, tab, setTab, onSelect, selId, prodCat, webCat }) {
  const stages = tab==='closing' ? CS : BS
  const key    = tab==='closing' ? 'closingStage' : 'begleitungStage'
  const inPipe = contacts.filter(c => c.pipelines.includes(tab))
  return (
    <div style={{flex:1,overflow:'hidden',display:'flex',flexDirection:'column'}}>
      <div style={{padding:'20px 24px 0',display:'flex',gap:6}}>
        {[['closing','Closing'],['begleitung','Begleitung']].map(([t,l]) => {
          const n = contacts.filter(c => c.pipelines.includes(t)).length, a = tab===t
          return <button key={t} onClick={() => setTab(t)}
            style={{padding:'8px 22px',border:`0.5px solid ${a?C.br:C.bo}`,borderBottom:a?`0.5px solid ${C.w}`:`0.5px solid ${C.bo}`,
              borderRadius:'10px 10px 0 0',cursor:'pointer',background:a?C.w:'transparent',
              color:a?C.br:C.tL,fontSize:13,fontWeight:a?500:400,letterSpacing:'.2px',transition:'all .2s'}}>
            {l}<span style={{marginLeft:8,background:a?C.be:'rgba(0,0,0,.04)',color:C.tL,padding:'2px 9px',borderRadius:20,fontSize:10.5}}>{n}</span>
          </button>
        })}
      </div>
      <div style={{flex:1,overflowX:'auto',overflowY:'hidden',padding:'0 24px 24px',background:C.w,borderTop:`0.5px solid ${C.bo}`}}>
        <div style={{display:'flex',gap:16,height:'100%',paddingTop:20,minWidth:'max-content'}}>
          {stages.map(stage => {
            const cards = inPipe.filter(c => c[key] === stage), sc = STAGE_C[stage]
            return (
              <div key={stage} style={{width:240,flexShrink:0,display:'flex',flexDirection:'column',gap:8}}>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'0 2px 10px',borderBottom:`1.5px solid ${sc||'rgba(0,0,0,.08)'}`}}>
                  <span style={{fontSize:10.5,fontWeight:500,letterSpacing:1.2,textTransform:'uppercase',color:sc||C.tL}}>{stage}</span>
                  <span style={{background:C.beL,color:C.tL,padding:'2px 9px',borderRadius:20,fontSize:10.5,fontWeight:500}}>{cards.length}</span>
                </div>
                <div style={{flex:1,overflowY:'auto',display:'flex',flexDirection:'column',gap:8,paddingBottom:8}}>
                  {[...cards].sort((a,b) => {
                    const aU = hasOff(a)||isUrgent(a); const bU = hasOff(b)||isUrgent(b)
                    if(aU&&!bU)return -1; if(!aU&&bU)return 1; return 0
                  }).map(c => <KCard key={c.id} contact={c} onSelect={onSelect} isSel={c.id===selId} prodCat={prodCat} webCat={webCat}/>)}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

function KCard({ contact, onSelect, isSel, prodCat, webCat }) {
  const off = hasOff(contact), urgent = isUrgent(contact), ovd = hasOvd(contact)
  const days = daysLeft(contact.offboardingDate)
  const bc = off||urgent ? C.er : ovd ? '#d97706' : isSel ? C.br : C.bo
  const bg = off||urgent ? '#fff5f5' : ovd ? '#fffbf0' : C.beL
  const rev = contact.products.reduce((s,p) => s+p.price, 0)
  const openTasks = (contact.timeline||[]).filter(e=>e.type==='activity'&&e.actType==='task'&&!e.completed).length
  const notes = (contact.timeline||[]).filter(e => e.type==='note').length
  return (
    <div className="ch" onClick={() => onSelect(contact)}
      style={{background:isSel?C.w:C.w,border:`0.5px solid ${bc}`,borderRadius:12,padding:'13px 15px',cursor:'pointer',
        boxShadow:isSel?`0 0 0 2px ${C.br}30, 0 4px 16px rgba(162,106,37,.08)`:off||urgent?`0 0 0 1.5px ${C.er}`:ovd?`0 0 0 1.5px #d97706`:'0 1px 4px rgba(0,0,0,.04)',
        transition:'all .2s cubic-bezier(.4,0,.2,1)'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:5}}>
        <div style={{flex:1,minWidth:0,paddingRight:6}}>
          <div style={{fontWeight:500,fontSize:13,lineHeight:1.3}}>{contact.name}</div>
          {contact.gesprachsScore && <div style={{display:'flex',gap:1,marginTop:2}}>
            {[1,2,3,4,5].map(n=><span key={n} style={{fontSize:9,color:n<=contact.gesprachsScore?'#f59e0b':'#d1c9c0'}}>★</span>)}
          </div>}
        </div>
        <div style={{display:'flex',gap:3,flexShrink:0,alignItems:'center',flexWrap:'wrap',justifyContent:'flex-end'}}>
          {off && <span style={{fontSize:9,background:C.er,color:C.w,padding:'1px 5px',borderRadius:3,fontWeight:700}}>OFFBOARD</span>}
          {!off && urgent && days !== null && <span style={{fontSize:9.5,background:C.er,color:C.w,padding:'1px 6px',borderRadius:3,fontWeight:700}}>{days===0?'Heute!':days+'T'}</span>}
          {!off && !urgent && days !== null && days > 0 && <span style={{fontSize:9.5,background:days<=14?'#d97706':C.ok,color:C.w,padding:'1px 6px',borderRadius:3,fontWeight:600}}>{days}T</span>}
          {openTasks>0 && <span style={{fontSize:9,background:'#2563ad',color:C.w,padding:'1px 6px',borderRadius:3,fontWeight:600}}>{openTasks} To-do</span>}
          {contact.pipelines.length>1 && <span style={{fontSize:9,color:C.br,background:C.brBg,padding:'1px 5px',borderRadius:3}}>beide</span>}
        </div>
      </div>
      {contact.labels.length>0 && <div style={{display:'flex',gap:3,marginBottom:5,flexWrap:'wrap'}}>{contact.labels.slice(0,3).map(l => <STag key={l} text={l}/>)}</div>}
      <div style={{display:'flex',flexWrap:'wrap',gap:3,marginBottom:3}}>
        {contact.products.map(p => { const col=gc(prodCat.find(x=>x.id===p.catalogId)?.color); return <span key={p.id} style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'1px 5px',borderRadius:3,fontSize:9.5,fontWeight:500}}>{p.name}</span> })}
        {contact.webinars.map(w => { const col=gc(webCat.find(x=>x.id===w.catalogId)?.color||'blau'); return <span key={w.id} style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'1px 5px',borderRadius:3,fontSize:9.5}}>{w.name}</span> })}
      </div>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginTop:4,fontSize:11,color:C.tL}}>
        <span>{notes>0?`${notes} Notiz${notes>1?'en':''}`:''}</span>
        {rev>0 && <span style={{fontWeight:700,color:C.ok}}>{rev.toLocaleString('de-DE')} €</span>}
      </div>
    </div>
  )
}

// ── Contacts View ─────────────────────────────────────────────
function ContactsView({ contacts, onSelect, selId, prodCat, webCat, onImport }) {
  const [q, setQ] = useState('')
  const [filterProds, setFilterProds] = useState([])
  const [filterWebs,  setFilterWebs]  = useState([])
  const [filterLabels,setFilterLabels]= useState([])
  const [openDrop, setOpenDrop] = useState(null)
  const [dropSearch, setDropSearch] = useState('')
  const [showImport, setShowImport] = useState(false)
  const [importRows, setImportRows] = useState([])
  const [importing, setImporting] = useState(false)
  const [importDone, setImportDone] = useState(null)
  const fileRef = React.useRef()

  const parseCSV = (text) => {
    // BOM entfernen
    const clean = text.replace(/^\uFEFF/, '').replace(/\r\n/g, '\n').replace(/\r/g, '\n')
    const lines = clean.split('\n').filter(l => l.trim())
    if (lines.length < 2) return []

    // Header parsen
    const parseRow = (line) => {
      const cols = []; let cur = '', inQ = false
      for (let i = 0; i < line.length; i++) {
        const c = line[i]
        if (c === '"') { inQ = !inQ }
        else if (c === ',' && !inQ) { cols.push(cur.trim()); cur = '' }
        else cur += c
      }
      cols.push(cur.trim())
      return cols
    }

    const headers = parseRow(lines[0])
    const rows = []
    for (let i = 1; i < lines.length; i++) {
      const cols = parseRow(lines[i])
      const row = {}
      headers.forEach((h, idx) => { row[h] = (cols[idx] || '').trim() })
      rows.push(row)
    }
    return rows.filter(r => r['E-Mail'] || r['email'] || r['Email'])
  }

  const handleFile = (e) => {
    const file = e.target.files[0]; if(!file) return
    const reader = new FileReader()
    reader.onload = (ev) => {
      const rows = parseCSV(ev.target.result)
      const mapped = rows.map(r => {
        const email = (r['E-Mail'] || r['email'] || r['Email'] || '').toLowerCase().trim()
        const firstName = r['Vorname'] || r['First Name'] || r['first_name'] || ''
        const lastName  = r['Nachname'] || r['Last Name'] || r['last_name'] || ''
        const name = `${firstName} ${lastName}`.trim() || email
        const phone = r['Telefonnummer'] || r['Phone'] || r['phone'] || ''
        const tagsRaw = r['Tags'] || r['tags'] || r['Label'] || ''
        const tags = tagsRaw ? tagsRaw.split(',').map(t=>t.trim()).filter(Boolean) : []
        return { id: uid(), name, email, phone, tags, labels: [], pipelines: [], closing_stage: 'Strategiegespräch', products: [], webinars: [], timeline: [], website: '', spezialisierung: '', drive_url: '' }
      }).filter(r => r.email)
      setImportRows(mapped)
      setShowImport(true)
    }
    reader.readAsText(file, 'UTF-8')
  }

  const doImport = async () => {
    setImporting(true)
    await onImport(importRows)
    setImporting(false)
    setImportDone(importRows.length)
    setTimeout(() => { setShowImport(false); setImportRows([]); setImportDone(null) }, 2500)
  }

  const toggleP = (id) => setFilterProds(p => p.includes(id) ? p.filter(x=>x!==id) : [...p, id])
  const toggleW = (id) => setFilterWebs(p => p.includes(id) ? p.filter(x=>x!==id) : [...p, id])
  const toggleL = (l)  => setFilterLabels(p => p.includes(l)  ? p.filter(x=>x!==l)  : [...p, l])
  const clearAll = () => { setFilterProds([]); setFilterWebs([]); setFilterLabels([]); setQ('') }
  const hasFilter = filterProds.length>0 || filterWebs.length>0 || filterLabels.length>0 || q.length>0
  const [selected, setSelected] = useState([])
  const deleteSelected = async () => {
    if (!window.confirm(`${selected.length} Kontakte wirklich löschen?`)) return
    for (const id of selected) { try { await DB.del(id) } catch(e) { console.error(e) } }
    setSelected([])
  }

  // Collect all labels used
  const allLabels = [...new Set(contacts.flatMap(c=>c.labels||[]))]

  const f = contacts.filter(c => {
    if (q && !c.name.toLowerCase().includes(q.toLowerCase()) && !c.email?.toLowerCase().includes(q.toLowerCase())) return false
    if (filterProds.length>0 && !filterProds.every(pid => c.products.some(p => p.catalogId===pid))) return false
    if (filterWebs.length>0  && !filterWebs.every(wid  => c.webinars.some(w => w.catalogId===wid))) return false
    if (filterLabels.length>0 && !filterLabels.every(l => (c.labels||[]).includes(l))) return false
    return true
  })

  const tot = contacts.reduce((s,c) => s+c.products.reduce((ps,p)=>ps+p.price,0), 0)

  const Dropdown = ({ id, label, items, selected, onToggle, getColor }) => {
    const shown = items.filter(it => (it.name||it).toLowerCase().includes(dropSearch.toLowerCase()))
    const isOpen = openDrop===id
    return (
      <div style={{position:'relative'}}>
        <button onClick={()=>{setOpenDrop(isOpen?null:id);setDropSearch('')}}
          style={{display:'flex',alignItems:'center',gap:6,padding:'6px 12px',border:`0.5px solid ${selected.length>0?C.br:C.bo}`,borderRadius:8,cursor:'pointer',
            background:selected.length>0?C.be:'transparent',color:selected.length>0?C.br:C.tL,fontSize:12,fontWeight:selected.length>0?500:400,transition:'all .15s',whiteSpace:'nowrap'}}>
          {label}{selected.length>0&&<span style={{background:C.br,color:C.w,borderRadius:9,fontSize:10,padding:'0 6px',fontWeight:600}}>{selected.length}</span>}
          <span style={{fontSize:9,opacity:.6}}>{isOpen?'▲':'▼'}</span>
        </button>
        {isOpen && (
          <div style={{position:'absolute',top:'calc(100% + 6px)',left:0,minWidth:220,background:C.w,border:`0.5px solid ${C.bo}`,borderRadius:12,boxShadow:'0 8px 32px rgba(0,0,0,.12)',zIndex:100,overflow:'hidden'}}>
            <div style={{padding:'10px 12px',borderBottom:`0.5px solid ${C.bo}`}}>
              <div style={{display:'flex',alignItems:'center',gap:8,background:C.beL,borderRadius:7,padding:'7px 10px'}}>
                <span style={{fontSize:13,color:C.tL}}>🔍</span>
                <input autoFocus value={dropSearch} onChange={e=>setDropSearch(e.target.value)}
                  placeholder="Suchen …" style={{border:'none',background:'transparent',outline:'none',fontSize:12.5,color:C.s,flex:1}}/>
              </div>
            </div>
            <div style={{maxHeight:260,overflowY:'auto',padding:'6px 0'}}>
              {shown.length===0 && <div style={{padding:'10px 14px',fontSize:12,color:C.tL}}>Nichts gefunden</div>}
              {shown.map(it => {
                const name = it.name||it
                const iid  = it.id||it
                const active = selected.includes(iid)
                const col = getColor ? gc(it.color) : null
                return (
                  <div key={iid} onClick={()=>onToggle(iid)}
                    style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'8px 14px',cursor:'pointer',transition:'background .1s'}}
                    onMouseEnter={e=>e.currentTarget.style.background=C.beL}
                    onMouseLeave={e=>e.currentTarget.style.background='transparent'}>
                    <span style={{display:'inline-flex',alignItems:'center',gap:8}}>
                      {col && <span style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'2px 9px',borderRadius:4,fontSize:11.5,fontWeight:500}}>{name}</span>}
                      {!col && <span style={{fontSize:13,color:C.s}}>{name}</span>}
                    </span>
                    {active && <span style={{color:C.br,fontWeight:700,fontSize:14}}>✓</span>}
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div style={{flex:1,overflow:'hidden',display:'flex',flexDirection:'column',padding:20,gap:12}}
      onClick={e=>{if(!e.target.closest('[data-drop]'))setOpenDrop(null)}}>

      {/* CSV Import Modal */}
      {showImport && (
        <div style={{position:'fixed',inset:0,background:'rgba(0,0,0,.4)',zIndex:200,display:'flex',alignItems:'center',justifyContent:'center'}}>
          <div style={{background:C.w,borderRadius:16,padding:28,width:520,maxHeight:'80vh',overflowY:'auto',boxShadow:'0 24px 80px rgba(0,0,0,.2)'}}>
            <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:22,fontWeight:600,marginBottom:6}}>CSV importieren</div>
            {importDone ? (
              <div style={{textAlign:'center',padding:'24px 0',color:C.ok,fontSize:16,fontWeight:500}}>✅ {importDone} Kontakte importiert!</div>
            ) : (
              <>
                <div style={{fontSize:12,color:C.tL,marginBottom:14}}>{importRows.length} Kontakte gefunden – Vorschau:</div>
                <div style={{border:`0.5px solid ${C.bo}`,borderRadius:10,overflow:'hidden',marginBottom:16}}>
                  <table style={{width:'100%',borderCollapse:'collapse',fontSize:12}}>
                    <thead><tr style={{background:C.beL}}>
                      {['Name','E-Mail','Telefon','Labels'].map(h=><th key={h} style={{padding:'8px 12px',textAlign:'left',fontWeight:500,color:C.tL,fontSize:10.5,textTransform:'uppercase',letterSpacing:.7}}>{h}</th>)}
                    </tr></thead>
                    <tbody>
                      {importRows.slice(0,10).map((r,i)=>(
                        <tr key={i} style={{borderTop:`0.5px solid ${C.bo}`}}>
                          <td style={{padding:'7px 12px',color:C.s}}>{r.name||'—'}</td>
                          <td style={{padding:'7px 12px',color:C.tL,fontSize:11}}>{r.email}</td>
                          <td style={{padding:'7px 12px',color:C.tL,fontSize:11}}>{r.phone||'—'}</td>
                          <td style={{padding:'7px 12px'}}>{r.labels.slice(0,2).map(l=><span key={l} style={{background:C.beL,border:`0.5px solid ${C.bo}`,borderRadius:3,fontSize:10,padding:'1px 5px',marginRight:3}}>{l}</span>)}{r.labels.length>2&&<span style={{fontSize:10,color:C.tL}}>+{r.labels.length-2}</span>}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {importRows.length>10&&<div style={{padding:'8px 12px',fontSize:11,color:C.tL,background:C.beL}}>... und {importRows.length-10} weitere</div>}
                </div>
                <div style={{display:'flex',gap:10,justifyContent:'flex-end'}}>
                  <button onClick={()=>{setShowImport(false);setImportRows([])}} style={{padding:'9px 20px',border:`0.5px solid ${C.bo}`,borderRadius:8,cursor:'pointer',background:'none',color:C.tL,fontSize:13}}>Abbrechen</button>
                  <button onClick={doImport} disabled={importing} className="bp"
                    style={{padding:'9px 24px',background:importing?C.wg:C.br,color:C.w,border:'none',borderRadius:8,cursor:importing?'wait':'pointer',fontSize:13,fontWeight:500}}>
                    {importing?'Wird importiert …':`${importRows.length} Kontakte importieren`}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
      <input ref={fileRef} type="file" accept=".csv" style={{display:'none'}} onChange={handleFile}/>
      {/* Stats */}
      <div style={{display:'flex',gap:10}}>
        {[{l:'Gesamt',v:contacts.length},{l:'Closing',v:contacts.filter(c=>c.pipelines.includes('closing')).length},{l:'Begleitung',v:contacts.filter(c=>c.pipelines.includes('begleitung')).length},{l:'Umsatz',v:tot.toLocaleString('de-DE')+' €'}].map(s => (
          <div key={s.l} style={{background:C.w,border:`0.5px solid rgba(0,0,0,.07)`,borderRadius:12,padding:'12px 16px',flex:1,boxShadow:'0 2px 8px rgba(0,0,0,.04)'}}>
            <div style={{fontSize:10,textTransform:'uppercase',letterSpacing:1,color:C.tL,marginBottom:4}}>{s.l}</div>
            <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:22,fontWeight:600,color:C.br}}>{s.v}</div>
          </div>
        ))}
        <button onClick={()=>fileRef.current.click()}
          style={{padding:'12px 18px',background:C.w,border:`0.5px solid ${C.bo}`,borderRadius:12,cursor:'pointer',color:C.br,fontSize:12,fontWeight:500,boxShadow:'0 2px 8px rgba(0,0,0,.04)',whiteSpace:'nowrap',display:'flex',alignItems:'center',gap:6,transition:'all .15s'}}
          onMouseEnter={e=>e.currentTarget.style.borderColor=C.br} onMouseLeave={e=>e.currentTarget.style.borderColor=C.bo}>
          📥 CSV importieren
        </button>
      </div>

      {/* Filter Bar */}
      <div style={{background:C.w,border:`0.5px solid ${C.bo}`,borderRadius:12,padding:'12px 16px',display:'flex',gap:8,alignItems:'center',flexWrap:'wrap',boxShadow:'0 1px 4px rgba(0,0,0,.03)'}}>
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="🔍  Name oder E-Mail …"
          style={{...IS,width:200,flex:'none',borderRadius:8,fontSize:12.5}}/>
        <div style={{width:'0.5px',height:22,background:C.bo,margin:'0 2px'}}/>
        <div data-drop="1" style={{display:'flex',gap:6,alignItems:'center',flexWrap:'wrap'}}>
          {prodCat?.length>0 && <Dropdown id="prod" label="Produkt" items={prodCat} selected={filterProds} onToggle={toggleP} getColor/>}
          {webCat?.length>0  && <Dropdown id="web"  label="Webinar" items={webCat}  selected={filterWebs}  onToggle={toggleW} getColor/>}
          {allLabels.length>0 && <Dropdown id="label" label="Label" items={allLabels} selected={filterLabels} onToggle={toggleL}/>}
        </div>
        {hasFilter && (
          <button onClick={clearAll} style={{padding:'5px 12px',border:`0.5px solid ${C.bo}`,borderRadius:7,cursor:'pointer',background:'none',color:C.tL,fontSize:11.5,marginLeft:'auto',whiteSpace:'nowrap'}}>
            × Filter löschen · {f.length} Ergebnis{f.length!==1?'se':''}
          </button>
        )}
        {!hasFilter && <span style={{fontSize:12,color:C.tL,marginLeft:'auto'}}>{contacts.length} Kontakte</span>}
      </div>

      {/* Table */}
      <div style={{flex:1,overflowY:'auto',background:C.w,border:`1px solid ${C.bo}`,borderRadius:12,position:'relative'}}>
        {selected.length>0&&(
          <div style={{position:'sticky',top:0,zIndex:10,background:'#fff8f0',borderBottom:`1px solid ${C.bo}`,padding:'8px 14px',display:'flex',alignItems:'center',gap:12}}>
            <span style={{fontSize:13,fontWeight:500,color:C.br}}>{selected.length} ausgewählt</span>
            <button onClick={deleteSelected} style={{padding:'5px 14px',background:C.er,color:C.w,border:'none',borderRadius:7,cursor:'pointer',fontSize:12,fontWeight:500}}>
              Löschen
            </button>
            <button onClick={()=>setSelected([])} style={{padding:'5px 14px',background:'none',border:`0.5px solid ${C.bo}`,borderRadius:7,cursor:'pointer',fontSize:12,color:C.tL}}>
              Abwählen
            </button>
          </div>
        )}
        <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
          <thead><tr style={{borderBottom:`1px solid ${C.bo}`}}>
            <th style={{padding:'9px 12px',width:36}}>
              <input type="checkbox" checked={selected.length===f.length&&f.length>0}
                onChange={e=>setSelected(e.target.checked?f.map(c=>c.id):[])}
                style={{cursor:'pointer',accentColor:C.br}}/>
            </th>
            {['Name & Telefon','Status','Spezialisierung','Produkte','Webinare','Labels','Tags'].map(h=><th key={h} style={{padding:'9px 14px',textAlign:'left',fontSize:10.5,color:C.tL,fontWeight:500,letterSpacing:.7,textTransform:'uppercase',whiteSpace:'nowrap'}}>{h}</th>)}
          </tr></thead>
          <tbody>
            {f.map(c => {
              const isSel = c.id===selId
              const isChk = selected.includes(c.id)
              const bg = isChk?'#fff8f0':isSel?C.beL:'transparent'
              return <tr key={c.id} className="rh" style={{borderBottom:`1px solid ${C.bo}`,cursor:'pointer',background:bg}}>
                <td style={{padding:'9px 12px'}} onClick={e=>e.stopPropagation()}>
                  <input type="checkbox" checked={isChk}
                    onChange={e=>setSelected(s=>e.target.checked?[...s,c.id]:s.filter(x=>x!==c.id))}
                    style={{cursor:'pointer',accentColor:C.br}}/>
                </td>
                <td style={{padding:'9px 14px'}} onClick={()=>onSelect(c)}>
                  <div style={{fontWeight:500}}>{c.name}</div>
                  <div style={{fontSize:11,color:C.tL,marginTop:1}}>{c.email}</div>
                  {c.phone && <a href={`tel:${c.phone}`} onClick={e=>e.stopPropagation()} style={{fontSize:11,color:C.br,marginTop:1,display:'block',textDecoration:'none'}}>{c.phone}</a>}
                </td>
                <td style={{padding:'9px 14px'}} onClick={()=>onSelect(c)}>
                  {c.pipelines.includes('closing')&&<div style={{fontSize:11,background:C.brBg,color:C.br,padding:'1px 7px',borderRadius:4,marginBottom:2,width:'fit-content'}}>C: {c.closingStage}</div>}
                  {c.pipelines.includes('begleitung')&&<div style={{fontSize:11,background:C.okBg,color:C.ok,padding:'1px 7px',borderRadius:4,width:'fit-content'}}>B: {c.begleitungStage}</div>}
                </td>
                <td style={{padding:'9px 14px',color:C.tL,fontSize:12}} onClick={()=>onSelect(c)}>{c.spezialisierung||'—'}</td>
                <td style={{padding:'9px 14px',maxWidth:180}} onClick={()=>onSelect(c)}>
                  {c.products.length>0 ? <div style={{display:'flex',flexWrap:'wrap',gap:3}}>
                    {c.products.map(p=>{const col=gc(prodCat?.find(x=>x.id===p.catalogId)?.color);return <span key={p.id} style={{background:col.bg,color:col.tx,padding:'1px 6px',borderRadius:3,fontSize:10.5,fontWeight:500,whiteSpace:'nowrap'}}>{p.name}</span>})}
                  </div> : <span style={{color:C.tL}}>—</span>}
                </td>
                <td style={{padding:'9px 14px',maxWidth:180}} onClick={()=>onSelect(c)}>
                  {c.webinars.length>0 ? <div style={{display:'flex',flexWrap:'wrap',gap:3}}>
                    {c.webinars.map(w=>{const col=gc(webCat?.find(x=>x.id===w.catalogId)?.color||'blau');return <span key={w.id} style={{background:col.bg,color:col.tx,padding:'1px 6px',borderRadius:3,fontSize:10.5,whiteSpace:'nowrap'}}>{w.name}</span>})}
                  </div> : <span style={{color:C.tL}}>—</span>}
                </td>
                <td style={{padding:'9px 14px'}} onClick={()=>onSelect(c)}><div style={{display:'flex',gap:3,flexWrap:'wrap'}}>{c.labels.map(l=><STag key={l} text={l}/>)}</div></td>
                <td style={{padding:'9px 14px',maxWidth:220}} onClick={()=>onSelect(c)}>
                  {(c.tags||[]).length>0 ? <div style={{display:'flex',flexWrap:'wrap',gap:3}}>
                    {(c.tags||[]).slice(0,3).map(t=><span key={t} style={{background:'#f0f0f0',color:'#555',padding:'1px 7px',borderRadius:3,fontSize:10,whiteSpace:'nowrap'}}>{t}</span>)}
                    {(c.tags||[]).length>3&&<span style={{fontSize:10,color:C.tL}}>+{(c.tags||[]).length-3}</span>}
                  </div> : <span style={{color:C.tL}}>—</span>}
                </td>
              </tr>
            })}
          </tbody>
        </table>
        {f.length===0 && <div style={{padding:28,textAlign:'center',color:C.tL,fontSize:13}}>Keine Kontakte gefunden</div>}
      </div>
    </div>
  )
}

// ── Catalog View ──────────────────────────────────────────────
function CatalogView({ prodCat, webCat, onSaveP, onSaveW }) {
  const [tab, setTab] = useState('products')
  const [np, setNp] = useState({name:'',price:'',color:'braun'})
  const [nw, setNw] = useState({name:'',color:'gruen'})
  const [expandedProd, setExpandedProd] = useState(null)
  const [editingProd,  setEditingProd]  = useState(null)
  const addP = () => { if(!np.name.trim()||!np.price)return; onSaveP([...prodCat,{id:uid(),name:np.name.trim(),price:parseFloat(np.price),color:np.color}]); setNp({name:'',price:'',color:'braun'}) }
  const addW = () => { if(!nw.name.trim())return; onSaveW([...webCat,{id:uid(),name:nw.name.trim(),color:nw.color}]); setNw({name:'',color:'gruen'}) }
  const LINK_FIELDS = [['verkaufsLink','🛒 Verkaufslink'],['ratenLink','💳 Ratenzahlung'],['anmeldeLink','📋 Anmeldeseite'],['aufzeichnungLink','🎬 Aufzeichnung'],['driveLink','📁 Drive-Ordner']]
  return (
    <div style={{flex:1,overflow:'hidden',display:'flex',flexDirection:'column',padding:20,gap:14}}>
      <div style={{display:'flex',gap:6}}>
        {[['products','📦 Produkte'],['webinars','🎯 Webinare']].map(([t,l]) => (
          <button key={t} onClick={()=>setTab(t)}
            style={{padding:'8px 22px',border:`0.5px solid ${tab===t?C.br:C.bo}`,borderBottom:tab===t?`0.5px solid ${C.w}`:`0.5px solid ${C.bo}`,
              borderRadius:'10px 10px 0 0',cursor:'pointer',background:tab===t?C.w:'transparent',
              color:tab===t?C.br:C.tL,fontSize:13,fontWeight:tab===t?500:400,letterSpacing:'.2px',transition:'all .2s'}}>{l}
          </button>
        ))}
      </div>
      {tab==='products' && (
        <div style={{flex:1,overflowY:'auto',display:'flex',flexDirection:'column',gap:10,maxWidth:720}}>
          {prodCat.map(p => {
            const col=gc(p.color)
            const isExp  = expandedProd===p.id
            const isEdit = editingProd===p.id && isExp
            const updP   = (field,val) => onSaveP(prodCat.map(x=>x.id===p.id?{...x,[field]:val}:x))
            const hasLinks = LINK_FIELDS.some(([f])=>p[f])
            const hasCustom = (p.customFields||[]).some(cf=>cf.label&&cf.value)

            return (
              <div key={p.id} style={{background:C.w,border:`0.5px solid ${isExp?C.br:C.bo}`,borderRadius:14,overflow:'hidden',
                boxShadow:isExp?`0 4px 20px rgba(162,106,37,.08)`:'0 1px 4px rgba(0,0,0,.04)',transition:'all .2s'}}>

                {/* Header */}
                <div style={{padding:'14px 18px',display:'flex',alignItems:'center',gap:14,cursor:'pointer'}}
                  onClick={()=>{setExpandedProd(isExp?null:p.id);if(!isExp)setEditingProd(null)}}>
                  <span style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'4px 14px',borderRadius:6,fontSize:12.5,fontWeight:500,minWidth:160}}>{p.name}</span>
                  <span style={{fontWeight:600,color:C.ok,fontSize:15}}>{p.price.toLocaleString('de-DE')} €</span>
                  {(hasLinks||hasCustom)&&!isExp&&<span style={{fontSize:10.5,color:C.tL,background:C.beL,padding:'2px 8px',borderRadius:4}}>🔗 Links</span>}
                  {p.notes&&!isExp&&<span style={{fontSize:10.5,color:C.tL,background:C.beL,padding:'2px 8px',borderRadius:4}}>📝</span>}
                  <div style={{marginLeft:'auto',display:'flex',gap:8,alignItems:'center'}}>
                    {isExp&&!isEdit&&<button onClick={e=>{e.stopPropagation();setEditingProd(p.id)}}
                      style={{padding:'5px 13px',border:`0.5px solid ${C.bo}`,borderRadius:7,cursor:'pointer',background:'none',color:C.s,fontSize:12,fontWeight:500,transition:'all .15s'}}
                      onMouseEnter={e=>e.currentTarget.style.borderColor=C.br} onMouseLeave={e=>e.currentTarget.style.borderColor=C.bo}>✏️ Bearbeiten</button>}
                    {isEdit&&<button onClick={e=>{e.stopPropagation();setEditingProd(null)}}
                      style={{padding:'5px 16px',border:'none',borderRadius:7,cursor:'pointer',background:C.br,color:C.w,fontSize:12,fontWeight:500}}>✓ Fertig</button>}
                    {!isExp&&<button onClick={e=>{e.stopPropagation();onSaveP(prodCat.filter(x=>x.id!==p.id))}}
                      style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:16,padding:'0 4px'}}>×</button>}
                    <span style={{fontSize:11,color:C.tL,opacity:.5}}>{isExp?'▲':'▼'}</span>
                  </div>
                </div>

                {/* READ mode */}
                {isExp&&!isEdit&&(
                  <div style={{padding:'2px 18px 18px',borderTop:`0.5px solid ${C.bo}`}}>
                    {(hasLinks||hasCustom)&&<div style={{paddingTop:14}}>
                      <div style={{fontSize:10,color:C.tL,textTransform:'uppercase',letterSpacing:1,marginBottom:8}}>Links & Dokumente</div>
                      <div style={{display:'flex',flexWrap:'wrap',gap:7}}>
                        {LINK_FIELDS.filter(([f])=>p[f]).map(([f,label])=>(
                          <a key={f} href={p[f]} target="_blank"
                            style={{display:'inline-flex',alignItems:'center',gap:4,padding:'6px 13px',background:C.beL,border:`0.5px solid ${C.bo}`,borderRadius:8,fontSize:12,color:C.br,textDecoration:'none',fontWeight:500,transition:'all .15s'}}
                            onMouseEnter={e=>{e.currentTarget.style.background=C.be;e.currentTarget.style.borderColor=C.br}}
                            onMouseLeave={e=>{e.currentTarget.style.background=C.beL;e.currentTarget.style.borderColor=C.bo}}>
                            {label} ↗
                          </a>
                        ))}
                        {(p.customFields||[]).filter(cf=>cf.label&&cf.value).map((cf,i)=>(
                          <a key={i} href={cf.value.startsWith('http')?cf.value:'#'} target="_blank"
                            style={{display:'inline-flex',alignItems:'center',gap:4,padding:'6px 13px',background:C.beL,border:`0.5px solid ${C.bo}`,borderRadius:8,fontSize:12,color:C.s,textDecoration:'none',transition:'all .15s'}}
                            onMouseEnter={e=>e.currentTarget.style.background=C.be} onMouseLeave={e=>e.currentTarget.style.background=C.beL}>
                            {cf.label}{cf.value.startsWith('http')?' ↗':''}
                          </a>
                        ))}
                      </div>
                    </div>}
                    {p.notes&&<div style={{marginTop:12,paddingTop:12,borderTop:`0.5px solid ${C.bo}`}}>
                      <div style={{fontSize:10,color:C.tL,textTransform:'uppercase',letterSpacing:1,marginBottom:6}}>Notizen</div>
                      <div style={{fontSize:13,color:C.s,lineHeight:1.65,whiteSpace:'pre-wrap'}}>{p.notes}</div>
                    </div>}
                    {!hasLinks&&!hasCustom&&!p.notes&&<div style={{paddingTop:14,fontSize:13,color:C.tL,fontStyle:'italic'}}>Noch keine Links oder Notizen. Klicke ✏️ Bearbeiten um Details hinzuzufügen.</div>}
                  </div>
                )}

                {/* EDIT mode */}
                {isExp&&isEdit&&(
                  <div style={{padding:'14px 18px 18px',borderTop:`0.5px solid ${C.bo}`,display:'flex',flexDirection:'column',gap:10}}>
                    <div style={{display:'flex',gap:8,alignItems:'center'}}>
                      <input value={p.name} onChange={e=>updP('name',e.target.value)} placeholder="Produktname" style={{...IS,flex:2,fontSize:13}}/>
                      <input value={p.price} onChange={e=>updP('price',parseFloat(e.target.value)||0)} type="number" style={{...IS,width:100}}/>
                    </div>
                    <div style={{display:'flex',alignItems:'center',gap:10}}>
                      <span style={{fontSize:12,color:C.tL}}>Farbe:</span>
                      <div style={{display:'flex',gap:5}}>{PAL.map(cl=><div key={cl.id} className="pal" onClick={()=>updP('color',cl.id)}
                        style={{width:18,height:18,borderRadius:'50%',background:cl.bg,border:`2.5px solid ${p.color===cl.id?cl.tx:cl.bo}`,cursor:'pointer'}}/>)}</div>
                    </div>
                    <div style={{fontSize:10,color:C.tL,textTransform:'uppercase',letterSpacing:1}}>Links & Dokumente</div>
                    {LINK_FIELDS.map(([field,label])=>(
                      <div key={field} style={{display:'flex',alignItems:'center',gap:8}}>
                        <span style={{fontSize:12,color:C.tL,width:130,flexShrink:0}}>{label}</span>
                        <input value={p[field]||''} onChange={e=>updP(field,e.target.value)} placeholder="https://…" style={{...IS,flex:1,fontSize:12}}/>
                        {p[field]&&<a href={p[field]} target="_blank" style={{color:C.br,fontSize:13,textDecoration:'none'}}>↗</a>}
                      </div>
                    ))}
                    {(p.customFields||[]).length>0&&<div style={{fontSize:10,color:C.tL,textTransform:'uppercase',letterSpacing:1}}>Eigene Felder</div>}
                    {(p.customFields||[]).map((cf,i)=>(
                      <div key={i} style={{display:'flex',alignItems:'center',gap:6}}>
                        <input value={cf.label} onChange={e=>{const f=[...(p.customFields||[])];f[i]={...f[i],label:e.target.value};updP('customFields',f)}} placeholder="Feldname" style={{...IS,width:120,fontSize:12}}/>
                        <input value={cf.value} onChange={e=>{const f=[...(p.customFields||[])];f[i]={...f[i],value:e.target.value};updP('customFields',f)}} placeholder="URL oder Text" style={{...IS,flex:1,fontSize:12}}/>
                        {cf.value?.startsWith('http')&&<a href={cf.value} target="_blank" style={{color:C.br,fontSize:13,textDecoration:'none'}}>↗</a>}
                        <button onClick={()=>updP('customFields',(p.customFields||[]).filter((_,j)=>j!==i))} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:15}}>×</button>
                      </div>
                    ))}
                    <button onClick={()=>updP('customFields',[...(p.customFields||[]),{label:'',value:''}])}
                      style={{alignSelf:'flex-start',padding:'5px 14px',border:`1px dashed ${C.br}`,borderRadius:6,cursor:'pointer',background:'transparent',color:C.br,fontSize:12}}>
                      + Eigenes Feld
                    </button>
                    <div style={{fontSize:10,color:C.tL,textTransform:'uppercase',letterSpacing:1}}>Interne Notizen</div>
                    <textarea value={p.notes||''} onChange={e=>updP('notes',e.target.value)} placeholder="Interne Notizen …"
                      style={{...IS,resize:'vertical',minHeight:60,fontSize:12,padding:'7px 10px',lineHeight:1.5}}/>
                    <div style={{display:'flex',justifyContent:'flex-end'}}>
                      <button onClick={()=>{onSaveP(prodCat.filter(x=>x.id!==p.id));setExpandedProd(null);setEditingProd(null)}}
                        style={{padding:'5px 12px',border:`0.5px solid ${C.er}`,borderRadius:6,cursor:'pointer',background:'none',color:C.er,fontSize:11}}>
                        Produkt löschen
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
          <div style={{background:C.w,border:`1px dashed ${C.bo}`,borderRadius:14,padding:'14px 18px'}}>
            <div style={{fontSize:10,color:C.tL,textTransform:'uppercase',letterSpacing:1,marginBottom:10}}>Neues Produkt</div>
            <div style={{display:'flex',gap:8,alignItems:'center',flexWrap:'wrap'}}>
              <input value={np.name} onChange={e=>setNp({...np,name:e.target.value})} placeholder="Produktname" style={{...IS,flex:2,minWidth:140}}/>
              <input value={np.price} onChange={e=>setNp({...np,price:e.target.value})} placeholder="Preis €" type="number" style={{...IS,width:100}}/>
              <div style={{display:'flex',gap:4}}>{PAL.map(cl=><div key={cl.id} className="pal" onClick={()=>setNp({...np,color:cl.id})} style={{width:18,height:18,borderRadius:'50%',background:cl.bg,border:`2.5px solid ${np.color===cl.id?cl.tx:cl.bo}`,cursor:'pointer'}}/>)}</div>
              <Abtn onClick={addP}/>
            </div>
          </div>
        </div>
      )}
      {tab==='webinars' && (
        <div style={{flex:1,overflowY:'auto',display:'flex',flexDirection:'column',gap:10,maxWidth:680}}>
          {webCat.map(w => { const col=gc(w.color); return (
            <div key={w.id} style={{background:C.w,border:`1px solid ${C.bo}`,borderRadius:10,padding:'12px 16px',display:'flex',alignItems:'center',gap:12}}>
              <span style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'3px 12px',borderRadius:5,fontSize:12,fontWeight:500,minWidth:200}}>{w.name}</span>
              <div style={{display:'flex',gap:4,marginLeft:'auto',alignItems:'center'}}>
                {PAL.map(cl=><div key={cl.id} className="pal" onClick={()=>onSaveW(webCat.map(x=>x.id===w.id?{...x,color:cl.id}:x))} style={{width:15,height:15,borderRadius:'50%',background:cl.bg,border:`2px solid ${w.color===cl.id?cl.tx:cl.bo}`,cursor:'pointer',flexShrink:0}}/>)}
                <button onClick={()=>onSaveW(webCat.filter(x=>x.id!==w.id))} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:16,marginLeft:6}}>×</button>
              </div>
            </div>
          )})}
          <div style={{background:C.w,border:`1px dashed ${C.bo}`,borderRadius:10,padding:'12px 16px',display:'flex',gap:8,alignItems:'center'}}>
            <input value={nw.name} onChange={e=>setNw({...nw,name:e.target.value})} placeholder="Webinar-Name" style={{...IS,flex:1}}/>
            <div style={{display:'flex',gap:4}}>{PAL.map(cl=><div key={cl.id} className="pal" onClick={()=>setNw({...nw,color:cl.id})} style={{width:18,height:18,borderRadius:'50%',background:cl.bg,border:`2px solid ${nw.color===cl.id?cl.tx:cl.bo}`,cursor:'pointer'}}/>)}</div>
            <Abtn onClick={addW}/>
          </div>
        </div>
      )}
    </div>
  )
}

// ── Kundenakte ────────────────────────────────────────────────
function Akte({ contact, prodCat, webCat, onUpdate, onDelete, onClose, userEmail }) {
  const [tab, setTab]     = useState('overview')
  const [newLabel, setNL] = useState('')
  const upd = (f) => onUpdate({ ...contact, ...f })
  const rev = contact.products.reduce((s,p)=>s+p.price,0)
  const addLabel = () => { const l=newLabel.trim(); if(!l||contact.labels.includes(l))return; upd({labels:[...contact.labels,l]}); setNL('') }
  const changeStage = (pipeline, newStage) => {
    const sk = pipeline==='closing'?'closingStage':'begleitungStage'
    const old = contact[sk]; if(old===newStage)return
    const te = {id:uid(),type:'status',field:pipeline==='closing'?'Closing':'Begleitung',from:old,to:newStage,date:today(),ts:new Date().toISOString()}
    upd({[sk]:newStage,timeline:[...(contact.timeline||[]),te]})
  }
  const togglePipe = (p) => {
    let pipes = contact.pipelines.includes(p)?contact.pipelines.filter(x=>x!==p):[...contact.pipelines,p]
    if(pipes.length===0)pipes=[p]
    const ex={}; if(p==='closing'&&!contact.closingStage)ex.closingStage='Strategiegespräch'; if(p==='begleitung'&&!contact.begleitungStage)ex.begleitungStage='Onboarding'
    upd({pipelines:pipes,...ex})
  }
  const TABS = [['overview','Übersicht'],['verlauf','Verlauf'],['products','Produkte'],['webinars','Webinare']]
  return (
    <aside style={{width:395,background:C.w,borderLeft:`0.5px solid rgba(0,0,0,.07)`,display:'flex',flexDirection:'column',overflow:'hidden',flexShrink:0,boxShadow:'-4px 0 24px rgba(0,0,0,.05)'}}>
      <div style={{padding:'20px 20px 14px',background:`linear-gradient(160deg, #ede8e2 0%, #e8e1da 100%)`,borderBottom:`0.5px solid rgba(0,0,0,.07)`,flexShrink:0}}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start'}}>
          <div>
            <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:23,fontWeight:600,lineHeight:1.2,letterSpacing:'.2px'}}>{contact.name}</div>
            <div style={{fontSize:11.5,color:C.tL,marginTop:2,letterSpacing:'.1px'}}>{contact.email}</div>
          </div>
          <button onClick={onClose} style={{background:'rgba(0,0,0,.06)',border:'none',cursor:'pointer',color:C.s,fontSize:14,lineHeight:1,padding:'6px 8px',borderRadius:6,fontWeight:500,transition:'all .15s'}}
            onMouseEnter={e=>e.target.style.background='rgba(0,0,0,.12)'} onMouseLeave={e=>e.target.style.background='rgba(0,0,0,.06)'}>✕</button>
        </div>
        <div style={{display:'flex',gap:5,marginTop:9,flexWrap:'wrap',alignItems:'center'}}>
          {contact.pipelines.includes('closing')&&<span style={{fontSize:11,background:C.brBg,color:C.br,padding:'2px 9px',borderRadius:5,fontWeight:500,whiteSpace:'nowrap'}}>Closing · {contact.closingStage}</span>}
          {contact.pipelines.includes('begleitung')&&<span style={{fontSize:11,background:C.okBg,color:C.ok,padding:'2px 9px',borderRadius:5,fontWeight:500,whiteSpace:'nowrap'}}>Begleitung · {contact.begleitungStage}</span>}
          <div style={{display:'flex',gap:2,marginLeft:4}}>
            {[1,2,3,4,5].map(n=>(
              <span key={n} onClick={()=>upd({gesprachsScore:n===contact.gesprachsScore?null:n})}
                style={{cursor:'pointer',fontSize:16,color:n<=(contact.gesprachsScore||0)?'#f59e0b':'#d1c9c0',transition:'color .15s'}} title={`Score: ${n}`}>★</span>
            ))}
          </div>
          {rev>0&&<span style={{marginLeft:'auto',fontSize:12,fontWeight:700,color:C.ok}}>{rev.toLocaleString('de-DE')} €</span>}
        </div>
        <div style={{display:'flex',flexWrap:'wrap',gap:4,marginTop:9,alignItems:'center'}}>
          {contact.labels.map(l=>(
            <span key={l} style={{display:'inline-flex',alignItems:'center',gap:2,background:C.w,border:`1px solid ${C.bo}`,color:C.br,padding:'2px 6px',borderRadius:4,fontSize:11,whiteSpace:'nowrap'}}>
              {l}<button onClick={()=>upd({labels:contact.labels.filter(x=>x!==l)})} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:12,lineHeight:1,padding:0,marginLeft:1}}>×</button>
            </span>
          ))}
          <input value={newLabel} onChange={e=>setNL(e.target.value)} onKeyDown={e=>e.key==='Enter'&&addLabel()}
            placeholder="+ Label" style={{width:68,padding:'2px 6px',border:`1px dashed ${C.bo}`,borderRadius:4,fontSize:11,background:'transparent',outline:'none',color:C.s}}/>
        </div>
      </div>
      <div style={{display:'flex',borderBottom:`0.5px solid ${C.bo}`,flexShrink:0,background:C.w}}>
        {TABS.map(([t,l])=>(
          <button key={t} onClick={()=>setTab(t)} style={{flex:1,padding:'11px 2px',border:'none',background:'none',cursor:'pointer',fontSize:11.5,fontWeight:tab===t?500:400,color:tab===t?C.br:C.tL,
            borderBottom:`2px solid ${tab===t?C.br:'transparent'}`,transition:'all .2s',letterSpacing:'.2px'}}>{l}</button>
        ))}
      </div>
      <div style={{flex:1,overflowY:'auto',padding:'14px 18px',display:'flex',flexDirection:'column',gap:14}}>
        {tab==='overview' && <OvTab contact={contact} upd={upd} prodCat={prodCat} webCat={webCat} changeStage={changeStage} togglePipe={togglePipe} userEmail={userEmail}/>}
        {tab==='verlauf'  && <VTab contact={contact} upd={upd} userEmail={userEmail}/>}
        {tab==='products' && <PTab contact={contact} prodCat={prodCat} upd={upd}/>}
        {tab==='webinars' && <WTab contact={contact} webCat={webCat} upd={upd}/>}
      </div>
      <div style={{padding:'10px 18px',borderTop:`1px solid ${C.bo}`,flexShrink:0}}>
        <button onClick={()=>{if(window.confirm(`${contact.name} wirklich löschen?`))onDelete(contact.id)}} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:12}}>Kontakt löschen</button>
      </div>
    </aside>
  )
}

// ── Begleitung Setup ──────────────────────────────────────────
function BegleitungSetup({ contact, upd, userEmail }) {
  const [startISO, setStartISO] = useState(todayISO())
  const [mode, setMode]         = useState('3')
  const [custom, setCustom]     = useState('')

  const calcEnd = () => {
    if (!startISO) return null
    const d = new Date(startISO)
    if (mode === 'custom') { d.setDate(d.getDate() + parseInt(custom||0) * 7) }
    else { d.setMonth(d.getMonth() + parseInt(mode)) }
    return d.toLocaleDateString('de-DE')
  }
  const endDE = calcEnd()
  const days = daysLeft(contact.offboardingDate)
  const durLabel = mode==='custom' ? (custom||'?')+' Wochen' : mode+' Monate'

  const setup = () => {
    if (!startISO || !endDE) return
    const author = userEmail ? userEmail.split('@')[0] : 'System'
    const te = { id:uid(), type:'activity', actType:'offboarding', title:`Begleitung endet (${durLabel})`, date:endDE, time:'', completed:false, ts:new Date().toISOString(), author }
    upd({ offboardingDate: endDE, timeline: [...(contact.timeline||[]), te] })
  }

  return (
    <div style={{border:`1px solid ${contact.offboardingDate?(days!==null&&days<=7?C.er:C.ok):C.bo}`,borderRadius:9,padding:'12px 14px',background:C.beL}}>
      <div style={{fontSize:11,fontWeight:500,color:C.s,marginBottom:10,textTransform:'uppercase',letterSpacing:.5}}>Begleitung</div>
      {contact.offboardingDate && (
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'8px 10px',borderRadius:7,marginBottom:10,background:days!==null&&days<=7?'#fff5f5':days!==null&&days<=14?'#fffbf0':C.okBg}}>
          <div>
            <div style={{fontSize:12,fontWeight:500,color:C.s}}>Läuft bis {contact.offboardingDate}</div>
          </div>
          <span style={{fontSize:16,fontWeight:700,color:days!==null&&days<=7?C.er:days!==null&&days<=14?'#d97706':C.ok}}>
            {days===null?'—':days<=0?'Abgelaufen':days===0?'Heute!':days+'T'}
          </span>
        </div>
      )}
      <div style={{display:'flex',flexDirection:'column',gap:8}}>
        <div style={{display:'flex',alignItems:'center',gap:8}}>
          <span style={{fontSize:12,color:C.tL,width:80,flexShrink:0}}>Startdatum</span>
          <input type="date" value={startISO} onChange={e=>setStartISO(e.target.value)} style={{...IS,flex:1}}/>
        </div>
        <div style={{display:'flex',alignItems:'center',gap:8,flexWrap:'wrap'}}>
          <span style={{fontSize:12,color:C.tL,width:80,flexShrink:0}}>Dauer</span>
          <div style={{display:'flex',gap:5,flex:1,flexWrap:'wrap'}}>
            {[['3','3 Monate'],['6','6 Monate'],['custom','Individuell']].map(([v,l])=>(
              <button key={v} onClick={()=>setMode(v)}
                style={{padding:'3px 11px',border:`1px solid ${mode===v?C.br:C.bo}`,borderRadius:5,cursor:'pointer',background:mode===v?C.be:'transparent',color:mode===v?C.br:C.tL,fontSize:12,fontWeight:mode===v?500:400}}>
                {l}
              </button>
            ))}
          </div>
        </div>
        {mode==='custom' && (
          <div style={{display:'flex',alignItems:'center',gap:8}}>
            <span style={{fontSize:12,color:C.tL,width:80,flexShrink:0}}>Wochen</span>
            <input value={custom} onChange={e=>setCustom(e.target.value)} placeholder="z.B. 10" type="number" style={{...IS,width:80}}/>
          </div>
        )}
        {endDE && (
          <div style={{fontSize:12,color:C.tL,padding:'3px 0'}}>
            → Enddatum: <strong style={{color:C.s}}>{endDE}</strong>
          </div>
        )}
        <button onClick={setup} className="bp"
          style={{padding:'7px',background:C.br,color:C.w,border:'none',borderRadius:7,cursor:'pointer',fontSize:12,fontWeight:500,transition:'background .15s'}}>
          {contact.offboardingDate ? '🔄 Begleitung aktualisieren' : '✓ Begleitung einrichten'}
        </button>
      </div>
    </div>
  )
}

function DebouncedTextarea({ value, onChange, placeholder, style }) {
  const [local, setLocal] = React.useState(value||'')
  const timer = React.useRef(null)
  React.useEffect(() => { setLocal(value||'') }, [value])
  const handleChange = (v) => {
    setLocal(v)
    clearTimeout(timer.current)
    timer.current = setTimeout(() => onChange(v), 600)
  }
  return <textarea value={local} onChange={e=>handleChange(e.target.value)} placeholder={placeholder} style={style}/>
}

function DebouncedInput({ value, onChange, type='text', placeholder='', style }) {
  const [local, setLocal] = React.useState(value||'')
  const timer = React.useRef(null)
  React.useEffect(() => { setLocal(value||'') }, [value])
  const handleChange = (v) => {
    setLocal(v)
    clearTimeout(timer.current)
    timer.current = setTimeout(() => onChange(v), 600)
  }
  return <input type={type} value={local} onChange={e=>handleChange(e.target.value)} placeholder={placeholder} style={style}/>
}

// ── Overview Tab ──────────────────────────────────────────────
function OvTab({ contact, upd, prodCat, webCat, changeStage, togglePipe, userEmail }) {
  const tl = contact.timeline || []
  const recentNotes = [...tl].filter(e=>e.type==='note').reverse().slice(0,6)
  const [editMode, setEditMode] = React.useState(false)

  const FIELDS = [
    { label:'Name',          field:'name',           type:'text'  },
    { label:'E-Mail',        field:'email',          type:'email' },
    { label:'Telefon',       field:'phone',          type:'tel',  link: v => `tel:${v}`,            linkIcon:'📞' },
    { label:'Website',       field:'website',        type:'url',  link: v => v,                      linkIcon:'↗' },
    { label:'Spezialisierung', field:'spezialisierung', multiline: true },
    { label:'Drive-Ordner',  field:'driveUrl',       type:'url',  link: v => v,                      linkIcon:'📁' },
  ]

  return <>
    <Sec title={
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <span>Kontaktdaten</span>
        <button onClick={()=>setEditMode(e=>!e)}
          style={{padding:'3px 12px',border:`0.5px solid ${editMode?C.br:C.bo}`,borderRadius:6,cursor:'pointer',
            background:editMode?C.be:'transparent',color:editMode?C.br:C.tL,fontSize:11,fontWeight:editMode?500:400,
            display:'flex',alignItems:'center',gap:4,transition:'all .15s'}}>
          {editMode ? '✓ Fertig' : '✏️ Bearbeiten'}
        </button>
      </div>
    }>
      {FIELDS.map(({label,field,type='text',link,linkIcon,multiline}) => (
        <div key={field} style={{marginBottom:10}}>
          <div style={{fontSize:10,color:C.tL,fontWeight:500,textTransform:'uppercase',letterSpacing:.8,marginBottom:3}}>{label}</div>
          {editMode ? (
            <div style={{display:'flex',gap:6,alignItems:'center'}}>
              {multiline
                ? <DebouncedTextarea value={contact[field]} onChange={v=>upd({[field]:v})}
                    style={{...IS,width:'100%',resize:'vertical',minHeight:52,padding:'7px 10px',fontSize:13,lineHeight:1.55}}/>
                : <DebouncedInput value={contact[field]} onChange={v=>upd({[field]:v})} type={type}
                    style={{...IS,flex:1,fontSize:13}}/>
              }
              {link&&contact[field]&&<a href={link(contact[field])} target="_blank" style={{color:C.br,fontSize:14,textDecoration:'none',flexShrink:0}}>{linkIcon}</a>}
            </div>
          ) : (
            <div style={{display:'flex',alignItems:'center',gap:8,minHeight:28}}>
              <span style={{fontSize:13.5,color:contact[field]?C.s:C.tL,flex:1,lineHeight:1.5,whiteSpace:'pre-wrap',wordBreak:'break-word'}}>
                {contact[field] || <span style={{fontStyle:'italic',fontSize:12,color:C.tL}}>nicht angegeben</span>}
              </span>
              {link&&contact[field]&&<a href={link(contact[field])} target="_blank" style={{color:C.br,fontSize:14,textDecoration:'none',flexShrink:0}}>{linkIcon}</a>}
            </div>
          )}
        </div>
      ))}
    </Sec>
    <Sec title="Kunden-Ziele">
      <DebouncedTextarea value={contact.kundenZiele||''} onChange={v=>upd({kundenZiele:v})}
        placeholder="Was möchte diese Person konkret erreichen?"
        style={{...IS,width:'100%',resize:'vertical',minHeight:70,padding:'8px 10px',fontSize:12.5,lineHeight:1.6}}/>
    </Sec>
    <Sec title="Pipeline-Steuerung">
      {[['closing','Closing',CS,'closingStage'],['begleitung','Begleitung',BS,'begleitungStage']].map(([p,l,stages,sk]) => {
        const active = contact.pipelines.includes(p)
        return (
          <div key={p} style={{border:`0.5px solid ${C.bo}`,borderRadius:9,padding:'9px 12px',marginBottom:8}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:active?8:0}}>
              <span style={{fontSize:12.5,fontWeight:500,color:active?C.s:C.tL}}>{l}</span>
              <button onClick={()=>togglePipe(p)} className="bg" style={{padding:'2px 10px',border:`0.5px solid ${active?C.br:C.bo}`,borderRadius:5,cursor:'pointer',fontSize:11,background:active?C.be:'transparent',color:active?C.br:C.tL}}>{active?'Aktiv':'Inaktiv'}</button>
            </div>
            {active&&<select value={contact[sk]||''} onChange={e=>changeStage(p,e.target.value)} style={{width:'100%',padding:'6px 10px',border:`0.5px solid ${C.bo}`,borderRadius:7,fontSize:12.5,background:C.beL,color:C.s,outline:'none',cursor:'pointer'}}>
              {stages.map(s=><option key={s}>{s}</option>)}
            </select>}
          </div>
        )
      })}
    </Sec>
    {contact.pipelines.includes('begleitung') && <BegleitungSetup contact={contact} upd={upd} userEmail={userEmail}/>}
    {contact.products.length>0 && <Sec title="Produkte">
      <div style={{display:'flex',flexWrap:'wrap',gap:5}}>
        {contact.products.map(p => { const col=gc(prodCat.find(x=>x.id===p.catalogId)?.color); return <span key={p.id} style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'3px 10px',borderRadius:5,fontSize:11.5,fontWeight:500}}>{p.name} · {p.price.toLocaleString('de-DE')} €{p.bonuses?.length>0?` · ${p.bonuses.join(', ')}`:''}</span> })}
      </div>
    </Sec>}
    {contact.webinars.length>0 && <Sec title="Webinare">
      <div style={{display:'flex',flexWrap:'wrap',gap:5}}>
        {contact.webinars.map(w => { const col=gc(webCat.find(x=>x.id===w.catalogId)?.color||'blau'); return <span key={w.id} style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'3px 10px',borderRadius:5,fontSize:11.5}}>{w.name}</span> })}
      </div>
    </Sec>}
    {recentNotes.length>0 && <Sec title={`Kurzrückblick (letzte ${recentNotes.length})`}>
      {recentNotes.map(n => (
        <div key={n.id} style={{padding:'8px 11px',background:C.beL,borderRadius:7,marginBottom:6,borderLeft:`2px solid ${C.wg}`}}>
          <div style={{fontSize:10,color:C.tL,marginBottom:3,textTransform:'uppercase',letterSpacing:.5}}>{n.date}</div>
          <div style={{fontSize:12.5,lineHeight:1.5,color:C.s}}>{stripH(n.html).slice(0,100)}{stripH(n.html).length>100?'…':''}</div>
        </div>
      ))}
    </Sec>}
  </>
}

// ── Verlauf Tab ───────────────────────────────────────────────
function VTab({ contact, upd, userEmail }) {
  const [showEditor,  setShowEditor]  = useState(false)
  const [showActForm, setShowActForm] = useState(false)
  const [expanded,    setExpanded]    = useState({})
  const tl = [...(contact.timeline||[])].sort((a,b) => (b.ts||b.date||'').localeCompare(a.ts||a.date||''))
  const author = userEmail ? userEmail.split('@')[0] : 'Team'

  const addNote = (html) => { upd({timeline:[...(contact.timeline||[]),{id:uid(),type:'note',html,date:today(),ts:new Date().toISOString(),author}]}); setShowEditor(false) }
  const addAct  = (act)  => {
    const te = {id:uid(),type:'activity',...act,completed:false,ts:new Date().toISOString(),author}
    const updates = {timeline:[...(contact.timeline||[]),te]}
    if(act.actType==='offboarding'&&act.date) updates.offboardingDate = act.date
    upd(updates); setShowActForm(false)
  }
  const completeAct = (id) => upd({timeline:(contact.timeline||[]).map(e=>e.id===id?{...e,completed:true,completedDate:today(),completedBy:author}:e)})
  const del = (id) => upd({timeline:(contact.timeline||[]).filter(e=>e.id!==id)})
  const tog = (id) => setExpanded(p=>({...p,[id]:!p[id]}))

  return (
    <div style={{display:'flex',flexDirection:'column',gap:10}}>
      <div style={{display:'flex',gap:8}}>
        <button onClick={()=>{setShowEditor(true);setShowActForm(false)}} style={{flex:1,padding:'7px',border:`1px solid ${C.bo}`,borderRadius:7,cursor:'pointer',background:showEditor?C.be:C.beL,color:showEditor?C.br:C.s,fontSize:12,fontWeight:500}}>+ Notiz</button>
        <button onClick={()=>{setShowActForm(true);setShowEditor(false)}} style={{flex:1,padding:'7px',border:`1px solid ${C.bo}`,borderRadius:7,cursor:'pointer',background:showActForm?C.be:C.beL,color:showActForm?C.br:C.s,fontSize:12,fontWeight:500}}>+ Aktivität</button>
      </div>
      {showEditor  && <RichEditor defaultValue="" onSave={addNote} onCancel={()=>setShowEditor(false)}/>}
      {showActForm && <ActivityForm onSave={addAct} onCancel={()=>setShowActForm(false)} userEmail={userEmail}/>}
      {tl.map(entry => {
        if (entry.type === 'note') {
          const exp = expanded[entry.id]
          const preview = stripH(entry.html).slice(0,85)
          return (
            <div key={entry.id} style={{background:C.beL,borderRadius:8,border:`1px solid ${C.bo}`,overflow:'hidden'}}>
              <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'9px 12px',cursor:'pointer',gap:8}} onClick={()=>tog(entry.id)}>
                <div style={{flex:1,minWidth:0}}>
                  <div style={{fontSize:9.5,color:C.tL,marginBottom:2,display:'flex',gap:6,alignItems:'center'}}>
                    <span style={{textTransform:'uppercase',letterSpacing:.5}}>📝 {entry.date}</span>
                    {entry.author && <span style={{background:C.be,color:C.br,padding:'0px 6px',borderRadius:3,fontSize:9,fontWeight:500}}>{entry.author}</span>}
                  </div>
                  {!exp && <div style={{fontSize:12.5,color:C.s,overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{preview}{preview.length>=85?'…':''}</div>}
                </div>
                <div style={{display:'flex',gap:5,alignItems:'center',flexShrink:0}}>
                  <span style={{fontSize:11,color:C.tL}}>{exp?'▲':'▼'}</span>
                  <button onClick={e=>{e.stopPropagation();del(entry.id)}} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:15,padding:0,lineHeight:1}}>×</button>
                </div>
              </div>
              {exp && <div className="rich" style={{padding:'0 12px 12px',fontSize:13,lineHeight:1.65,color:C.s}} dangerouslySetInnerHTML={{__html:entry.html}}/>}
            </div>
          )
        }
        if (entry.type === 'activity') {
          const act = ACTS.find(a=>a.id===entry.actType)||{l:entry.actType,e:'📌'}
          const ovd = !entry.completed && isExp(entry.date)
          return (
            <div key={entry.id} style={{background:ovd?'#fffbf0':C.beL,border:`1.5px solid ${ovd?'#d97706':C.bo}`,borderRadius:8,padding:'9px 12px',display:'flex',gap:10,alignItems:'flex-start'}}>
              <span style={{fontSize:18,marginTop:1,flexShrink:0}}>{act.e}</span>
              <div style={{flex:1,minWidth:0}}>
                <div style={{display:'flex',gap:5,alignItems:'center',marginBottom:2,flexWrap:'wrap'}}>
                  <span style={{fontWeight:500,fontSize:13}}>{entry.title}</span>
                  {ovd && <span style={{fontSize:9.5,background:'#d97706',color:C.w,padding:'1px 6px',borderRadius:3,fontWeight:700}}>ÜBERFÄLLIG</span>}
                  {entry.completed && <span style={{fontSize:9.5,background:C.ok,color:C.w,padding:'1px 6px',borderRadius:3}}>✓ Erledigt</span>}
                </div>
                <div style={{fontSize:11,color:C.tL,display:'flex',gap:6,flexWrap:'wrap',alignItems:'center'}}>
                  <span>{act.l} · {entry.date}{entry.time?' · '+entry.time:''}</span>
                  {entry.assignee && <span style={{background:'#e6effc',color:'#1e5fad',padding:'0px 6px',borderRadius:3,fontSize:10,fontWeight:500}}>→ {entry.assignee}</span>}
                  {entry.author && entry.author!==entry.assignee && <span style={{background:C.be,color:C.br,padding:'0px 6px',borderRadius:3,fontSize:10,fontWeight:500}}>{entry.author}</span>}
                  {entry.completed && entry.completedDate && <span>· Erledigt: {entry.completedDate}{entry.completedBy?' von '+entry.completedBy:''}</span>}
                </div>
              </div>
              <div style={{display:'flex',gap:5,alignItems:'center',flexShrink:0}}>
                {!entry.completed && <button onClick={()=>completeAct(entry.id)} style={{padding:'3px 8px',border:`1px solid ${C.ok}`,borderRadius:5,cursor:'pointer',background:C.okBg,color:C.ok,fontSize:11}}>✓</button>}
                <button onClick={()=>del(entry.id)} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:15,padding:0,lineHeight:1}}>×</button>
              </div>
            </div>
          )
        }
        if (entry.type === 'status') {
          return (
            <div key={entry.id} style={{display:'flex',gap:8,alignItems:'center',padding:'5px 10px',borderRadius:6}}>
              <span style={{width:6,height:6,borderRadius:'50%',background:C.wg,flexShrink:0}}/>
              <span style={{fontSize:11.5,color:C.tL,flex:1}}>{entry.date} · <strong style={{color:C.s}}>{entry.field}:</strong> {entry.from} → <strong style={{color:C.br}}>{entry.to}</strong></span>
              <button onClick={()=>del(entry.id)} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:13,padding:0}}>×</button>
            </div>
          )
        }
        return null
      })}
      {tl.length===0&&!showEditor&&!showActForm && <div style={{textAlign:'center',padding:24,color:C.tL,fontSize:13}}>Noch kein Verlauf vorhanden</div>}
    </div>
  )
}

// ── Products Tab ──────────────────────────────────────────────
function PTab({ contact, prodCat, upd }) {
  const [selProd, setSelProd] = useState('')
  const [bonus, setBonus]     = useState('')
  const [purchDate, setPurchDate] = useState(todayISO())
  const addProd = () => {
    const cat = prodCat.find(x=>x.id===selProd); if(!cat)return
    const dt = purchDate ? toDE(purchDate) : today()
    upd({products:[...contact.products,{id:uid(),catalogId:cat.id,name:cat.name,price:cat.price,date:dt,bonuses:bonus.trim()?[bonus.trim()]:[]}]})
    setSelProd(''); setBonus(''); setPurchDate(todayISO())
  }
  return (
    <div style={{display:'flex',flexDirection:'column',gap:10}}>
      {contact.products.map(p => {
        const cat=prodCat.find(x=>x.id===p.catalogId), col=gc(cat?.color)
        return (
          <div key={p.id} style={{background:C.beL,borderRadius:9,padding:'10px 13px',border:`1px solid ${col.bo}`}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start'}}>
              <div>
                <span style={{background:col.bg,color:col.tx,padding:'2px 9px',borderRadius:4,fontSize:12,fontWeight:500}}>{p.name}</span>
                {p.date&&<span style={{fontSize:11,color:C.tL,marginLeft:8}}>Gekauft: {p.date}</span>}
                {p.bonuses?.length>0&&<div style={{fontSize:11,color:C.br,marginTop:4}}>{p.bonuses.join(' · ')}</div>}
              </div>
              <div style={{display:'flex',alignItems:'center',gap:8}}>
                <span style={{fontWeight:700,color:C.ok,fontSize:14}}>{p.price.toLocaleString('de-DE')} €</span>
                <Xb onClick={()=>upd({products:contact.products.filter(x=>x.id!==p.id)})}/>
              </div>
            </div>
          </div>
        )
      })}
      <div style={{display:'flex',flexDirection:'column',gap:7,padding:'12px 14px',background:C.beL,borderRadius:10,border:`1px dashed ${C.bo}`}}>
        <select value={selProd} onChange={e=>setSelProd(e.target.value)} style={{...IS,width:'100%',padding:'7px 10px',background:C.w}}>
          <option value="">Produkt auswählen …</option>
          {prodCat.map(p=><option key={p.id} value={p.id}>{p.name} – {p.price.toLocaleString('de-DE')} €</option>)}
        </select>
        <div style={{display:'flex',alignItems:'center',gap:8}}>
          <span style={{fontSize:12,color:C.tL,flexShrink:0}}>Kaufdatum</span>
          <input type="date" value={purchDate} onChange={e=>setPurchDate(e.target.value)} style={{...IS,flex:1}}/>
          <span style={{fontSize:11,color:C.tL}}>(leer = heute)</span>
        </div>
        <textarea value={bonus} onChange={e=>setBonus(e.target.value)} placeholder="Infos (optional) – z.B. Bonus, Besonderheiten …"
          style={{...IS,resize:'vertical',minHeight:52,padding:'7px 10px',fontSize:12,lineHeight:1.5}}/>
        <Abtn onClick={addProd}/>
      </div>
    </div>
  )
}

// ── Webinars Tab ──────────────────────────────────────────────
function WTab({ contact, webCat, upd }) {
  const [selWeb, setSelWeb] = useState('')
  const addWeb = () => {
    const cat = webCat.find(x=>x.id===selWeb); if(!cat)return
    if(contact.webinars.find(w=>w.catalogId===cat.id))return
    upd({webinars:[...contact.webinars,{id:uid(),catalogId:cat.id,name:cat.name,date:today()}]}); setSelWeb('')
  }
  return (
    <div style={{display:'flex',flexDirection:'column',gap:8}}>
      {contact.webinars.map(w => { const col=gc(webCat.find(x=>x.id===w.catalogId)?.color||'blau'); return (
        <div key={w.id} style={{background:C.beL,borderRadius:9,padding:'9px 13px',display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <span style={{background:col.bg,color:col.tx,border:`1px solid ${col.bo}`,padding:'2px 9px',borderRadius:4,fontSize:12,fontWeight:500}}>{w.name}</span>
          <Xb onClick={()=>upd({webinars:contact.webinars.filter(x=>x.id!==w.id)})}/>
        </div>
      )})}
      <div style={{display:'flex',gap:6,marginTop:4}}>
        <select value={selWeb} onChange={e=>setSelWeb(e.target.value)} style={{...IS,flex:1,padding:'7px 10px',background:C.w}}>
          <option value="">Webinar auswählen …</option>
          {webCat.filter(w=>!contact.webinars.find(cw=>cw.catalogId===w.id)).map(w=><option key={w.id} value={w.id}>{w.name}</option>)}
        </select>
        <Abtn onClick={addWeb}/>
      </div>
    </div>
  )
}

// ── Rich Text Editor ──────────────────────────────────────────
function RichEditor({ defaultValue, onSave, onCancel }) {
  const ref = useRef(null)
  useEffect(() => { if(ref.current){ref.current.innerHTML=defaultValue||'';setTimeout(()=>ref.current?.focus(),60)} }, []) // eslint-disable-line
  const ex = (cmd, val) => { ref.current?.focus(); document.execCommand(cmd, false, val||null) }
  const mkLink = () => { const u=prompt('URL:','https://'); if(u&&u.length>8)ex('createLink',u) }
  const TB = ({cmd,ch,st}) => <button className="tbe" onMouseDown={e=>{e.preventDefault();ex(cmd)}} style={st||{}}>{ch}</button>
  return (
    <div style={{border:`1px solid ${C.bo}`,borderRadius:9,overflow:'hidden',boxShadow:'0 2px 8px rgba(0,0,0,.06)'}}>
      <div style={{display:'flex',gap:3,padding:'5px 8px',background:'#f8f5f2',borderBottom:`1px solid ${C.bo}`,flexWrap:'wrap',alignItems:'center'}}>
        <TB cmd="bold"      ch="B" st={{fontWeight:700}}/>
        <TB cmd="italic"    ch="I" st={{fontStyle:'italic'}}/>
        <TB cmd="underline" ch="U" st={{textDecoration:'underline'}}/>
        <span style={{width:1,background:C.bo,height:18,margin:'0 2px'}}/>
        <TB cmd="insertUnorderedList" ch="•≡"/>
        <TB cmd="insertOrderedList"   ch="1."/>
        <span style={{width:1,background:C.bo,height:18,margin:'0 2px'}}/>
        <button className="tbe" onMouseDown={e=>{e.preventDefault();mkLink()}}>🔗</button>
        <select style={{height:24,fontSize:11,border:`1px solid ${C.bo}`,borderRadius:4,padding:'0 5px',color:C.s,background:C.w,outline:'none'}} onChange={e=>ex('fontSize',e.target.value)} onMouseDown={e=>e.stopPropagation()}>
          <option value="3">Normal</option><option value="2">Klein</option><option value="4">Groß</option><option value="5">XL</option>
        </select>
      </div>
      <div ref={ref} contentEditable suppressContentEditableWarning data-ph="Notiz eingeben …" className="rich"
        style={{minHeight:90,maxHeight:220,overflowY:'auto',padding:'10px 12px',fontSize:13,lineHeight:1.65,color:C.s,background:'#fffef8'}}/>
      <div style={{display:'flex',justifyContent:'flex-end',gap:8,padding:'7px 10px',borderTop:`1px solid ${C.bo}`,background:'#f8f5f2'}}>
        <button onClick={onCancel} style={{padding:'5px 14px',border:`1px solid ${C.bo}`,borderRadius:6,cursor:'pointer',background:'none',color:C.tL,fontSize:12}}>Abbrechen</button>
        <button onClick={()=>onSave(ref.current?.innerHTML||'')} style={{padding:'5px 16px',background:C.ok,color:C.w,border:'none',borderRadius:6,cursor:'pointer',fontSize:12,fontWeight:500}}>Speichern</button>
      </div>
    </div>
  )
}

// ── Activity Form ─────────────────────────────────────────────
function ActivityForm({ onSave, onCancel, userEmail }) {
  const [title,   setTitle]   = useState('')
  const [actType, setActType] = useState('task')
  const [date,    setDate]    = useState(todayISO())
  const [time,    setTime]    = useState('')
  const [assignee,setAssignee]= useState(userEmail?.split('@')[0]||'')
  const [err,     setErr]     = useState('')
  const save = () => {
    if(!title.trim()) { setErr('Bitte Titel eingeben'); return }
    if(!date) { setErr('Bitte Datum wählen'); return }
    onSave({actType, title:title.trim(), date:toDE(date), time, assignee:assignee.trim()||userEmail?.split('@')[0]||''})
  }
  return (
    <div style={{border:`1px solid ${C.bo}`,borderRadius:9,overflow:'hidden',background:C.w,boxShadow:'0 2px 8px rgba(0,0,0,.06)'}}>
      <div style={{padding:'12px 14px',borderBottom:`1px solid ${C.bo}`,display:'flex',flexDirection:'column',gap:10}}>
        <input value={title} onChange={e=>{setTitle(e.target.value);setErr('')}} placeholder="Titel eingeben (Pflichtfeld) *"
          style={{...IS,width:'100%',padding:'8px 12px',border:`1px solid ${err&&!title.trim()?C.er:C.bo}`}} onKeyDown={e=>e.key==='Enter'&&save()}/>
        <div style={{display:'flex',gap:5,flexWrap:'wrap'}}>
          {ACTS.map(a=>(
            <button key={a.id} onClick={()=>setActType(a.id)}
              style={{display:'flex',alignItems:'center',gap:4,padding:'4px 9px',border:`1px solid ${actType===a.id?C.br:C.bo}`,borderRadius:6,cursor:'pointer',background:actType===a.id?C.be:'transparent',color:actType===a.id?C.br:C.tL,fontSize:11,fontWeight:actType===a.id?500:400,whiteSpace:'nowrap'}}>
              <span style={{fontSize:12}}>{a.e}</span>{a.l}
            </button>
          ))}
        </div>
        <div style={{display:'flex',gap:8}}>
          <input type="date" value={date} onChange={e=>setDate(e.target.value)} style={{...IS,flex:2}}/>
          <input type="time" value={time} onChange={e=>setTime(e.target.value)} style={{...IS,width:100}}/>
        </div>
        <div style={{display:'flex',alignItems:'center',gap:8}}>
          <span style={{fontSize:12,color:C.tL,flexShrink:0}}>Zugewiesen an:</span>
          <input value={assignee} onChange={e=>setAssignee(e.target.value)} placeholder="Name oder E-Mail"
            style={{...IS,flex:1,fontSize:12}}/>
        </div>
        {actType==='offboarding'&&<div style={{fontSize:11.5,color:C.er,background:'#fff5f5',padding:'6px 10px',borderRadius:6}}>⚠️ Offboarding: Kachel wird rot wenn Datum abläuft.</div>}
        {err&&<div style={{fontSize:12,color:C.er}}>{err}</div>}
      </div>
      <div style={{display:'flex',justifyContent:'flex-end',gap:8,padding:'8px 12px',background:'#f8f5f2'}}>
        <button onClick={onCancel} style={{padding:'5px 14px',border:`1px solid ${C.bo}`,borderRadius:6,cursor:'pointer',background:'none',color:C.tL,fontSize:12}}>Abbrechen</button>
        <button onClick={save} className="bp" style={{padding:'5px 16px',background:C.br,color:C.w,border:'none',borderRadius:6,cursor:'pointer',fontSize:12,fontWeight:500,transition:'background .15s'}}>Planen</button>
      </div>
    </div>
  )
}

// ── Modals ────────────────────────────────────────────────────
function AddModal({ onAdd, onClose }) {
  const [f, setF] = useState({name:'',email:'',phone:''})
  const sub = () => { if(!f.name.trim())return; onAdd(f); onClose() }
  return <MModal title="Neuer Kontakt" onClose={onClose}>
    {[['name','Name *','text'],['email','E-Mail','email'],['phone','Telefon','tel']].map(([k,p,t])=>(
      <input key={k} type={t} value={f[k]} onChange={e=>setF({...f,[k]:e.target.value})} placeholder={p}
        onKeyDown={e=>e.key==='Enter'&&sub()} style={{...IS,display:'block',width:'100%',marginBottom:10,padding:'9px 12px'}}/>
    ))}
    <div style={{display:'flex',gap:8,marginTop:8}}>
      <button onClick={onClose} style={{flex:1,padding:'9px',border:`1px solid ${C.bo}`,borderRadius:8,cursor:'pointer',background:'none',color:C.tL,fontSize:13}}>Abbrechen</button>
      <button onClick={sub} className="bp" style={{flex:1,padding:'9px',background:C.br,color:C.w,border:'none',borderRadius:8,cursor:'pointer',fontSize:13,fontWeight:500,transition:'background .15s'}}>Erstellen</button>
    </div>
  </MModal>
}
function TidyModal({ onAdd, onClose }) {
  const [f, setF] = useState({name:'',email:'',phone:'',note:''})
  const sub = () => { if(!f.name.trim()||!f.email.trim())return; onAdd(f) }
  return <MModal title="📅 TidyCal-Termin" onClose={onClose}>
    <div style={{fontSize:12,color:C.tL,marginBottom:14,lineHeight:1.6}}>Simuliert eine eingehende TidyCal-Buchung → landet in Closing · Strategiegespräch.</div>
    {[['name','Name *','text'],['email','E-Mail *','email'],['phone','Telefon','tel'],['note','Buchungsnotiz','text']].map(([k,p,t])=>(
      <input key={k} type={t} value={f[k]} onChange={e=>setF({...f,[k]:e.target.value})} placeholder={p}
        onKeyDown={e=>e.key==='Enter'&&sub()} style={{...IS,display:'block',width:'100%',marginBottom:10,padding:'9px 12px'}}/>
    ))}
    <div style={{display:'flex',gap:8,marginTop:8}}>
      <button onClick={onClose} style={{flex:1,padding:'9px',border:`1px solid ${C.bo}`,borderRadius:8,cursor:'pointer',background:'none',color:C.tL,fontSize:13}}>Abbrechen</button>
      <button onClick={sub} className="bp" style={{flex:1,padding:'9px',background:C.br,color:C.w,border:'none',borderRadius:8,cursor:'pointer',fontSize:13,fontWeight:500,transition:'background .15s'}}>Eintragen</button>
    </div>
  </MModal>
}
function MModal({ title, children, onClose }) {
  return (
    <div style={{position:'fixed',inset:0,background:'rgba(26,20,16,.35)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:200}}>
      <div style={{background:C.w,borderRadius:16,padding:26,width:360,boxShadow:'0 24px 64px rgba(0,0,0,.18)'}}>
        <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:21,fontWeight:600,marginBottom:18,color:C.s}}>{title}</div>
        {children}
      </div>
    </div>
  )
}

// ── Helpers ───────────────────────────────────────────────────
function Loader() { return <div style={{height:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:C.beL}}><span style={{color:C.br,fontSize:12,letterSpacing:3}}>LADEN …</span></div> }
function Sec({title,children}){return<div><div style={{fontSize:10,textTransform:'uppercase',letterSpacing:1,color:C.tL,marginBottom:7,fontWeight:500}}>{title}</div>{children}</div>}
function IR({label,value}){return<div style={{display:'flex',justifyContent:'space-between',padding:'5px 0',borderBottom:`1px solid ${C.bo}`,fontSize:12.5}}><span style={{color:C.tL}}>{label}</span><span style={{color:C.s}}>{value}</span></div>}
function STag({text}){return<span style={{background:C.be,color:C.br,padding:'1px 5px',borderRadius:3,fontSize:10.5,fontWeight:500,whiteSpace:'nowrap'}}>{text}</span>}
function Xb({onClick}){return<button onClick={onClick} style={{background:'none',border:'none',cursor:'pointer',color:C.tL,fontSize:15,padding:'0 2px',lineHeight:1}}>×</button>}
function Abtn({onClick}){return<button onClick={onClick} className="bp" style={{padding:'7px 14px',background:C.br,color:C.w,border:'none',borderRadius:8,cursor:'pointer',fontSize:14,fontWeight:500,transition:'background .15s'}}>+</button>}

// ── Start ─────────────────────────────────────────────────────
ReactDOM.createRoot(document.getElementById('root')).render(<Root />)
</script>
</body>
</html>
