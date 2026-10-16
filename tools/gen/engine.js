/* Game engine shared by the topics. Injected before it: LANG, EDITION, TOPIC_KEY, OTHER, SHEET, WORLDS, TX, LV, STAGE */
const UK=LANG==='uk';
const KEY='ponya-bulya-'+TOPIC_KEY+'-'+LANG+'-v1';
const PKEY='ponya-bulya-profile-v1';
let P={name:'',g:'',world:'meadow',names:{}};
let firstVisit=true;
try{const s=JSON.parse(localStorage.getItem(PKEY)||'null');if(s){P=Object.assign(P,s);firstVisit=false}}catch(e){}
if(!P.names||typeof P.names!=='object')P.names={};
if(!WORLDS[P.world])P.world='meadow';
function saveP(){try{localStorage.setItem(PKEY,JSON.stringify(P))}catch(e){}}
const esc=t=>String(t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const W=()=>WORLDS[P.world];
const heroName=r=>{const c=((P.names[P.world]||{})[r]||'').trim();return esc(c||W().roles[r].name[LANG])};
const SVGR=r=>W().roles[r].svg;
const $=s=>document.querySelector(s);
const ROLES=['hostA','hostB','tidy','messy'];
const LEVELS=['a','b','c'];

/* ---------- numbers ---------- */
const fnum=v=>{let s=String(Math.round(v*1e9)/1e9);if(UK)s=s.replace('.',',');return s.replace('-','−')};
function parseNum(s){
  s=String(s).trim().replace(/[−–—]/g,'-').replace(/\s+/g,' ').replace(/°/g,'');
  if(s==='')return null;
  let m=s.match(/^(-?)(\d+) (\d+)\/(\d+)$/);            // mixed number 1 4/5
  if(m){const v=+m[2]+(+m[3])/(+m[4]);return m[1]?-v:v}
  m=s.match(/^(-?\d+(?:[.,]\d+)?)\s*\/\s*(-?\d+(?:[.,]\d+)?)$/); // fraction 81/256
  if(m){const d=Number(m[2].replace(',','.'));if(!d)return null;return Number(m[1].replace(',','.'))/d}
  s=s.replace(',','.');
  if(!/^-?(\d+\.?\d*|\.\d+)$/.test(s))return null;
  return Number(s);
}
const same=(a,b)=>a!==null&&b!==null&&b!==undefined&&Math.abs(a-b)<=1e-9*Math.max(1,Math.abs(b));

/* ---------- texts ---------- */
const BASE={uk:{
  langLink:'<a href="'+OTHER+'">English version</a>'+(SHEET?' · <a href="'+SHEET+'">Шпаргалка окремо</a>':''),
  yourStars:'Твої зірки:',resetAll:'Почати все спочатку',resetSure:'Точно? Натисни ще раз',
  tabLearn:'Урок',tabR:'Мій звіт',
  next:'Далі',check:'Перевірити',hint:'Підказка: ',typeNum:'Заповни всі клітинки числами.',
  task:(i,n)=>`Завдання ${i} з ${n}`,done:'Рівень пройдено',
  stepDone:'Крок зроблено!',orderReset:'Скинути',orderHint:'Натискай картки по черзі, щоб скласти їх у правильному порядку.',
  orderFill:'Розклади всі картки.',
  toB:'До рівня 2',toC:'До рівня 3',toR:'Подивитися мій звіт',levelReset:'Почати рівень заново',
  rH:'Мій звіт',copy:'Скопіювати звіт',copyFail:'Автоматично скопіювати не вийшло. Текст звіту виділено нижче: скопіюй його вручну.',
  first:'з першої спроби',nth:n=>`з ${n}-ї спроби`,withHint:', з підказкою',notYet:n=>`ще не розв’язано (${n} ${plUK(n,['спроба','спроби','спроб'])})`,
  repStars:s=>`Зірки: ${s} з 3.`,repSum:(a,b,c,d)=>`Розв’язано ${a} з ${b} задач, з першої спроби: ${c}. Підказки були в ${d}.`,
  complete:'пройдено',locale:'uk-UA',bad:'Ще не так.',
  heap:k=>`Ще ${k} ${plUK(k,['картка','картки','карток'])}`,count:(k,n)=>`${k} з ${n}`,
  notTried:'{me:ще не робив:ще без спроб:ще без спроб}',notStarted:'{me:ще не почав:ще не почато:ще не почато}',
  repDates:(a,b)=>`${P.g==='m'?'Почав':P.g==='f'?'Почала':'Початок'}: ${a}. Остання спроба: ${b}.`
},en:{
  langLink:'<a href="'+OTHER+'">Українська версія</a>'+(SHEET?' · <a href="'+SHEET+'">Cheat sheet on its own</a>':''),
  yourStars:'Your stars:',resetAll:'Start everything again',resetSure:'Sure? Tap again',
  tabLearn:'Lesson',tabR:'My report',
  next:'Next',check:'Check',hint:'Hint: ',typeNum:'Fill in all the boxes with numbers.',
  task:(i,n)=>`Task ${i} of ${n}`,done:'Level complete',
  stepDone:'Step done!',orderReset:'Start again',orderHint:'Tap the cards one by one to put them in the right order.',
  orderFill:'Place all the cards first.',
  toB:'On to level 2',toC:'On to level 3',toR:'See my report',levelReset:'Start this level again',
  rH:'My report',copy:'Copy my report',copyFail:'Couldn\'t copy automatically. The report text is selected below: copy it by hand.',
  first:'first try',nth:n=>`on attempt ${n}`,withHint:', with a hint',notYet:n=>`not solved yet (${n} ${n===1?'attempt':'attempts'})`,
  repStars:s=>`Stars: ${s} of 3.`,repSum:(a,b,c,d)=>`Solved ${a} of ${b} problems, ${c} on the first try. Hints used on ${d}.`,
  complete:'complete',locale:'en-GB',bad:'Not quite.',
  heap:k=>`${k} ${k===1?'card':'cards'} to go`,count:(k,n)=>`${k} of ${n}`,
  notTried:'not tried yet',notStarted:'not started yet',
  repDates:(a,b)=>`Started: ${a}. Last attempt: ${b}.`
}}[LANG];
function plUK(n,f){const a=n%10,b=n%100;return a===1&&b!==11?f[0]:(a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2])}
/* templates: {hostA} names, {g:role:m:f} hero gender, {me:m:f:x} pupil's form of address */
function tpl(s){
  if(typeof s!=='string')return s;
  return s.replace(/\{(hostA|hostB|tidy|messy)\}/g,(_,r)=>heroName(r))
    .replace(/\{g:(hostA|hostB|tidy|messy):([^:}]*):([^}]*)\}/g,(_,r,m,f)=>W().roles[r].g==='f'?f:m)
    .replace(/\{me:([^:}]*):([^:}]*):([^}]*)\}/g,(_,m,f,x)=>P.g==='m'?m:P.g==='f'?f:x);
}
let S;
function buildS(){
  const w=TX.worlds[P.world];S=Object.assign({},BASE);
  for(const k in TX)if(k!=='worlds'&&k!=='h1')S[k]=TX[k];
  for(const k in w)S[k]=w[k];
  for(const k in S)if(typeof S[k]==='string')S[k]=tpl(S[k]);
  S.h1=TX.h1[P.world];
  S.lvA=S.tabA.replace(/^\d\.\s*/,'');S.lvB=S.tabB.replace(/^\d\.\s*/,'');S.lvC=S.tabC.replace(/^\d\.\s*/,'');
  const nm=P.name.trim();
  S.repHead=[S.repHead,nm?(UK?`Ім’я: ${nm}.`:`Name: ${nm}.`):'',(UK?'Світ: ':'World: ')+W().label[LANG]+'.'].filter(Boolean).join(' ');
}
const PS={uk:{profBtn:'Вибрати світ і ім’я',profBtn2:'Змінити світ або ім’я',wbTitle:w=>`Твій світ: ${w}`,wbNew:'Можна вибрати один із трьох світів (луг, космос, цеглинки), вписати своє ім’я і перейменувати героїв.',wbHas:n=>`Грає: ${n}. Світ, ім’я й героїв можна змінити будь-коли.`,profH:'Твій профіль',nameL:'Як тебе звати?',namePh:'Ім’я',addrL:'Як до тебе звертатися?',addrM:'Я хлопчик',addrF:'Я дівчинка',addrN:'Не вказувати',worldL:'Вибери світ',heroesL:'Імена героїв (можна змінити)',heroesReset:'Повернути звичні імена',done:'Готово',tip:'Профіль зберігається лише в браузері на цьому пристрої. Прогрес у рівнях не зникне, якщо змінити світ.'},
 en:{profBtn:'Choose a world and name',profBtn2:'Change world or name',wbTitle:w=>`Your world: ${w}`,wbNew:'You can pick one of three worlds (meadow, space, bricks), add your name and rename the heroes.',wbHas:n=>`Player: ${n}. You can change the world, your name and the heroes any time.`,profH:'Your profile',nameL:'What\'s your name?',namePh:'Name',addrL:'How should we talk to you?',addrM:'I\'m a boy',addrF:'I\'m a girl',addrN:'Rather not say',worldL:'Choose a world',heroesL:'Hero names (you can change them)',heroesReset:'Bring back the usual names',done:'Done',tip:'Your profile is saved only in the browser on this device. Your progress stays when you change the world.'}}[LANG];
function applyTexts(){
  buildS();
  document.querySelectorAll('[data-t]').forEach(el=>{const v=S[el.dataset.t];if(v!==undefined)el.innerHTML=v});
  $('#resetAll').textContent=S.resetAll;
  const nm=P.name.trim();
  $('#profBtn').textContent=nm?PS.profBtn2:PS.profBtn;
  $('#wbTitle').textContent=PS.wbTitle(W().label[LANG]);
  $('#wbSub').textContent=nm?PS.wbHas(nm):PS.wbNew;
  $('#wbMini').innerHTML=Object.values(WORLDS).map(w=>w.roles.messy.svg).join('');
  document.querySelectorAll('[data-world]').forEach(g=>g.hidden=g.dataset.world!==P.world);
  document.querySelectorAll('[data-hero]').forEach(el=>el.innerHTML=SVGR(el.dataset.hero));
  document.querySelectorAll('[data-name]').forEach(el=>el.innerHTML=heroName(el.dataset.name));
}
buildS();

/* ---------- characters & profile ---------- */
function renderCast(){
  $('#heroCast').innerHTML=ROLES.map(r=>`<div class="who">${SVGR(r)}<span class="nm">${heroName(r)}</span></div>`).join('');
  $('#meet').innerHTML=S.meet.map(([r,t])=>`<div class="card">${SVGR(r)}<p><b>${heroName(r)}</b><br>${tpl(t)}</p></div>`).join('');
  document.querySelectorAll('.notePig').forEach(n=>n.innerHTML=SVGR('hostA'));
}
let profOpen=false;
function renderProfile(){
  const box=$('#profile');box.hidden=!profOpen;if(!profOpen)return;
  const seg=[['m',PS.addrM],['f',PS.addrF],['',PS.addrN]].map(([v,l])=>`<button type="button" data-g="${v}" aria-pressed="${P.g===v}">${l}</button>`).join('');
  const worlds=Object.entries(WORLDS).map(([id,w])=>`<button type="button" class="wcard" data-w="${id}" aria-pressed="${P.world===id}"><span class="mini">${ROLES.map(r=>w.roles[r].svg).join('')}</span><b>${w.label[LANG]}</b><span>${w.blurb[LANG]}</span></button>`).join('');
  const nm=P.names[P.world]||{};
  const heroes=ROLES.map(r=>`<label>${SVGR(r)}<input id="hn-${r}" maxlength="16" autocomplete="off" placeholder="${esc(W().roles[r].name[LANG])}" value="${esc(nm[r]||'')}"></label>`).join('');
  box.innerHTML=`<h2>${PS.profH}</h2>
   <div class="pf-row"><b><label for="pfName">${PS.nameL}</label></b><input class="pf-name" id="pfName" maxlength="20" autocomplete="off" placeholder="${PS.namePh}" value="${esc(P.name)}"></div>
   <div class="pf-row"><b>${PS.addrL}</b><div class="seg">${seg}</div></div>
   <div class="pf-row"><b>${PS.worldL}</b><div class="worlds">${worlds}</div></div>
   <div class="pf-row"><b>${PS.heroesL}</b><div class="heroes">${heroes}</div><div><button type="button" class="btn ghost" id="hnReset">${PS.heroesReset}</button></div></div>
   <p class="pf-tip">${PS.tip}</p>
   <div><button type="button" class="btn" id="pfDone">${PS.done}</button></div>`;
  $('#pfName').oninput=e=>{P.name=e.target.value.slice(0,20);saveP();refresh(false)};
  box.querySelectorAll('[data-g]').forEach(b=>b.onclick=()=>{P.g=b.dataset.g;saveP();refresh(true)});
  box.querySelectorAll('[data-w]').forEach(b=>b.onclick=()=>{P.world=b.dataset.w;saveP();refresh(true)});
  ROLES.forEach(r=>{$('#hn-'+r).oninput=e=>{(P.names[P.world]=P.names[P.world]||{})[r]=e.target.value.slice(0,16);saveP();refresh(false)}});
  $('#hnReset').onclick=()=>{P.names[P.world]={};saveP();refresh(true)};
  $('#pfDone').onclick=()=>{profOpen=false;saveP();renderProfile();$('#profBtn').focus()};
}
$('#profBtn').onclick=()=>{profOpen=!profOpen;renderProfile();if(profOpen)$('#profile').scrollIntoView({block:'start'})};
function refresh(redrawProfile){
  applyTexts();renderCast();LEVELS.forEach(l=>renderLevel(l));stars();
  if(state.tab==='report')renderReport();
  if(redrawProfile)renderProfile();
}

/* ---------- state ---------- */
const fresh=()=>({tab:'learn',pos:{a:0,b:0,c:0},sub:{a:0,b:0,c:0},done:{a:false,b:false,c:false},log:{},firstAt:null,lastAt:null});
let state=fresh();
try{const s=JSON.parse(localStorage.getItem(KEY)||'null');if(s&&s.pos)state=Object.assign(state,s)}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}}
function rec(key,ok,hint){const e=state.log[key]||(state.log[key]={t:0,h:false,ok:false});if(e.ok)return;e.t++;if(hint)e.h=true;if(ok)e.ok=true;const now=Date.now();if(!state.firstAt)state.firstAt=now;state.lastAt=now;save()}
function clearLog(p){Object.keys(state.log).forEach(k=>{if(k[0]===p)delete state.log[k]})}
const tabs=['learn','a','b','c','report'];
function show(t){
  state.tab=t;save();if(t==='report')renderReport();
  tabs.forEach(x=>{$('#p-'+x).hidden=x!==t;$('#t-'+x).setAttribute('aria-selected',x===t)});
}
const go=t=>{show(t);window.scrollTo({top:0})};
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>show(b.dataset.tab));
document.addEventListener('click',e=>{const b=e.target.closest('[data-go]');if(b)go(b.dataset.go)});
function stars(){
  LEVELS.forEach(l=>$('#st-'+l).classList.toggle('on',!!state.done[l]));
  $('#diploma').hidden=!(state.done.a&&state.done.b&&state.done.c);
}
const dots=(n,i)=>`<div class="dots">${Array.from({length:n},(_,j)=>`<span class="dot ${j<i?'on':''} ${j===i?'cur':''}"></span>`).join('')}</div>`;
function hintBox(el,txt){el.hidden=false;el.innerHTML=S.hint+txt}

/* anonymous error types for the teacher (only on the site, where ponyaTrack exists) */
const sentErr=new Set();
function T(name){if(sentErr.has(name))return;sentErr.add(name);try{window.ponyaTrack&&window.ponyaTrack(name)}catch(e){}}

/* ---------- levels ---------- */
const GAP='<span class="gap"></span>';
function preHTML(s){return String(s||'').split(GAP).map(p=>p?`<span class="pre">${p}</span>`:'').join(GAP)}
const tries={a:0,b:0,c:0};
const locked={a:false,b:false,c:false};
let orderPick={a:[],b:[],c:[]};
function stageCtx(L,i,sub,finished){const tasks=LV[L].tasks;return {L,i,n:tasks.length,t:tasks[Math.min(i,tasks.length-1)],sub,finished,W:W(),S,tpl,heroName,SVGR}}
function renderLevel(L){
  const tasks=LV[L].tasks, box=$('#'+L+'Task'), st=$('#'+L+'Stage');
  if(state.done[L]||state.pos[L]>=tasks.length){
    state.done[L]=true;save();stars();
    st.innerHTML=STAGE[L](stageCtx(L,tasks.length,0,true));
    const nextBtn=L==='a'?`<button class="btn" data-go="b">${S.toB}</button>`:L==='b'?`<button class="btn" data-go="c">${S.toC}</button>`:`<button class="btn" data-go="report">${S.toR}</button>`;
    box.innerHTML=`<div class="step">${S.done}</div><h3>${S[L+'DoneH']}</h3><p>${S[L+'DoneP']}</p><div class="row">${nextBtn}</div>`;
    return;
  }
  const i=state.pos[L], t=tasks[i], sub=Math.min(state.sub[L]||0,t.steps.length-1), sp=t.steps[sub];
  locked[L]=false;
  st.innerHTML=STAGE[L](stageCtx(L,i,sub,false));
  let h=`<div class="step">${S.task(i+1,tasks.length)}</div>${dots(tasks.length,i)}`;
  if(t.teacher)h+=`<span class="teach">${TX.teacherTag}</span>`;
  if(t.q)h+=`<p class="tq">${tpl(t.q)}</p>`;
  if(t.show)h+=`<div class="big"><span class="q">${t.show}</span></div>`;
  if(sub>0)h+=`<div class="donesteps">${t.steps.slice(0,sub).map(s=>`<div class="ds">✓ ${s.ok||''}</div>`).join('')}</div>`;
  if(t.steps.length>1)h+=`<div class="stepno">${UK?'Крок':'Step'} ${sub+1}/${t.steps.length}</div>`;
  if(sp.p)h+=`<p class="sp">${tpl(sp.p)}</p>`;
  if(sp.type==='choice'){
    h+=`<div class="opts ${sp.style||''}">${sp.opts.map(([id,lab],k)=>`<button type="button" class="opt" data-opt="${id}" style="--c:${sp.colors?sp.colors[k]:'var(--sky)'}">${sp.icons?`<span class="oi">${sp.icons[k]}</span>`:''}<span>${lab}</span></button>`).join('')}</div>`;
  }else if(sp.type==='num'){
    h+=`<div class="eqrow">${sp.f.map((f,k)=>`${preHTML(f.pre)}<input class="ans ${f.sup?'sup':''} ${f.wide?'wide':''}" id="${L}f${k}" inputmode="${f.text?'text':'decimal'}" autocomplete="off" aria-label="${esc(f.aria||(UK?'відповідь':'answer'))}">${f.post?`<span class="pre">${f.post}</span>`:''}`).join('')}</div>`;
    if(sp.tip)h+=`<p class="tip">${sp.tip}</p>`;
    h+=`<div class="row"><button class="btn" id="${L}Check">${S.check}</button></div>`;
  }else if(sp.type==='order'){
    const pick=orderPick[L];
    const pool=sp.mix.filter(k=>!pick.includes(k));
    h+=`<div class="oline" aria-live="polite">${pick.map((k,j)=>`<button type="button" class="ocard on" data-un="${j}"><b>${j+1}</b> ${sp.cards[k]}</button>`).join('')||`<span class="tip">${S.orderHint}</span>`}</div>
     <div class="opool">${pool.map(k=>`<button type="button" class="ocard" data-pk="${k}">${sp.cards[k]}</button>`).join('')}</div>
     <div class="row"><button class="btn" id="${L}Check">${S.check}</button><button class="btn ghost" id="${L}OReset">${S.orderReset}</button></div>`;
  }
  h+=`<div class="fb" id="${L}Fb" aria-live="polite"></div><div class="hint" id="${L}Hint" hidden></div><div id="${L}Next"></div>`;
  box.innerHTML=h;
  const fb=$('#'+L+'Fb'), hint=$('#'+L+'Hint'), key=L+i;
  const wrong=(msg,tags)=>{
    tries[L]++;
    (tags||[]).forEach(tg=>T(`err-${key}-${tg}`));
    rec(key,false,true);fb.className='fb bad pop';fb.innerHTML=msg||S.bad;
    hintBox(hint,tpl(tries[L]>=2&&sp.h[1]?sp.h[1]:sp.h[0]));
  };
  const right=()=>{
    tries[L]=0;orderPick[L]=[];
    if(sub<t.steps.length-1){
      locked[L]=true;fb.className='fb good pop';fb.textContent=S.stepDone;
      state.sub[L]=sub+1;save();setTimeout(()=>renderLevel(L),750);return;
    }
    rec(key,true,false);locked[L]=true;
    state.pos[L]=i+1;state.sub[L]=0;save();
    const sc=stageCtx(L,i+1,0,i+1>=tasks.length);sc.t=t;sc.sub=t.steps.length;sc.solved=true;st.innerHTML=STAGE[L](sc);
    fb.className='fb good pop';fb.innerHTML=`${tpl(S[L+'Good']||'✓')} ${t.after?tpl(t.after):''}`;
    box.querySelectorAll('input,.opt,.ocard,#'+L+'Check').forEach(x=>x.disabled=true);
    hint.hidden=true;
    $('#'+L+'Next').innerHTML=`<button class="btn" id="${L}Go">${S.next}</button>`;
    $('#'+L+'Go').onclick=()=>{renderLevel(L);box.scrollIntoView({block:'nearest'})};$('#'+L+'Go').focus({preventScroll:true});
  };
  if(sp.type==='choice'){
    box.querySelectorAll('[data-opt]').forEach(b=>b.onclick=()=>{
      if(locked[L])return;const o=b.dataset.opt;
      box.querySelectorAll('[data-opt]').forEach(x=>x.classList.remove('picked','badpick'));
      if(o===String(sp.ans)){b.classList.add('picked');right()}
      else{b.classList.add('badpick');wrong(sp.bad&&sp.bad[o]?tpl(sp.bad[o]):null,[(sp.tag&&sp.tag[o])||('chose-'+o)])}
    });
  }else if(sp.type==='num'){
    const check=()=>{
      if(locked[L])return;
      const vals=sp.f.map((f,k)=>parseNum($('#'+L+'f'+k).value));
      if(vals.some(v=>v===null)){fb.className='fb bad pop';fb.textContent=S.typeNum;return}
      const tags=[];let ok=true;
      sp.f.forEach((f,k)=>{
        const acc=[].concat(f.ans), good=acc.some(a=>same(vals[k],a));
        $('#'+L+'f'+k).classList.toggle('ok',good);$('#'+L+'f'+k).classList.toggle('bad',!good);
        if(!good){ok=false;const tr=(sp.traps||[]).find(([fi,v])=>fi===k&&same(vals[k],v));tags.push(tr?tr[2]:(f.n||('f'+k))+'-other')}
      });
      if(ok)right();else wrong(null,tags);
    };
    $('#'+L+'Check').onclick=check;box.querySelectorAll('input').forEach(x=>x.onkeydown=e=>{if(e.key==='Enter')check()});
  }else if(sp.type==='order'){
    box.querySelectorAll('[data-pk]').forEach(b=>b.onclick=()=>{if(locked[L])return;orderPick[L].push(+b.dataset.pk);renderLevel(L)});
    box.querySelectorAll('[data-un]').forEach(b=>b.onclick=()=>{if(locked[L])return;orderPick[L].splice(+b.dataset.un,1);renderLevel(L)});
    $('#'+L+'OReset').onclick=()=>{orderPick[L]=[];renderLevel(L)};
    $('#'+L+'Check').onclick=()=>{
      if(locked[L])return;const pick=orderPick[L];
      if(pick.length<sp.cards.length){fb.className='fb bad pop';fb.textContent=S.orderFill;return}
      if(pick.every((k,j)=>k===j))right();
      else{const firstBad=pick.findIndex((k,j)=>k!==j);wrong(null,['order-pos'+(firstBad+1)])}
    };
  }
}
LEVELS.forEach(L=>{$('#'+L+'Reset').onclick=()=>{state.pos[L]=0;state.sub[L]=0;state.done[L]=false;tries[L]=0;orderPick[L]=[];clearLog(L);save();stars();renderLevel(L)}});

/* ---------- report ---------- */
function fmtDate(ts){return ts?new Date(ts).toLocaleDateString(S.locale):S.notStarted}
function statusOf(key){
  const e=state.log[key];
  if(!e||!e.t)return {cls:'no',txt:S.notTried};
  const h=e.h?S.withHint:'';
  if(e.ok)return e.t===1?{cls:'ok',txt:S.first}:{cls:'mid',txt:S.nth(e.t)+h};
  return {cls:'bad',txt:S.notYet(e.t)+h};
}
function reportData(){
  return LEVELS.map(L=>({name:S['lv'+L.toUpperCase()],done:state.done[L],rows:LV[L].tasks.map((t,i)=>({key:L+i,label:t.label}))}));
}
function renderReport(){
  const data=reportData();let solved=0,total=0,first=0,hints=0;
  data.forEach(l=>l.rows.forEach(r=>{const e=state.log[r.key];total++;if(e&&e.ok){solved++;if(e.t===1)first++}if(e&&e.h)hints++}));
  const n=LEVELS.filter(L=>state.done[L]).length;
  $('#reportCard').innerHTML=`<div class="rep">
    <p><b>${S.repStars(n)}</b> ${S.repSum(solved,total,first,hints)}</p>
    ${data.map(l=>`<div><h3>${l.name}${l.done?` <span class="st ok">${S.complete}</span>`:''}</h3><ul>${l.rows.map(r=>{const s=statusOf(r.key);return `<li><span>${r.label}</span><span class="st ${s.cls}">${s.txt}</span></li>`}).join('')}</ul></div>`).join('')}
    <p class="hint">${S.repDates(fmtDate(state.firstAt),fmtDate(state.lastAt))}</p></div>`;
  const lines=[S.repHead,S.repStars(n),S.repSum(solved,total,first,hints),''];
  data.forEach(l=>{lines.push(`${l.name}${l.done?` (${S.complete})`:''}:`);l.rows.forEach(r=>lines.push(`• ${r.label}: ${statusOf(r.key).txt}`));lines.push('')});
  lines.push(S.repDates(fmtDate(state.firstAt),fmtDate(state.lastAt)));
  $('#reportText').value=lines.join('\n');
}
$('#copyReport').onclick=()=>{
  renderReport();const txt=$('#reportText').value, fb=$('#copyFb');
  const manual=()=>{const ta=$('#reportText');ta.hidden=false;ta.focus();ta.select();fb.className='fb bad';fb.textContent=S.copyFail};
  try{navigator.clipboard.writeText(txt).then(()=>{fb.className='fb good pop';fb.textContent=S.copied},manual)}catch(e){manual()}
};
let armed=false;
$('#resetAll').onclick=()=>{
  const b=$('#resetAll');
  if(!armed){armed=true;b.textContent=S.resetSure;setTimeout(()=>{armed=false;b.textContent=S.resetAll},4000);return}
  armed=false;b.textContent=S.resetAll;state=fresh();LEVELS.forEach(L=>{tries[L]=0;orderPick[L]=[]});save();
  show('learn');LEVELS.forEach(L=>renderLevel(L));stars();window.scrollTo({top:0});
};
applyTexts();renderCast();
show(tabs.includes(state.tab)?state.tab:'learn');
LEVELS.forEach(L=>renderLevel(L));stars();
if(firstVisit){profOpen=true;renderProfile()}
