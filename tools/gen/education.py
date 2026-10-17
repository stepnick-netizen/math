"""Page «Ми — козацького роду»: Cossack heritage, attempts to destroy Ukraine, how education makes nations strong.
Facts checked 17.10.2026: Orlyk constitution 5.04.1710 (telegraf.com.ua, historian), Hetmanate schools 766 in 1740–47 for 1,099
settlements (Encyclopedia of Ukraine), Pokrova / Defenders Day / Cossack Day (Ukrinform), kharakternyky legends (telegraf.com.ua),
Hinsley (British Academy), Korea (Library of Congress), Estonia (educationestonia.org), literacy 99.97% (2012), MESM 1950,
Viazovska (Fields 2022), Brave1 (itc.ua), Valuev 1863 / Ems 1876 (Radio Svoboda), schools (Ukrinform, 5.09.2025).
Also: Berestechko 1651 (zaxid.net), Budapest Memorandum 5.12.1994 (Wikipedia; third-largest arsenal; guarantors RU/US/UK).
Fight: Kruty >500 vs ~4000, 5 h, delay (fakty.com.ua); Khotyn 2–28.09.1621, Cossacks > half (armyinform); Konotop 1659 (armyinform); 6.3 mln vs Nazism, armies list (texty.org.ua); Norilsk 1953 >20k (Radio Svoboda); Franko 14 langs, 48, 50 vols, 3 arrests, Vienna 1893, Nobel (armyinform).\nUPA: 14.10.1942 symbolic, vs Nazis & Bolsheviks, >100k over time, Shukhevych 5.03.1950 (Ukrinform); Volhynia formula 2002 Huzar & Yavorsky (NV, Hrytsak 2016).\nRus: Nebelivka ~300 ha (zaxid.net), Danylo crowned 1253 Dorohychyn (zaxid.net), Moscow first mentioned 1147, Kyiv 482 tradition."""
import math
from svgkit import text, hand, line, rect, circle, path, svg, width, arrow
from common import wrap

from fontTools.ttLib import TTFont as _TT
_K = _TT('/root/.fonts/Kurale-Regular.ttf')
_KC, _KM, _KU = _K.getBestCmap(), _K['hmtx'].metrics, _K['head'].unitsPerEm


def kw(s, size):
    return sum(_KM[_KC.get(ord(c)) or _KC[ord('?')]][0] for c in s) * size / _KU


def cap(x, y, s, size=22, col='m', maxw=300):
    """caption in Kurale (a serious book face), shrunk to fit maxw."""
    size = min(size, size * maxw / max(kw(s, size), 1))
    return hand(x, y, s, round(size, 1), col)


CSS = """
/* Layout: parchment page with an embroidered band; numbered cards in sections with banner headings */
:root{--bg:#F3EEE3;--paper:#FFFDF8;--ink:#1F1A16;--muted:#5E554A;--line:#DDD3C2;--shadow:rgba(40,28,16,.12);
--yarn:#B3202E;--plum:#1F4E99;--hay:#C9971A;--leaf:#2F6B3A;--sky:#1F4E99;--bad:#B3202E;--good:#2F6B3A;--marker:#F2C94C;--marker-ink:#2A1E00;--cell:#F6F0E4;--skin:#E8B98E;--hair:#2B2118;--sil:#1A1512;
--display:'Ruslan Display','Comfortaa',serif;--title:'Kurale','Nunito',serif;--body:'Nunito',system-ui,-apple-system,'Segoe UI',sans-serif;--hand:'Caveat','Comic Sans MS',cursive}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17130F;--paper:#221C16;--ink:#F1E9DC;--muted:#B9AC98;--line:#3E342A;--shadow:rgba(0,0,0,.4);
--yarn:#E5525E;--plum:#7FA7EA;--hay:#E9BE4E;--leaf:#78B884;--sky:#7FA7EA;--bad:#E5525E;--good:#78B884;--marker:#C9A43A;--marker-ink:#1C1400;--cell:#2C251D;--skin:#D9A77C;--hair:#0F0B08;--sil:#0B0806;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17130F;--paper:#221C16;--ink:#F1E9DC;--muted:#B9AC98;--line:#3E342A;--shadow:rgba(0,0,0,.4);
--yarn:#E5525E;--plum:#7FA7EA;--hay:#E9BE4E;--leaf:#78B884;--sky:#7FA7EA;--bad:#E5525E;--good:#78B884;--marker:#C9A43A;--marker-ink:#1C1400;--cell:#2C251D;--skin:#D9A77C;--hair:#0F0B08;--sil:#0B0806;color-scheme:dark}
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
.viz .h{font-family:var(--title);font-weight:400}
.tail{font-size:15px;color:var(--muted)}
.key .tail{color:var(--marker-ink)}
.more{background:var(--cell);border-radius:10px;padding:8px 12px;font-size:15.5px}
.tl{margin:0;padding-left:1.1em;display:grid;gap:6px;font-size:15.5px}.tl b{color:var(--yarn)}
.anthem{font-family:var(--title);font-size:20px;line-height:1.4;border-left:4px solid var(--yarn);padding-left:14px;margin:4px 0}
.final{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px}.final .kozak{width:140px;margin:0}.final>div{flex:1 1 280px;min-width:0;display:grid;gap:8px}
.box.mem{background:#1A1512;color:#F3EEE3;border-color:#1A1512;border-top:6px solid var(--yarn);--ink:#F3EEE3;--muted:#CDBFAA;--paper:#2A221B;--cell:#2A221B}
.box.mem .tail{color:#E4D8C6}.box.mem .n{background:var(--yarn)}
.memrow{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px 28px}.memrow .viz{flex:1 1 260px;max-width:340px}
.vow{font-family:var(--display);font-size:clamp(24px,5.4vw,34px);line-height:1.25;margin:0;flex:0 1 auto}.vow span{color:#FF5A66}
.big{font-family:var(--display);font-size:clamp(28px,6vw,40px);color:var(--yarn)}
/* page sections: small chips under the header */
.sec-nav{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.sec-nav span{font:800 13px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.sec-nav a{font:700 14.5px var(--body);color:var(--ink);text-decoration:none;background:var(--paper);border:1.5px solid var(--line);border-left:4px solid var(--yarn);border-radius:10px;padding:6px 11px}
.sec-nav a:hover{border-color:var(--yarn)}.band{scroll-margin-top:12px}
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


def kozak(cls='kozak', uid='kz'):
    """a stern Cossack medallion in linocut style: black profile bust with oseledets and a long moustache drawn as
    hair (red engraved strands), a sabre behind, on a red disc in a gold ring; clipped to the circle so it works in dark mode."""
    ink, red = 'var(--sil)', 'var(--yarn)'
    face = ("M100 36 C116 36 132 44 138 58 L142 70 L140 77 L157 97 C158 100 154 102 147 102 "
            "C153 112 156 134 152 158 C151 166 149 172 146 180 C144 168 142 152 139 141 "
            "C136 141 128 141 116 140 L118 152 L120 160 C140 164 166 172 180 190 C188 202 190 216 190 230 "
            "L12 230 C12 214 14 196 26 182 C38 168 58 160 76 152 L74 120 C64 108 58 92 60 72 C62 50 80 36 100 36 Z")
    lock = ("M104 40 C98 26 80 20 66 28 C54 36 50 52 54 66 C58 80 66 90 70 104 "
            "C72 96 68 84 62 72 C58 60 60 44 70 38 C80 32 92 34 98 42 Z")
    strands = ''.join(f'<path d="M{147 - k * 1.5} {104 + k * 2} C{151 - k * 2} 116 {152 - k * 2.5} 136 {148 - k * 2.5} {160 + k * 2}" '
                      f'stroke="{red}" stroke-width="1.4" fill="none" opacity=".85"/>' for k in range(3))
    return (f'<svg viewBox="0 0 200 200" class="{cls}" role="img" aria-label="козак">'
            f'<defs><clipPath id="{uid}"><circle cx="100" cy="100" r="92"/></clipPath></defs>'
            f'<circle cx="100" cy="100" r="96" fill="var(--hay)"/><circle cx="100" cy="100" r="92" fill="{red}"/>'
            f'<g clip-path="url(#{uid})" transform="translate(0 -8)">'
            f'<path d="M40 204 C18 146 20 76 60 14 C40 76 38 140 54 200 Z" fill="{ink}"/>'
            f'<path d="M30 204 L62 196" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'
            f'<path fill="{ink}" d="{face}"/>'
            f'<path d="M139 141 C141 128 140 116 142 106" stroke="{red}" stroke-width="2" fill="none" stroke-linecap="round"/>{strands}'
            f'<path d="{lock}" fill="{ink}" stroke="{red}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<path d="M98 40 C88 30 72 32 64 44 C58 56 60 70 66 82" stroke="{red}" stroke-width="1.3" fill="none" opacity=".8"/>'
            f'<path d="M112 66 L140 63" stroke="{red}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M124 76 L136 75" stroke="{red}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<path d="M98 84 C93 86 93 98 98 101" stroke="{red}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
            '<path d="M56 178 C76 200 100 206 124 202 C146 198 160 188 168 178" stroke="var(--hay)" stroke-width="4" fill="none"/></g></svg>')


def big(num, label, col='y', w=320, sub=None):
    b = text(w / 2, 78, num, 54 if width(num, 54) < w - 20 else 38, col, 'd', 'middle')
    b += cap(w / 2, 118, label, 24, 'm')
    h = 130
    if sub:
        b += cap(w / 2, 142, sub, 20, 'm')
        h = 152
    return svg(w, h, b, f'{num} {label}')


def card(n, cls, h3, p, sv='', tail='', extra=''):
    return (f'<section class="box {cls}"><span class="n">{n}</span><h3>{h3}</h3><p>{p}</p>{sv}'
            + (f'<p class="tail">{tail}</p>' if tail else '') + extra + '</section>')


def band(title, sub, uid):
    return f'<div class="band wide" id="s-{uid}">{ornament(uid)}<h2>{title}</h2><p>{sub}</p></div>'


SECNAV = [('b0', 'Початки', 'Beginnings'), ('b1', 'Козаки', 'Cossacks'), ('b2', 'Нас нищили', 'They tried to destroy us'),
          ('b2b', 'Ми боролися', 'We fought back'), ('b3s', 'Науковці', 'Scientists'), ('b3c', 'Культура', 'Culture'),
          ('b3e', 'Освіта', 'Education'), ('b4', 'Сучасні козаки', 'Cossacks today')]


def secnav(lang):
    t = (lambda uk, en: uk if lang == 'uk' else en)
    return (f'<nav class="sec-nav" aria-label="{t("Розділи сторінки", "Sections of this page")}"><span>{t("Розділи:", "Sections:")}</span>'
            + ''.join(f'<a href="#s-{u}">{uk if lang == "uk" else en}</a>' for u, uk, en in SECNAV) + '</nav>')


def content(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    num = [0]

    def nx():
        num[0] += 1
        return num[0]
    h = ''
    # ---------- 0. Where Ukraine begins
    h += band(t('Звідки починається Україна', 'Where Ukraine begins'),
              t('Від трипільців до Київської Русі й короля Данила: наша історія налічує тисячі років.', 'From the Trypillians to Kyivan Rus and King Danylo: our history goes back thousands of years.'), 'b0')
    h += '<div class="grid">'
    b = path('M118 22 H202 C204 34 196 40 208 50 C236 70 240 104 220 126 C206 142 196 146 184 150 H136 C124 146 114 142 100 126 C80 104 84 70 112 50 C124 40 116 34 118 22 Z', 'i', 3, 'var(--cell)')
    for k in range(3):
        x = 116 + k * 32
        b += path(f'M{x} 88 c 0 -12 16 -12 16 0 c 0 12 16 12 16 0', 'y', 4)
        b += circle(x + 8, 86, 3.4, 'var(--yarn)', 'y', 0)
    b += line(104, 64, 216, 64, 'i', 2) + line(100, 112, 220, 112, 'i', 2)
    b += cap(160, 176, t('спіраль, що повторюється по колу', 'a spiral repeating all the way round'), 20, 'm')
    h += card(nx(), '', t('Трипілля', 'Trypillia'),
              t('Від семи до п’яти тисяч років тому на нашій землі жили трипільці. Вони будували величезні поселення: Небелівка на Кіровоградщині займала близько 300 гектарів — одне з найбільших поселень тодішньої Європи.',
                'Between seven and five thousand years ago the Trypillians lived on our land. They built huge settlements: Nebelivka in the Kirovohrad region covered about 300 hectares, one of the largest settlements in Europe at the time.'),
              svg(320, 186, b, t('трипільський глечик', 'Trypillian pot')),
              t('Трипільці прикрашали глечики спіралями, що повторюються по колу. Повтор і симетрія — та сама математика, що й у вишиванці.',
                'Trypillians decorated their pots with spirals that repeat all the way round. Repetition and symmetry: the same maths as in Ukrainian embroidery.'))
    b = path('M30 92 C46 60 62 60 78 92 Z M64 92 C82 50 102 50 120 92 Z', 'i', 0, 'var(--ink)')
    b += line(30, 100, 290, 100, 'i', 3) + circle(60, 100, 7, 'var(--yarn)', 'y', 0) + circle(276, 100, 7, 'var(--ink)', 'i', 0)
    b += text(60, 128, '482', 20, 'y', 'd', 'middle') + text(276, 128, '1147', 20, 'i', 'd', 'middle')
    b += cap(60, 150, t('Київ', 'Kyiv'), 18, 'm') + cap(276, 150, t('Москва', 'Moscow'), 18, 'm')
    b += arrow(70, 86, 266, 86, 'y', -0.18, 2.6) + text(170, 40, t('665 років', '665 years'), 20, 'y', 'd', 'middle')
    h += card(nx(), 'gold', t('Київ старший за Москву на 665 років', 'Kyiv is 665 years older than Moscow'),
              t('За переказом, Київ заснували брати Кий, Щек і Хорив та їхня сестра Либідь. За традицією історію міста відлічують від 482 року: у 1982 році Київ святкував 1500-річчя.',
                'Legend says Kyiv was founded by the brothers Kyi, Shchek and Khoryv and their sister Lybid. By tradition the city counts its history from 482: in 1982 Kyiv celebrated its 1,500th anniversary.'),
              svg(320, 160, b, '1147 − 482 = 665'),
              t('Москву вперше згадали в літописі в 1147 році. Порахуй: 1147 − 482 = 665. Тож Русь — це Київ, і її історія — наша історія.',
                'Moscow was first mentioned in a chronicle in 1147. Work it out: 1147 − 482 = 665. So Rus is Kyiv, and its history is our history.'))
    b = rect(76, 92, 168, 56, 'var(--ink)', 'i', 0, 2)
    for x, w_, hgt in ((160, 30, 62), (110, 20, 44), (210, 20, 44), (88, 14, 30), (232, 14, 30)):
        b += rect(x - w_ / 2, 92 - hgt + w_ / 2, w_, hgt - w_ / 2, 'var(--ink)', 'i', 0, 0) + circle(x, 92 - hgt + w_ / 2, w_ / 2, 'var(--hay)', 'i', 0)
        b += line(x, 92 - hgt, x, 92 - hgt - 12, 'h', 2.5)
    for x in range(96, 236, 22):
        b += rect(x, 110, 8, 22, 'var(--cell)', 'i', 0, 4)
    b += cap(160, 172, t('Софія Київська, XI століття', 'St Sophia’s, Kyiv, 11th century'), 20, 'm')
    h += card(nx(), 'blue', t('Київська Русь і Ярослав Мудрий', 'Kyivan Rus and Yaroslav the Wise'),
              t('Київська Русь була однією з найбільших держав Європи. У 988 році князь Володимир хрестив Русь, а його син Ярослав Мудрий дав їй «Руську правду» — перший писаний звід законів.',
                'Kyivan Rus was one of the largest states in Europe. In 988 Prince Volodymyr baptised Rus, and his son Yaroslav the Wise gave it the Ruska Pravda, its first written code of laws.'),
              svg(320, 182, b, t('Софія Київська', 'St Sophia’s Cathedral')),
              t('Ярослав збудував Софійський собор і, за літописом, зібрав при ньому бібліотеку. Софія Київська стоїть уже майже тисячу років і внесена до Списку всесвітньої спадщини ЮНЕСКО.',
                'Yaroslav built St Sophia’s Cathedral and, the chronicle says, gathered a library there. St Sophia’s has stood for almost a thousand years and is a UNESCO World Heritage Site.'))
    b = text(160, 70, 'АНА РЪИНА', 34, 'i', 'd', 'middle') + line(60, 86, 260, 86, 'y', 4)
    b += cap(160, 120, t('«Анна королева» — підпис кирилицею', '"Anna the queen", signed in Cyrillic'), 20, 'm')
    h += card(nx(), '', t('Анна Ярославна — королева Франції', 'Anna of Kyiv, Queen of France'),
              t('Дочка Ярослава Мудрого Анна вийшла заміж за короля Франції Генріха I і стала французькою королевою. На одній французькій грамоті вона підписалася кирилицею.',
                'Yaroslav the Wise’s daughter Anna married King Henry I of France and became Queen of France. On one French charter she signed her name in Cyrillic.'),
              svg(320, 134, b, 'АНА РЪИНА'),
              t('Освічені київські князівни були бажаними нареченими в Європі: доньки Ярослава стали королевами Франції, Норвегії й Угорщини.',
                'Educated princesses from Kyiv were sought-after brides across Europe: Yaroslav’s daughters became queens of France, Norway and Hungary.'))
    b = path('M100 110 L92 52 L124 80 L160 40 L196 80 L228 52 L220 110 Z', 'i', 3, 'var(--hay)') + rect(96, 110, 128, 18, 'var(--ink)', 'i', 0, 3)
    for x, c in ((92, 'var(--yarn)'), (160, 'var(--sky)'), (228, 'var(--yarn)')):
        b += circle(x, 50 if x != 160 else 38, 7, c, 'i', 0)
    b += text(160, 162, '1253', 24, 'y', 'd', 'middle') + cap(160, 188, t('король Русі', 'King of Rus'), 21, 'm')
    h += card(nx(), 'gold wide', t('Данило — король Русі', 'Danylo, King of Rus'),
              t('У 1253 році в Дорогичині князь Данило Романович отримав корону від папи римського й став королем Русі.',
                'In 1253 in Dorohychyn, Prince Danylo Romanovych received a crown from the Pope and became King of Rus.'),
              svg(320, 196, b, t('корона 1253', 'crown 1253')),
              t('Галицько-Волинська держава берегла традиції Русі аж до середини XIV століття. Від неї тягнеться нитка до козаків, а від козаків — до нас.',
                'The Galicia-Volhynia state kept the traditions of Rus alive until the middle of the 14th century. From it a thread runs to the Cossacks, and from the Cossacks to us.'))
    h += '</div>'
    # ---------- I. Cossacks
    h += band(t('Козацький рід', 'Cossack roots'), t('Звідки ми і чому нам є ким пишатися.', 'Where we come from, and why we have people to be proud of.'), 'b1')
    h += '<div class="grid">'
    def sabre(x0, y0, x1, y1, bow=0.18):
        """a curved Cossack sabre as a filled ink blade from hilt (x0,y0) to tip (x1,y1), with guard and grip."""
        dx, dy = x1 - x0, y1 - y0
        L = (dx * dx + dy * dy) ** .5
        nx_, ny_ = -dy / L, dx / L
        cx, cy = x0 + dx * .55 + nx_ * L * bow, y0 + dy * .55 + ny_ * L * bow
        w = 6
        d = (f'M{x0 + nx_ * w:.1f} {y0 + ny_ * w:.1f} Q{cx + nx_ * w:.1f} {cy + ny_ * w:.1f} {x1:.1f} {y1:.1f} '
             f'Q{cx - nx_ * w * .2:.1f} {cy - ny_ * w * .2:.1f} {x0 - nx_ * w:.1f} {y0 - ny_ * w:.1f} Z')
        g = path(d, 'i', 0, 'var(--ink)')
        g += line(x0 + nx_ * 14, y0 + ny_ * 14, x0 - nx_ * 14, y0 - ny_ * 14, 'i', 5)
        g += line(x0, y0, x0 - dx / L * 26, y0 - dy / L * 26, 'i', 7)
        return g
    b = sabre(86, 122, 262, 20, -.12)
    b += line(250, 124, 112, 34, 'i', 7)
    for k in range(8):
        a_ = math.radians(k * 45)
        b += line(104 + 10 * math.cos(a_), 28 + 10 * math.sin(a_), 104 + 21 * math.cos(a_), 28 + 21 * math.sin(a_), 'h', 6, cap='butt')
    b += circle(104, 28, 11, 'var(--hay)', 'i', 2.5)
    b += cap(170, 158, t('булава і шабля — влада й сила', 'the mace and the sabre: power and strength'), 21, 'm')
    h += card(nx(), '', t('Запорозька Січ', 'The Zaporozhian Sich'),
              t('У середині XVI століття за дніпровськими порогами постала Запорозька Січ — вільне козацьке військо. Отамана й гетьмана обирали самі козаки на раді.',
                'In the middle of the 16th century, the Zaporozhian Sich grew up beyond the Dnipro rapids: a free Cossack army. The Cossacks themselves chose their otaman and hetman at a council.'),
              svg(340, 168, b, t('булава і шабля', 'mace and sabre')),
              t('Велику раду козаки скликали на Покрову, 14 жовтня. Тепер цього дня Україна вшановує захисників і захисниць — сучасних козаків — і відзначає День українського козацтва.',
                'Cossacks held their great council on the feast of Pokrova, 14 October. Today on that day Ukraine honours its defenders, the Cossacks of our time, and celebrates Ukrainian Cossack Day.'))
    b = rect(70, 14, 200, 120, 'var(--cell)', 'h', 3, 10) + path('M70 22 Q60 14 70 6 M270 22 Q280 14 270 6', 'h', 3)
    for k, lab in enumerate([t('закони', 'laws'), t('гетьман', 'hetman'), t('суд', 'courts')]):
        x = 106 + k * 64
        b += rect(x - 29, 64, 58, 52, 'var(--paper)', 'y', 2.5, 6) + cap(x, 96, lab, 16, 'y', 50)
    b += text(170, 46, '1710', 26, 'y', 'd', 'middle') + cap(170, 156, t('влада поділена на три гілки', 'power split into three branches'), 21, 'm')
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
    b += cap(160, 122, t('школа — приблизно в 7 поселеннях із 10', 'a school in about 7 settlements out of 10'), 21, 'm')
    h += card(nx(), 'blue', t('Козацькі школи', 'Cossack schools'),
              t('У 1740–1747 роках у семи полках Гетьманщини працювало 766 шкіл на 1099 сіл і міст.',
                'In 1740–1747 the seven regiments of the Cossack Hetmanate had 766 schools for 1,099 villages and towns.'),
              svg(320, 134, b, '766 / 1099'),
              t('Козаки знали: грамотний народ — сильний народ. А в 1632 році в Києві постала Києво-Могилянська колегія, майбутня академія.',
                'The Cossacks knew that a people who can read is a strong people. And in 1632 the Kyiv-Mohyla College, later an academy, was founded in Kyiv.'))
    pts = ''.join(f'{"M" if q == 0 else "L"}{160 + (30 if q % 2 == 0 else 13) * math.cos(math.radians(-90 + q * 22.5)):.1f} {34 + (30 if q % 2 == 0 else 13) * math.sin(math.radians(-90 + q * 22.5)):.1f} ' for q in range(16))
    b = sabre(100, 124, 236, 62, -.1) + sabre(220, 124, 84, 62, .1)
    b += path(pts + 'Z', 'i', 1.5, 'var(--hay)')
    b += cap(160, 162, t('справжні чари — знання й сміливість', 'the real magic: knowledge and courage'), 22, 'm')
    h += card(nx(), '', t('Характерники', 'The kharakternyky'),
              t('У легендах козаки-характерники заговорювали кулі, мали дев’ять життів і могли перекидатися на звірів.',
                'In legends, the kharakternyky were Cossacks who could charm bullets, had nine lives and could turn into animals.'),
              svg(320, 172, b, t('зоря і шаблі', 'star and sabres')),
              t('Це легенди. Але вороги так боялися козацької вправності, що пояснювали її чарами. Справжня «магія» козаків — сміливість, знання й уміння. Цього можна навчитися: щодня, з кожною розв’язаною задачею.',
                'These are legends. But enemies feared Cossack skill so much that they explained it with magic. The Cossacks’ real "magic" was courage, knowledge and skill. And you can learn those, every day, with every problem you solve.'))
    b = ''
    for y in (44, 64, 84, 104):
        b += path(f'M16 {y} q 14 -7 28 0 t 28 0 t 28 0 t 28 0 t 28 0 t 28 0 t 28 0 t 28 0 t 28 0 t 28 0 t 28 0', 's', 2)
    for k in range(8):
        b += rect(118, 116 - k * 12, 54, 9, 'var(--ink)', 'i', 0, 1)
    b += line(16, 124, 304, 124, 'i', 4) + line(16, 24, 304, 24, 'i', 4)
    b += arrow(200, 118, 200, 30, 'y', 0, 3.4)
    b += cap(160, 154, t('гать через болото: вози, дерево, мішки', 'a causeway over the marsh: wagons, timber, sacks'), 19, 'm')
    h += card(nx(), 'wide', t('Берестечко, 1651: союзник зрадив — козаки вистояли', 'Berestechko, 1651: an ally betrayed them, the Cossacks held on'),
              t('Посеред битви під Берестечком союзник козаків, кримський хан, пішов із поля бою й захопив у полон гетьмана Богдана Хмельницького. Козацьке військо опинилося в оточенні біля болота.',
                'In the middle of the battle of Berestechko, the Cossacks’ ally, the Crimean khan, left the battlefield and took Hetman Bohdan Khmelnytsky prisoner. The Cossack army was surrounded beside a marsh.'),
              svg(320, 164, b, t('гать через болото', 'causeway over the marsh')),
              t('Козаки не здалися. Вони обрали ватажком Івана Богуна й почали будувати гаті через болото й річку Пляшівку з возів, дерева, одягу й мішків. Частина війська вирвалася з оточення. Урок на всі часи: союзник може піти, а власна сила, власний розум і побратими поруч лишаються з тобою.',
                'The Cossacks did not give up. They chose Ivan Bohun as their leader and began building causeways across the marsh and the Pliashivka river from wagons, timber, clothes and sacks. Part of the army broke out. A lesson for all time: an ally may leave, but your own strength, your own mind and your comrades beside you stay with you.'))
    h += '</div>'
    # ---------- II. They tried to destroy us
    h += band(t('Нас намагалися знищити — а ми є', 'They tried to destroy us, and we are still here'),
              t('Російська імперія, радянська влада, нацистська окупація, а тепер знову Росія — Україну не раз намагалися стерти: мову, школи, учених і саме життя.',
                'The Russian Empire, the Soviet regime, Nazi occupation and now Russia again: over and over, others tried to wipe Ukraine out: its language, schools, scholars and very lives.'), 'b2')
    ev = [('1863', t('Валуєвський', 'Valuev'), t('циркуляр', 'circular')), ('1876', t('Емський', 'Ems'), t('указ', 'decree')),
          ('1932–33', t('Голодомор', 'Holodomor'), ''), ('1937', t('Великий', 'Great'), t('терор', 'Terror')),
          ('1941', t('нацистська', 'Nazi'), t('окупація', 'occupation')), ('1944', t('депортація', 'deportation of'), t('кримських татар', 'Crimean Tatars')),
          ('1994', t('Будапештський', 'Budapest'), t('меморандум', 'Memorandum')), ('2014', t('Крим', 'Crimea'), t('і Донбас', 'and Donbas')), ('2022', t('повномасштабне', 'full-scale'), t('вторгнення', 'invasion'))]
    b = ''
    for row in range(3):
        y = 46 + row * 100
        b += line(20, y, 400, y, 'i', 3)
        for k in range(3):
            yr, c1, c2 = ev[row * 3 + k]
            x = 76 + k * 134
            b += circle(x, y, 8, 'var(--yarn)', 'y', 0) + text(x, y - 18, yr, 16 if len(yr) == 4 else 14, 'y', 'd', 'middle')
            b += cap(x, y + 28, c1, 17, 'm', 128) + (cap(x, y + 46, c2, 17, 'm', 128) if c2 else '')
    b += cap(210, 330, t('а ми — тут, вчимося й живемо', 'and we are still here, learning and living'), 23, 'l')
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
        t('<b>1994.</b> Будапештський меморандум: Україна віддала ядерну зброю, а Росія, США й Велика Британія пообіцяли поважати її незалежність і кордони. Через 20 років Росія порушила цю обіцянку.',
          '<b>1994.</b> The Budapest Memorandum: Ukraine gave up its nuclear weapons, and Russia, the US and the UK promised to respect its independence and borders. Twenty years later Russia broke that promise.'),
        t('<b>2014.</b> Після Революції Гідності Росія напала на Україну: окупувала Крим і розв’язала війну на Донбасі. Відтоді Україна захищається.',
          '<b>2014.</b> After the Revolution of Dignity, Russia attacked Ukraine: it occupied Crimea and started the war in Donbas. Ukraine has been defending itself ever since.'),
        t('<b>2022.</b> 24 лютого Росія почала повномасштабне вторгнення. За даними МОН на серпень 2025 року, 1779 шкіл пошкоджено, а 226 зруйновано.',
          '<b>2022.</b> On 24 February Russia launched its full-scale invasion. According to Ukraine’s Ministry of Education, by August 2025 1,779 schools had been damaged and 226 destroyed.')])
    snyder = t('Американський історик Тімоті Снайдер з Єльського університету показує: у 1933–1945 роках Україна опинилася в серці «кривавих земель» між Гітлером і Сталіном, де загинули близько 14 мільйонів мирних людей. Україну хотіли зробити колонією й житницею для чужих.',
               'American historian Timothy Snyder of Yale University shows that in 1933–1945 Ukraine lay at the heart of the "bloodlands" between Hitler and Stalin, where about 14 million civilians were killed. Others wanted to turn Ukraine into a colony and a breadbasket for themselves.')
    h += '<div class="grid">' + card(nx(), 'wide', t('Чому саме мова й школи?', 'Why language and schools?'),
                                     t('Бо освічений народ, який знає свою історію, не скориш. Тому навчання для нас — це теж захист.',
                                       'Because a people that is educated and knows its history cannot be conquered. That is why learning is also a way to defend ourselves.'),
                                     svg(420, 346, b, t('спроби знищити Україну', 'attempts to destroy Ukraine')), '',
                                     f'<p class="more">{snyder}</p><ul class="tl">{tl}</ul>')
    b = rect(100, 12, 120, 126, 'var(--paper)', 'i', 3, 4) + text(160, 44, '1994', 24, 'i', 'd', 'middle')
    for y in (62, 74, 86):
        b += line(118, y, 202, y, 'm', 2)
    for x in (122, 160, 198):
        b += path(f'M{x - 14} 118 q 6 -10 10 0 t 10 0 t 8 -4', 'i', 2)
    b += path('M112 14 L150 60 L138 76 L182 104 L172 116 L210 138', 'y', 5)
    b += text(256, 92, '2014', 24, 'y', 'd', 'middle')
    b += cap(160, 164, t('підпис на папері сам не захищає', 'a signature on paper does not protect on its own'), 20, 'm')
    vow = t('Нам обіцяли.<br>Нас заспокоювали.<br><span>Ми пам’ятаємо.</span>', 'They promised us.<br>They reassured us.<br><span>We remember.</span>')
    h += card(nx(), 'wide mem', t('Будапештський меморандум: нам обіцяли', 'The Budapest Memorandum: they promised us'),
              t('5 грудня 1994 року Україна погодилася віддати ядерну зброю, яка лишилася на її землі від СРСР, — третій за розміром ядерний арсенал у світі. Натомість Росія, США й Велика Британія підписали обіцянку поважати незалежність і кордони України й не застосовувати проти неї силу.',
                'On 5 December 1994 Ukraine agreed to give up the nuclear weapons left on its soil by the USSR, the third-largest nuclear arsenal in the world. In return, Russia, the US and the UK signed a promise to respect Ukraine’s independence and borders and not to use force against it.'),
              f'<div class="memrow">{svg(320, 176, b, t("Будапештський меморандум", "Budapest Memorandum"))}<p class="vow">{vow}</p></div>',
              t('Це були лише запевнення, а не обов’язок нас захищати: нас заспокоювали словами. У 2014 році Росія напала, хоча сама поставила підпис під цією обіцянкою, і жодна з держав, що підписали меморандум, не захистила наших кордонів. Висновок той самий, що й у козаків під Берестечком: підпис на папері сам не захищає. Захищають власна армія, власні інженери й власні знання. Ми пам’ятаємо.',
                'These were only assurances, not a duty to defend us: we were reassured with words. In 2014 Russia attacked, although it had signed that very promise itself, and none of the states that signed the memorandum defended our borders. The lesson is the same as the Cossacks learned at Berestechko: a signature on paper does not protect on its own. What protects us is our own army, our own engineers and our own knowledge. We remember.'))
    h += '</div>'
    # ---------- II-b. We fought back
    h += band(t('Ми не тільки вистояли — ми боролися', 'We did not just survive: we fought back'),
              t('Сміливість, наполегливість і характер: українці раз у раз боронили свою свободу й перемагали.',
                'Courage, persistence and character: again and again Ukrainians defended their freedom, and won.'), 'b2b')
    h += '<div class="grid">'
    h += card(nx(), 'wide more-card', t('Брама Європи', 'The Gates of Europe'),
              t('Історик Гарвардського університету Сергій Плохій назвав свою книжку про історію України «Брама Європи». Наша земля віками стояла на перехресті імперій. І щоразу знаходилися люди, які не корилися: козаки, повстанці, солдати, поети, студенти, волонтери.',
                'Harvard historian Serhii Plokhy called his book on Ukraine’s history “The Gates of Europe”. For centuries our land stood at the crossroads of empires. And every time there were people who would not give in: Cossacks, insurgents, soldiers, poets, students, volunteers.'))
    # Khotyn / Kaffa: a Cossack chaika boat
    b = path('M40 92 Q160 128 280 92 L262 104 Q160 132 58 104 Z', 'i', 0, 'var(--ink)')
    for x in range(78, 250, 26):
        b += line(x, 104, x - 14, 128, 'i', 3)
    b += line(160, 92, 160, 26, 'i', 4) + path('M160 30 L212 52 L160 74 Z', 'y', 0, 'var(--yarn)')
    b += cap(160, 158, t('козацька чайка', 'a Cossack chaika boat'), 20, 'm')
    h += card(nx(), '', t('Хотин, 1621: козаки зупинили імперію', 'Khotyn, 1621: the Cossacks stopped an empire'),
              t('Восени 1621 року під Хотином величезна армія Османської імперії майже місяць штурмувала табір польського й козацького війська. Козаки гетьмана Петра Сагайдачного становили більшу частину захисників — і табір вистояв. Наступ імперії на Європу зупинили.',
                'In the autumn of 1621, at Khotyn, the huge army of the Ottoman Empire stormed the camp of the Polish and Cossack forces for almost a month. Hetman Petro Sahaidachny’s Cossacks were most of the defenders, and the camp held. The empire’s advance into Europe was stopped.'),
              svg(320, 168, b, t('чайка', 'chaika')),
              t('А ще раніше, у 1616 році, козаки Сагайдачного на легких човнах-чайках перепливли море, взяли фортецю Кафу в Криму й визволили з невільничого ринку бранців.',
                'Even earlier, in 1616, Sahaidachny’s Cossacks crossed the sea in light chaika boats, took the fortress of Kaffa in Crimea and freed captives from its slave market.'))
    # Konotop: a war banner
    b = line(110, 150, 110, 18, 'i', 5) + path('M110 22 L226 30 L206 62 L226 94 L110 86 Z', 'y', 0, 'var(--yarn)')
    b += cap(160, 176, '1659', 22, 'i')
    h += card(nx(), 'gold', t('Конотоп, 1659: перемога над московським військом', 'Konotop, 1659: victory over the Muscovite army'),
              t('Влітку 1659 року біля Конотопа військо гетьмана Івана Виговського разом із кримськими союзниками розбило велике московське військо, яке прийшло підкорити Гетьманщину.',
                'In the summer of 1659, near Konotop, Hetman Ivan Vyhovsky’s army and its Crimean allies defeated a large Muscovite army that had come to subdue the Hetmanate.'),
              svg(320, 186, b, t('корогва', 'banner')),
              t('Це одна з найбільших перемог козацької доби. Вона показала: українці можуть перемагати навіть набагато сильнішого ворога.',
                'It was one of the greatest victories of the Cossack age. It showed that Ukrainians can win even against a much stronger enemy.'))
    # Kruty: 500 vs 4000
    b = ''
    for k in range(8):
        b += rect(30 + k * 34, 38, 28, 28, 'var(--ink)', 'i', 0, 3)
    b += rect(30, 96, 28, 28, 'var(--yarn)', 'y', 0, 3)
    b += text(30, 28, t('≈ 4000 більшовиків', '≈ 4,000 Bolsheviks'), 15, 'i', 'd', 'start') + text(70, 116, t('500+ оборонців', '500+ defenders'), 15, 'y', 'd', 'start')
    b += cap(160, 158, t('кожен квадрат — 500 вояків', 'each square is 500 soldiers'), 19, 'm')
    h += card(nx(), '', t('Крути, 1918: юнаки проти армії', 'Kruty, 1918: young men against an army'),
              t('29 січня 1918 року біля станції Крути понад 500 юних добровольців — студентів, гімназистів, курсантів — стали проти більшовицької армії Муравйова: близько 4000 вояків із бронепоїздом і гарматами.',
                'On 29 January 1918, near Kruty station, over 500 young volunteers, students, schoolboys and cadets, stood against Muravyov’s Bolshevik army: about 4,000 soldiers with an armoured train and artillery.'),
              svg(320, 168, b, '500 / 4000'),
              t('Вони трималися понад п’ять годин, а відступаючи, підірвали колії й затримали наступ на кілька днів. Ворог переважав їх приблизно у 8 разів (4000 : 500 = 8). Сьогодні 29 січня — День пам’яті Героїв Крут.',
                'They held out for over five hours and, as they withdrew, blew up the tracks and delayed the advance by several days. The enemy outnumbered them about 8 to 1 (4,000 ÷ 500 = 8). Today 29 January is the Day of Remembrance of the Heroes of Kruty.'))
    # Kholodny Yar: dark forest
    b = ''
    for x, hh in ((40, 70), (78, 96), (118, 80), (160, 104), (202, 84), (242, 96), (280, 72)):
        b += path(f'M{x} {124 - hh} L{x + 22} 124 L{x - 22} 124 Z', 'i', 0, 'var(--ink)')
    b += line(20, 124, 300, 124, 'i', 3) + path('M150 30 h40 v26 h-40 z', 'i', 0, 'var(--yarn)') + line(150, 30, 150, 70, 'i', 3)
    b += cap(160, 156, t('«Воля України — або смерть»', '“Freedom for Ukraine, or death”'), 19, 'm')
    h += card(nx(), 'blue', t('Холодний Яр: повстанці не здалися', 'Kholodny Yar: the insurgents did not surrender'),
              t('У 1919–1922 роках у лісах Холодного Яру на Черкащині селяни й колишні вояки створили повстанську республіку. Роками вони боролися проти більшовицької влади, коли інші землі вже були окуповані.',
                'In 1919–1922, in the forests of Kholodny Yar in the Cherkasy region, peasants and former soldiers created an insurgent republic. For years they fought the Bolshevik regime, when other lands were already occupied.'),
              svg(320, 166, b, t('Холодний Яр', 'Kholodny Yar')),
              t('На їхньому прапорі було написано «Воля України — або смерть».', 'Their flag read “Freedom for Ukraine, or death”.'))
    # WW2: a fighter plane + 6 million
    b = path('M60 70 L250 62 L268 70 L250 78 Z', 'i', 0, 'var(--ink)') + path('M140 68 L120 28 L150 28 L176 68 Z M140 72 L120 112 L150 112 L176 72 Z', 'i', 0, 'var(--ink)')
    b += path('M64 70 L52 50 L70 50 L84 68 Z M64 70 L52 90 L70 90 L84 72 Z', 'i', 0, 'var(--ink)') + circle(268, 70, 4, 'var(--yarn)', 'y', 0)
    b += text(160, 150, t('понад 6 000 000', 'over 6,000,000'), 22, 'y', 'd', 'middle')
    h += card(nx(), 'gold', t('Проти нацизму', 'Against Nazism'),
              t('У Другій світовій війні понад 6 мільйонів українців воювали проти нацизму в різних арміях: у Червоній армії, у військах Польщі, США, Канади, Франції, Чехословаччини.',
                'In the Second World War over 6 million Ukrainians fought against Nazism in different armies: the Red Army and the forces of Poland, the USA, Canada, France and Czechoslovakia.'),
              svg(320, 166, b, t('понад 6 мільйонів', 'over 6 million')),
              t('Найрезультативнішим льотчиком-винищувачем усієї антигітлерівської коаліції був українець із Сумщини Іван Кожедуб: понад 60 збитих літаків.',
                'The highest-scoring fighter pilot of all the Allied forces was Ivan Kozhedub, a Ukrainian from the Sumy region: over 60 aircraft shot down.'))
    # UPA: forest and mountains, two empires pressing from both sides
    b = path('M20 120 L80 52 L120 92 L170 34 L230 96 L262 66 L300 120 Z', 'i', 0, 'var(--ink)')
    for x in range(40, 290, 22):
        b += path(f'M{x} 120 L{x + 8} 98 L{x + 16} 120 Z', 'l', 0, 'var(--leaf)')
    b += path('M6 20 L46 40 L6 60 Z', 'y', 0, 'var(--muted)') + path('M314 20 L274 40 L314 60 Z', 'y', 0, 'var(--muted)')
    b += cap(160, 154, t('проти двох імперій', 'against two empires'), 20, 'm')
    h += card(nx(), 'blue', t('УПА: проти двох імперій', 'The UPA: against two empires'),
              t('У 1942 році постала Українська повстанська армія. Вона воювала одночасно проти двох імперій — нацистської Німеччини й Радянського Союзу — за незалежну Україну. За весь час у її лавах воювали понад 100 тисяч людей.',
                'In 1942 the Ukrainian Insurgent Army was formed. It fought two empires at once, Nazi Germany and the Soviet Union, for an independent Ukraine. Over 100,000 people fought in its ranks over the years.'),
              svg(320, 164, b, t('ліси й гори', 'forests and mountains')),
              t('Після війни повстанці ще роками боролися з радянською владою в лісах і горах. Головнокомандувач УПА Роман Шухевич загинув у бою 5 березня 1950 року під Львовом, не здавшись. Символічною датою створення УПА вважають 14 жовтня, Покрову, — цього дня Україна вшановує своїх захисників і захисниць.',
                'After the war the insurgents fought the Soviet regime for years in the forests and mountains. The UPA commander-in-chief Roman Shukhevych was killed in battle near Lviv on 5 March 1950, refusing to surrender. 14 October, the feast of Pokrova, is regarded as the symbolic founding day of the UPA, and on that day Ukraine honours its defenders.'))
    # Volhynia: two candles of remembrance
    b = ''
    for x in (120, 200):
        b += rect(x - 12, 70, 24, 64, '#F3EEE3', 'i', 2, 3) + path(f'M{x} 66 C{x - 12} 52 {x - 4} 38 {x} 26 C{x + 4} 38 {x + 12} 52 {x} 66 Z', 'h', 0, 'var(--hay)')
    b += cap(160, 164, t('«Прощаємо і просимо прощення»', '“We forgive and ask for forgiveness”'), 19, 'm')
    h += card(nx(), 'gold', t('Волинь, 1943: пам’ять і примирення', 'Volhynia, 1943: remembrance and reconciliation'),
              t('У цій історії є й болюча сторінка. У 1943 році на Волині спалахнула жорстока війна між українцями й поляками. Загинули десятки тисяч мирних людей з обох боків.',
                'This story has a painful page too. In 1943 a brutal conflict between Ukrainians and Poles broke out in Volhynia. Tens of thousands of civilians on both sides were killed.'),
              svg(320, 176, b, t('дві свічки', 'two candles')),
              t('Українські й польські церковні лідери знайшли слова для примирення: «Прощаємо і просимо прощення». Сьогодні Україна й Польща — союзники, і Польща прийняла мільйони українців, які рятувалися від війни. Пам’ятати правду й простягати руку — теж сила.',
                'Ukrainian and Polish church leaders found the words for reconciliation: “We forgive and ask for forgiveness.” Today Ukraine and Poland are allies, and Poland took in millions of Ukrainians fleeing the war. Remembering the truth and holding out a hand is strength too.'))
    # Gulag uprisings: broken barbed wire
    b = line(30, 40, 290, 40, 'i', 3) + line(30, 70, 140, 70, 'i', 3) + line(180, 70, 290, 70, 'i', 3) + line(30, 100, 290, 100, 'i', 3)
    for x in range(40, 290, 24):
        for y in (40, 100):
            b += path(f'M{x - 5} {y - 5} L{x + 5} {y + 5} M{x + 5} {y - 5} L{x - 5} {y + 5}', 'i', 2)
    b += path('M140 70 L150 60 M180 70 L170 80', 'y', 3) + cap(160, 140, t('Норильськ, 1953: понад 20 000 в’язнів', 'Norilsk, 1953: over 20,000 prisoners'), 19, 'm')
    h += card(nx(), '', t('Повстання в радянських таборах', 'Uprisings in the Soviet camps'),
              t('Навіть у таборах ГУЛАГу українці не корилися. Влітку 1953 року в Норильську повстали понад 20 тисяч в’язнів, і серед організаторів були українці. Повстання жорстоко придушили.',
                'Even in the Gulag camps Ukrainians did not submit. In the summer of 1953 over 20,000 prisoners rose up in Norilsk, and Ukrainians were among the organisers. The uprising was brutally crushed.'),
              svg(320, 150, b, t('колючий дріт', 'barbed wire')),
              t('Історики вважають, що такі повстання підточили саму систему радянських таборів.', 'Historians believe that uprisings like this undermined the whole Soviet camp system.'))
    # Dissidents: a pen against a wall
    b = rect(40, 30, 120, 100, 'var(--cell)', 'i', 3, 2)
    for y in range(46, 126, 16):
        b += line(40, y, 160, y, 'i', 1.5)
    b += path('M196 128 L262 30 L276 40 L210 138 Z', 'i', 0, 'var(--ink)') + path('M196 128 L192 146 L210 138 Z', 'y', 0, 'var(--yarn)')
    b += cap(160, 166, t('слово проти системи', 'words against a system'), 20, 'm')
    h += card(nx(), 'blue', t('Дисиденти: слово сильніше за страх', 'Dissidents: words stronger than fear'),
              t('У 1976 році в Києві постала Українська Гельсінська група: вона розповідала світові, як радянська влада порушує права людей. Її учасників за це кидали до таборів.',
                'In 1976 the Ukrainian Helsinki Group was founded in Kyiv: it told the world how the Soviet regime violated people’s rights. Its members were sent to prison camps for it.'),
              svg(320, 176, b, t('перо', 'pen')),
              t('Поет Василь Стус провів у неволі багато років, але не відмовився від своїх переконань. Він загинув у таборі в 1985 році. Сьогодні його вірші вчать у школі.',
                'The poet Vasyl Stus spent many years in captivity but never gave up his beliefs. He died in a camp in 1985. Today his poems are studied at school.'))
    # 1990-1991: bar 90.32 %
    b = rect(30, 50, 260, 34, 'var(--cell)', 'i', 2, 6) + rect(30, 50, 260 * 0.9032, 34, 'var(--sky)', 's', 0, 6)
    b += text(150, 74, '90,32 % «так»' if lang == 'uk' else '90.32% “yes”', 17, 'w', 'd', 'middle')
    b += cap(160, 120, t('референдум 1 грудня 1991 року', 'referendum of 1 December 1991'), 20, 'm')
    h += card(nx(), 'gold', t('Студенти на граніті — і незалежність', 'Students on the granite, and independence'),
              t('У жовтні 1990 року студенти поставили намети в центрі Києва й оголосили голодування. Влада поступилася: голова уряду пішов у відставку. Це назвали Революцією на граніті.',
                'In October 1990 students pitched tents in the centre of Kyiv and went on hunger strike. The authorities gave in: the head of government resigned. It became known as the Revolution on Granite.'),
              svg(320, 132, b, '90.32%'),
              t('24 серпня 1991 року Україна проголосила незалежність, а 1 грудня на референдумі її підтримали 90,32 % тих, хто голосував, — це понад 9 із кожних 10.',
                'On 24 August 1991 Ukraine declared independence, and on 1 December 90.32% of those who voted backed it in a referendum: more than 9 in every 10.'))
    # Maidan
    b = ''
    for k in range(9):
        x = 40 + k * 30
        b += path(f'M{x} 110 Q{x + 6} {84 - (k % 3) * 8} {x} {60 - (k % 3) * 8} Q{x - 6} {84 - (k % 3) * 8} {x} 110 Z', 'y', 0, 'var(--yarn)')
        b += path(f'M{x} 104 Q{x + 3} 92 {x} 80 Q{x - 3} 92 {x} 104 Z', 'h', 0, 'var(--hay)')
    b += line(20, 112, 300, 112, 'i', 3) + cap(160, 146, t('Майдан, 2013–2014', 'Maidan, 2013–2014'), 20, 'm')
    h += card(nx(), 'wide', t('Революція Гідності', 'The Revolution of Dignity'),
              t('Взимку 2013–2014 років сотні тисяч українців вийшли на Майдан у Києві й на площі по всій країні, щоб відстояти свій вибір — жити вільно, за правилами, у Європі. Люди стояли на морозі тижнями.',
                'In the winter of 2013–2014 hundreds of thousands of Ukrainians took to the Maidan in Kyiv and to squares across the country to defend their choice: to live freely, by the rules, in Europe. People stood in the cold for weeks.'),
              svg(320, 156, b, t('Майдан', 'Maidan')),
              t('Понад сто людей загинули — їх називають Небесною сотнею. Але народ переміг.', 'More than a hundred people were killed; they are called the Heavenly Hundred. But the people won.'))
    # 2022: shield
    b = path('M160 18 L232 40 V88 C232 122 196 142 160 152 C124 142 88 122 88 88 V40 Z', 'i', 0, 'var(--sky)')
    b += path('M160 52 V120 M136 66 V96 Q148 112 160 120 Q172 112 184 96 V66', 'h', 5)
    b += cap(160, 178, t('Київ вистояв', 'Kyiv stood firm'), 20, 'm')
    h += card(nx(), 'blue wide', t('2022: світ побачив, які ми', '2022: the world saw who we are'),
              t('У лютому 2022 року Росія розраховувала захопити Київ за кілька днів. Київ вистояв, і вже на початку квітня ворожі війська відступили з Київщини, Чернігівщини й Сумщини. Восени Україна звільнила більшу частину Харківщини, а 11 листопада — Херсон.',
                'In February 2022 Russia expected to take Kyiv in a few days. Kyiv stood firm, and by early April the enemy had withdrawn from the Kyiv, Chernihiv and Sumy regions. In the autumn Ukraine liberated most of the Kharkiv region, and on 11 November, Kherson.'),
              svg(320, 192, b, t('щит', 'shield')),
              t('14 квітня 2022 року флагман російського Чорноморського флоту крейсер «Москва» затонув після удару українських ракет «Нептун», створених українськими інженерами. Сила, характер і знання — ось наша зброя.',
                'On 14 April 2022 the flagship of Russia’s Black Sea Fleet, the cruiser Moskva, sank after being hit by Ukrainian Neptune missiles designed by Ukrainian engineers. Strength, character and knowledge: those are our weapons.'))
    h += '</div>'
    # ---------- III. Ukrainian scientists
    h += band(t('Українські науковці, що змінили світ', 'Ukrainian scientists who changed the world'),
              t('Декого з них переслідували — а вони відкривали людям космос, небо й нові знання.', 'Some of them were persecuted, yet they opened up space, the sky and new knowledge for everyone.'), 'b3s')
    h += '<div class="grid">'
    b = circle(120, 86, 34, 'var(--sky)', 's', 0, ) + path('M70 120 Q160 20 260 60', 'h', 2.5, dash='6 6') + circle(260, 60, 7, 'var(--hay)', 'h', 0)
    b += path('M254 52 L266 46 M268 66 L278 72 M262 70 L258 82', 'h', 2.5)
    b += cap(160, 146, t('1957: перший супутник', '1957: first satellite'), 20, 'm') + cap(160, 168, t('1961: перша людина в космосі', '1961: first person in space'), 20, 'm')
    h += card(nx(), 'blue', t('Сергій Корольов', 'Serhiy Korolyov'),
              t('Народився в Житомирі у 1907 році, вчився в Київському політехнічному інституті. Головний конструктор, під чиїм керівництвом запустили перший супутник Землі й першу людину в космос.',
                'Born in Zhytomyr in 1907, he studied at the Kyiv Polytechnic Institute. He was the chief designer who led the launch of the first Earth satellite and the first person in space.'),
              svg(320, 176, b, t('супутник', 'satellite')),
              t('У 1938 році радянська влада його заарештувала, він працював навіть на золотій копальні на Колимі. Вижив — і повів людство в космос. Його ім’я тоді тримали в таємниці.',
                'In 1938 the Soviet regime arrested him; he was even sent to a gold mine in Kolyma. He survived and led humanity into space. At the time his name was kept secret.'))
    b = circle(70, 90, 30, 'var(--sky)', 's', 0) + circle(250, 80, 16, 'var(--line)', 'm', 2)
    b += path('M100 90 C150 30 220 40 250 56 C280 70 270 106 250 104 C220 102 160 120 100 96', 'y', 2.5, dash='6 5')
    b += cap(160, 150, t('траса Кондратюка до Місяця', 'Kondratyuk’s route to the Moon'), 21, 'm')
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
    b += cap(160, 150, t('найвища нагорода математиків', 'the highest prize in maths'), 22, 'm')
    h += card(nx(), 'blue', t('Марина В’язовська', 'Maryna Viazovska'),
              t('Народилася в Києві у 1984 році. У 2022 році отримала Філдсівську премію — другою жінкою в історії.',
                'Born in Kyiv in 1984. In 2022 she won the Fields Medal, only the second woman ever to do so.'),
              svg(320, 160, b, 'Fields Medal 2022'),
              t('Над тим, як найщільніше укласти кулі, математики думали понад 400 років, ще з часів Кеплера. Марина довела відповідь для 8-вимірного простору.',
                'Mathematicians have wondered how to pack spheres as tightly as possible for over 400 years, since Kepler. Maryna proved the answer in 8 dimensions.'))
    h += '</div>'
    # ---------- Culture
    h += band(t('Наша культура — теж наша сила', 'Our culture is our strength too'),
              t('Те, що створили українці, знає весь світ. Саме тому окупанти нищать наші музеї, бібліотеки й книжки.',
                'The whole world knows what Ukrainians have created. That is exactly why the occupiers destroy our museums, libraries and books.'), 'b3c')
    h += '<div class="grid">'
    b = rect(96, 14, 104, 128, 'var(--cell)', 'i', 3, 4) + line(108, 14, 108, 142, 'i', 2)
    b += text(152, 64, t('КОБЗАР', 'KOBZAR'), 17, 'i', 'd', 'middle') + text(152, 104, '1840', 22, 'y', 'd', 'middle')
    b += path('M252 14 C236 40 222 80 214 136 C226 96 244 60 262 22 Z', 'i', 0, 'var(--ink)') + line(214, 136, 208, 150, 'i', 2.5)
    b += cap(160, 172, t('1814: народився кріпаком · 1840: «Кобзар»', '1814: born a serf · 1840: Kobzar'), 20, 'm')
    h += card(nx(), '', t('Тарас Шевченко', 'Taras Shevchenko'),
              t('Народився кріпаком у 1814 році. У 1838 році друзі-митці викупили його на волю, а в 1840 році вийшов його «Кобзар». Шевченко був ще й художником.',
                'He was born a serf in 1814. In 1838 artist friends bought his freedom, and in 1840 his Kobzar was published. Shevchenko was a painter too.'),
              svg(320, 182, b, t('Кобзар 1840', 'Kobzar 1840')),
              t('За вірші імперія відправила його на заслання в солдати й заборонила писати й малювати. Він однаково писав. Його слова й досі з нами: «Борітеся — поборете!»',
                'For his poems the empire sent him into exile as a soldier and banned him from writing and painting. He wrote anyway. His words are still with us: "Fight on, and you will win!"'))
    b = path('M70 150 L110 96 L170 104 L228 82 L262 150 Z', 'i', 0, 'var(--ink)') + path('M150 104 L178 120 L160 136', 'm', 2)
    import math as _m
    cx, cy, dx_, dy_ = 212.0, 62.0, -_m.sqrt(.5), _m.sqrt(.5)          # head centre, handle direction (towards the stone)
    px_, py_ = _m.sqrt(.5), _m.sqrt(.5)
    pts = [(cx + px_ * a + dx_ * c, cy + py_ * a + dy_ * c) for a, c in ((-22, -10), (22, -10), (22, 10), (-22, 10))]
    b += line(cx, cy, cx + 62 * _m.sqrt(.5), cy - 62 * _m.sqrt(.5), 'h', 7)
    b += path('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z', 'i', 2, 'var(--muted)')
    for dx, dy in ((-20, -8), (-10, -20), (-24, 8), (2, -16)):
        b += line(172, 100, 172 + dx, 100 + dy, 'y', 2.5)
    b += cap(160, 178, t('Каменяр: 14 мов, 50 томів творів', 'The Stonebreaker: 14 languages, 50 volumes'), 19, 'm')
    h += card(nx(), 'gold', t('Іван Франко — «академія в одній особі»', 'Ivan Franko, “an academy in one person”'),
              t('Народився 1856 року в селі Нагуєвичі на Львівщині, у родині коваля. Знав 14 мов і перекладав із 48. Сорок років писав так, що новий твір з’являвся в середньому що два дні: вірші, повісті, казки, наукові праці. Зібрання його творів — 50 томів, і це лише частина написаного.',
                'He was born in 1856 in the village of Nahuievychi near Lviv, the son of a blacksmith. He knew 14 languages and translated from 48. For forty years he wrote so much that a new work appeared on average every two days: poems, stories, fairy tales and scholarly works. His collected works fill 50 volumes, and that is only part of what he wrote.'),
              svg(320, 188, b, t('молот і камінь', 'hammer and stone')),
              t('Австрійська влада тричі кидала його до в’язниці, а він писав далі. У 1893 році захистив докторську дисертацію у Відні, а наприкінці життя його висунули на Нобелівську премію. Його називають Каменярем: він ламав скелю несправедливості словом. Дітям він подарував «Лиса Микиту» й «Захара Беркута».',
                'The Austrian authorities jailed him three times, and he kept writing. In 1893 he earned a doctorate in Vienna, and near the end of his life he was nominated for the Nobel Prize. He is called the Stonebreaker: he broke the rock of injustice with words. For children he wrote “Fox Mykyta” and “Zakhar Berkut”.'))
    b = rect(70, 12, 180, 118, 'var(--sil)', 'i', 0, 8) + rect(150, 74, 20, 50, '#F3EEE3', 'i', 0, 2)
    b += path('M160 72 C150 60 154 48 160 36 C166 48 170 60 160 72 Z', 'h', 0, 'var(--hay)')
    b += ''.join(circle(x, y, 1.6, '#F3EEE3', 'i', 0) for x, y in ((92, 30), (118, 52), (214, 28), (232, 60), (200, 46), (96, 92)))
    b += cap(160, 158, 'Contra spem spero!', 24, 'y')
    h += card(nx(), 'blue', t('Леся Українка', 'Lesya Ukrainka'),
              t('З дитинства тяжко хворіла, але знала багато мов, писала вірші, драми й переклади.',
                'She was seriously ill from childhood, yet she knew many languages and wrote poems, plays and translations.'),
              svg(320, 172, b, 'Contra spem spero'),
              t('У 19 років вона написала вірш «Contra spem spero!» — «Без надії сподіваюсь!». Це про нас: навіть у темряві ми не здаємося.',
                'At 19 she wrote the poem "Contra spem spero!", "Against hope I hope!". That is us: even in the dark, we do not give up.'))
    b = ''.join(line(24, y, 296, y, 'm', 1.5) for y in (40, 50, 60, 70, 80))
    for k, (dy) in enumerate([60, 65, 60, 70] * 2):
        x = 52 + k * 32
        b += f'<ellipse cx="{x}" cy="{dy}" rx="6.5" ry="5" transform="rotate(-20 {x} {dy})" fill="var(--ink)"/>' + line(x + 6, dy, x + 6, dy - 30, 'i', 2)
    b += path('M40 98 H164', 'y', 3) + path('M168 98 H292', 'y', 3, dash='6 5')
    b += cap(160, 126, t('чотири ноти по колу — як візерунок', 'four notes round and round, like a pattern'), 20, 'm')
    b += text(160, 156, t('1916 Київ → 1922 Нью-Йорк', '1916 Kyiv → 1922 New York'), 16, 'y', 'd', 'middle')
    h += card(nx(), 'gold', t('Микола Леонтович і «Щедрик»', 'Mykola Leontovych and Shchedryk'),
              t('У 1916 році в Києві вперше прозвучав «Щедрик» Леонтовича. 5 жовтня 1922 року хор Олександра Кошиця заспівав його в Карнегі-Холі в Нью-Йорку.',
                'In 1916 Leontovych’s Shchedryk was first performed in Kyiv. On 5 October 1922 Oleksandr Koshyts’s choir sang it at Carnegie Hall in New York.'),
              svg(320, 166, b, t('ноти Щедрика', 'Shchedryk notes')),
              t('Тепер увесь світ співає його на Різдво як «Carol of the Bells». А самого Леонтовича в 1921 році вбив агент радянської ЧК.',
                'Now the whole world sings it at Christmas as "Carol of the Bells". Leontovych himself was killed in 1921 by an agent of the Soviet secret police, the Cheka.'))
    b = rect(110, 8, 100, 100, '#F3EEE3', 'i', 2.5, 2) + rect(124, 22, 72, 72, '#1A1512', 'i', 0, 0)
    b += text(160, 138, '1915', 22, 'i', 'd', 'middle') + cap(160, 166, t('квадрат — теж мистецтво', 'a square can be art'), 20, 'm')
    h += card(nx(), '', t('Казимир Малевич', 'Kazimir Malevich'),
              t('Народився в Києві у 1879 році. У 1915 році показав «Чорний квадрат» — картину, з якої почався новий напрям у мистецтві.',
                'Born in Kyiv in 1879. In 1915 he showed his Black Square, the painting that started a new movement in art.'),
              svg(320, 176, b, t('Чорний квадрат', 'Black Square')),
              t('Він доводив, що з простих фігур — квадрата, кола, хреста — можна будувати цілі світи. Геометрія, яку ти вчиш, — теж мова мистецтва.',
                'He showed that whole worlds can be built from simple shapes: a square, a circle, a cross. The geometry you learn is a language of art too.'))
    b = rect(100, 10, 120, 96, 'var(--cell)', 'i', 4, 2) + line(160, 92, 160, 56, 'l', 3)
    for k in range(6):
        a_ = math.radians(k * 60)
        b += f'<ellipse cx="{160 + 13 * math.cos(a_):.1f}" cy="{46 + 13 * math.sin(a_):.1f}" rx="9" ry="5" transform="rotate({k * 60} {160 + 13 * math.cos(a_):.1f} {46 + 13 * math.sin(a_):.1f})" fill="var(--yarn)"/>'
    b += circle(160, 46, 6, 'var(--hay)', 'i', 0)
    for x in (112, 140, 168, 196):
        b += path(f'M{x} 136 C{x - 8} 126 {x - 2} 116 {x + 6} 108 C{x + 8} 118 {x + 18} 124 {x + 12} 136 Z', 'y', 0, 'var(--yarn)')
        b += path(f'M{x + 3} 136 C{x} 130 {x + 3} 124 {x + 6} 120 C{x + 8} 126 {x + 11} 130 {x + 9} 136 Z', 'h', 0, 'var(--hay)')
    b += cap(160, 164, t('25 лютого 2022: картини винесли з вогню', '25 February 2022: paintings carried out of the fire'), 20, 'm')
    h += card(nx(), 'gold', t('Марія Примаченко', 'Maria Prymachenko'),
              t('Художниця із села Болотня на Київщині, малювала дивовижних звірів і квіти. 2009 рік ЮНЕСКО оголосило роком Марії Примаченко.',
                'An artist from the village of Bolotnia near Kyiv who painted wondrous beasts and flowers. UNESCO named 2009 the Year of Maria Prymachenko.'),
              svg(320, 174, b, t('врятовані картини', 'rescued paintings')),
              t('25 лютого 2022 року російський снаряд підпалив музей в Іванкові. Місцеві чоловіки виламали ґрати на вікні й винесли її картини з вогню. Нашу культуру намагаються спалити, а ми її рятуємо.',
                'On 25 February 2022 a Russian shell set the museum in Ivankiv on fire. Local men broke the bars on a window and carried her paintings out of the flames. They try to burn our culture, and we save it.'))
    cols = ['var(--yarn)', 'var(--sky)', 'var(--hay)', 'var(--leaf)', 'var(--ink)', 'var(--yarn)', 'var(--hay)', 'var(--sky)', 'var(--leaf)']
    b = ''
    for k in range(9):
        x, y = 112 + (k % 3) * 34, 8 + (k // 3) * 34
        ex, ey = x + 15, y + 15
        b += rect(x, y, 30, 30, 'var(--cell)', 'i', 2, 2) + f'<ellipse cx="{ex}" cy="{ey}" rx="9" ry="12" fill="{cols[k]}"/>'
        b += path(f'M{ex - 9} {ey} q 4.5 -3 9 0 t 9 0', 'w', 1.6) + line(ex - 8, ey - 6, ex + 8, ey - 6, 'w', 1.2) + line(ex - 8, ey + 6, ex + 8, ey + 6, 'w', 1.2)
    b += text(160, 136, '3 × 3 = 3² = 9', 20, 'y', 'd', 'middle') + cap(160, 164, t('писанки рядами: повтор — це множення', 'pysanky in rows: repeating is multiplying'), 20, 'm')
    h += card(nx(), 'blue wide', t('Енді Воргол — Андрій Вархола', 'Andy Warhol, born Andrii Varkhola'),
              t('Справжнє ім’я короля поп-арту — Андрій Вархола. Він народився в 1928 році в Піттсбурзі (США) в родині лемків із карпатського села Мікова біля Меджилабірців. Лемки — карпатська гілка українського народу. Коли кордони переділили, їхні села опинилися в Польщі й Словаччині.',
                'The real name of the king of pop art was Andrii Varkhola. He was born in 1928 in Pittsburgh, USA, into a Lemko family from the Carpathian village of Miková near Medzilaborce. The Lemkos are the Carpathian branch of the Ukrainian people. When borders were redrawn, their villages ended up in Poland and Slovakia.'),
              svg(320, 174, b, '3 x 3'),
              t('Родина берегла свої звичаї: ходила до греко-католицької церкви, а мама щороку на Великдень розписувала з Андрієм писанки. Згодом він повторював одне зображення рядами в різних кольорах: 3 рядки по 3 — це 9 картинок. Повтор і множення — та сама математика, що й у степенях.',
                'The family kept its traditions: they went to the Greek Catholic church, and every Easter his mother painted pysanky, decorated eggs, with Andrii. Later he repeated one image in rows, in different colours: 3 rows of 3 make 9 pictures. Repeating and multiplying: the same maths as in powers.'))
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
    b += cap(160, 152, t('дорослі, що вміють читати', 'adults who can read'), 21, 'm')
    h += card(nx(), '', t('Із бідності — до лідерства', 'From poverty to the top'),
              t('Південна Корея, зруйнована війною. У 1945 році читати вмів лише кожен п’ятий дорослий. Країна вклалася в школи.',
                'South Korea, wrecked by war. In 1945 only one adult in five could read. The country invested in schools.'),
              svg(320, 162, b, '22% → 88%'),
              t('За 25 років читати вміли майже 9 із 10. Сьогодні Корея — одна з найрозвиненіших технологічних країн світу.',
                'Within 25 years almost 9 in 10 could read. Today Korea is one of the world’s most advanced technology countries.'))
    b = line(30, 70, 290, 70, 'i', 3)
    for x, yr, lab_ in ((40, '1996', t('старт', 'start')), (180, '2000', t('комп’ютери', 'computers')), (280, '2001', t('інтернет', 'internet'))):
        b += circle(x, 70, 9, 'var(--sky)', 's', 0) + text(x, 50, yr, 18, 's', 'd', 'middle') + cap(x, 100, lab_, 20, 'm', 120)
    b += cap(160, 136, t('у кожній школі країни', 'in every school in the country'), 22, 'l')
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
          f'<div class="final">{kozak(uid='kz2')}<div>'
          f'<p class="anthem">{anthem}</p><p class="tail">{t("Державний Гімн України, слова Павла Чубинського", "National Anthem of Ukraine, words by Pavlo Chubynsky")}</p>'
          f'<p><b>{t("Нас намагалися знищити сотні років, нам давали обіцянки, які нас не захистили, — а ми тут. Ми вижили. Ми є. Ми вчимося, творимо й захищаємо одне одного. Кожен урок, навіть в укритті чи онлайн, робить Україну сильнішою.", "They tried to destroy us for hundreds of years, they gave us promises that did not protect us, and we are still here. We survived. We exist. We learn, create and protect one another. Every lesson, even in a shelter or online, makes Ukraine stronger.")}</b></p>'
          f'<p class="big">{t("Україна була, є і буде!", "Ukraine was, is and will be!")}</p></div></div></section>')
    return h


def page(kind, lang, links):
    t = lambda uk, en: uk if lang == 'uk' else en
    title = t('Ми — козацького роду · Математична пасіка', 'Of Cossack Kin · The Maths Apiary')
    lk = ' · '.join(f'<a href="{h}">{n}</a>' for n, h in links if h)
    body = (f'<div class="page">\n <header class="head"><div class="htext"><h1>{t("Ми — <span>козацького роду</span>", "Of <span>Cossack kin</span>")}</h1>'
            f'<p class="lead">{t("Україна була, є і буде. Ось наша історія: Трипілля й Київська Русь, козаки, які обирали гетьмана й писали конституцію, люди, яких намагалися знищити, і як ми боролися й перемагали, обіцянки, що нас не захистили, наша культура і чому освіта завжди була нашою силою.", "Ukraine was, is and will be. Here is our story: Trypillia and Kyivan Rus, Cossacks who elected their hetman and wrote a constitution, a people others tried to destroy and how we fought back and won, promises that did not protect us, our culture, and why education has always been our strength.")}</p>'
            f'<p class="links">{lk}</p></div>{kozak(uid='kz1')}</header>\n{secnav(lang)}\n{content(lang)}\n</div>')
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
            page('site', lang, site_links).replace('href="../index.html"', 'href="index.html"' if lang == 'uk' else 'href="index-en.html"').replace('href="../favicon', 'href="favicon').replace('href="../apple-touch', 'href="apple-touch'))
        art_links = [('English version' if lang == 'uk' else 'Українська версія', arts.get(other, ''))]
        (out / 'art' / f'education-{lang}.html').write_text(page('art', lang, art_links))
    print('ok')
