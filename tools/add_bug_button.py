# Run from the repo root after building or changing topic pages: python3 tools/add_bug_button.py
"""Add a 'Spotted a mistake?' button to every topic page and cheat sheet; it opens the Google Form with the topic, tab, task number and expression prefilled."""
import sys, re, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _inject import put_style
from pathlib import Path
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSclI7maoMiImANIDKjVunHHJG4Sk_i8yCumRAxyPL9OjDzocw/viewform'
ENTRY = sys.argv[1] if len(sys.argv) > 1 else 'entry.649258102'
CSS = ('/* bug button */.bug-btn{position:fixed;right:max(12px,env(safe-area-inset-right,0px));bottom:max(12px,env(safe-area-inset-bottom,0px));z-index:60;'
       'display:inline-flex;align-items:center;gap:6px;background:var(--paper,#fff);color:var(--ink,#222)!important;text-decoration:none!important;'
       'border:2px solid var(--yarn,#D9486F);border-radius:999px;padding:8px 14px;font:700 14px/1.2 Nunito,system-ui,sans-serif;box-shadow:0 3px 12px rgba(0,0,0,.2)}'
       '.bug-btn:hover{background:var(--cell,#f4f4f4)}.bug-btn:focus-visible{outline:3px solid var(--hay,#D99A1E);outline-offset:2px}'
       'body::after{content:"";display:block;height:64px}@media print{.bug-btn{display:none}body::after{display:none}}')
JS = ('<script>/* bug button */(function(){var F=%r,E=%r,uk=(document.documentElement.lang||"uk").indexOf("en")!==0;'
      'function vis(e){return e&&e.offsetParent!==null}'
      'function txt(e){var c=e.cloneNode(true);[].slice.call(c.querySelectorAll("sup")).forEach(function(s){s.textContent="^"+s.textContent});return c.textContent.replace(/\\s+/g," ").trim()}'
      'function ctx(){var p=[document.title.split(" · ")[0]],tab=document.querySelector("[role=tab][aria-selected=true]");if(tab)p.push(txt(tab));'
      'var st=[].slice.call(document.querySelectorAll(".step")).filter(vis)[0];if(st)p.push(txt(st));'
      'var q=[].slice.call(document.querySelectorAll(".q")).filter(vis)[0];if(q)p.push(txt(q));'
      'p.push(uk?"мова: укр.":"lang: en");return p.join(" · ")+(uk?"\\nЩо не так: ":"\\nWhat is wrong: ")}'
      'var a=document.createElement("a");a.className="bug-btn";a.href=F;a.target="_blank";a.rel="noopener";'
      'a.innerHTML=(uk?"Знайшли помилку?":"Spotted a mistake?");'
      'a.addEventListener("click",function(){a.href=F+(E?"?usp=pp_url&"+E+"="+encodeURIComponent(ctx()):"")});'
      'document.body.appendChild(a)})();</script>') % (FORM, ENTRY)
files = [f for f in glob.glob('*/*.html')]
for f in files:
    p = Path(f); s = p.read_text()
    s = put_style(s, 'bug', CSS, legacy=['bug button'])
    s = re.sub(r'<script>/\* bug button \*/.*?</script>', '', s, flags=re.S)
    j = s.rindex('</body>'); s = s[:j] + JS + s[j:]
    p.write_text(s)
print(len(files), 'pages; entry =', ENTRY or '(none)')
