#!/usr/bin/env python3
"""Light / dark / auto theme switch on every page of the site.

Run from the repo root after building or changing pages:  python3 tools/add_theme_toggle.py
Idempotent. Adds:
  * a tiny script in <head> that applies the saved choice before the page paints (no flash);
  * styles for the switch;
  * a script at the end of <body> that puts the switch into the top row (nav.site-home),
    or into its own row at the top of pages that have no such nav (the home pages).
The pages' CSS already understands :root[data-theme="light"|"dark"]; "auto" removes the attribute
so the device setting decides. The choice is kept in localStorage under 'apiary-theme'.
"""
import glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEAD = ('<script>/* theme-head */try{var t=localStorage.getItem("apiary-theme");'
        'if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>')
CSS = ('/* theme switch */.theme-sw{display:inline-flex;gap:2px;background:var(--cell,#eee);border:1px solid var(--line,#ccc);border-radius:999px;padding:2px;margin-left:auto;flex:none}'
       '.theme-sw button{border:0;background:transparent;color:var(--muted,#555);font:700 13px/1 var(--body,system-ui,sans-serif);padding:6px 9px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:4px}'
       '.theme-sw button[aria-pressed="true"]{background:var(--paper,#fff);color:var(--ink,#111);box-shadow:0 1px 3px rgba(0,0,0,.18)}'
       '.theme-sw button:focus-visible{outline:2px solid var(--sky,#3E7FB8);outline-offset:1px}.theme-sw svg{width:15px;height:15px}'
       '.theme-row{width:100%;max-width:920px;margin:0 auto;padding:10px 0 0;display:flex;justify-content:flex-end;justify-self:stretch}'
       'nav.site-home{display:flex;flex-wrap:wrap;align-items:center;gap:6px}'
       '@media (max-width:420px){.theme-sw .tl{display:none}}@media print{.theme-sw,.theme-row{display:none}}')
SUN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><g stroke="currentColor" stroke-width="2.2" stroke-linecap="round">'
       '<path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></g></svg>')
MOON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z" fill="currentColor"/></svg>'
JS = ('<script>/* theme switch */(function(){var uk=(document.documentElement.lang||"uk").indexOf("en")!==0,K="apiary-theme",de=document.documentElement;'
      'var L=uk?{l:"Світла",d:"Темна",a:"Авто",g:"Тема сторінки",at:"Як на пристрої"}:{l:"Light",d:"Dark",a:"Auto",g:"Page theme",at:"Same as the device"};'
      'var w=document.createElement("div");w.className="theme-sw";w.setAttribute("role","group");w.setAttribute("aria-label",L.g);'
      'w.innerHTML=\'<button type="button" data-t="light" title="\'+L.l+\'">' + SUN.replace('"', '\\"') + '<span class="tl">\'+L.l+\'</span></button>\''
      '+\'<button type="button" data-t="dark" title="\'+L.d+\'">' + MOON.replace('"', '\\"') + '<span class="tl">\'+L.d+\'</span></button>\''
      '+\'<button type="button" data-t="auto" title="\'+L.at+\'">\'+L.a+\'</button>\';'
      'function cur(){var t=null;try{t=localStorage.getItem(K)}catch(e){}return t==="light"||t==="dark"?t:"auto"}'
      'function mark(){var c=cur();[].forEach.call(w.querySelectorAll("button"),function(b){b.setAttribute("aria-pressed",b.getAttribute("data-t")===c)})}'
      'w.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;var t=b.getAttribute("data-t");'
      'try{if(t==="auto")localStorage.removeItem(K);else localStorage.setItem(K,t)}catch(x){}'
      'if(t==="auto")de.removeAttribute("data-theme");else de.setAttribute("data-theme",t);mark()});'
      'var nav=document.querySelector("nav.site-home");if(nav)nav.appendChild(w);else{var r=document.createElement("div");r.className="theme-row";r.appendChild(w);'
      'var host=document.querySelector(".wrap,.page")||document.body;host.insertBefore(r,host.firstChild)}mark()})();</script>')


def run():
    files = glob.glob(str(ROOT / '*.html')) + glob.glob(str(ROOT / '*' / '*.html'))
    for f in files:
        p = Path(f); s = p.read_text()
        s = re.sub(r'<script>/\* theme-head \*/.*?</script>', '', s, flags=re.S)
        s = re.sub(r'<script>/\* theme switch \*/.*?</script>', '', s, flags=re.S)
        s = re.sub(r'/\* theme switch \*/.*?(?=</style>)', '', s, count=1, flags=re.S)
        i = s.index('</title>') + len('</title>')
        s = s[:i] + HEAD + s[i:]
        i = s.index('</style>')
        s = s[:i] + CSS + s[i:]
        j = s.rindex('</body>')
        s = s[:j] + JS + s[j:]
        p.write_text(s)
    print(len(files), 'pages')


if __name__ == '__main__':
    run()
