"""Page «Ми — козацького роду»: Cossack heritage, attempts to destroy Ukraine, how education makes nations strong.
Facts checked 17.10.2026: Orlyk constitution 5.04.1710 (telegraf.com.ua, historian), Hetmanate schools 766 in 1740–47 for 1,099
settlements (Encyclopedia of Ukraine), Pokrova / Defenders Day / Cossack Day (Ukrinform), kharakternyky legends (telegraf.com.ua),
Hinsley (British Academy), Korea (Library of Congress), Estonia (educationestonia.org), literacy 99.97% (2012), MESM 1950,
Viazovska (Fields 2022), Brave1 (itc.ua), Valuev 1863 / Ems 1876 (Radio Svoboda), schools (Ukrinform, 5.09.2025)."""
from svgkit import text, hand, line, rect, circle, path, svg, width
from common import wrap

CSS = """
/* Layout: parchment page with an embroidered band; numbered cards in sections with banner headings */
:root{--bg:#F3EEE3;--paper:#FFFDF8;--ink:#1F1A16;--muted:#5E554A;--line:#DDD3C2;--shadow:rgba(40,28,16,.12);
--yarn:#B3202E;--plum:#1F4E99;--hay:#C9971A;--leaf:#2F6B3A;--sky:#1F4E99;--bad:#B3202E;--good:#2F6B3A;--marker:#F2C94C;--marker-ink:#2A1E00;--cell:#F6F0E4;--skin:#E8B98E;--hair:#2B2118;
--display:'Ruslan Display','Comfortaa',serif;--title:'Kurale','Nunito',serif;--body:'Nunito',system-ui,-apple-system,'Segoe UI',sans-serif;--hand:'Caveat','Comic Sans MS',cursive}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17130F;--paper:#221C16;--ink:#F1E9DC;--muted:#B9AC98;--line:#3E342A;--shadow:rgba(0,0,0,.4);
--yarn:#E5525E;--plum:#7FA7EA;--hay:#E9BE4E;--leaf:#78B884;--sky:#7FA7EA;--bad:#E5525E;--good:#78B884;--marker:#C9A43A;--marker-ink:#1C1400;--cell:#2C251D;--skin:#D9A77C;--hair:#0F0B08;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17130F;--paper:#221C16;--ink:#F1E9DC;--muted:#B9AC98;--line:#3E342A;--shadow:rgba(0,0,0,.4);
--yarn:#E5525E;--plum:#7FA7EA;--hay:#E9BE4E;--leaf:#78B884;--sky:#7FA7EA;--bad:#E5525E;--good:#78B884;--marker:#C9A43A;--marker-ink:#1C1400;--cell:#2C251D;--skin:#D9A77C;--hair:#0F0B08;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16.5px;line-height:1.55;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));margin:0}
.page{max-width:920px;margin:0 auto;padding-block:20px 40px;display:grid;gap:18px}
.head{display:flex;flex-wrap:wrap;align-items:center;gap:12px 24px}
.htext{flex:1 1 320px;min-width:0;display:grid;gap:12px}
h1{font-family:var(--display);font-weight:400;font-size:clamp(34px,8vw,58px);line-height:1.05;margin:0;letter-spacing:.01em;text-wrap:balance}
h1 span{color:var(--yarn)}
.lead{font-size:18px;max-width:56ch;margin:0}
.links{font-size:15px;margin:0}.links a{color:var(--sky);font-weight:700}
.kozak{width:clamp(150px,34vw,210px);height:auto;flex:none;margin-inline:auto}
.orn{display:block;width:100%;height:22px}
.band{display:grid;gap:6px;margin-top:10px}
.band h2{font-family:var(--display);font-weight:400;font-size:clamp(24px,5vw,32px);margin:0;color:var(--yarn);text-wrap:balance}
.band p{margin:0;color:var(--muted);max-width:60ch}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:14px}
.box{position:relative;background:var(--paper);border:1px solid var(--line);border-top:4px solid var(--yarn);border-radius:14px;padding:16px 18px 14px;box-shadow:0 3px 0 var(--shadow);display:grid;gap:8px;align-content:start;min-width:0}
.box.blue{border-top-color:var(--sky)}.box.gold{border-top-color:var(--hay)}
.box h3{font-family:var(--title);font-size:22px;line-height:1.2;margin:0;padding-right:44px;text-wrap:balance}
.box p{margin:0}
.wide{grid-column:1/-1}
.n{position:absolute;top:12px;right:14px;width:32px;height:32px;border-radius:50%;background:var(--sky);color:var(--paper);font:400 17px var(--display);display:grid;place-items:center}
.box.key{background:var(--marker);color:var(--marker-ink);border-color:var(--marker);border-top-color:var(--yarn)}
.box.key .n{background:var(--yarn)}
.viz{width:100%;height:auto;max-width:440px;justify-self:center;overflow:visible}
.viz .d{font-family:var(--display);font-weight:400}
.viz .h{font-family:var(--hand);font-weight:600}
.tail{font-size:15px;color:var(--muted)}
.key .tail{color:var(--marker-ink)}
.more{background:var(--cell);border-radius:10px;padding:8px 12px;font-size:15.5px}
.tl{margin:0;padding-left:1.1em;display:grid;gap:6px;font-size:15.5px}.tl b{color:var(--yarn)}
.anthem{font-family:var(--title);font-size:20px;line-height:1.4;border-left:4px solid var(--yarn);padding-left:14px;margin:4px 0}
.final{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px}.final .kozak{width:140px;margin:0}.final>div{flex:1 1 280px;min-width:0;display:grid;gap:8px}
.big{font-family:var(--display);font-size:clamp(28px,6vw,40px);color:var(--yarn)}
.site-home{max-width:920px;margin:0 auto;padding-top:12px;font:700 15px var(--body)}.site-home a{color:var(--sky);text-decoration:none}
.site-copy{max-width:920px;margin:0 auto;padding-block:14px 28px;border-top:1px solid var(--line);font:14px/1.5 var(--body);color:var(--muted);text-align:center}.site-copy small{display:block;font-size:12px;opacity:.8;margin-top:2px}
"""
FONTS_EXTRA = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ruslan+Display&family=Kurale&display=swap">'


def ornament(uid='o'):
    """embroidered band: red rhombi with black centres and gold dots (an original cross-stitch-like pattern)."""
    cell = (f'<path d="M12 2 L22 11 L12 20 L2 11 Z" fill="var(--yarn)"/><path d="M12 7 L16 11 L12 15 L8 11 Z" fill="var(--hair)"/>'
            f'<rect x="11" y="10" width="2" height="2" fill="var(--hay)"/><rect x="0" y="10" width="2" height="2" fill="var(--hay)"/>')
    return (f'<svg class="orn" aria-hidden="true"><defs><pattern id="{uid}" width="24" height="22" patternUnits="userSpaceOnUse">{cell}</pattern></defs>'
            f'<rect width="100%" height="22" fill="url(#{uid})"/></svg>')


def kozak(cls='kozak'):
    """an original Cossack bust: oseledets, long moustache, red zhupan with gold trim."""
    return (f'<svg viewBox="0 0 200 230" class="{cls}" role="img" aria-label="козак">'
            '<path d="M14 230 Q22 160 100 150 Q178 160 186 230 Z" fill="var(--yarn)"/>'
            '<path d="M100 152 L84 230 M100 152 L116 230" stroke="var(--hay)" stroke-width="5"/>'
            '<circle cx="100" cy="178" r="4" fill="var(--hay)"/><circle cx="100" cy="198" r="4" fill="var(--hay)"/><circle cx="100" cy="218" r="4" fill="var(--hay)"/>'
            '<path d="M14 230 Q26 186 60 168" stroke="var(--sky)" stroke-width="8" fill="none" opacity=".9"/>'
            '<rect x="86" y="126" width="28" height="30" rx="8" fill="var(--skin)"/>'
            '<ellipse cx="56" cy="92" rx="9" ry="13" fill="var(--skin)"/><ellipse cx="144" cy="92" rx="9" ry="13" fill="var(--skin)"/>'
            '<ellipse cx="100" cy="88" rx="44" ry="52" fill="var(--skin)"/>'
            '<path d="M100 38 C122 28 150 40 140 64 C134 78 122 70 126 58" stroke="var(--hair)" stroke-width="9" fill="none" stroke-linecap="round"/>'
            '<path d="M84 74 Q92 68 98 74 M102 74 Q108 68 116 74" stroke="var(--hair)" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<circle cx="91" cy="84" r="3.6" fill="var(--hair)"/><circle cx="109" cy="84" r="3.6" fill="var(--hair)"/>'
            '<path d="M100 86 Q96 100 100 104" stroke="var(--hair)" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".6"/>'
            '<path d="M99 108 C86 104 72 112 68 138" stroke="var(--hair)" stroke-width="8" fill="none" stroke-linecap="round"/>'
            '<path d="M101 108 C114 104 128 112 132 138" stroke="var(--hair)" stroke-width="8" fill="none" stroke-linecap="round"/>'
            '<path d="M92 118 Q100 122 108 118" stroke="#9A4A3A" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
            '</svg>')


def big(num, cap, col='y', w=320, sub=None):
    b = text(w / 2, 78, num, 54 if width(num, 54) < w - 20 else 38, col, 'd', 'middle')
    b += hand(w / 2, 118, cap, 24, 'm')
    h = 130
    if sub:
        b += hand(w / 2, 142, sub, 20, 'm')
        h = 152
    return svg(w, h, b, f'{num} {cap}')


def card(n, cls, h3, p, sv='', tail='', extra=''):
    return (f'<section class="box {cls}"><span class="n">{n}</span><h3>{h3}</h3><p>{p}</p>{sv}'
            + (f'<p class="tail">{tail}</p>' if tail else '') + extra + '</section>')


def band(title, sub, uid):
    return f'<div class="band wide">{ornament(uid)}<h2>{title}</h2><p>{sub}</p></div>'


def content(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    num = [0]

    def nx():
        num[0] += 1
        return num[0]
    h = ''
    # ---------- I. Cossacks
    h += band(t('Козацький рід', 'Cossack roots'), t('Звідки ми і чому нам є ким пишатися.', 'Where we come from, and why we have people to be proud of.'), 'b1')
    h += '<div class="grid">'
    b = (path('M60 120 L150 30', 'h', 7) + circle(152, 28, 20, 'var(--hay)', 'h', 0)
         + ''.join(path(f'M152 28 L{152 + 26 * dx} {28 + 26 * dy}', 'h', 6) for dx, dy in ((1, 0), (0, -1), (-.7, -.7), (.7, -.7), (.7, .7))))
    b += hand(220, 120, t('булава — знак гетьмана', 'the mace: the hetman’s sign'), 22, 'm')
    h += card(nx(), '', t('Запорозька Січ', 'The Zaporozhian Sich'),
              t('У середині XVI століття за дніпровськими порогами постала Запорозька Січ — вільне козацьке військо. Отамана й гетьмана обирали самі козаки на раді.',
                'In the middle of the 16th century, the Zaporozhian Sich grew up beyond the Dnipro rapids: a free Cossack army. The Cossacks themselves chose their otaman and hetman at a council.'),
              svg(340, 136, b, t('булава', 'mace')),
              t('Велику раду козаки скликали на Покрову, 14 жовтня. Тепер цього дня Україна вшановує захисників і захисниць — сучасних козаків — і відзначає День українського козацтва.',
                'Cossacks held their great council on the feast of Pokrova, 14 October. Today on that day Ukraine honours its defenders, the Cossacks of our time, and celebrates Ukrainian Cossack Day.'))
    b = rect(70, 14, 200, 120, 'var(--cell)', 'h', 3, 10) + path('M70 22 Q60 14 70 6 M270 22 Q280 14 270 6', 'h', 3)
    for k, lab in enumerate([t('закони', 'laws'), t('гетьман', 'hetman'), t('суд', 'courts')]):
        x = 106 + k * 64
        b += rect(x - 29, 64, 58, 52, 'var(--paper)', 'y', 2.5, 6) + hand(x, 96, lab, 16, 'y')
    b += text(170, 46, '1710', 26, 'y', 'd', 'middle') + hand(170, 156, t('влада поділена на три гілки', 'power split into three branches'), 21, 'm')
    h += card(nx(), 'gold', t('Конституція Пилипа Орлика', 'Pylyp Orlyk’s Constitution'),
              t('5 квітня 1710 року козаки ухвалили Конституцію Пилипа Орлика. Дослідники вважають її однією з перших конституцій у Європі.',
                'On 5 April 1710 the Cossacks adopted Pylyp Orlyk’s Constitution. Historians consider it one of the first constitutions in Europe.'),
              svg(340, 166, b, t('Конституція 1710', 'Constitution of 1710')),
              t('Вона ділила владу на законодавчу, виконавчу й судову, щоб гетьман не міг правити сам, як захоче. На цій ідеї тримаються сучасні демократії й наша Конституція.',
                'It split power into law-making, governing and courts, so that the hetman could not rule alone however he liked. Modern democracies, and our own Constitution, rest on that idea.'))
    b = ''
    for k in range(10):
        x = 22 + k * 30
        on = k < 7
        b += path(f'M{x} 70 L{x + 12} 56 L{x + 24} 70 Z', 'y' if on else 'm', 0, 'var(--yarn)' if on else 'var(--line)')
        b += rect(x + 2, 70, 20, 22, 'var(--paper)', 'y' if on else 'var(--line)', 2, 2)
    b += text(160, 40, '766 : 1099 ≈ 0,7' if lang == 'uk' else '766 : 1099 ≈ 0.7', 22, 'y', 'd', 'middle')
    b += hand(160, 122, t('школа — приблизно в 7 поселеннях із 10', 'a school in about 7 settlements out of 10'), 21, 'm')
    h += card(nx(), 'blue', t('Козацькі школи', 'Cossack schools'),
              t('У 1740–1747 роках у семи полках Гетьманщини працювало 766 шкіл на 1099 сіл і міст.',
                'In 1740–1747 the seven regiments of the Cossack Hetmanate had 766 schools for 1,099 villages and towns.'),
              svg(320, 134, b, '766 / 1099'),
              t('Козаки знали: грамотний народ — сильний народ. А в 1632 році в Києві постала Києво-Могилянська колегія, майбутня академія.',
                'The Cossacks knew that a people who can read is a strong people. And in 1632 the Kyiv-Mohyla College, later an academy, was founded in Kyiv.'))
    b = ''
    import math
    for k in range(7):
        a = math.radians(-90 + k * 360 / 7)
        b += circle(160 + 70 * math.cos(a), 70 + 46 * math.sin(a), 3, 'var(--hay)', 'h', 0)
    pts = ''.join(f'{"M" if q == 0 else "L"}{160 + (26 if q % 2 == 0 else 11) * math.cos(math.radians(-90 + q * 36)):.1f} {70 + (26 if q % 2 == 0 else 11) * math.sin(math.radians(-90 + q * 36)):.1f} ' for q in range(10))
    b += path(pts + 'Z', 'h', 0, 'var(--hay)')
    b += hand(160, 140, t('справжні чари — знання й сміливість', 'the real magic: knowledge and courage'), 22, 'm')
    h += card(nx(), '', t('Характерники', 'The kharakternyky'),
              t('У легендах козаки-характерники заговорювали кулі, мали дев’ять життів і могли перекидатися на звірів.',
                'In legends, the kharakternyky were Cossacks who could charm bullets, had nine lives and could turn into animals.'),
              svg(320, 150, b, t('зоря', 'star')),
              t('Це легенди. Але вороги так боялися козацької вправності, що пояснювали її чарами. Справжня «магія» козаків — сміливість, знання й уміння. Цього можна навчитися: щодня, з кожною розв’язаною задачею.',
                'These are legends. But enemies feared Cossack skill so much that they explained it with magic. The Cossacks’ real "magic" was courage, knowledge and skill. And you can learn those, every day, with every problem you solve.'))
    h += '</div>'
    # ---------- II. They tried to destroy us
    h += band(t('Нас намагалися знищити — а ми є', 'They tried to destroy us, and we are still here'),
              t('Російська імперія, радянська влада, нацистська окупація, а тепер знову Росія — Україну не раз намагалися стерти: мову, школи, учених і саме життя.',
                'The Russian Empire, the Soviet regime, Nazi occupation and now Russia again: over and over, others tried to wipe Ukraine out: its language, schools, scholars and very lives.'), 'b2')
    ev = [('1863', t('Валуєвський', 'Valuev'), t('циркуляр', 'circular')), ('1876', t('Емський', 'Ems'), t('указ', 'decree')),
          ('1932–33', t('Голодомор', 'Holodomor'), ''), ('1937', t('Великий', 'Great'), t('терор', 'Terror')),
          ('1941', t('нацистська', 'Nazi'), t('окупація', 'occupation')), ('1944', t('депортація', 'deportation of'), t('кримських татар', 'Crimean Tatars')),
          ('2014', t('Крим', 'Crimea'), t('і Донбас', 'and Donbas')), ('2022', t('повномасштабне', 'full-scale'), t('вторгнення', 'invasion'))]
    b = ''
    for row in range(2):
        y = 50 + row * 112
        b += line(20, y, 400, y, 'i', 3)
        for k in range(4):
            yr, c1, c2 = ev[row * 4 + k]
            x = 58 + k * 102
            b += circle(x, y, 8, 'var(--yarn)', 'y', 0) + text(x, y - 18, yr, 16 if len(yr) == 4 else 14, 'y', 'd', 'middle')
            b += hand(x, y + 28, c1, 17, 'm') + (hand(x, y + 46, c2, 17, 'm') if c2 else '')
    b += hand(210, 270, t('а ми — тут, вчимося й живемо', 'and we are still here, learning and living'), 23, 'l')
    tl = ''.join(f'<li>{x}</li>' for x in [
        t('<b>1863.</b> Міністр Валуєв підписав циркуляр, де йшлося, що окремої української мови «не було, немає і бути не може», і заборонив друкувати нею підручники та книжки для народу.',
          '<b>1863.</b> Minister Valuev signed a circular claiming that a separate Ukrainian language had never existed and could not exist, and stopped schoolbooks and books for ordinary people being printed in Ukrainian.'),
        t('<b>1876.</b> Емський указ заборонив навіть ноти з українськими словами й вистави українською.', '<b>1876.</b> The Ems decree banned even sheet music with Ukrainian words and plays in Ukrainian.'),
        t('<b>1932–1933.</b> Голодомор: штучний голод, влаштований радянською владою, забрав життя мільйонів українців. Україна визнала його геноцидом українського народу.',
          '<b>1932–1933.</b> The Holodomor: a famine engineered by the Soviet regime killed millions of Ukrainians. Ukraine recognises it as genocide of the Ukrainian people.'),
        t('<b>1937–1938.</b> Великий терор: радянська влада розстріляла й ув’язнила сотні тисяч людей, серед них українських письменників, учених і вчителів. Це покоління називають «Розстріляним відродженням».',
          '<b>1937–1938.</b> The Great Terror: the Soviet regime shot or imprisoned hundreds of thousands of people, among them Ukrainian writers, scholars and teachers. That generation is called the Executed Renaissance.'),
        t('<b>1941–1944.</b> Нацистська окупація. За оцінкою Снайдера, політика нацистів убила близько 3,5 мільйона мирних жителів України, а разом із загиблими на фронті Україна втратила близько 6,5 мільйона людей. У вересні 1941 року в Бабиному Яру в Києві нацисти за два дні розстріляли десятки тисяч євреїв.',
          '<b>1941–1944.</b> Nazi occupation. Snyder estimates that Nazi policies killed about 3.5 million civilians in Ukraine; counting those who died at the front, Ukraine lost about 6.5 million people. In September 1941, at Babyn Yar in Kyiv, the Nazis shot tens of thousands of Jews in two days.'),
        t('<b>1944.</b> Радянська влада за кілька днів вивезла з Криму весь кримськотатарський народ. Багато людей загинули в дорозі й на засланні.',
          '<b>1944.</b> In a few days the Soviet regime deported the whole Crimean Tatar people from Crimea. Many died on the way and in exile.'),
        t('<b>2014.</b> Після Революції Гідності Росія напала на Україну: окупувала Крим і розв’язала війну на Донбасі. Відтоді Україна захищається.',
          '<b>2014.</b> After the Revolution of Dignity, Russia attacked Ukraine: it occupied Crimea and started the war in Donbas. Ukraine has been defending itself ever since.'),
        t('<b>2022.</b> 24 лютого Росія почала повномасштабне вторгнення. За даними МОН на серпень 2025 року, 1779 шкіл пошкоджено, а 226 зруйновано.',
          '<b>2022.</b> On 24 February Russia launched its full-scale invasion. According to Ukraine’s Ministry of Education, by August 2025 1,779 schools had been damaged and 226 destroyed.')])
    snyder = t('Американський історик Тімоті Снайдер з Єльського університету показує: у 1933–1945 роках Україна опинилася в серці «кривавих земель» між Гітлером і Сталіном, де загинули близько 14 мільйонів мирних людей. Україну хотіли зробити колонією й житницею для чужих.',
               'American historian Timothy Snyder of Yale University shows that in 1933–1945 Ukraine lay at the heart of the "bloodlands" between Hitler and Stalin, where about 14 million civilians were killed. Others wanted to turn Ukraine into a colony and a breadbasket for themselves.')
    h += '<div class="grid">' + card(nx(), 'wide', t('Чому саме мова й школи?', 'Why language and schools?'),
                                     t('Бо освічений народ, який знає свою історію, не скориш. Тому навчання для нас — це теж захист.',
                                       'Because a people that is educated and knows its history cannot be conquered. That is why learning is also a way to defend ourselves.'),
                                     svg(420, 286, b, t('спроби знищити Україну', 'attempts to destroy Ukraine')), '',
                                     f'<p class="more">{snyder}</p><ul class="tl">{tl}</ul>') + '</div>'
    # ---------- III. Ukrainian scientists
    h += band(t('Українські науковці, що змінили світ', 'Ukrainian scientists who changed the world'),
              t('Декого з них переслідували — а вони відкривали людям космос, небо й нові знання.', 'Some of them were persecuted, yet they opened up space, the sky and new knowledge for everyone.'), 'b3s')
    h += '<div class="grid">'
    b = circle(120, 86, 34, 'var(--sky)', 's', 0, ) + path('M70 120 Q160 20 260 60', 'h', 2.5, dash='6 6') + circle(260, 60, 7, 'var(--hay)', 'h', 0)
    b += path('M254 52 L266 46 M268 66 L278 72 M262 70 L258 82', 'h', 2.5)
    b += hand(160, 146, t('1957: перший супутник', '1957: first satellite'), 20, 'm') + hand(160, 168, t('1961: перша людина в космосі', '1961: first person in space'), 20, 'm')
    h += card(nx(), 'blue', t('Сергій Корольов', 'Serhiy Korolyov'),
              t('Народився в Житомирі у 1907 році, вчився в Київському політехнічному інституті. Головний конструктор, під чиїм керівництвом запустили перший супутник Землі й першу людину в космос.',
                'Born in Zhytomyr in 1907, he studied at the Kyiv Polytechnic Institute. He was the chief designer who led the launch of the first Earth satellite and the first person in space.'),
              svg(320, 176, b, t('супутник', 'satellite')),
              t('У 1938 році радянська влада його заарештувала, він працював навіть на золотій копальні на Колимі. Вижив — і повів людство в космос. Його ім’я тоді тримали в таємниці.',
                'In 1938 the Soviet regime arrested him; he was even sent to a gold mine in Kolyma. He survived and led humanity into space. At the time his name was kept secret.'))
    b = circle(70, 90, 30, 'var(--sky)', 's', 0) + circle(250, 80, 16, 'var(--line)', 'm', 2)
    b += path('M100 90 C150 30 220 40 250 56 C280 70 270 106 250 104 C220 102 160 120 100 96', 'y', 2.5, dash='6 5')
    b += hand(160, 150, t('траса Кондратюка до Місяця', 'Kondratyuk’s route to the Moon'), 21, 'm')
    h += card(nx(), 'gold', t('Юрій Кондратюк', 'Yuri Kondratyuk'),
              t('Народився в Полтаві у 1897 році. Ще до польотів у космос розрахував, як долетіти до Місяця: корабель лишається на орбіті, а на Місяць спускається маленький модуль.',
                'Born in Poltava in 1897. Long before spaceflight, he calculated how to reach the Moon: the ship stays in orbit while a small lander goes down to the Moon.'),
              svg(320, 160, b, t('траса до Місяця', 'route to the Moon')),
              t('Саме цю ідею використали інженери програми «Аполлон», коли люди вперше висадилися на Місяць. Це математика траєкторій — та сама, що й у наших кутах і пропорціях.',
                'Apollo engineers used this very idea when people first landed on the Moon. It is the mathematics of trajectories: the same maths behind our angles and ratios.'))
    b = rect(110, 80, 100, 36, 'var(--cell)', 's', 3, 18) + path('M160 80 V58 M90 56 H230', 's', 4) + path('M210 98 H270 M270 88 V108', 's', 3)
    b += text(160, 140, '1939', 22, 's', 'd', 'middle')
    h += card(nx(), '', t('Ігор Сікорський', 'Igor Sikorsky'),
              t('Народився в Києві у 1889 році, вчився в Київському політехнічному інституті. У 1939 році створив гелікоптер VS-300 — перший практичний гелікоптер.',
                'Born in Kyiv in 1889, he studied at the Kyiv Polytechnic Institute. In 1939 he built the VS-300, the first practical helicopter.'),
              svg(320, 152, b, t('гелікоптер', 'helicopter')),
              t('Компанія Sikorsky досі будує гелікоптери, які рятують людей у горах, на морі й під час пожеж.', 'The Sikorsky company still builds helicopters that rescue people in the mountains, at sea and in fires.'))
    b = line(20, 90, 300, 90, 'h', 6) + ''.join(line(x, 90, x, 128, 'h', 4) for x in range(40, 300, 52)) + path('M20 128 Q160 140 300 128', 's', 3)
    b += text(160, 60, '1543 м' if lang == 'uk' else '1,543 m', 24, 'h', 'd', 'middle')
    h += card(nx(), 'gold', t('Євген Патон', 'Yevhen Paton'),
              t('У 1953 році в Києві відкрили міст Патона завдовжки 1543 метри — один із перших у світі суцільнозварних мостів.',
                'In 1953 the Paton Bridge opened in Kyiv: 1,543 metres long and one of the first all-welded bridges in the world.'),
              svg(320, 150, b, t('міст Патона', 'Paton Bridge')),
              t('Київська школа зварювання Патонів і сьогодні відома на весь світ.', 'The Paton school of welding in Kyiv is still famous around the world.'))
    b = circle(160, 76, 46, 'none', 'p', 3) + circle(160, 76, 30, 'none', 'p', 2) + circle(160, 76, 8, 'var(--plum)', 'p', 0)
    b += text(160, 150, '1918', 24, 'p', 'd', 'middle')
    h += card(nx(), '', t('Володимир Вернадський', 'Volodymyr Vernadsky'),
              t('У 1918 році постала Українська академія наук, і першим її президентом обрали Володимира Вернадського.',
                'In 1918 the Ukrainian Academy of Sciences was founded, and Volodymyr Vernadsky was elected its first president.'),
              svg(320, 160, b, t('Академія наук', 'Academy of Sciences')),
              t('Навіть у буремні роки українці будували науку, бо знали: без неї держава не встоїть.', 'Even in stormy years Ukrainians built science, because they knew a state cannot stand without it.'))
    b = circle(160, 70, 52, 'var(--marker)', 'h', 4) + text(160, 64, '2022', 26, 'k', 'd', 'middle') + text(160, 94, t('Філдс', 'Fields'), 18, 'k', 'd', 'middle')
    b += hand(160, 150, t('найвища нагорода математиків', 'the highest prize in maths'), 22, 'm')
    h += card(nx(), 'blue', t('Марина В’язовська', 'Maryna Viazovska'),
              t('Народилася в Києві у 1984 році. У 2022 році отримала Філдсівську премію — другою жінкою в історії.',
                'Born in Kyiv in 1984. In 2022 she won the Fields Medal, only the second woman ever to do so.'),
              svg(320, 160, b, 'Fields Medal 2022'),
              t('Над тим, як найщільніше укласти кулі, математики думали понад 400 років, ще з часів Кеплера. Марина довела відповідь для 8-вимірного простору.',
                'Mathematicians have wondered how to pack spheres as tightly as possible for over 400 years, since Kepler. Maryna proved the answer in 8 dimensions.'))
    h += '</div>'
    # ---------- III. Education makes nations strong
    h += band(t('Освіта робить країни сильними', 'Education makes nations strong'), t('Справжні історії з інших країн.', 'True stories from other countries.'), 'b3e')
    h += '<div class="grid">'
    h += card(nx(), 'blue', t('Математики скоротили війну', 'Mathematicians shortened a war'),
              t('Британія, 1939–1945. У Блечлі-Парку математики, серед них Алан Тюрінг, зламали німецький шифр «Енігма».',
                'Britain, 1939–1945. At Bletchley Park, mathematicians including Alan Turing broke the German Enigma code.'),
              big(t('−2 роки', '−2 years'), t('війни', 'of war'), 's'),
              t('Історик розвідки Гаррі Гінслі, який сам там працював, оцінив: без цієї роботи Друга світова могла тривати на рік-два довше.',
                'Intelligence historian Harry Hinsley, who worked there himself, estimated that without this work the Second World War could have lasted one to two years longer.'))
    b = rect(70, 104 - 22 * 0.9, 60, 22 * 0.9, 'var(--yarn)', 'y', 0, 4) + rect(190, 104 - 88 * 0.9, 60, 88 * 0.9, 'var(--sky)', 's', 0, 4)
    b += line(50, 104, 270, 104, 'i', 2) + text(100, 74, '22 %', 20, 'y', 'd', 'middle') + text(220, 16, '≈ 88 %', 20, 's', 'd', 'middle')
    b += text(100, 126, '1945', 18, 'm', 'd', 'middle') + text(220, 126, '1970', 18, 'm', 'd', 'middle')
    b += hand(160, 152, t('дорослі, що вміють читати', 'adults who can read'), 21, 'm')
    h += card(nx(), '', t('Із бідності — до лідерства', 'From poverty to the top'),
              t('Південна Корея, зруйнована війною. У 1945 році читати вмів лише кожен п’ятий дорослий. Країна вклалася в школи.',
                'South Korea, wrecked by war. In 1945 only one adult in five could read. The country invested in schools.'),
              svg(320, 162, b, '22% → 88%'),
              t('За 25 років читати вміли майже 9 із 10. Сьогодні Корея — одна з найрозвиненіших технологічних країн світу.',
                'Within 25 years almost 9 in 10 could read. Today Korea is one of the world’s most advanced technology countries.'))
    b = line(30, 70, 290, 70, 'i', 3)
    for x, yr, cap in ((40, '1996', t('старт', 'start')), (180, '2000', t('комп’ютери', 'computers')), (280, '2001', t('інтернет', 'internet'))):
        b += circle(x, 70, 9, 'var(--sky)', 's', 0) + text(x, 50, yr, 18, 's', 'd', 'middle') + hand(x, 100, cap, 20, 'm')
    b += hand(160, 136, t('у кожній школі країни', 'in every school in the country'), 22, 'l')
    h += card(nx(), 'gold wide', t('Маленька країна, великий стрибок', 'A small country, a big leap'),
              t('Естонія, 1996 рік. Програма «Стрибок тигра»: за п’ять років усі школи отримали комп’ютери й інтернет.',
                'Estonia, 1996. The Tiger Leap programme: within five years every school had computers and the internet.'),
              svg(320, 148, b, 'Tiger Leap 1996–2001'),
              t('Ці діти виросли й побудували одну з найцифровіших держав світу.', 'Those children grew up and built one of the most digital countries in the world.'))
    h += '</div>'
    # ---------- V. Today's Cossacks
    h += band(t('Сучасні козаки', 'The Cossacks of our time'), t('Країна, яка вчиться й захищається.', 'A country that learns and defends itself.'), 'b4')
    h += '<div class="grid">'
    h += card(nx(), 'blue', t('Україна — країна, яка вчиться', 'Ukraine is a country that learns'),
              t('Читати й писати в Україні вміють майже всі дорослі.', 'Almost every adult in Ukraine can read and write.'),
              big('99,97 %' if lang == 'uk' else '99.97%', t('дорослих грамотні', 'of adults can read'), 's', sub=t('за даними 2012 року', 'figure for 2012')),
              t('А в Києві в 1950 році запрацювала МЕСМ — одна з перших електронних обчислювальних машин у Європі. Її створила команда Сергія Лебедєва.',
                'And in Kyiv in 1950 MESM started working: one of the first electronic computers in Europe, built by Serhiy Lebedev’s team.'))
    h += card(nx(), '', t('Інженери-захисники', 'Engineers who defend us'),
              t('У 2023 році в Україні запрацював оборонний кластер Brave1. Інженери й програмісти приносять туди свої винаходи.',
                'In 2023 Ukraine launched the Brave1 defence tech cluster. Engineers and programmers bring their inventions there.'),
              big('1671', t('розробка за перший рік', 'inventions in the first year')),
              t('Дрони, роботи для розмінування, техніка для евакуації поранених. Це сучасні характерники: їхня «магія» — знання. І всі вони колись розв’язували задачі в школі.',
                'Drones, demining robots, vehicles to rescue the wounded. These are today’s kharakternyky: their "magic" is knowledge. And every one of them once solved problems at school.'))
    h += '</div>'
    # ---------- final
    anthem = t('Душу й тіло ми положим за нашу свободу,<br>і покажем, що ми, браття, козацького роду.',
               'We will give our soul and body for our freedom,<br>and show that we, brothers, are of Cossack kin.')
    h += ornament('b5')
    h += (f'<section class="box key wide"><span class="n">{nx()}</span><h3>{t("Ми — нащадки козаків", "We are the descendants of the Cossacks")}</h3>'
          f'<div class="final">{kozak()}<div>'
          f'<p class="anthem">{anthem}</p><p class="tail">{t("Державний Гімн України, слова Павла Чубинського", "National Anthem of Ukraine, words by Pavlo Chubynsky")}</p>'
          f'<p><b>{t("Нас намагалися знищити сотні років — а ми тут. Ми вижили. Ми є. Ми вчимося, творимо й захищаємо одне одного. Кожен урок, навіть в укритті чи онлайн, робить Україну сильнішою.", "They tried to destroy us for hundreds of years, and we are still here. We survived. We exist. We learn, create and protect one another. Every lesson, even in a shelter or online, makes Ukraine stronger.")}</b></p>'
          f'<p class="big">{t("Україна була, є і буде!", "Ukraine was, is and will be!")}</p></div></div></section>')
    return h


def page(kind, lang, links):
    t = lambda uk, en: uk if lang == 'uk' else en
    title = t('Ми — козацького роду', 'Of Cossack Kin')
    lk = ' · '.join(f'<a href="{h}">{n}</a>' for n, h in links if h)
    body = (f'<div class="page">\n <header class="head"><div class="htext"><h1>{t("Ми — <span>козацького роду</span>", "Of <span>Cossack kin</span>")}</h1>'
            f'<p class="lead">{t("Україна була, є і буде. Ось наша історія: козаки, які обирали гетьмана й писали конституцію, люди, яких намагалися знищити, і чому освіта завжди була нашою силою.", "Ukraine was, is and will be. Here is our story: Cossacks who elected their hetman and wrote a constitution, a people others tried to destroy, and why education has always been our strength.")}</p>'
            f'<p class="links">{lk}</p></div>{kozak()}</header>\n{content(lang)}\n</div>')
    html = wrap(kind, lang, title, [CSS], body, '')
    # this page has its own palette: drop the meadow site stylesheet colours by placing ours last, and add the display fonts
    html = html.replace('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Comfortaa', FONTS_EXTRA + '\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Comfortaa', 1)
    return html


if __name__ == '__main__':
    import sys, json
    from pathlib import Path
    out = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/out')
    arts = {}
    p = Path(__file__).parent / 'artifacts.json'
    if p.exists():
        arts = json.loads(p.read_text()).get('education', {})
    (out / 'site').mkdir(parents=True, exist_ok=True)
    (out / 'art').mkdir(parents=True, exist_ok=True)
    for lang in ('uk', 'en'):
        other = 'en' if lang == 'uk' else 'uk'
        site_links = [('English version' if lang == 'uk' else 'Українська версія', 'education-en.html' if lang == 'uk' else 'education.html')]
        (out / 'site' / ('education.html' if lang == 'uk' else 'education-en.html')).write_text(
            page('site', lang, site_links).replace('href="../index.html"', 'href="index.html"' if lang == 'uk' else 'href="index-en.html"'))
        art_links = [('English version' if lang == 'uk' else 'Українська версія', arts.get(other, ''))]
        (out / 'art' / f'education-{lang}.html').write_text(page('art', lang, art_links))
    print('ok')
