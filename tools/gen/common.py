"""Page assembly shared by the topics: game page, cheat sheet, site/artifact wrappers, rights chips and the 'why' card."""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
BASE_CSS = (HERE / 'base.css').read_text()
SITE_CSS = (HERE / 'site.css').read_text()
DEFS = (HERE / 'defs.svg').read_text()
ENGINE = (HERE / 'engine.js').read_text()
ICONS_JS = (HERE / 'icons.js').read_text()
SHARE_JS = (HERE / 'share.js').read_text()
STATS_JS = (HERE / 'stats.js').read_text()
_W = json.loads((HERE / 'worlds.json').read_text())
WORLDS = {k: {kk: vv for kk, vv in v.items() if kk not in ('progress', 'h1', 'shelf')} for k, v in _W.items()}
ROLE_SVG = {w: {r: v['roles'][r]['svg'] for r in v['roles']} for w, v in _W.items()}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@600;700&family=Nunito:wght@400;600;800&family=Caveat:wght@600&display=swap">')
RESET = ('<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'html{scroll-padding-top:env(safe-area-inset-top,0px)}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#000}'
         'img{max-width:100%}[hidden]:not([hidden=until-found i]){display:none!important}</style>')
COPY = {'uk': '© 2026 Пасіка Ігор Петрович, учитель математики, Ліцей №157, м. Київ, Україна<small>Побудовано на його презентаціях і уроках. Зробив Микола Степанов для доньки Варі</small><small>Сайт рахує анонімну статистику відвідувань: без cookies і без імен.</small>',
        'en': '© 2026 Ihor Petrovych Pasika, maths teacher, Lyceum No. 157, Kyiv, Ukraine<small>Built on his slides and lessons. Made by Mykola Stepanov for his daughter Varia</small><small>This site keeps anonymous visit statistics: no cookies and no names.</small>'}
ICONS = ('<link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="icon" href="../favicon.ico" sizes="48x48">'
         '<link rel="apple-touch-icon" href="../apple-touch-icon.png"><meta name="theme-color" content="#E8A317">')
HOME = {'uk': '← Математична пасіка: усі теми', 'en': '← The Maths Apiary: all topics'}

GAME_CSS = """
/* engine: task steps, choice tiles, equation rows, ordering cards, stage drawings */
.teach{justify-self:start;font:800 12.5px var(--body);letter-spacing:.05em;text-transform:uppercase;color:var(--plum);background:var(--cell);border:1.5px dashed var(--plum);border-radius:999px;padding:2px 10px}
.tq{font-size:17px}
.sp{font-weight:700}
.stepno{font:800 13px var(--body);color:var(--hay);letter-spacing:.06em;text-transform:uppercase}
.donesteps{display:grid;gap:4px;background:var(--cell);border-radius:10px;padding:8px 12px}
.ds{color:var(--good);font-weight:700;font-size:16px}
.ds .mono,.ds sup{color:inherit}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,128px),1fr));gap:10px}
.opt{display:grid;justify-items:center;align-content:start;gap:4px;font:700 16px/1.3 var(--body);border:2px solid var(--c);background:var(--paper);color:var(--ink);border-radius:14px;padding:10px 8px 12px;cursor:pointer;text-align:center;min-width:0}
.opt .oi svg{width:70px;height:auto}
.opt.picked{background:var(--c);color:var(--paper);border-style:solid}
.opt.badpick{border-style:dashed;opacity:.55}
.opt:disabled{cursor:default}
.opts.pills{display:flex;flex-wrap:wrap}
.opts.pills .opt{border-radius:999px;padding:8px 16px;font-size:17px}
.opts.big .opt{font:700 26px var(--display);padding:8px 18px;min-width:64px}
.eqrow{display:flex;flex-wrap:wrap;align-items:center;gap:6px 6px;font:700 clamp(22px,5.6vw,28px) var(--display)}
.eqrow .gap{width:100%;height:0}
.eqrow .pre{white-space:nowrap}
.eqrow input.ans{font-size:20px}
.eqrow input.sup{width:46px;font-size:16px;padding:3px 4px;align-self:flex-start;margin:-4px 2px 0 -2px}
.eqrow input.wide{width:112px}
.eqrow .lbl{font:700 17px var(--body);color:var(--muted)}
.ocard{font:700 16px/1.35 var(--body);border:2px solid var(--line);background:var(--paper);color:var(--ink);border-radius:12px;padding:8px 12px;cursor:pointer;text-align:left}
.ocard.on{border-color:var(--leaf);background:var(--cell)}
.ocard b{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:var(--leaf);color:var(--paper);font-size:14px;margin-right:6px;vertical-align:1px}
.oline,.opool{display:grid;gap:8px}
.oline{border:2px dashed var(--line);border-radius:14px;padding:10px;min-height:56px}
.mono .b,.big .b,.b{color:var(--plum)}
sup.e,.e{color:var(--yarn)}
.stg{width:100%;max-width:380px;height:auto;overflow:visible}
.stg .d{font-family:var(--display);font-weight:700}
.stg .h{font-family:var(--hand);font-weight:600}
.stage .say{justify-content:center}
.stage .say .pig{width:84px}
.stage .bubble{font-size:21px}
.count{font:700 16px var(--display);color:var(--muted)}
.word{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.word span{width:38px;height:46px;border-radius:10px;border:2px dashed var(--line);display:grid;place-items:center;font:700 24px var(--display);color:var(--muted);background:var(--cell)}
.word span.on{border:2px solid var(--leaf);background:var(--paper);color:var(--leaf)}
.chips{display:flex;flex-wrap:wrap;gap:4px;justify-content:center}
.chip{font:700 14px var(--display);background:var(--cell);border-radius:8px;padding:2px 7px;white-space:nowrap}
.why-card{display:grid;gap:8px;border:2px solid var(--leaf)}.why-card ul{margin:0;padding-left:1.2em;display:grid;gap:6px}.why-card b{color:var(--leaf)}.why-dip{margin-top:6px;font-weight:700}
.right-chip{display:grid;gap:3px;margin-top:4px;padding:10px 12px;border-left:4px solid var(--sky);background:var(--cell);border-radius:8px;font-size:14.5px;line-height:1.45}.right-chip b{font-size:12.5px;letter-spacing:.03em;text-transform:uppercase;color:var(--sky)}.right-chip q,.right-chip i{font-style:italic}.right-chip span{color:var(--muted)}
"""

SHEET_CSS = """
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.sheet{max-width:900px;margin:0 auto;padding-block:22px 36px;display:grid;gap:16px}
.head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 20px}
.htext{display:grid;gap:10px;flex:1 1 300px;min-width:0}
h1{font-family:var(--display);font-size:clamp(30px,6vw,44px);margin:0;line-height:1.1;text-wrap:balance}h1 span{color:var(--yarn)}
.cast{display:flex;gap:2px;flex-wrap:wrap;align-items:flex-end}.cast .pig{width:84px;height:auto}
.final{justify-content:center;flex-wrap:wrap}
.links{font-size:15px}
.box,.head,.final{break-inside:avoid}
"""


def card_css():
    """card styles = the 'living cards' block of base.css (shared by lesson and sheet)."""
    a = BASE_CSS.index('/* living cards */')
    b = BASE_CSS.index('body{background')
    head = BASE_CSS[:BASE_CSS.index('/* living cards */')]
    return head + BASE_CSS[a:b]


def rights_js(pool, lang):
    lab = 'Твої права · Конституція України, стаття ' if lang == 'uk' else 'Your rights · Constitution of Ukraine, Article '
    items = [{'n': n, 'q': (q_uk if lang == 'uk' else q_en), 'm': (m_uk if lang == 'uk' else m_en)} for n, q_uk, m_uk, q_en, m_en in pool]
    qtag = 'q' if lang == 'uk' else 'i'
    return ('<script>(function(){var POOL=' + json.dumps(items, ensure_ascii=False) + ',LAB=' + json.dumps(lab, ensure_ascii=False) + ';'
            'var panels=[].slice.call(document.querySelectorAll(".panel")).filter(function(p){return p.id!=="p-learn"&&p.id!=="p-report"});'
            'function solved(pref){try{return Object.keys(state.log).filter(function(k){return k[0]===pref&&state.log[k].ok}).length}catch(e){return 0}}'
            'function chip(panel,i){var k=(i*3+solved(panel.id[2]))%POOL.length,it=POOL[k];var d=document.createElement("div");d.className="right-chip";'
            f'd.innerHTML="<b></b><{qtag}></{qtag}><span></span>";d.children[0].textContent=LAB+it.n;d.children[1].textContent=it.q;d.children[2].textContent=it.m;return d}}'
            'function place(panel,i){var host=null;[].slice.call(panel.querySelectorAll(".task")).forEach(function(t){if(!t.hidden&&!host)host=t});'
            'if(!host){var l=panel.querySelector(".lead");if(!l)return;host=l}var old=host.querySelector(":scope > .right-chip"),n=chip(panel,i);'
            'if(old){if(old.textContent!==n.textContent)old.replaceWith(n);return}host.appendChild(n)}'
            'panels.forEach(function(panel,i){place(panel,i);new MutationObserver(function(){place(panel,i)}).observe(panel,{childList:true,subtree:true,attributes:true,attributeFilter:["hidden"]})});})();</script>')


def hist_banner(href, lang):
    """the 'separate section' banner that leads to the history and culture page (styles: /* history banner */ in base.css)."""
    if lang == 'uk':
        k, t, s, c = ('Окремий розділ сайту', 'Історія і культура України',
                      'Трипілля й Київська Русь, козаки, Будапештський меморандум, Корольов, Шевченко, «Щедрик», Примаченко',
                      'Тисни і дізнайся')
    else:
        k, t, s, c = ('A separate section of this site', 'Ukraine’s history and culture',
                      'Trypillia and Kyivan Rus, the Cossacks, the Budapest Memorandum, Korolyov, Shevchenko, Shchedryk, Prymachenko',
                      'Tap to find out')
    return (f'<a class="hist-banner" href="{href}"><span class="hb-medal" aria-hidden="true"></span><span class="hb-text">'
            f'<span class="hb-kicker">{k}</span><span class="hb-title">{t}</span><span class="hb-sub">{s}</span>'
            f'<span class="hb-cta">{c} <i>→</i></span></span></a>')


def why_js(why, lang, more=''):
    head = 'Навіщо це мені?' if lang == 'uk' else 'Why does this matter?'
    lis = ''.join(f'<li><b>{t}</b> {d}</li>' for t, d in why['items'])
    mp = hist_banner(more, lang) if more else ''
    card = f'<div class="card why-card"><h3>{head}</h3><ul>{lis}</ul>{mp}</div>'
    return ('<script>(function(){var box=document.getElementById("p-learn");if(box){var go=box.querySelectorAll("[data-go]"),last=go[go.length-1];'
            'var host=last?last.parentElement:null;while(host&&host.parentElement!==box)host=host.parentElement;var c=document.createElement("div");'
            'c.innerHTML=' + json.dumps(card, ensure_ascii=False) + ';if(host)box.insertBefore(c.firstChild,host);else box.appendChild(c.firstChild);}'
            'var dip=document.getElementById("diploma");if(dip){var p=document.createElement("p");p.className="why-dip";p.textContent='
            + json.dumps(why['dip'], ensure_ascii=False) + ';dip.appendChild(p);}})();</script>')


def wrap(kind, lang, title, styles, body, tail, desc=''):
    """kind: 'site' -> full document with home link, footer and site scripts; 'art' -> artifact fragment."""
    css = ''.join(f'<style>\n{s}\n</style>' for s in styles)
    if kind == 'site':
        return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">{RESET}\n'
                f'<title>{title}</title>\n{ICONS}\n{FONTS}\n{css}<style>{SITE_CSS}</style></head>\n'
                f'<body><nav class="site-home"><a href="../index.html">{HOME[lang]}</a></nav>\n{DEFS}\n{body}\n'
                f'<footer class="site-copy">{COPY[lang]}</footer>\n<script>{SHARE_JS}</script>\n{tail}\n<script>{STATS_JS}</script>\n</body></html>\n')
    return (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n{css}\n{DEFS}\n{body}\n{tail}\n'
            f'<script>document.documentElement.lang={json.dumps(lang)}</script>\n')


GAME_BODY = """<div class="wrap">
  <header class="hero">
    <div class="hero-text">
      <h1 data-t="h1"></h1>
      <p data-t="intro"></p>
      <p style="font-size:15px" data-t="langLink"></p>
      <div class="stars" aria-live="polite">
        <span data-t="yourStars"></span>
        <span class="star" id="st-a">★</span>
        <span class="star" id="st-b">★</span>
        <span class="star" id="st-c">★</span>
        <button class="btn ghost" id="resetAll" style="padding:4px 12px;font-size:14px"></button>
      </div>
      <div class="worldbar" id="worldbar"><span class="wb-mini" id="wbMini"></span><div class="wb-text"><b id="wbTitle"></b><span id="wbSub"></span></div><button class="btn" id="profBtn"></button></div>
      <div class="diploma" id="diploma" hidden><h3 data-t="dipH"></h3><p data-t="dipP"></p></div>
    </div>
    <div class="cast" id="heroCast"></div>
  </header>

  <section class="profile" id="profile" hidden></section>

  <nav class="tabs" role="tablist">
    <button class="tab" role="tab" data-tab="learn" id="t-learn" data-t="tabLearn"></button>
    <button class="tab" role="tab" data-tab="a" id="t-a" data-t="tabA"></button>
    <button class="tab" role="tab" data-tab="b" id="t-b" data-t="tabB"></button>
    <button class="tab" role="tab" data-tab="c" id="t-c" data-t="tabC"></button>
    <button class="tab" role="tab" data-tab="report" id="t-report" data-t="tabR"></button>
  </nav>

  <section class="panel" id="p-learn">
    <div class="lead"><h2 data-t="lH"></h2><p data-t="lIntro"></p></div>
    <div class="meet" id="meet"></div>
    __LESSON__
    <div class="note"><div class="notePig"></div><p class="hand" data-t="lBye"></p></div>
    <div><button class="btn" data-go="a" data-t="toA"></button></div>
  </section>
__LEVELS__
  <section class="panel" id="p-report" hidden>
    <div class="lead"><h2 data-t="rH"></h2><p data-t="rIntro"></p></div>
    <div class="card" id="reportCard"></div>
    <div class="row"><button class="btn" id="copyReport" data-t="copy"></button><span class="fb" id="copyFb" aria-live="polite"></span></div>
    <textarea id="reportText" readonly hidden rows="14" aria-label="Report text"></textarea>
  </section>
</div>"""

LEVEL_HTML = """
  <section class="panel" id="p-{L}" hidden>
    <div class="lead"><h2 data-t="{L}H"></h2><p data-t="{L}Intro"></p></div>
    <div class="level">
      <div class="card stage" id="{L}Stage"></div>
      <div class="card task" id="{L}Task"></div>
    </div>
    <div><button class="btn ghost" id="{L}Reset" data-t="levelReset"></button></div>
  </section>"""


def game_page(kind, lang, edition, title, lesson_html, tx, lv, stage_js, links, topic_key, pool, why, extra_css=''):
    body = GAME_BODY.replace('__LESSON__', lesson_html).replace('__LEVELS__', ''.join(LEVEL_HTML.replace('{L}', L) for L in 'abc'))
    cfg = (f'const LANG={json.dumps(lang)};const EDITION={json.dumps(edition)};const TOPIC_KEY={json.dumps(topic_key)};'
           f'const OTHER={json.dumps(links["other"])}, SHEET={json.dumps(links["sheet"])};\n'
           f'const WORLDS={json.dumps(WORLDS, ensure_ascii=False)};\n'
           f'const TX={json.dumps(tx, ensure_ascii=False)};\nconst LV={json.dumps(lv, ensure_ascii=False)};\n')
    script = f'<script>\n{cfg}{ICONS_JS}\n{stage_js}\n{ENGINE}</script>'
    tail = why_js(why, lang, links.get('edu', '')) + '\n' + rights_js(pool, lang)
    return wrap(kind, lang, title, [BASE_CSS, GAME_CSS + extra_css], body + '\n' + script, tail)


def sheet_page(kind, lang, title, h1, bubble, cast_svgs, cards_html, final_svg, final_text, links_html, extra_css=''):
    body = (f'<div class="sheet">\n <header class="head">\n  <div class="htext"><h1>{h1}</h1><p class="bubble">{bubble}</p>'
            f'<p class="links">{links_html}</p></div>\n  <div class="cast">{"".join(cast_svgs)}</div>\n </header>\n'
            f' <div class="grid">{cards_html}</div>\n <div class="say final">{final_svg}<p class="bubble">{final_text}</p></div>\n</div>')
    return wrap(kind, lang, title, [card_css(), SHEET_CSS + GAME_CSS + extra_css], body, '')


def pig(svg_markup, flip=False):
    """role svg -> small 'pig' icon used in .say blocks."""
    s = svg_markup.replace('class="pig"', 'class="pig"')
    if flip:
        s = s.replace('<svg ', '<svg style="transform:scaleX(-1)" ', 1)
    return s
