"""Build one topic: site pages (school edition) and artifact pages (home edition).
usage: python3 build.py powers [out_dir]"""
import json, sys, importlib
from pathlib import Path
import common

FOLDER = {'powers': 'powers', 'angles': 'angles', 'identities': 'identities'}
TITLE = {'powers': ('Степені з Понею і Булею', 'Powers with Ponya and Bulya'),
         'angles': ('Суміжні кути з Понею і Булею', 'Adjacent angles with Ponya and Bulya'),
         'identities': ('Тотожності з Понею і Булею', 'Identities with Ponya and Bulya')}


def build(topic, out):
    m = importlib.import_module('topic_' + topic)
    folder = FOLDER[topic]
    arts = {}
    p = Path(__file__).parent / 'artifacts.json'
    if p.exists():
        arts = json.loads(p.read_text()).get(topic, {})
    res = {}
    for lang in ('uk', 'en'):
        other = 'en' if lang == 'uk' else 'uk'
        for kind, edition in (('site', 'school'), ('art', 'home')):
            if kind == 'site':
                links = {'other': f'../{folder}/{other}.html', 'sheet': f'../{folder}/cheatsheet-{lang}.html', 'edu': '../education.html' if lang == 'uk' else '../education-en.html'}
                sheet_links = {'game': f'../{folder}/{lang}.html', 'other': f'../{folder}/cheatsheet-{other}.html',
                               'pdf': f'../{folder}/cheatsheet-{lang}.pdf'}
            else:
                links = {'other': arts.get(f'game-{other}', '#'), 'sheet': arts.get(f'sheet-{lang}', ''), 'edu': json.loads(p.read_text()).get('education', {}).get(lang, '') if p.exists() else ''}
                sheet_links = {'game': arts.get(f'game-{lang}', ''), 'other': arts.get(f'sheet-{other}', ''), 'pdf': ''}
            title = TITLE[topic][0 if lang == 'uk' else 1]
            if kind == 'site':
                title = title.replace(' з Понею і Булею', ' · Математична пасіка').replace(' with Ponya and Bulya', ' · The Maths Apiary')
            html = common.game_page(kind, lang, edition, title, m.lesson(lang), m.texts(lang, edition), m.levels(lang, edition),
                                    m.STAGE_JS, links, m.KEY, m.rights(), m.why(lang), getattr(m, 'EXTRA_CSS', ''))
            name = f'{lang}.html' if kind == 'site' else f'game-{lang}.html'
            res[(kind, name)] = html
            sh = m.sheet(lang)
            t = (lambda uk, en: uk if lang == 'uk' else en)
            parts = []
            if sheet_links['game']:
                parts.append(f'<a href="{sheet_links["game"]}">{t("Урок і гра", "Lesson and game")}</a>')
            if sheet_links['other']:
                parts.append(f'<a href="{sheet_links["other"]}">{t("English version", "Українська версія")}</a>')
            if sheet_links['pdf']:
                parts.append(f'<a href="{sheet_links["pdf"]}">{t("PDF для друку", "PDF to print")}</a>')
            shtml = common.sheet_page(kind, lang, sh['title'], sh['h1'], sh['bubble'], sh['cast'], sh['cards'], sh['final_svg'],
                                      sh['final'], ' · '.join(parts), getattr(m, 'EXTRA_CSS', ''))
            res[(kind, f'cheatsheet-{lang}.html' if kind == 'site' else f'sheet-{lang}.html')] = shtml
    for (kind, name), html in res.items():
        d = Path(out) / kind / folder
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(html)
    # data for task labels / stats
    labels = {}
    for lang in ('uk', 'en'):
        lv = m.levels(lang, 'school')
        tx = m.texts(lang, 'school')
        names = {L: tx['worlds']['meadow']['tab' + L.upper()].split('. ', 1)[1] for L in 'abc'}
        labels[f'{folder}-{lang}'] = [{'level': names[L], 'rows': [[L + str(i), t['label']] for i, t in enumerate(lv[L]['tasks'])]} for L in 'abc']
    (Path(out) / f'labels-{folder}.json').write_text(json.dumps(labels, ensure_ascii=False, indent=1))
    return res


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '/home/claude/work/out')
    print('ok')
