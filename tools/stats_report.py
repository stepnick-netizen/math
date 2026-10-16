#!/usr/bin/env python3
"""Teacher report from GoatCounter statistics of the "Maths with Ponya and Bulya" site.

Usage:
  GC_TOKEN=... python3 tools/stats_report.py --out report.html [--json summary.json] [--start 2026-10-16]
  python3 tools/stats_report.py --from-json hits.json --out report.html     (offline test)

The token needs only "Read statistics". It is never written to any output.
Everything is anonymous: GoatCounter stores no names, only counts of visits and events.
"""
import argparse, collections, datetime as dt, html, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

SITE = 'https://varia-math.goatcounter.com'
HERE = Path(__file__).parent
LABELS = json.loads((HERE / 'task-labels.json').read_text())

TOPICS = {'percentages': 'Відсотки', 'proportions': 'Пропорції', 'monomials': 'Одночлени',
          'powers': 'Степені', 'angles': 'Суміжні кути', 'identities': 'Тотожності й вирази'}
LEVELS = {  # tab id -> level name, star id -> level
    'percentages': {'tabs': {'plaid': 'Плед', 'shop': 'Ярмарок', 'det': 'Детектив'},
                    'stars': {'plaid': 'Плед', 'shop': 'Ярмарок', 'det': 'Детектив'}},
    'proportions': {'tabs': {'p': 'Терези', 'k': 'Кухня', 'c': 'Картки'},
                    'stars': {'p': 'Терези', 'k': 'Кухня', 'c': 'Картки'}},
    'monomials': {'tabs': {'a': 'Рівень 1 (кошики)', 'b': 'Рівень 2 (бирки)', 'c': 'Рівень 3 (множення і степені)'},
                  'stars': {'a': 'Рівень 1 (кошики)', 'b': 'Рівень 2 (бирки)', 'c': 'Рівень 3 (множення і степені)'}},
    'powers': {'tabs': {'a': 'Рівень 1 (правила)', 'b': 'Рівень 2 (замки)', 'c': 'Рівень 3 (спільна основа)'},
               'stars': {'a': 'Рівень 1 (правила)', 'b': 'Рівень 2 (замки)', 'c': 'Рівень 3 (спільна основа)'}},
    'angles': {'tabs': {'a': 'Рівень 1 (чи суміжні)', 'b': 'Рівень 2 (креслення)', 'c': 'Рівень 3 (відношення)'},
               'stars': {'a': 'Рівень 1 (чи суміжні)', 'b': 'Рівень 2 (креслення)', 'c': 'Рівень 3 (відношення)'}},
    'identities': {'tabs': {'a': 'Рівень 1 (тотожність чи ні)', 'b': 'Рівень 2 (блоки)', 'c': 'Рівень 3 (доведення)'},
                   'stars': {'a': 'Рівень 1 (тотожність чи ні)', 'b': 'Рівень 2 (блоки)', 'c': 'Рівень 3 (доведення)'}},
}
WORLDS = {'meadow': 'Луг', 'space': 'Космос', 'bricks': 'Цеглинки'}
BASKET = {'no': '«не одночлен»', 'mess': '«одночлен, але безлад»', 'std': '«стандартний вигляд»'}

# monomials error codes -> what the teacher should know
ERR = {
    'coef-sign': 'загубили або додали мінус у коефіцієнті',
    'coef-added': 'числа додали замість того, щоб перемножити',
    'coef-first-only': 'взяли лише перше число, решту чисел не помножили',
    'coef-times-n': 'число помножили на показник замість піднести до степеня (напр. 3·2 замість 3²)',
    'coef-not-powered': 'забули піднести число до степеня',
    'coef-multiplied': 'числа перемножили замість поділити',
    'coef-subtracted': 'числа відняли замість поділити',
    'coef-divided-by-n': 'число поділили на показник замість добути корінь',
    'coef-not-rooted': 'залишили число без змін замість добути корінь',
    'coef-other': 'інша помилка в коефіцієнті',
    'exp-not-combined': 'не об’єднали однакові літери (x·x лишили як x)',
    'exp-multiplied': 'показники перемножили замість додати',
    'exp-forgot-hidden-1': 'забули, що літера без показника має показник 1',
    'exp-added': 'показники додали замість перемножити (або відняти)',
    'exp-not-raised': 'показник літери не помножили на степінь за дужкою',
    'exp-divided': 'показники поділили замість відняти',
    'exp-not-subtracted': 'показник не зменшили (не відняли)',
    'exp-subtracted': 'від показника відняли степінь замість поділити',
    'exp-not-divided': 'показник не поділили на степінь',
    'exp-other': 'інша помилка в показнику',
    'label-coef-sign': 'у бирці: коефіцієнт з неправильним знаком',
    'label-coef-hidden-1-as-0': 'у бирці: невидиму одиничку записали як 0',
    'label-coef-other': 'у бирці: неправильний коефіцієнт',
    'label-degree-added-coef': 'у бирці: до степеня додали коефіцієнт',
    'label-degree-counted-letters': 'у бирці: замість степеня порахували кількість літер',
    'label-degree-largest-only': 'у бирці: взяли лише найбільший показник',
    'label-degree-forgot-hidden-1': 'у бирці: у степені не врахували показники 1',
    'label-degree-other': 'у бирці: інша помилка в степені',
    # powers, angles, identities
    'exp-all-added': 'усі показники додали, хоча треба було відняти при діленні',
    'exp-brackets-ignored': 'не врахували дужки в знаменнику',
    'exp-added-not-multiplied': 'у степені степеня показники додали замість перемножити',
    'value-times-n': 'основу помножили на показник (напр. 9·2 замість 9²)',
    'value-sign': 'загубили або додали мінус у відповіді',
    'value-square': 'піднесли до квадрата замість куба',
    'value-added': 'множники додали замість перемножити',
    'added-bases': 'основи додали замість перемножити',
    'copied-angle': 'переписали відомий кут замість знайти суміжний',
    'used-90': 'віднімали від 90° замість 180°',
    'added-180': 'додали 180° замість відняти',
    'said-yes': 'відповіли «так», хоча кути не суміжні',
    'said-no': 'відповіли «ні», хоча кути суміжні (або рівні)',
    'bisector-halved': 'бісектрису поділили ще раз навпіл',
    'bisector-same': 'забули, що бісектриса ділить кут навпіл',
    'whole-not-part': 'узяли весь кут замість частини',
    'subtracted-one': 'відняли від 180° лише один із кутів',
    'difference': 'знайшли різницю кутів замість потрібного кута',
    'guess-90': 'відповіли 90° навмання',
    'half-not-whole': 'знайшли половину кута замість усього кута',
    'used-whole-angle': 'віднімали весь кут замість половини',
    'divided-by-3': 'поділили 180° на 3 замість на 4 частини',
    'divided-by-2': 'поділили 180° навпіл, не врахувавши відношення',
    'ignored-difference': 'не врахували різницю між кутами',
    'bigger-not-smaller': 'знайшли більший кут замість меншого',
    'not-halved': 'забули поділити на 2',
    'difference-as-angle': 'різницю сприйняли як сам кут',
    'used-7-parts': 'ділили 180° лише на частини більшого кута',
    'added-not-multiplied': 'частини додали замість помножити',
    'divided-by-one-part': 'ділили 180° на частини лише одного кута',
    'left-sign': 'помилка знаку в лівій частині',
    'right-sign': 'помилка знаку в правій частині',
    'not-identity-as-identity': 'назвали тотожністю рівність, яка нею не є',
    'identity-as-not': 'тотожність назвали «не тотожністю»',
    'power-missed': 'не помітили, що блок треба піднести до степеня',
    'factor-missed': 'не помітили множник перед блоком',
    'sign': 'помилка знаку',
    'zero': 'відповіли 0 замість найменшого значення виразу',
    'added-2': 'додали число з дужки до відповіді',
    'coef-added': 'числа додали замість перемножити',
}


def fetch_hits(token, start, end):
    hits, exclude = [], []
    for _ in range(50):
        q = [('start', start), ('end', end), ('limit', '100')] + [('exclude_paths', str(i)) for i in exclude]
        req = urllib.request.Request(f'{SITE}/api/v0/stats/hits?' + urllib.parse.urlencode(q),
                                     headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        new = [h for h in d.get('hits', []) if h['path_id'] not in exclude]
        hits += new
        exclude += [h['path_id'] for h in new]
        if not d.get('more') or not new:
            break
    return [{'path': h['path'], 'count': h['count'], 'event': h.get('event', False),
             'days': {s['day']: s.get('daily', 0) for s in h.get('stats', [])}} for h in hits]


def label_for(topic, key):
    for lang in ('uk', 'en'):
        for lvl in (LABELS.get(f'{topic}-{lang}') or []):
            for k, lab in lvl['rows']:
                if k == key:
                    return lab
    return key


def analyse(hits, since=None):
    pages = collections.Counter()
    ev = collections.defaultdict(collections.Counter)  # topic -> event name -> count
    recent = collections.defaultdict(collections.Counter)
    for h in hits:
        p = h['path']
        if not h['event']:
            pages[p] += h['count']
            continue
        m = re.match(r'^([a-z]+)-(uk|en|index)/(.+)$', p) or re.match(r'^(math)-(index|index-en)/(.+)$', p)
        if not m:
            continue
        topic = m.group(1)
        ev[topic][m.group(3)] += h['count']
        if since:
            recent[topic][m.group(3)] += sum(v for d, v in h['days'].items() if d >= since)
    return pages, ev, recent


def topic_summary(topic, e):
    lv = LEVELS[topic]
    funnel = []
    for tid, name in lv['tabs'].items():
        funnel.append((name, e.get(f'tab-{tid}', 0), e.get(f'level-done-{tid}', 0)))
    tasks = collections.OrderedDict()
    for name, cnt in e.items():
        m = re.match(r'^task-(.+)-(first-try|after-mistakes|mistake)$', name)
        if m:
            tasks.setdefault(m.group(1), collections.Counter())[m.group(2)] += cnt
    typed = collections.defaultdict(collections.Counter)
    for name, cnt in e.items():
        m = re.match(r'^typed-([^/]+)/(.+)$', name)
        if m:
            typed[m.group(1)][m.group(2)] += cnt
    errs = collections.defaultdict(collections.Counter)
    for name, cnt in e.items():
        m = re.match(r'^err-([a-z])(\d+)-(.+)$', name)
        if not m:
            continue
        key, rest = m.group(1) + m.group(2), m.group(3)
        mb = re.match(r'^(no|mess|std)-as-(no|mess|std)$', rest)
        mr = re.match(r'^rule-(add|sub|mul)-as-(add|sub|mul)$', rest)
        RULES = {'add': 'додати показники', 'sub': 'відняти показники', 'mul': 'помножити показники'}
        mo = re.match(r'^order-pos(\d+)$', rest)
        if mr:
            desc = f'вибрали правило «{RULES[mr.group(2)]}» замість «{RULES[mr.group(1)]}»'
        elif mo:
            desc = f'у доведенні переплутали порядок (перша помилка на кроці {mo.group(1)})'
        elif re.match(r'^(right|acute)-as-(acute|right|obtuse)$', rest):
            a, b = rest.split('-as-')
            nm = {'right': 'прямий', 'acute': 'гострий', 'obtuse': 'тупий'}
            desc = f'суміжний із кутом «{nm[a]}» назвали «{nm[b]}»'
        elif mb:
            desc = f'поклали в кошик {BASKET[mb.group(2)]} замість {BASKET[mb.group(1)]}'
        else:
            code = re.sub(r'^exp-[a-z]-', 'exp-', rest)
            letter = re.match(r'^exp-([a-z])-', rest)
            desc = ERR.get(code, rest) + (f' (літера {letter.group(1)})' if letter else '')
        errs[key][desc] += cnt
    rows = []
    for key, c in tasks.items():
        solved = c['first-try'] + c['after-mistakes']
        rate = c['first-try'] / solved if solved else None
        rows.append(dict(key=key, label=label_for(topic, key), first=c['first-try'], after=c['after-mistakes'],
                         mistake=c['mistake'], rate=rate, typed=typed[key].most_common(3), errs=errs[key].most_common(3)))
    rows.sort(key=lambda r: (r['rate'] if r['rate'] is not None else 2, -r['mistake']))
    return dict(funnel=funnel, tasks=rows, worlds={WORLDS.get(k[6:], k[6:]): v for k, v in e.items() if k.startswith('world-')},
                sent=e.get('report-send', 0), copied=e.get('report-copy', 0), diplomas=e.get('diploma', 0),
                lesson=e.get('tab-learn', 0), report_tab=e.get('tab-report', 0))


def pct(x):
    return '—' if x is None else f'{round(x * 100)}%'


def render(pages, ev, recent, start, end, since):
    E = html.escape
    total_views = sum(v for p, v in pages.items())
    topic_views = {t: sum(v for p, v in pages.items() if f'/{t}/' in p and 'cheatsheet' not in p) for t in TOPICS}
    sheet_views = sum(v for p, v in pages.items() if 'cheatsheet' in p)
    sections, insights = [], []
    for t, tname in TOPICS.items():
        e = ev.get(t, {})
        if not e and not topic_views[t]:
            sections.append(f'<section class="card"><h2>{tname}</h2><p class="muted">Поки що немає даних.</p></section>')
            continue
        s = topic_summary(t, e)
        fun = ''.join(f'<tr><td>{E(n)}</td><td class="num">{o}</td><td class="num">{d}</td><td class="num">{pct(d / o if o else None)}</td></tr>'
                      for n, o, d in s['funnel'])
        trs = []
        for r in s['tasks']:
            hard = r['rate'] is not None and r['rate'] < 0.5 and (r['first'] + r['after']) >= 3
            typed = ', '.join(f'{E(v)} ({c})' for v, c in r['typed']) or '—'
            errs = '<br>'.join(f'{E(d)} — {c}' for d, c in r['errs']) or ''
            trs.append(f'<tr class="{"hard" if hard else ""}"><td>{E(r["label"])}</td><td class="num">{r["first"]}</td>'
                       f'<td class="num">{r["after"]}</td><td class="num"><b>{pct(r["rate"])}</b></td><td>{typed}</td><td>{errs}</td></tr>')
            if hard:
                insights.append(f'<li><b>{E(tname)}</b>: «{E(r["label"])}» — з першої спроби лише {pct(r["rate"])}'
                                + (f'; найчастіше: {E(r["errs"][0][0])}' if r['errs'] else '') + '.</li>')
        worlds = ', '.join(f'{E(k)}: {v}' for k, v in sorted(s['worlds'].items(), key=lambda x: -x[1])) or '—'
        sections.append(f'''<section class="card"><h2>{tname}</h2>
<p class="muted">Переглядів сторінок гри: {topic_views[t]} · дипломів: {s["diplomas"]} · звітів надіслано: {s["sent"]}, скопійовано: {s["copied"]}{f" · світи: {worlds}" if s["worlds"] else ""}</p>
<h3>Хто доходить до кінця рівня</h3>
<div class="scroll"><table><tr><th>Рівень</th><th class="num">Відкрили</th><th class="num">Пройшли</th><th class="num">Частка</th></tr>{fun}</table></div>
<h3>Задачі: від найважчих до найлегших</h3>
<div class="scroll"><table><tr><th>Задача</th><th class="num">З першої спроби</th><th class="num">Після помилок</th><th class="num">Частка з першої</th><th>Що вводили неправильно</th><th>Типові помилки</th></tr>{"".join(trs) or '<tr><td colspan="6" class="muted">Поки що немає розв’язаних задач.</td></tr>'}</table></div>
</section>''')
    rec_total = sum(sum(c.values()) for c in recent.values())
    head = f'''<p>Період: <b>{start} — {end}</b>. Переглядів сторінок: <b>{total_views}</b> (шпаргалки: {sheet_views}). Подій за останні 2 дні: <b>{rec_total}</b>.</p>'''
    ins = f'<section class="card key"><h2>Головне для вчителя</h2><ul>{"".join(insights[:8])}</ul></section>' if insights else \
          '<section class="card key"><h2>Головне для вчителя</h2><p>Поки що замало розв’язаних задач для висновків. Важкою задача вважається, коли менше половини учнів розв’язує її з першої спроби (і є хоча б 3 спроби).</p></section>'
    return f'''<title>Статистика сайту з математики</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@700&family=Nunito:wght@400;700;800&display=swap">
<style>
/* Layout: meadow palette report; key findings first, then one card per topic with funnel and task tables */
:root{{--bg:#EEF3E4;--paper:#fff;--ink:#26301F;--muted:#5F6B55;--line:#D3DCC5;--yarn:#D9486F;--marker:#FFE24A;--marker-ink:#2A2300;--bad:#C2413B;--cell:#F4F7EE;
--display:'Comfortaa','Nunito',system-ui,sans-serif;--body:'Nunito',system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#171C14;--paper:#222A1D;--ink:#EDF2E3;--muted:#A8B49B;--line:#3A4532;--yarn:#F07898;--marker:#E8C93A;--marker-ink:#1D1800;--bad:#F07A72;--cell:#2C3526;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#171C14;--paper:#222A1D;--ink:#EDF2E3;--muted:#A8B49B;--line:#3A4532;--yarn:#F07898;--marker:#E8C93A;--marker-ink:#1D1800;--bad:#F07A72;--cell:#2C3526;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.wrap{{max-width:1000px;margin:0 auto;padding-block:20px 48px;display:grid;gap:18px}}
h1,h2,h3{{font-family:var(--display);margin:0;line-height:1.2;text-wrap:balance}} h1{{font-size:clamp(26px,5vw,38px)}} h2{{font-size:22px}} h3{{font-size:16px;margin-top:6px}}
p{{margin:0}} .muted{{color:var(--muted)}}
.card{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:16px 18px;display:grid;gap:10px;min-width:0}}
.key{{background:var(--marker);color:var(--marker-ink);border-color:var(--marker)}}
.key ul{{margin:0;padding-left:1.2em;display:grid;gap:4px}}
.scroll{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:14.5px}}
th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-weight:800;color:var(--muted);font-size:13px}}
th.num,td.num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
tr.hard td{{background:color-mix(in srgb,var(--bad) 12%,transparent)}}
.foot{{font-size:13px;color:var(--muted)}}
</style>
<div class="wrap">
<h1>Статистика сайту з математики</h1>
{head}
{ins}
{"".join(sections)}
<p class="foot">Дані анонімні: GoatCounter рахує відвідування й події без імен і без cookies. Частина відвідувань не потрапляє в статистику через блокувальники реклами. «Частка з першої» = з першої спроби / усі розв’язані. Червоним позначено задачі, де з першої спроби розв’язує менше половини (від 3 розв’язків).</p>
</div>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--json')
    ap.add_argument('--start', default='2026-10-16')
    ap.add_argument('--from-json')
    a = ap.parse_args()
    end = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    since = (dt.date.today() - dt.timedelta(days=2)).isoformat()
    if a.from_json:
        hits = json.loads(Path(a.from_json).read_text())
    else:
        tok = os.environ.get('GC_TOKEN')
        if not tok:
            sys.exit('GC_TOKEN is not set')
        hits = fetch_hits(tok, a.start, end)
    pages, ev, recent = analyse(hits, since)
    Path(a.out).write_text(render(pages, ev, recent, a.start, dt.date.today().isoformat(), since))
    if a.json:
        Path(a.json).write_text(json.dumps({
            'pages': pages, 'events': {t: dict(c) for t, c in ev.items()},
            'topics': {t: topic_summary(t, ev.get(t, {})) for t in TOPICS if t in ev}}, ensure_ascii=False, indent=1, default=str))
    print(f'hits: {len(hits)}, events by topic:', {t: sum(c.values()) for t, c in ev.items()})


if __name__ == '__main__':
    main()
