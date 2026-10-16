"""Page «Освіта — наша сила»: true stories of countries that grew strong through education, and Ukraine.
Facts checked 17.10.2026: Hinsley (British Academy memoir), Korea (Library of Congress country study), Estonia (educationestonia.org),
Ukraine literacy 99.97% (World Bank/UNESCO via indexmundi, 2012), MESM (Kyiv, 1950), Viazovska (Fields Medal 2022), Brave1 (itc.ua, 29.04.2024)."""
from svgkit import Run, text, hand, line, rect, circle, path, svg, width
from common import ROLE_SVG, pig, wrap, card_css, SHEET_CSS, GAME_CSS


def big(num, cap, col='l', w=320, h=150, sub=None):
    b = text(w / 2, 82, num, 56 if width(num, 56) < w - 20 else 40, col, 'd', 'middle')
    b += hand(w / 2, 124, cap, 24, 'm')
    if sub:
        b += hand(w / 2, 148, sub, 20, 'm')
        h = 160
    return svg(w, h, b, f'{num} {cap}')


def cards(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    W = 'meadow'
    out = []
    # 1 Bletchley
    out.append(('', t('Математики скоротили війну', 'Mathematicians shortened a war'),
                t('Британія, 1939–1945. У Блечлі-Парку математики, серед них Алан Тюрінг, зламали німецький шифр «Енігма» і читали таємні накази ворога.',
                  'Britain, 1939–1945. At Bletchley Park, mathematicians including Alan Turing broke the German Enigma code and read the enemy’s secret orders.'),
                big(t('−2 роки', '−2 years'), t('війни', 'of war')),
                t('Історик розвідки Гаррі Гінслі, який сам там працював, оцінив: без цієї роботи Друга світова могла тривати на рік-два довше. Це мільйони врятованих життів.',
                  'Intelligence historian Harry Hinsley, who worked there himself, estimated that without this work the Second World War could have lasted one to two years longer. That means millions of lives saved.')))
    # 2 Korea
    b = rect(70, 104 - 22 * 0.9, 60, 22 * 0.9, 'var(--bad)', 'b', 0, 4) + rect(190, 104 - 88 * 0.9, 60, 88 * 0.9, 'var(--leaf)', 'l', 0, 4)
    b += line(50, 104, 270, 104, 'i', 2) + text(100, 74, '22 %', 20, 'b', 'd', 'middle') + text(220, 16, '≈ 88 %', 20, 'l', 'd', 'middle')
    b += text(100, 126, '1945', 18, 'm', 'd', 'middle') + text(220, 126, '1970', 18, 'm', 'd', 'middle')
    b += hand(160, 152, t('дорослі, що вміють читати', 'adults who can read'), 21, 'm')
    out.append(('', t('Із бідності — до лідерства', 'From poverty to the top'),
                t('Південна Корея, зруйнована війною. У 1945 році читати вмів лише кожен п’ятий дорослий. Країна вклалася в школи й університети.',
                  'South Korea, wrecked by war. In 1945 only one adult in five could read. The country invested in schools and universities.'),
                svg(320, 162, b, '22% → 88%'),
                t('За 25 років читати вміли майже 9 із 10. Сьогодні Корея — одна з найрозвиненіших технологічних країн світу: телефони, кораблі, комп’ютерні чипи.',
                  'Within 25 years almost 9 in 10 could read. Today Korea is one of the world’s most advanced technology countries: phones, ships, computer chips.')))
    # 3 Estonia
    b = line(30, 70, 290, 70, 'i', 3)
    for x, yr, cap in ((40, '1996', t('старт', 'start')), (180, '2000', t('комп’ютери', 'computers')), (280, '2001', t('інтернет', 'internet'))):
        b += circle(x, 70, 9, 'var(--sky)', 's', 0) + text(x, 50, yr, 18, 's', 'd', 'middle') + hand(x, 100, cap, 20, 'm')
    b += hand(160, 136, t('у кожній школі країни', 'in every school in the country'), 22, 'l')
    out.append(('', t('Маленька країна, великий стрибок', 'A small country, a big leap'),
                t('Естонія, 1996 рік. Програма «Стрибок тигра»: за п’ять років усі школи отримали комп’ютери й інтернет, а вчителі вчилися нового.',
                  'Estonia, 1996. The Tiger Leap programme: within five years every school had computers and the internet, and teachers learned new skills.'),
                svg(320, 148, b, 'Tiger Leap 1996–2001'),
                t('Ці діти виросли й побудували одну з найцифровіших держав світу.', 'Those children grew up and built one of the most digital countries in the world.')))
    # 4 Ukraine literacy + MESM
    out.append(('', t('Україна — країна, яка вчиться', 'Ukraine is a country that learns'),
                t('Читати й писати в Україні вміють майже всі дорослі.', 'Almost every adult in Ukraine can read and write.'),
                big('99,97 %' if lang == 'uk' else '99.97%', t('дорослих грамотні', 'of adults can read'), sub=t('за даними 2012 року', 'figure for 2012')),
                t('А ще в Києві в 1950 році запрацювала МЕСМ — одна з перших електронних обчислювальних машин у Європі. Її створила команда Сергія Лебедєва.',
                  'And in Kyiv in 1950 MESM started working: one of the first electronic computers in Europe, built by Serhiy Lebedev’s team.')))
    # 5 Viazovska
    b = circle(160, 70, 52, 'var(--marker)', 'h', 4) + text(160, 64, '2022', 26, 'k', 'd', 'middle') + text(160, 92, t('Філдс', 'Fields'), 18, 'k', 'd', 'middle')
    b += hand(160, 150, t('найвища нагорода математиків', 'the highest prize in maths'), 22, 'm')
    out.append(('', t('Українка — серед найкращих математиків світу', 'A Ukrainian among the world’s best mathematicians'),
                t('Марина В’язовська народилася в Києві у 1984 році. У 2022 році вона отримала Філдсівську премію — другою жінкою в історії.',
                  'Maryna Viazovska was born in Kyiv in 1984. In 2022 she won the Fields Medal, only the second woman ever to do so.'),
                svg(320, 160, b, 'Fields Medal 2022'),
                t('Над тим, як найщільніше укласти кулі, математики думали понад 400 років, ще з часів Кеплера. Марина довела відповідь для 8-вимірного простору. А почалося все з математичних олімпіад, у яких вона брала участь школяркою в Києві.',
                  'Mathematicians have wondered how to pack spheres as tightly as possible for over 400 years, since Kepler. Maryna proved the answer in 8 dimensions. It all started with maths olympiads she took part in as a schoolgirl in Kyiv.')))
    # 6 Brave1
    out.append(('', t('Освіта захищає сьогодні', 'Education protects us today'),
                t('У 2023 році в Україні запрацював оборонний кластер Brave1. Інженери й програмісти приносять туди свої винаходи.',
                  'In 2023 Ukraine launched the Brave1 defence tech cluster. Engineers and programmers bring their inventions there.'),
                big('1671', t('розробка за перший рік', 'inventions in the first year'), 'y'),
                t('Дрони, роботи для розмінування, техніка для евакуації поранених. За кожною розробкою — люди, які колись так само розв’язували задачі в школі.',
                  'Drones, demining robots, vehicles to rescue the wounded. Behind every invention are people who once solved problems at school, just like you.')))
    html = ''
    for i, (cls, h2, p, sv, tail) in enumerate(out, 1):
        html += f'<section class="box {cls}"><span class="n">{i}</span><h2>{h2}</h2><p>{p}</p>{sv}<p class="tail">{tail}</p></section>'
    # 7. why the empire feared Ukrainian schools: a timeline
    ev = [(1863, t('Валуєвський циркуляр', 'Valuev circular')), (1876, t('Емський указ', 'Ems decree')),
          (1933, t('Голодомор', 'Holodomor')), (1937, t('Розстріляне відродження', 'Executed Renaissance')), (2022, t('велика війна', 'full-scale war'))]
    b = line(20, 60, 400, 60, 'i', 3)
    xs = [40, 122, 205, 290, 375]
    for (yr, cap), x in zip(ev, xs):
        b += circle(x, 60, 8, 'var(--yarn)', 'y', 0) + text(x, 40, str(yr) if yr != 1933 else '1932–33', 15 if yr != 1933 else 13, 'y', 'd', 'middle')
        words = cap.split(' ', 1)
        b += hand(x, 88, words[0], 17, 'm') + (hand(x, 106, words[1], 17, 'm') if len(words) > 1 else '')
    b += hand(210, 146, t('а ми — тут, вчимося й живемо', 'and we are still here, learning and living'), 23, 'l')
    sv = svg(420, 158, b, t('спроби знищити Україну', 'attempts to destroy Ukraine'))
    hist = (f'<section class="box wide"><span class="n">7</span><h2>{t("Чому нас хотіли лишити без мови й шкіл", "Why they tried to take our language and schools")}</h2>'
            f'<p>{t("Російська імперія, а потім радянська влада не раз намагалися знищити українців: їхню мову, школи, учених і саме життя.", "The Russian Empire, and later the Soviet regime, tried again and again to destroy Ukrainians: their language, their schools, their scholars and their very lives.")}</p>{sv}'
            '<ul class="tl">'
            + ''.join(f'<li>{x}</li>' for x in [
                t('<b>1863.</b> Міністр Валуєв підписав циркуляр, де йшлося, що окремої української мови «не було, немає і бути не може», і заборонив друкувати нею підручники та книжки для народу.',
                  '<b>1863.</b> Minister Valuev signed a circular claiming that a separate Ukrainian language had never existed and could not exist, and stopped schoolbooks and books for ordinary people being printed in Ukrainian.'),
                t('<b>1876.</b> Емський указ заборонив навіть ноти з українськими словами й вистави українською.', '<b>1876.</b> The Ems decree banned even sheet music with Ukrainian words and plays in Ukrainian.'),
                t('<b>1932–1933.</b> Голодомор: штучний голод, влаштований радянською владою, забрав життя мільйонів українців. Україна визнала його геноцидом українського народу.',
                  '<b>1932–1933.</b> The Holodomor: a famine engineered by the Soviet regime killed millions of Ukrainians. Ukraine recognises it as genocide of the Ukrainian people.'),
                t('<b>1930-ті.</b> Радянська влада знищила сотні українських письменників, учених і вчителів. Це покоління називають «Розстріляним відродженням».',
                  '<b>1930s.</b> The Soviet regime killed hundreds of Ukrainian writers, scholars and teachers. This generation is called the Executed Renaissance.'),
                t('<b>Від 2022.</b> Росія веде повномасштабну війну проти України. За даними МОН на серпень 2025 року, 1779 шкіл пошкоджено, а 226 зруйновано.',
                  '<b>Since 2022.</b> Russia has been waging a full-scale war against Ukraine. According to Ukraine’s Ministry of Education, by August 2025 1,779 schools had been damaged and 226 destroyed.')])
            + '</ul>'
            f'<p class="more">{t("Чому саме мова й школи? Бо освічений народ, який знає свою історію, не скориш. Ось чому навчання для нас — це теж захист.", "Why language and schools? Because a people that is educated and knows its history cannot be conquered. That’s why learning is also a way to defend ourselves.")}</p></section>')
    final = t('Нас намагалися знищити сотні років — а ми тут: вчимося, творимо, захищаємо одне одного. Україна була, є і буде!',
              'They tried to destroy us for hundreds of years, and we are still here: learning, creating and protecting each other. Ukraine was, is and will be!')
    key = (f'<section class="box key wide"><span class="n">8</span><h2>{t("Що з цього для тебе", "What this means for you")}</h2>'
           f'<p><b>{t("Країни ставали сильними тоді, коли їхні діти вчилися. Україна — освічена країна, і від кожного з нас залежить, щоб так було й далі. Кожен урок, навіть в укритті чи онлайн, робить Україну сильнішою.", "Countries grew strong when their children learned. Ukraine is an educated country, and it’s up to each of us to keep it that way. Every lesson, even in a shelter or online, makes Ukraine stronger.")}</b></p>'
           f'<div class="say">{pig(ROLE_SVG[W]["tidy"])}<p class="hand">{final}</p></div></section>')
    html += hist
    return html + key


def page(kind, lang, links):
    t = lambda uk, en: uk if lang == 'uk' else en
    title = t('Освіта — наша сила', 'Education is our strength')
    cast = ''.join(pig(ROLE_SVG['meadow'][r], r == 'hostB') for r in ('hostA', 'hostB', 'tidy', 'messy'))
    lk = ' · '.join(f'<a href="{h}">{n}</a>' for n, h in links if h)
    body = (f'<div class="sheet">\n <header class="head">\n  <div class="htext"><h1>{t("Освіта — <span>наша сила</span>", "Education is <span>our strength</span>")}</h1>'
            f'<p class="bubble">{t("Привіт! Ми зібрали справжні історії про країни, які стали сильними завдяки навчанню. І про Україну: чому нас хотіли лишити без шкіл і чому ми все одно вчимося.", "Hi! Here are true stories of countries that became strong by learning. And about Ukraine: why others tried to take our schools away, and why we keep learning anyway.")}</p>'
            f'<p class="links">{lk}</p></div>\n  <div class="cast">{cast}</div>\n </header>\n <div class="grid">{cards(lang)}</div>\n</div>')
    if kind == 'site':
        body = body  # wrap() adds the home link and footer
    return wrap(kind, lang, title, [card_css(), SHEET_CSS + GAME_CSS + '.tl{margin:0;padding-left:1.1em;display:grid;gap:6px;font-size:15.5px}.tl b{color:var(--yarn)}'], body, '')


if __name__ == '__main__':
    import sys
    from pathlib import Path
    out = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/out')
    arts = {}
    p = Path(__file__).parent / 'artifacts.json'
    if p.exists():
        import json
        arts = json.loads(p.read_text()).get('education', {})
    for lang in ('uk', 'en'):
        other = 'en' if lang == 'uk' else 'uk'
        (out / 'site').mkdir(parents=True, exist_ok=True)
        (out / 'art').mkdir(parents=True, exist_ok=True)
        site_links = [('English version' if lang == 'uk' else 'Українська версія', 'education-en.html' if lang == 'uk' else 'education.html')]
        (out / 'site' / ('education.html' if lang == 'uk' else 'education-en.html')).write_text(page('site', lang, site_links).replace('href="../index.html"', 'href="index.html"' if lang == 'uk' else 'href="index-en.html"'))
        art_links = [('English version' if lang == 'uk' else 'Українська версія', arts.get(other, ''))]
        (out / 'art' / f'education-{lang}.html').write_text(page('art', lang, art_links))
    print('ok')
