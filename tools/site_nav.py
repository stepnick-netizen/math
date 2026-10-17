#!/usr/bin/env python3
"""Site navigation built from tools/topics.json.

Run from the repo root after adding a lesson or rebuilding pages:
    python3 tools/site_nav.py

It (re)writes, idempotently:
  * the contents block on index.html / index-en.html (between <!--toc--> and <!--/toc-->):
    numbered lessons grouped by subject, search (title, keywords, textbook exercise numbers),
    subject filter chips and progress stars read from each game's localStorage;
  * the breadcrumb at the top of every topic page and cheat sheet (nav.site-home);
  * «previous / next lesson» links at the bottom of every topic page.
"""
import json, re, html
from _inject import put_style
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'tools' / 'topics.json').read_text())
SECS = {s['id']: s for s in DATA['sections']}
T = {
    'uk': dict(home='Математична пасіка', toc='Зміст', all='Усі', lesson='Урок', sheet='шпаргалка', play='Урок і гра', cheat='Шпаргалка',
               pdf='PDF', ph='Тема або № вправи, напр. 401', none='Нічого не знайдено. Спробуй інше слово або номер вправи.',
               ex='Вправа №{n} — з цього уроку', new='Новий', prev='Попередній урок', next='Наступний урок', stars='{n} з 3 рівнів',
               search='Пошук уроку', index='index.html', lead='Номери уроків — як у презентаціях Ігоря Петровича. § — параграф підручника.'),
    'en': dict(home='The Maths Apiary', toc='Contents', all='All', lesson='Lesson', sheet='cheat sheet', play='Lesson and game', cheat='Cheat sheet',
               pdf='PDF', ph='Topic or exercise no., e.g. 401', none='Nothing found. Try another word or exercise number.',
               ex='Exercise {n} is from this lesson', new='New', prev='Previous lesson', next='Next lesson', stars='{n} of 3 levels',
               search='Find a lesson', index='index-en.html', lead='Lesson numbers match Ihor Petrovych’s presentations. § is the textbook section.'),
}


def esc(s):
    return html.escape(s, quote=True)


def numkey(n):
    return [float(x) for x in n.split('.')] if n else [999]


def ordered():
    out = []
    for s in DATA['sections']:
        ls = sorted([l for l in DATA['lessons'] if l['section'] == s['id']], key=lambda l: (numkey(l['num']), l['added']))
        out.append((s, ls))
    return out


def label(l, lang):
    """'Урок 9.1' or the topic title for unnumbered revision lessons."""
    return f"{T[lang]['lesson']} {l['num']}" if l['num'] else l[lang]


def progress_spec(l, lang):
    p = l['progress']
    keys = []
    for lg in ('uk', 'en'):          # a pupil may have played in either language
        k = p['key'][lg] if isinstance(p['key'], dict) else p['key'].replace('{lang}', lg)
        keys.append(k)
    spec = {'keys': keys, 'type': p['type']}
    if p['type'] == 'flags':
        spec['flags'] = p['flags']
    return json.dumps(spec, ensure_ascii=False)


# ---------------------------------------------------------------- index contents
CSS = """/* toc */.toc{display:grid;gap:14px}.toc-head{display:grid;gap:8px}.toc-head p{margin:0;color:var(--muted);font-size:15px}
.toc-search{display:flex;align-items:center;gap:8px;background:var(--paper);border:2px solid var(--line);border-radius:14px;padding:4px 6px 4px 12px}
.toc-search:focus-within{border-color:var(--hay)}.toc-search svg{flex:none;width:20px;height:20px}
.toc-search input{flex:1;min-width:0;border:0;background:transparent;color:var(--ink);font:600 17px var(--body);padding:9px 2px;outline:none}
.toc-search input::placeholder{color:var(--muted);font-weight:400}.toc-search input::-webkit-search-cancel-button{display:none}
.toc-clear{border:0;background:var(--cell);color:var(--ink);border-radius:10px;font:700 14px var(--body);padding:7px 10px;cursor:pointer}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{border:2px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;font:800 14.5px var(--body);padding:7px 14px;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.toc-sec{display:grid;gap:10px}.toc-sec h3{font:700 21px var(--display);margin:8px 0 0;display:flex;align-items:center;gap:10px}
.toc-sec h3::before{content:"";width:14px;height:16px;background:var(--hay);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.toc-list{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.lesson{display:flex;gap:14px;align-items:flex-start;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:14px;box-shadow:0 2px 0 var(--shadow)}
.l-num{flex:none;width:62px;height:70px;display:grid;place-items:center;background:var(--hay);color:#2A1E00;text-decoration:none;font:700 20px var(--display);
clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}.l-num.sym{background:var(--marker);font-size:17px}
.l-body{flex:1;min-width:0;display:grid;gap:6px}.l-title{font:700 18.5px/1.3 var(--display);color:var(--ink);text-decoration:none}.l-title:hover{text-decoration:underline}
.l-meta{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:center;font:700 14px var(--body);color:var(--muted)}
.l-stars{color:var(--hay);letter-spacing:2px;font-size:16px}.l-new{background:var(--yarn);color:#fff;border-radius:999px;padding:2px 9px;font:800 12px var(--body);text-transform:uppercase;letter-spacing:.05em}
.l-blurb{margin:0;color:var(--muted);font-size:15px}.l-ex{margin:0;font:700 14.5px var(--body);color:var(--leaf)}
.lesson .links{display:flex;flex-wrap:wrap;gap:8px;margin-top:2px}.toc-none{color:var(--muted);margin:4px 0}
@media (max-width:480px){.lesson{padding:12px;gap:10px}.l-num{width:50px;height:57px;font-size:17px}.l-title{font-size:17px}}"""

JS = r"""<script>/* toc */(function(){var box=document.getElementById('toc');if(!box)return;
var q=document.getElementById('toc-q'),clr=document.getElementById('toc-clear'),none=document.getElementById('toc-none'),
chips=[].slice.call(box.querySelectorAll('.chip')),rows=[].slice.call(box.querySelectorAll('.lesson')),secs=[].slice.call(box.querySelectorAll('.toc-sec'));
var sec='all';try{sec=localStorage.getItem('apiary-toc-sec')||'all'}catch(e){}
var now=Date.now(),last=rows.map(function(r){return r.getAttribute('data-added')||''}).sort().pop();
rows.forEach(function(r){var a=r.getAttribute('data-added');if(a&&a===last&&now-Date.parse(a)<14*864e5){var b=r.querySelector('.l-new');if(b)b.hidden=false}
 var sp;try{sp=JSON.parse(r.getAttribute('data-p'))}catch(e){return}var n=0;
 sp.keys.forEach(function(k){var st=null;try{st=JSON.parse(localStorage.getItem(k)||'null')}catch(e){}if(!st)return;var c=0;
  if(sp.type==='done'){var d=st.done||{};c=['a','b','c'].filter(function(x){return d[x]}).length}else{c=sp.flags.filter(function(f){return st[f]}).length}
  n=Math.max(n,c)});
 var el=r.querySelector('.l-stars');if(el&&n>0){el.textContent='★★★'.slice(0,n)+'☆☆☆'.slice(0,3-n);el.title=el.getAttribute('data-t').replace('{n}',n);el.hidden=false}});
function norm(s){return s.toLowerCase().replace(/[№#]/g,' ').replace(/[’'ʼ]/g,'').replace(/\s+/g,' ').trim()}
function apply(){var v=norm(q.value),toks=v?v.split(' '):[],shown=0;clr.hidden=!v;
 chips.forEach(function(c){c.setAttribute('aria-pressed',c.getAttribute('data-sec')===sec)});
 rows.forEach(function(r){var ok=sec==='all'||r.getAttribute('data-sec')===sec,hit='';
  if(ok&&toks.length){var hay=r.getAttribute('data-s'),ex=(r.getAttribute('data-ex')||'').split(' ');
   ok=toks.every(function(t){if(/^\d+$/.test(t)){var m=ex.filter(function(e){return e&&e.indexOf(t)===0});if(m.length){if(t.length>=3)hit=m[0];return true}return hay.indexOf(t)>=0}return hay.indexOf(t)>=0})}
  r.hidden=!ok;if(ok)shown++;var exl=r.querySelector('.l-ex');if(exl){exl.hidden=!hit;if(hit)exl.textContent=exl.getAttribute('data-t').replace('{n}',hit)}});
 secs.forEach(function(s){s.hidden=!s.querySelector('.lesson:not([hidden])')});none.hidden=shown>0}
chips.forEach(function(c){c.addEventListener('click',function(){sec=c.getAttribute('data-sec');try{localStorage.setItem('apiary-toc-sec',sec)}catch(e){}apply()})});
q.addEventListener('input',apply);clr.addEventListener('click',function(){q.value='';apply();q.focus()});
if(location.hash){var h=location.hash.slice(1);if(chips.some(function(c){return c.getAttribute('data-sec')===h})){sec='all'}}
apply()})();</script>"""

LENS = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="var(--muted)" stroke-width="2.4"/><path d="M15.5 15.5 21 21" stroke="var(--muted)" stroke-width="2.6" stroke-linecap="round"/></svg>'


def toc(lang):
    t = T[lang]
    sfx = 'uk' if lang == 'uk' else 'en'
    h = (f'<!--toc--><section class="toc" id="toc"><div class="toc-head"><h2>{t["toc"]}</h2><p>{t["lead"]}</p></div>'
         f'<label class="toc-search">{LENS}<span class="sr" style="position:absolute;left:-9999px">{t["search"]}</span>'
         f'<input id="toc-q" type="search" inputmode="search" autocomplete="off" placeholder="{esc(t["ph"])}">'
         f'<button type="button" class="toc-clear" id="toc-clear" hidden>✕</button></label>'
         f'<div class="chips" role="group" aria-label="{t["toc"]}"><button type="button" class="chip" data-sec="all" aria-pressed="true">{t["all"]}</button>'
         + ''.join(f'<button type="button" class="chip" data-sec="{s["id"]}" aria-pressed="false">{s["chip_" + lang]}</button>' for s in DATA['sections'])
         + '</div>')
    for s, ls in ordered():
        h += f'<div class="toc-sec" id="{s["id"]}"><h3>{s[lang]}</h3><ol class="toc-list">'
        for l in ls:
            f = l['folder']
            game = f'{f}/{sfx}.html'
            hay = ' '.join([l[lang], l['uk'], l['en'], l['kw_' + lang], l['kw_uk'], l['num'], l['par'], s[lang], ' '.join(l['ex'])]).lower()
            hay = re.sub(r'[’\'ʼ№#]', '', hay)
            num = (f'<a class="l-num" href="{game}" aria-hidden="true" tabindex="-1">{l["num"]}</a>' if l['num'] else
                   f'<a class="l-num sym" href="{game}" aria-hidden="true" tabindex="-1">{esc(l["emblem"])}</a>')
            meta = []
            if l['num']:
                meta.append(f'{t["lesson"]} {l["num"]}')
            if l['par']:
                meta.append(l['par'])
            links = f'<a class="btn" href="{game}">{t["play"]}</a>'
            if l['sheet']:
                links += f'<a class="btn ghost" href="{f}/cheatsheet-{sfx}.html">{t["cheat"]}</a><a class="btn ghost" href="{f}/cheatsheet-{sfx}.pdf">{t["pdf"]}</a>'
            h += (f'<li class="lesson" data-sec="{s["id"]}" data-added="{l["added"]}" data-s="{esc(hay)}" data-ex="{" ".join(l["ex"])}" data-p="{esc(progress_spec(l, lang))}">'
                  f'{num}<div class="l-body"><a class="l-title" href="{game}">{esc(l[lang])}</a>'
                  f'<div class="l-meta">{"".join(f"<span>{m}</span>" for m in meta)}<span class="l-stars" data-t="{esc(t["stars"])}" hidden></span>'
                  f'<span class="l-new" hidden>{t["new"]}</span></div>'
                  f'<p class="l-blurb">{esc(l["blurb_" + lang])}</p><p class="l-ex" data-t="{esc(t["ex"])}" hidden></p>'
                  f'<div class="links">{links}</div></div></li>')
        h += '</ol></div>'
    h += f'<p class="toc-none" id="toc-none" hidden>{t["none"]}</p></section><!--/toc-->'
    return h


def put_css(s, css, marker):
    s = re.sub(re.escape(marker) + r'.*?(?=</style>)', '', s, count=1, flags=re.S)
    i = s.index('</style>')
    return s[:i] + css + s[i:]


QUICK = {
    'uk': {'label': 'Розділи сайту', 'items': [
        ('toc', '9.1', 'Уроки', 'зміст і пошук', '#toc'),
        ('fun', '?!', 'Цікавинки', 'історії про математику', 'cikavynky.html'),
        ('hist', '', 'Історія і культура', 'козаки, герої, науковці, митці', 'education.html')]},
    'en': {'label': 'Site sections', 'items': [
        ('toc', '9.1', 'Lessons', 'contents and search', '#toc'),
        ('fun', '?!', 'Curiosities', 'stories about maths', 'cikavynky-en.html'),
        ('hist', '', 'History and culture', 'Cossacks, heroes, scientists, artists', 'education-en.html')]},
}
QUICK_CSS = ("/* quick */.quick{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:10px}"
             ".quick a{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);background:var(--paper);border:1.5px solid var(--line);border-radius:14px;padding:9px 12px;box-shadow:0 2px 0 var(--shadow)}"
             ".quick a:hover{border-color:var(--hay)}.quick b{display:block;font:700 16px var(--display)}.quick small{display:block;color:var(--muted);font:600 13px var(--body)}"
             ".q-ic{flex:none;width:38px;height:43px;display:grid;place-items:center;font:700 14px var(--display);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}"
             "@media (max-width:480px){.quick{gap:6px}.quick a{padding:6px 10px}.quick small{display:none}.q-ic{width:30px;height:34px;font-size:12px}}"
             ".q-toc .q-ic{background:var(--hay);color:#2A1E00}.q-fun .q-ic{background:var(--marker);color:var(--marker-ink)}.q-hist .q-ic{background:linear-gradient(#0057B7 0 50%,#FFD700 50% 100%)}")


def do_index(lang):
    p = ROOT / ('index.html' if lang == 'uk' else 'index-en.html')
    s = p.read_text()
    block = toc(lang)
    # the contents go straight after the hero, so pupils see the lessons first
    s = re.sub(r'\s*<!--toc-->.*?<!--/toc-->', '', s, flags=re.S)
    s = re.sub(r'\s*<section class="topics">.*?</section>', '', s, count=1, flags=re.S)
    k = s.index('</header>') + len('</header>')
    s = s[:k] + '\n ' + block + s[k:]
    # small quick links right under the hero, so the separate sections are visible at once
    s = re.sub(r'\s*<!--quick-->.*?<!--/quick-->', '', s, flags=re.S)
    q = QUICK[lang]
    quick = ('<!--quick--><nav class="quick" aria-label="' + q['label'] + '">'
             + ''.join(f'<a href="{href}" class="q-{cls}"><span class="q-ic" aria-hidden="true">{ic}</span><span><b>{name}</b><small>{sub}</small></span></a>'
                       for cls, ic, name, sub, href in q['items']) + '</nav><!--/quick-->')
    k = s.index('</header>') + len('</header>')
    s = s[:k] + '\n ' + quick + s[k:]
    s = put_style(s, 'quick', QUICK_CSS, legacy=[])
    s = put_style(s, 'toc', CSS, legacy=['toc'])
    s = re.sub(r'<script>/\* toc \*/.*?</script>', '', s, flags=re.S)
    j = s.rindex('</body>')
    s = s[:j] + JS + s[j:]
    p.write_text(s)


# ---------------------------------------------------------------- topic pages
NAV_CSS = """/* nav */nav.site-home{display:flex;flex-wrap:wrap;gap:2px 6px;align-items:center;line-height:1.5}nav.site-home .sep{color:var(--muted);font-weight:400}
nav.site-home .here{color:var(--muted)}
.lesson-nav{max-width:920px;margin:20px auto 0;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.lesson-nav a{display:grid;gap:2px;background:var(--paper,#fff);border:2px solid var(--line,#ddd);border-radius:14px;padding:10px 14px;text-decoration:none;color:var(--ink,#222)}
.lesson-nav a:hover{border-color:var(--hay,#D99A1E)}.lesson-nav small{font:800 12.5px var(--body,sans-serif);letter-spacing:.05em;text-transform:uppercase;color:var(--muted,#666)}
.lesson-nav b{font:700 15.5px/1.3 var(--display,var(--body,sans-serif))}.lesson-nav .next{text-align:right;grid-column:2}
@media (max-width:520px){.lesson-nav{grid-template-columns:1fr}.lesson-nav .next{grid-column:1}}"""


def do_pages():
    for s, ls in ordered():
        for i, l in enumerate(ls):
            prev = ls[i - 1] if i > 0 else None
            nxt = ls[i + 1] if i + 1 < len(ls) else None
            for lang in ('uk', 'en'):
                t = T[lang]
                sfx = 'uk' if lang == 'uk' else 'en'
                for kind in ('game', 'sheet'):
                    p = ROOT / l['folder'] / (f'{sfx}.html' if kind == 'game' else f'cheatsheet-{sfx}.html')
                    if not p.exists():
                        continue
                    x = p.read_text()
                    here = label(l, lang) + (f' · {t["sheet"]}' if kind == 'sheet' else '')
                    crumbs = (f'<nav class="site-home" aria-label="breadcrumb"><a href="../{t["index"]}">← {t["home"]}</a><span class="sep">›</span>'
                              f'<a href="../{t["index"]}#{s["id"]}">{s[lang]}</a><span class="sep">›</span><span class="here">{esc(here)}</span></nav>')
                    x, n = re.subn(r'<nav class="site-home"[^>]*>.*?</nav>', lambda m: crumbs, x, count=1, flags=re.S)
                    assert n == 1, p
                    x = put_style(x, 'nav', NAV_CSS, legacy=['nav'])
                    x = re.sub(r'<nav class="lesson-nav".*?</nav>', '', x, flags=re.S)
                    if kind == 'game' and (prev or nxt):
                        nav = '<nav class="lesson-nav" aria-label="lessons">'
                        if prev:
                            nav += f'<a class="prev" href="../{prev["folder"]}/{sfx}.html"><small>← {t["prev"]}</small><b>{esc(label(prev, lang))}. {esc(prev[lang])}</b></a>' if prev['num'] else \
                                   f'<a class="prev" href="../{prev["folder"]}/{sfx}.html"><small>← {t["prev"]}</small><b>{esc(prev[lang])}</b></a>'
                        if nxt:
                            nav += f'<a class="next" href="../{nxt["folder"]}/{sfx}.html"><small>{t["next"]} →</small><b>{esc(label(nxt, lang))}. {esc(nxt[lang])}</b></a>' if nxt['num'] else \
                                   f'<a class="next" href="../{nxt["folder"]}/{sfx}.html"><small>{t["next"]} →</small><b>{esc(nxt[lang])}</b></a>'
                        nav += '</nav>'
                        k = x.index('<footer class="site-copy"')
                        x = x[:k] + nav + '\n' + x[k:]
                    p.write_text(x)


if __name__ == '__main__':
    do_index('uk')
    do_index('en')
    do_pages()
    print('ok')
