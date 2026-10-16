
(function(){
  /* own devices: open the site with #nostats once to stop counting this browser, #stats to count again */
  var SK='skipgc', skip=false;
  try{
    if(location.hash==='#nostats')localStorage.setItem(SK,'t');
    if(location.hash==='#stats')localStorage.removeItem(SK);
    skip=localStorage.getItem(SK)==='t';
  }catch(e){}
  var uk=document.documentElement.lang==='uk';
  if(location.hash==='#nostats'||location.hash==='#stats'){
    var n=document.createElement('div');
    n.textContent=skip?(uk?'Статистику на цьому пристрої вимкнено. Ваші відвідування не рахуються.':'Statistics are off on this device. Your visits are not counted.')
                      :(uk?'Статистику на цьому пристрої знову ввімкнено.':'Statistics are on again on this device.');
    n.style.cssText='position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:50;padding:12px 16px;border-radius:12px;background:#26301F;color:#fff;font:700 15px system-ui,sans-serif;text-align:center';
    document.body.appendChild(n);setTimeout(function(){n.remove()},6000);
  }
  if(skip){
    var f=document.querySelector('.site-copy');
    if(f){var m=document.createElement('small');m.textContent=uk?'(цей пристрій не враховується)':'(this device is not counted)';f.appendChild(m)}
    window.ponyaTrack=function(){};return;
  }
  var gs=document.createElement('script');gs.async=true;gs.src='//gc.zgo.at/count.js';
  gs.setAttribute('data-goatcounter','https://varia-math.goatcounter.com/count');document.head.appendChild(gs);

  var parts=location.pathname.replace(/\.html$/,'').split('/').filter(Boolean);
  var page=parts.slice(-2).join('-')||'index';            // e.g. monomials-uk, math-index
  var queue=[];
  function send(name){window.goatcounter.count({path:page+'/'+name,title:name,event:true})}
  function track(name){
    try{if(window.goatcounter&&window.goatcounter.count)send(name);else queue.push(name)}catch(e){}
  }
  gs.onload=function(){var q=queue;queue=[];q.forEach(function(n){try{send(n)}catch(e){}})};
  window.ponyaTrack=track;

  document.addEventListener('click',function(e){
    var t=e.target.closest('button,a');if(!t)return;
    if(t.classList.contains('tab')&&t.dataset.tab)track('tab-'+t.dataset.tab);
    else if(t.id==='copyReport')track('report-copy');
    else if(t.id==='shareReport')track('report-send');
    else if(t.dataset&&t.dataset.w)track('world-'+t.dataset.w);
    else if(t.tagName==='A'&&/\.pdf$/.test(t.getAttribute('href')||''))track('pdf-'+t.getAttribute('href').replace(/\W+/g,'-'));
  },true);

  /* every task: solved on the first try, solved after mistakes, and the wrong answers typed (numbers only) */
  if(typeof window.rec==='function'&&typeof state==='object'&&state&&state.log){
    var orig=window.rec, wrong={}, sentVals={};
    function typed(){
      var panel=document.querySelector('.panel:not([hidden])');if(!panel)return '';
      var vals=[];
      panel.querySelectorAll('input').forEach(function(i){
        if(!i.offsetParent||vals.length>=6)return;
        var v=String(i.value).trim().replace(/[−–]/g,'-').replace(',','.');
        vals.push(v===''?'_':(/^-?\d{1,6}(\.\d{1,4})?$/.test(v)?v:'x'));
      });
      return vals.join(';');
    }
    window.rec=function(key,ok,hint){
      var done=state.log[key]&&state.log[key].ok;
      if(!done){
        if(ok)track('task-'+key+(wrong[key]?'-after-mistakes':'-first-try'));
        else{
          if(!wrong[key])track('task-'+key+'-mistake');
          wrong[key]=(wrong[key]||0)+1;
          var v=typed();
          if(v&&!sentVals[key+v]){sentVals[key+v]=1;track('typed-'+key+'/'+v)}
        }
      }
      return orig.apply(this,arguments);
    };
  }

  /* a level is finished when its star lights up; the diploma appears after all three */
  document.querySelectorAll('.star').forEach(function(st){
    new MutationObserver(function(){if(st.classList.contains('on')&&!st.dataset.seen){st.dataset.seen=1;track('level-done-'+st.id.replace('st-',''))}})
      .observe(st,{attributes:true,attributeFilter:['class']});
  });
  var dip=document.getElementById('diploma');
  if(dip)new MutationObserver(function(){if(!dip.hidden)track('diploma')}).observe(dip,{attributes:true,attributeFilter:['hidden']});
})();
