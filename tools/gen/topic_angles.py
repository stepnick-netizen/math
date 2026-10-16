"""Topic: adjacent angles (Урок №6, геометрія) — lesson cards, cheat sheet, three levels, world texts."""
import math
from svgkit import Run, text, hand, arrow, line, circle, rect, path, svg, width, pt, arc, C
from common import ROLE_SVG, pig

KEY = 'angles'


def say(world, role, s, flip=False):
    return f'<div class="say">{pig(ROLE_SVG[world][role], flip)}<p class="hand">{s}</p></div>'


DEG = '°'


def fig(rays, arcs=(), vertex=(160, 150), R=120, vlabel='O', w=320, h=180, extra='', label='', cls='viz', lab_r=None, top=0):
    """rays: [(deg, label)]; arcs: [(a1, a2, text, col, r, dashed)]. Angles in maths orientation."""
    cx, cy = vertex
    b = ''
    for a1, a2, txt, col, r, dash in arcs:
        b += arc(cx, cy, r, a1, a2, col, 3, fill=col if not dash else None, dash='6 5' if dash else None)
    for deg, lab in rays:
        x, y = pt(cx, cy, R, deg)
        b += line(cx, cy, x, y, 'i', 3)
        if lab:
            lx, ly = pt(cx, cy, R + 16, deg)
            b += text(lx, ly + 7, lab, 20, 'i', 'd', 'middle')
    b += circle(cx, cy, 4, 'var(--ink)', 'i', 0)
    if vlabel:
        b += text(cx, cy + 26, vlabel, 20, 'i', 'd', 'middle')
    for a1, a2, txt, col, r, dash in arcs:
        if not txt:
            continue
        mid = (a1 + a2) / 2
        rr = r + (24 if a2 - a1 < 30 else 18)
        if lab_r:
            rr = lab_r
        x, y = pt(cx, cy, rr, mid)
        tw = width(txt, 18)
        b += f'<rect x="{x - tw / 2 - 4:.1f}" y="{y - 13:.1f}" width="{tw + 8:.1f}" height="22" rx="6" fill="var(--paper)" opacity=".85"/>'
        b += text(x, y + 5, txt, 18, col, 'd', 'middle')
    b += extra
    return svg(w, h, b, label, cls) if top == 0 else f'<svg viewBox="0 {top} {w} {h - top}" class="{cls}" role="img" aria-label="{label}">{b}</svg>'


def bar(rows, w=320, unit=None, total=None, label='', cls='viz', note=''):
    """rows: [(name, [(units, col, text)])]; draws a bar model. total: text for the brace over the first row."""
    maxu = max(sum(u for u, _, _ in segs) for _, segs in rows)
    x0, x1 = 60, w - 16
    uw = (x1 - x0) / maxu
    b = ''
    y = 40 if total else 18
    if total:
        tot_u = sum(u for u, _, _ in rows[0][1])
        b += path(f'M{x0} {y - 4} Q{x0} {y - 16} {x0 + 12} {y - 16} L{x0 + tot_u * uw - 12:.1f} {y - 16} Q{x0 + tot_u * uw:.1f} {y - 16} {x0 + tot_u * uw:.1f} {y - 4}', 'h', 2.5)
        b += text(x0 + tot_u * uw / 2, y - 22, total, 18, 'h', 'd', 'middle')
    for name, segs in rows:
        b += text(x0 - 8, y + 24, name, 18, 'i', 'd', 'end')
        x = x0
        for u, col, txt in segs:
            for k in range(int(round(u)) if u == int(u) else 1):
                ww = uw if u == int(u) else u * uw
                b += rect(x + 1, y + 2, ww - 2, 32, 'var(--cell)' if col == 'cell' else col, 'var(--line)' if col == 'cell' else col, 1.5, 6,
                          extra=' fill-opacity=".85"' if col != 'cell' else '')
                x += ww
            if txt:
                b += text(x - (u * uw) / 2, y + 24, txt, 16, 'w' if col != 'cell' else 'm', 'd', 'middle')
        y += 46
    for nt in ([note] if isinstance(note, str) and note else (note or [])):
        b += hand(w / 2, y + 16, nt, 21, 'm')
        y += 26
    return svg(w, y + 4, b, label, cls)


Y, Pp, S, H, L, B = 'var(--yarn)', 'var(--plum)', 'var(--sky)', 'var(--hay)', 'var(--leaf)', 'var(--bad)'


# ---------------------------------------------------------------- lesson cards
def cards(lang, world):
    t = lambda uk, en: uk if lang == 'uk' else en
    out = []
    # 1. straight angle
    s1 = fig([(0, 'B'), (180, 'A')], [(0, 180, '180°', 'h', 46, False)], vertex=(160, 130), R=130, h=170,
             extra=hand(160, 30, t('розгорнутий кут', 'straight angle'), 24, 'h'), label='∠AOB = 180°')
    out.append(('', t('Розгорнутий кут', 'A straight angle'),
                t('Промені OA і OB <b>доповняльні</b>: вони продовжують один одного й разом утворюють пряму. Кут між ними — <b>180°</b>.',
                  'Rays OA and OB are <b>opposite rays</b>: together they make a straight line. The angle between them is <b>180°</b>.'),
                s1, f'<p class="tail">{t("Так само, як половина повного оберту (360°).", "That’s half a full turn (360°).")}</p>'))
    # 2. adjacent angles definition
    ex = arrow(234, 104, 196, 100, 'h', -0.2) + hand(270, 112, t('спільна сторона', 'shared side'), 21, 'h')
    ex += hand(160, 196, t('OC і OB — доповняльні промені', 'OC and OB are opposite rays'), 21, 'm')
    s2 = fig([(0, 'B'), (180, 'C'), (65, 'A')], [(0, 65, '', 'p', 40, False), (65, 180, '', 'y', 52, False)], vertex=(160, 150), R=120, h=206,
             extra=ex, label='∠COA і ∠AOB — суміжні')
    out.append(('', t('Суміжні кути', 'Adjacent angles'),
                t('Два кути <b>суміжні</b>, якщо в них одна сторона спільна, а дві інші — доповняльні промені.',
                  'Two angles are <b>adjacent on a straight line</b> if they share one side and their other sides are opposite rays.'),
                s2, f'<p class="tail">{t("∠COA і ∠AOB — суміжні: разом вони складають розгорнутий кут COB.", "∠COA and ∠AOB are adjacent: together they make the straight angle COB.")}</p>'
                + say(world, 'hostB', t('Суміжні кути — як дві половинки одного розгорнутого кута.', 'Adjacent angles are two pieces of one straight angle.'), True)))
    # 3. KEY theorem
    ex = Run([('130°', 'y', 'n'), (' + ', 'k', 'n'), ('50°', 'p', 'n'), (' = ', 'k', 'n'), ('180°', 'h', 'n')], 160, 206, 28, 'middle').svg
    s3 = fig([(0, 'M'), (180, 'N'), (50, 'K')], [(0, 50, '50°', 'p', 46, False), (50, 180, '130°', 'y', 60, False)], vertex=(160, 150), R=118, vlabel='A', h=220,
             extra=ex, label='130° + 50° = 180°')
    out.append(('key wide two', t('Головне: сума суміжних кутів — 180°', 'Key rule: adjacent angles add up to 180°'),
                t('<b>∠NAK + ∠KAM = 180°.</b> Хоч як нахиляй промінь AK, два суміжні кути разом завжди дають розгорнутий кут.',
                  '<b>∠NAK + ∠KAM = 180°.</b> However you tilt ray AK, the two adjacent angles always make a straight angle together.'),
                s3, say(world, 'tidy', t('Один кут більшає — сусід менше. Разом завжди 180°!', 'One angle grows, its neighbour shrinks. Together they always make 180°!'))))
    # 4. find the partner
    ex = hand(160, 30, t('180° − 72° = 108°', '180° − 72° = 108°'), 28, 'l')
    s4 = fig([(0, ''), (180, ''), (72, '')], [(0, 72, '72°', 'p', 44, False), (72, 180, '?', 'h', 56, True)], vertex=(160, 160), R=118, vlabel='', h=180,
             extra=ex, label='суміжний з 72° — 108°')
    out.append(('', t('Знайди сусіда', 'Find the partner'),
                t('Знаєш один кут — віднімай від 180°: <b>суміжний = 180° − відомий</b>.', 'Know one angle? Subtract it from 180°: <b>partner = 180° − known angle</b>.'),
                s4, f'<p class="tail">{t("Перевірка: 72° + 108° = 180°.", "Check: 72° + 108° = 180°.")}</p>'))
    # 5. three consequences
    def mini(x0, a, l1, l2, c1, c2, cap1, cap2):
        cy = 96
        s = line(x0 - 52, cy, x0 + 52, cy, 'i', 3)
        ex_, ey_ = pt(x0, cy, 54, a)
        s += line(x0, cy, ex_, ey_, 'i', 3)
        s += arc(x0, cy, 22, 0, a, c1, 2.5, fill=c1) + arc(x0, cy, 30, a, 180, c2, 2.5, fill=c2)
        lx, ly = pt(x0, cy, 46, a / 2)
        s += text(lx + 6, ly + 4, l1, 15, c1, 'd', 'middle')
        lx, ly = pt(x0, cy, 50, (a + 180) / 2)
        s += text(lx - 6, ly + 4, l2, 15, c2, 'd', 'middle')
        s += circle(x0, cy, 3.5, 'var(--ink)', 'i', 0)
        s += hand(x0, 128, cap1, 18, 'm') + hand(x0, 148, cap2, 18, 'm')
        return s
    body = mini(64, 90, '90°', '90°', 'l', 'l', t('прямий →', 'right →'), t('прямий', 'right'))
    body += mini(190, 50, '50°', '130°', 'p', 'y', t('гострий →', 'acute →'), t('тупий', 'obtuse'))
    body += mini(316, 110, '110°', '70°', 'y', 'p', t('тупий →', 'obtuse →'), t('гострий', 'acute'))
    s5 = svg(380, 158, body, t('наслідки', 'consequences'))
    out.append(('wide two', t('Три наслідки', 'Three consequences'),
                t('Кут, суміжний із <b>прямим</b>, — прямий. Із <b>гострим</b> — тупий. Із <b>тупим</b> — гострий.',
                  'The partner of a <b>right</b> angle is right. The partner of an <b>acute</b> angle is obtuse. The partner of an <b>obtuse</b> angle is acute.'),
                s5, f'<p class="more">{t("І ще: якщо два кути рівні, то й суміжні з ними кути рівні. Два кути, суміжні з одним кутом, теж рівні.", "Also: if two angles are equal, their partners are equal too. Two angles that are both partners of the same angle are equal.")}</p>'))
    # 6. bisector
    ex = hand(250, 46, t('бісектриса', 'bisector'), 24, 's') + arrow(222, 52, 205, 82, 's', 0.2)
    s6 = fig([(0, 'B'), (80, 'A'), (40, 'L')], [(0, 40, '40°', 'p', 50, False), (40, 80, '40°', 'y', 50, False)], vertex=(110, 160), R=130, vlabel='O', h=196,
             extra=ex + text(194, 196, t('∠AOB = 80°', '∠AOB = 80°'), 18, 'm', 'd', 'start'), label='бісектриса ділить 80° на 40° і 40°')
    out.append(('', t('Бісектриса', 'The angle bisector'),
                t('<b>Бісектриса</b> — промінь, що ділить кут навпіл. Кут = 2 · половинка.', 'The <b>bisector</b> is the ray that splits an angle in half. Angle = 2 × half.'),
                s6, say(world, 'messy', t('Ділю порівну, як смаколик на двох!', 'Split it fairly, like a treat for two!'), True)))
    # 7. ratio 4 : 5
    s7 = bar([('', [(4, Pp, '4 ч.' if lang == 'uk' else '4 parts'), (5, Y, '5 ч.' if lang == 'uk' else '5 parts')])], total='180°',
             note=[t('① 4 + 5 = 9 частин', '① 4 + 5 = 9 parts'), t('② 180° : 9 = 20°', '② 180° ÷ 9 = 20°'), t('③ 4 · 20° = 80°, 5 · 20° = 100°', '③ 4 × 20° = 80°, 5 × 20° = 100°')], label='4 : 5 → 80°, 100°')
    out.append(('', t('Кути у відношенні 4 : 5', 'Angles in the ratio 4 : 5'),
                t('Суміжні кути відносяться як 4 : 5. Ділимо 180° на <b>частини</b>.', 'Two adjacent angles are in the ratio 4 : 5. Split 180° into <b>parts</b>.'),
                s7, f'<p class="tail">{t("Перевірка: 80° + 100° = 180°, і 80 : 100 = 4 : 5.", "Check: 80° + 100° = 180°, and 80 : 100 = 4 : 5.")}</p>'))
    # 8. bigger by 30
    s8 = bar([('x', [(5, Pp, '')]), ('x + 30°', [(5, Y, ''), (2, H, '30°')])], label='x + x + 30° = 180°',
             note=t('2x + 30° = 180° → 2x = 150° → x = 75°', '2x + 30° = 180° → 2x = 150° → x = 75°'))
    out.append(('', t('Один більший на 30°', 'One is 30° bigger'),
                t('Менший кут — <b>x</b>, більший — <b>x + 30°</b>. Разом 180°.', 'Call the smaller angle <b>x</b> and the bigger one <b>x + 30°</b>. Together they make 180°.'),
                s8, f'<p class="tail">{t("Відповідь: 75° і 105°. Перевірка: 105° − 75° = 30°.", "Answer: 75° and 105°. Check: 105° − 75° = 30°.")}</p>'))
    # 9. laptop
    lap = path('M40 150 H300', 'i', 3) + path('M160 150 L250 150', 's', 7) + path('M160 150 L119 37', 's', 7)
    lap += arc(160, 150, 40, 0, 110, 'y', 3, fill='y') + arc(160, 150, 52, 110, 180, 'p', 3, fill='p')
    lap += text(196, 106, '110°', 18, 'y', 'd', 'middle') + text(98, 116, '70°', 18, 'p', 'd', 'middle')
    lap += hand(240, 176, t('стіл', 'table'), 20, 'm') + hand(80, 60, t('кришка', 'lid'), 22, 's')
    s9 = svg(340, 188, lap, '110° + 70° = 180°')
    out.append(('wide two', t('Кути в житті', 'Angles in real life'),
                t('Кришку ноутбука відкрили на 110° від клавіатури. Тоді з продовженням стола вона утворює <b>70°</b>.',
                  'A laptop lid is opened to 110° from the keyboard. So it makes <b>70°</b> with the rest of the table line.'),
                s9, f'<p class="tail">{t("Будівельники, штурмани й розробники ігор щодня рахують такі кути.", "Builders, navigators and game designers work out angles like these every day.")}</p>'))
    out[4], out[5] = out[5], out[4]
    html = ''
    for i, (cls, h2, p, sv, extra) in enumerate(out, 1):
        if 'two' in cls:
            html += f'<section class="box {cls}"><div><span class="n">{i}</span><h2>{h2}</h2><p>{p}</p>{extra}</div>{sv}</section>'
        else:
            html += f'<section class="box {cls}"><span class="n">{i}</span><h2>{h2}</h2><p>{p}</p>{sv}{extra}</section>'
    return html


def lesson(lang):
    return ''.join(f'<div class="grid" data-world="{w}"{"" if w == "meadow" else " hidden"}>{cards(lang, w)}</div>' for w in ('meadow', 'space', 'bricks'))


def sheet(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    w = 'meadow'
    return dict(
        title=t('Шпаргалка: суміжні кути', 'Cheat sheet: adjacent angles'),
        h1=t('Суміжні кути <span>на одній сторінці</span>', 'Adjacent angles <span>on one page</span>'),
        bubble=t('Привіт! Тут усе головне про суміжні кути: що це таке, чому разом вони дають 180° і як розв’язувати задачі з бісектрисою й відношеннями.',
                 'Hi! Here is everything important about adjacent angles: what they are, why together they make 180°, and how to solve problems with bisectors and ratios.'),
        cast=[pig(ROLE_SVG[w][r], r == 'hostB') for r in ('hostA', 'hostB', 'tidy', 'messy')],
        cards=cards(lang, w), final_svg=pig(ROLE_SVG[w]['tidy']),
        final=t('Самоперевірка: склади знайдені суміжні кути. Вийшло 180°? Тоді все правильно!', 'Check yourself: add the two adjacent angles you found. Do you get 180°? Then you’re right!'))


# ---------------------------------------------------------------- levels
def levels(lang, edition):
    t = lambda uk, en: uk if lang == 'uk' else en
    yes, no = t('Так', 'Yes'), t('Ні', 'No')
    YN = lambda ans, why_yes, why_no: {'type': 'choice', 'style': 'pills', 'opts': [['yes', yes], ['no', no]], 'ans': ans,
                                       'tag': {'yes': 'said-yes', 'no': 'said-no'}}
    deg = lambda v, name='angle': {'pre': '', 'post': '°', 'ans': v, 'n': name, 'aria': t('градуси', 'degrees')}
    ang = lambda nm, v, name='angle': {'pre': f'{nm} =', 'post': '°', 'ans': v, 'n': name, 'aria': nm}
    A = []
    # a0 definition (teacher slide 2)
    p0 = fig([(0, 'B'), (180, 'C'), (70, 'A')], [(70, 180, '', 'y', 48, False), (0, 70, '70°', 'p', 38, False)], h=190, label='∠COA, ∠AOB', cls='stg')
    p0b = fig([(0, 'B'), (180, 'C'), (70, 'A')], [(70, 180, '110°', 'y', 48, False), (0, 70, '70°', 'p', 38, False)], h=190, label='∠COA = 110°', cls='stg')
    A.append(dict(teacher=True, pics=[p0, p0, p0b], steps=[
        dict(YN('yes', '', ''), p=t('∠COA і ∠AOB — суміжні?', 'Are ∠COA and ∠AOB adjacent?'),
             h=[t('перевір дві умови: є спільна сторона? Дві інші сторони лежать на одній прямій і дивляться в різні боки?', 'check two things: is there a shared side? Do the other two sides lie on one straight line, pointing opposite ways?'),
                t('спільна сторона — OA, а OC і OB разом утворюють пряму.', 'the shared side is OA, and OC and OB together make a straight line.')],
             ok=t('Так, суміжні', 'Yes, adjacent')),
        dict(type='num', p=t('∠AOB = 70°. Знайди ∠COA.', '∠AOB = 70°. Find ∠COA.'), f=[ang('∠COA', 110)], traps=[[0, 70, 'copied-angle'], [0, 20, 'used-90']],
             h=[t('суміжні кути разом дають 180°.', 'adjacent angles add up to 180°.'), '180° − 70° = ?'], ok='∠COA = 110°')],
        after=t('110° + 70° = 180°.', '110° + 70° = 180°.'), label=t('Чи суміжні ∠COA і ∠AOB; ∠COA = 110°', 'Adjacent? ∠COA = 110°')))
    # a1 theorem (teacher slide 3 figure)
    p1 = fig([(0, 'M'), (180, 'N'), (50, 'K')], [(50, 180, '130°', 'y', 56, False), (0, 50, '?', 'h', 42, True)], vlabel='A', h=190, label='∠NAK = 130°', cls='stg')
    p1b = fig([(0, 'M'), (180, 'N'), (50, 'K')], [(50, 180, '130°', 'y', 56, False), (0, 50, '50°', 'p', 42, False)], vlabel='A', h=190, label='∠KAM = 50°', cls='stg')
    A.append(dict(teacher=True, pics=[p1, p1b], steps=[
        dict(type='num', p=t('∠NAK = 130°. Знайди ∠KAM.', '∠NAK = 130°. Find ∠KAM.'), f=[ang('∠KAM', 50)], traps=[[0, 130, 'copied-angle'], [0, 230, 'added-180']],
             h=[t('∠NAK і ∠KAM — суміжні, разом 180°.', '∠NAK and ∠KAM are adjacent, so together they make 180°.'), '180° − 130° = ?'], ok='∠KAM = 50°')],
        after='130° + 50° = 180°.', label='∠NAK = 130° → ∠KAM = 50°'))
    # a2 not adjacent (sides not on one line)
    p2 = fig([(10, 'B'), (70, 'A'), (160, 'C')], [(10, 70, '60°', 'p', 40, False), (70, 160, '90°', 'y', 52, False)], h=190, label='∠BOA, ∠AOC', cls='stg')
    A.append(dict(teacher=False, pics=[p2, p2], steps=[
        dict(YN('no', '', ''), p=t('∠BOA і ∠AOC — суміжні?', 'Are ∠BOA and ∠AOC adjacent?'),
             h=[t('спільна сторона є. А чи лежать OB і OC на одній прямій?', 'there is a shared side. But do OB and OC lie on one straight line?'),
                t('60° + 90° = 150°, а не 180°. Отже, OB і OC не доповняльні.', '60° + 90° = 150°, not 180°. So OB and OC are not opposite rays.')],
             ok=t('Ні, не суміжні', 'No, not adjacent'))],
        after=t('Спільна сторона є, але OB і OC не утворюють пряму: 60° + 90° = 150°.', 'They share a side, but OB and OC don’t make a straight line: 60° + 90° = 150°.'),
        label=t('Чи суміжні ∠BOA і ∠AOC (60° і 90°)', 'Adjacent? 60° and 90°')))
    # a3 vertical angles
    vex = arc(160, 100, 34, 25, 145, 'y', 3, fill='y') + arc(160, 100, 34, 205, 325, 'p', 3, fill='p')
    vex += text(160, 58, '1', 20, 'y', 'd', 'middle') + text(160, 154, '2', 20, 'p', 'd', 'middle')
    p3 = fig([(25, ''), (205, ''), (145, ''), (325, '')], [], vertex=(160, 100), R=110, vlabel='', h=200, extra=vex, label='∠1, ∠2', cls='stg')
    A.append(dict(teacher=False, pics=[p3, p3], steps=[
        dict(YN('no', '', ''), p=t('Дві прямі перетнулися. ∠1 і ∠2 — суміжні?', 'Two lines cross. Are ∠1 and ∠2 adjacent?'),
             h=[t('чи є в цих кутів спільна сторона?', 'do these angles share a side?'), t('∠1 і ∠2 лише торкаються вершиною. Спільної сторони немає.', '∠1 and ∠2 only meet at the vertex. They share no side.')],
             ok=t('Ні, не суміжні', 'No, not adjacent'))],
        after=t('У них немає спільної сторони. Такі кути називають вертикальними — про них буде окремий урок.', 'They share no side. Angles like these are called vertically opposite angles: there’s a separate lesson on them.'),
        label=t('Чи суміжні кути при перетині прямих', 'Adjacent? Angles where two lines cross')))
    # a4 right angle consequence
    rx = rect(160, 122, 16, 16, 'none', 'l', 2, 0) + rect(144, 122, 16, 16, 'none', 'l', 2, 0)
    p4 = fig([(0, ''), (180, ''), (90, '')], [], vlabel='', h=190, extra=rx + text(206, 112, '90°', 18, 'l', 'd', 'middle'), label='90°', cls='stg')
    A.append(dict(teacher=False, pics=[p4, p4], steps=[
        dict(type='choice', style='pills', p=t('Один із суміжних кутів прямий. Яким буде другий?', 'One of two adjacent angles is a right angle. What is the other one?'),
             opts=[['acute', t('Гострий', 'Acute')], ['right', t('Прямий', 'Right')], ['obtuse', t('Тупий', 'Obtuse')]], ans='right',
             tag={'acute': 'right-as-acute', 'obtuse': 'right-as-obtuse'},
             h=[t('порахуй: 180° − 90° = ?', 'work it out: 180° − 90° = ?'), t('180° − 90° = 90°, а кут 90° — прямий.', '180° − 90° = 90°, and a 90° angle is a right angle.')],
             ok=t('Прямий', 'Right'))],
        after=t('180° − 90° = 90°: кут, суміжний із прямим, — теж прямий.', '180° − 90° = 90°: the partner of a right angle is also a right angle.'),
        label=t('Суміжний із прямим кутом', 'Partner of a right angle')))
    # a5 35°
    p5 = fig([(0, 'D'), (180, 'E'), (35, 'F')], [(0, 35, '35°', 'p', 52, False), (35, 180, '?', 'h', 40, True)], vlabel='O', h=190, label='35°', cls='stg')
    p5b = fig([(0, 'D'), (180, 'E'), (35, 'F')], [(0, 35, '35°', 'p', 52, False), (35, 180, '145°', 'y', 40, False)], vlabel='O', h=190, label='145°', cls='stg')
    A.append(dict(teacher=False, pics=[p5, p5b], steps=[
        dict(type='num', p=t('∠DOF = 35°. Знайди суміжний з ним ∠FOE.', '∠DOF = 35°. Find its partner ∠FOE.'), f=[ang('∠FOE', 145)], traps=[[0, 55, 'used-90'], [0, 35, 'copied-angle']],
             h=[t('суміжний = 180° − відомий. Не плутай із 90°!', 'partner = 180° − known angle. Don’t mix it up with 90°!'), '180° − 35° = ?'], ok='∠FOE = 145°')],
        after='35° + 145° = 180°.', label='∠DOF = 35° → ∠FOE = 145°'))
    # a6 acute -> obtuse
    p6 = fig([(0, ''), (180, ''), (58, '')], [(0, 58, '', 'p', 44, False), (58, 180, '?', 'h', 56, True)], vlabel='', h=190, label='гострий кут', cls='stg')
    A.append(dict(teacher=False, pics=[p6, p6], steps=[
        dict(type='choice', style='pills', p=t('Кут гострий. Яким буде суміжний з ним кут?', 'An angle is acute. What is its partner?'),
             opts=[['acute', t('Гострий', 'Acute')], ['right', t('Прямий', 'Right')], ['obtuse', t('Тупий', 'Obtuse')]], ans='obtuse',
             tag={'acute': 'acute-as-acute', 'right': 'acute-as-right'},
             h=[t('гострий кут менший за 90°. Що буде, якщо відняти його від 180°?', 'an acute angle is less than 90°. What happens when you take it away from 180°?'),
                t('наприклад, 180° − 40° = 140°. Це більше за 90°.', 'for example, 180° − 40° = 140°. That’s more than 90°.')],
             ok=t('Тупий', 'Obtuse'))],
        after=t('Від 180° забрали менше ніж 90° — лишилося більше ніж 90°. Кут тупий.', 'Take less than 90° from 180° and more than 90° is left. The angle is obtuse.'),
        label=t('Суміжний із гострим кутом', 'Partner of an acute angle')))
    # a7 equal angles -> equal partners
    eqx = (arc(80, 120, 26, 0, 64, 'p', 3, fill='p') + line(80, 120, 146, 120, 'i', 3) + line(80, 120, 14, 120, 'i', 3) + line(80, 120, 112, 54, 'i', 3)
           + arc(240, 120, 26, 0, 64, 'p', 3, fill='p') + line(240, 120, 306, 120, 'i', 3) + line(240, 120, 174, 120, 'i', 3) + line(240, 120, 272, 54, 'i', 3)
           + text(118, 104, '1', 18, 'p', 'd', 'middle') + text(278, 104, '2', 18, 'p', 'd', 'middle'))
    p7 = svg(320, 150, eqx + hand(160, 150, '∠1 = ∠2 = 64°', 22, 'p'), '∠1 = ∠2', 'stg')
    A.append(dict(teacher=False, pics=[p7, p7, p7], steps=[
        dict(YN('yes', '', ''), p=t('∠1 = ∠2. Чи рівні кути, суміжні з ними?', '∠1 = ∠2. Are their partners equal too?'),
             h=[t('кожен суміжний — це 180° мінус свій кут.', 'each partner is 180° minus its own angle.'), t('180° − ∠1 і 180° − ∠2: від однакового віднімаємо однакове.', '180° − ∠1 and 180° − ∠2: the same taken from the same.')],
             ok=t('Так, рівні', 'Yes, equal')),
        dict(type='num', p=t('∠1 = ∠2 = 64°. Скільки градусів у кожного суміжного кута?', '∠1 = ∠2 = 64°. How many degrees is each partner?'), f=[deg(116)], traps=[[0, 26, 'used-90']],
             h=[t('180° мінус 64°.', '180° minus 64°.'), '180° − 64° = ?'], ok='116°')],
        after=t('Обидва суміжні кути по 116°.', 'Both partners are 116°.'), label=t('Рівні кути → рівні суміжні (116°)', 'Equal angles → equal partners (116°)')))
    for i, a in enumerate(A):
        a['label'] = t(f'Справа {i + 1}: ', f'Case {i + 1}: ') + a['label']
        for s in a['steps']:
            s.setdefault('traps', [])

    # ---- level B: rays, bisectors and several angles (teacher's problems)
    Bt = []
    # b0 Problem 1: bisector, 130
    def b0pic(k):
        arcs = [(50, 180, '130°', 'y', 62, False)]
        if k >= 1:
            arcs.append((0, 50, '50°', 'p', 40, False))
        else:
            arcs.append((0, 50, '?', 'h', 40, True))
        if k >= 2:
            arcs.append((0, 100, '100°', 's', 92, False))
        return fig([(0, 'C'), (180, 'M'), (100, 'A'), (50, 'O')], arcs, vlabel='B', h=196, label='∠MBO = 130°', cls='stg', R=118)
    Bt.append(dict(teacher=True, q=t('Бісектриса BO кута ABC утворює з променем BM, доповняльним до BC, кут 130°. Знайди ∠ABC.',
                                     'Bisector BO of ∠ABC makes an angle of 130° with ray BM, the ray opposite BC. Find ∠ABC.'),
                   pics=[b0pic(0), b0pic(1), b0pic(2)], steps=[
        dict(type='num', p=t('Спершу ∠OBC:', 'First ∠OBC:'), f=[ang('∠OBC', 50)], traps=[[0, 130, 'copied-angle']],
             h=[t('∠MBO і ∠OBC — суміжні.', '∠MBO and ∠OBC are adjacent.'), '180° − 130° = ?'], ok='∠OBC = 50°'),
        dict(type='num', p=t('Тепер ∠ABC:', 'Now ∠ABC:'), f=[ang('∠ABC', 100)], traps=[[0, 25, 'bisector-halved'], [0, 50, 'bisector-same']],
             h=[t('BO — бісектриса: вона ділить ∠ABC навпіл.', 'BO is the bisector: it splits ∠ABC in half.'), '2 · 50° = ?'], ok='∠ABC = 100°')],
        after=t('∠ABC = 2 · 50° = 100°.', '∠ABC = 2 × 50° = 100°.'), label=t('Задача 1 (бісектриса, 130°): 100°', 'Problem 1 (bisector, 130°): 100°')))
    # b1 Problem 2: rays b, c inside straight angle (ad)
    def b1pic(k):
        arcs = [(20, 180, '', 'y', 30, False), (0, 140, '', 's', 104, False)]
        lab = ''
        known = [(0, 20, '20°' if k >= 1 else '?', 'p', 64, k < 1), (140, 180, '40°' if k >= 2 else '?', 'l', 64, k < 2),
                 (20, 140, '120°' if k >= 3 else '?', 'h', 50, k < 3)]
        extra = text(250, 182, '∠(ac) = 160°', 16, 'y', 'd', 'middle') + text(90, 182, '∠(bd) = 140°', 16, 's', 'd', 'middle')
        return fig([(0, 'd'), (180, 'a'), (140, 'b'), (20, 'c')], [arcs[0], arcs[1]] + known, vlabel='', h=196, label='∠(ac) = 160°, ∠(bd) = 140°', cls='stg', extra=extra, R=118)
    Bt.append(dict(teacher=True, q=t('Промені b і c ділять розгорнутий кут (ad) на три кути. ∠(ac) = 160°, ∠(bd) = 140°. Знайди найбільший із трьох кутів.',
                                     'Rays b and c split the straight angle (ad) into three angles. ∠(ac) = 160°, ∠(bd) = 140°. Find the largest of the three.'),
                   pics=[b1pic(0), b1pic(1), b1pic(2), b1pic(3), b1pic(3)], steps=[
        dict(type='num', p=t('∠(ac) і ∠(cd) — суміжні. Знайди ∠(cd):', '∠(ac) and ∠(cd) are adjacent. Find ∠(cd):'), f=[ang('∠(cd)', 20)],
             h=[t('180° мінус ∠(ac).', '180° minus ∠(ac).'), '180° − 160° = ?'], ok='∠(cd) = 20°'),
        dict(type='num', p=t('∠(ab) і ∠(bd) — суміжні. Знайди ∠(ab):', '∠(ab) and ∠(bd) are adjacent. Find ∠(ab):'), f=[ang('∠(ab)', 40)],
             h=[t('180° мінус ∠(bd).', '180° minus ∠(bd).'), '180° − 140° = ?'], ok='∠(ab) = 40°'),
        dict(type='num', p=t('Тепер середній ∠(bc):', 'Now the middle one, ∠(bc):'), f=[ang('∠(bc)', 120)], traps=[[0, 140, 'whole-not-part']],
             h=[t('∠(bd) складається з ∠(bc) і ∠(cd).', '∠(bd) is made of ∠(bc) and ∠(cd).'), '140° − 20° = ?'], ok='∠(bc) = 120°'),
        dict(type='choice', style='pills', p=t('Який кут найбільший?', 'Which angle is the largest?'),
             opts=[['ab', '∠(ab)'], ['bc', '∠(bc)'], ['cd', '∠(cd)']], ans='bc', h=[t('порівняй 40°, 120° і 20°.', 'compare 40°, 120° and 20°.'), t('120° — найбільше.', '120° is the biggest.')],
             ok=t('Найбільший ∠(bc) = 120°', 'The largest is ∠(bc) = 120°'))],
        after=t('Перевірка: 40° + 120° + 20° = 180°.', 'Check: 40° + 120° + 20° = 180°.'), label=t('Задача 2 (промені b і c): 120°', 'Problem 2 (rays b and c): 120°')))
    # b2 homework 2: 72 and 37
    def b2pic(k):
        return fig([(0, 'D'), (180, 'A'), (108, 'B'), (37, 'C')],
                   [(108, 180, '72°', 'y', 56, False), (0, 37, '37°', 'p', 56, False), (37, 108, '71°' if k else '?', 'h', 40, not k)],
                   h=196, label='∠AOB = 72°, ∠COD = 37°', cls='stg', R=118)
    Bt.append(dict(teacher=True, q=t('Промені OB і OC лежать усередині розгорнутого кута AOD. ∠AOB = 72°, ∠COD = 37°. Знайди ∠BOC.',
                                     'Rays OB and OC lie inside the straight angle AOD. ∠AOB = 72°, ∠COD = 37°. Find ∠BOC.'),
                   pics=[b2pic(0), b2pic(1)], steps=[
        dict(type='num', p='', f=[ang('∠BOC', 71)], traps=[[0, 109, 'subtracted-one'], [0, 143, 'subtracted-one'], [0, 35, 'difference']],
             h=[t('три кути разом складають розгорнутий кут 180°.', 'the three angles together make the straight angle, 180°.'), '180° − 72° − 37° = ?'], ok='∠BOC = 71°')],
        after='72° + 71° + 37° = 180°.', label=t('Д/з №2: ∠BOC = 71°', 'Homework 2: ∠BOC = 71°')))
    # b3 homework 4: 112 and 138
    def b3pic(k):
        arcs = [(0, 112, '112°', 's', 104, False), (42, 180, '138°', 'y', 30, False),
                (0, 42, '42°' if k >= 1 else '?', 'p', 64, k < 1), (42, 112, '70°' if k >= 2 else '?', 'h', 64, k < 2)]
        return fig([(0, 'D'), (180, 'A'), (112, 'B'), (42, 'C')], arcs, h=196, label='∠BOD = 112°, ∠AOC = 138°', cls='stg', R=118)
    Bt.append(dict(teacher=True, q=t('A, O, D лежать на одній прямій. ∠BOD = 112°, ∠AOC = 138°. Знайди ∠BOC.',
                                     'A, O and D lie on one straight line. ∠BOD = 112°, ∠AOC = 138°. Find ∠BOC.'),
                   pics=[b3pic(0), b3pic(1), b3pic(2)], steps=[
        dict(type='num', p=t('∠AOC і ∠COD — суміжні. Знайди ∠COD:', '∠AOC and ∠COD are adjacent. Find ∠COD:'), f=[ang('∠COD', 42)],
             h=[t('180° мінус ∠AOC.', '180° minus ∠AOC.'), '180° − 138° = ?'], ok='∠COD = 42°'),
        dict(type='num', p=t('Тепер ∠BOC:', 'Now ∠BOC:'), f=[ang('∠BOC', 70)], traps=[[0, 154, 'added'], [0, 26, 'difference']],
             h=[t('∠BOD складається з ∠BOC і ∠COD.', '∠BOD is made of ∠BOC and ∠COD.'), '112° − 42° = ?'], ok='∠BOC = 70°')],
        after=t('Інший шлях: 112° + 138° − 180° = 70°.', 'Another way: 112° + 138° − 180° = 70°.'), label=t('Д/з №4: ∠BOC = 70°', 'Homework 4: ∠BOC = 70°')))
    # b4 homework 3: 165
    def b4pic(k):
        arcs = [(15, 180, '165°', 'y', 40, False), (345, 375, '', 'p', 70, False)]
        arcs.append((0, 15, '15°' if k >= 1 else '?', 'h', 92, k < 1))
        ex = ''
        if k >= 2:
            ex = text(250, 40, '∠AOB = 30°', 18, 's', 'd', 'middle')
        return fig([(0, 'L'), (180, 'L₁'), (15, 'A'), (-15, 'B')], arcs, vertex=(150, 100), h=200, R=118, label='165°', cls='stg', extra=ex)
    Bt.append(dict(teacher=True, q=t('Сторона OA кута AOB утворює з променем OL₁, доповняльним до бісектриси OL, кут 165°. Знайди ∠AOB.',
                                     'Side OA of ∠AOB makes an angle of 165° with ray OL₁, the ray opposite the bisector OL. Find ∠AOB.'),
                   pics=[b4pic(0), b4pic(1), b4pic(2)], steps=[
        dict(type='num', p=t('Кут між стороною OA і бісектрисою OL:', 'The angle between side OA and the bisector OL:'), f=[ang('∠AOL', 15)],
             h=[t('∠AOL₁ і ∠AOL — суміжні.', '∠AOL₁ and ∠AOL are adjacent.'), '180° − 165° = ?'], ok='∠AOL = 15°'),
        dict(type='num', p=t('Тепер увесь кут:', 'Now the whole angle:'), f=[ang('∠AOB', 30)], traps=[[0, 7.5, 'bisector-halved']],
             h=[t('бісектриса ділить кут навпіл, тож кут удвічі більший за половинку.', 'the bisector halves the angle, so the angle is twice the half.'), '2 · 15° = ?'], ok='∠AOB = 30°')],
        after=t('∠AOB = 2 · 15° = 30°.', '∠AOB = 2 × 15° = 30°.'), label=t('Д/з №3 (165°): 30°', 'Homework 3 (165°): 30°')))
    # b5 homework 5: equation
    def b5pic(k):
        arcs = [(0, 60, '', 'p', 46, False), (60, 120, '', 'p', 58, False)]
        if k:
            arcs = [(0, 60, '60°', 'p', 46, False), (60, 120, '60°', 'p', 58, False), (120, 180, '60°', 'y', 46, False)]
        else:
            arcs.append((120, 180, '', 'y', 46, False))
        return fig([(0, 'A'), (180, 'A₁'), (120, 'B'), (60, 'L')], arcs, h=196, label='бісектриса і суміжний кут', cls='stg', R=118)
    Bt.append(dict(teacher=True, q=t('Бісектриса кута утворює з його стороною кут, що дорівнює куту, суміжному з даним. Знайди даний кут.',
                                     'The bisector of an angle makes an angle with one side that equals the angle’s partner (the adjacent angle). Find the angle.'),
                   pics=[b5pic(0), b5pic(1)], steps=[
        dict(type='num', p=t('Познач даний кут x. Знайди x:', 'Call the angle x. Find x:'), f=[{'pre': 'x =', 'post': '°', 'ans': 120, 'n': 'angle', 'aria': 'x'}],
             traps=[[0, 90, 'guess-90'], [0, 60, 'half-not-whole']],
             h=[t('половинка кута — x : 2, суміжний кут — 180° − x. Вони рівні.', 'half the angle is x ÷ 2; the partner is 180° − x. They are equal.'),
                t('x : 2 = 180° − x, тобто x + x : 2 = 180°: півтора x — це 180°.', 'x ÷ 2 = 180° − x, so x + x ÷ 2 = 180°: one and a half x make 180°.')], ok='x = 120°')],
        after=t('Перевірка: половинка 60°, суміжний 180° − 120° = 60°. Рівні!', 'Check: half is 60°, the partner is 180° − 120° = 60°. Equal!'), label=t('Д/з №5 (рівняння): 120°', 'Homework 5 (equation): 120°')))
    # b6 ours: bisector of 70, opposite ray
    def b6pic(k):
        arcs = [(0, 35, '35°' if k >= 1 else '?', 'p', 70, k < 1), (35, 70, '', 'p', 56, False), (35, 180, '145°' if k >= 2 else '?', 'h', 40, k < 2)]
        return fig([(0, 'A'), (180, 'M'), (70, 'B'), (35, 'K')], arcs, h=196, R=118, label='∠AOB = 70°', cls='stg',
                   extra=text(262, 44, '∠AOB = 70°', 17, 's', 'd', 'middle'))
    Bt.append(dict(teacher=False, q=t('∠AOB = 70°, OK — його бісектриса, OM — промінь, доповняльний до OA. Знайди ∠MOK.',
                                      '∠AOB = 70°, OK is its bisector and OM is the ray opposite OA. Find ∠MOK.'),
                   pics=[b6pic(0), b6pic(1), b6pic(2)], steps=[
        dict(type='num', p=t('Спершу ∠AOK:', 'First ∠AOK:'), f=[ang('∠AOK', 35)], traps=[[0, 70, 'bisector-same']],
             h=[t('бісектриса ділить кут навпіл.', 'the bisector splits the angle in half.'), '70° : 2 = ?'], ok='∠AOK = 35°'),
        dict(type='num', p=t('Тепер ∠MOK:', 'Now ∠MOK:'), f=[ang('∠MOK', 145)], traps=[[0, 110, 'used-whole-angle']],
             h=[t('∠AOK і ∠KOM — суміжні.', '∠AOK and ∠KOM are adjacent.'), '180° − 35° = ?'], ok='∠MOK = 145°')],
        after='35° + 145° = 180°.', label=t('Бісектриса кута 70°: ∠MOK = 145°', 'Bisector of 70°: ∠MOK = 145°')))
    for i, b in enumerate(Bt):
        b['label'] = t(f'Креслення {i + 1}: ', f'Drawing {i + 1}: ') + b['label']
        for s in b['steps']:
            s.setdefault('traps', [])

    # ---- level C: ratios and differences (bar model)
    pt_ = t('ч.', 'p.')
    Ct = []

    def two_angles(a, b_, la='', lb=''):
        return fig([(0, ''), (180, ''), (b_, '')], [(0, b_, f'{b_}°', 'p', 40, False), (b_, 180, f'{a}°', 'y', 52, False)], vlabel='', h=170, R=110, label=f'{a}°, {b_}°', cls='stg', vertex=(160, 140))
    # c0 homework 1a: one is 3 times the other
    Ct.append(dict(teacher=True, q=t('Знайди суміжні кути, якщо один із них утричі більший за другий.', 'Find two adjacent angles if one is three times the other.'),
                   pics=[bar([('', [(1, Pp, 'x'), (3, Y, '3x')])], total='180°', cls='stg', label='x + 3x = 180°'),
                         bar([('', [(1, Pp, '45°'), (3, Y, '135°')])], total='180°', cls='stg', label='45°, 135°'), two_angles(135, 45)], steps=[
        dict(type='num', p=t('Менший кут — x, більший — 3x. Знайди x:', 'The smaller angle is x and the bigger is 3x. Find x:'), f=[{'pre': 'x =', 'post': '°', 'ans': 45, 'n': 'part'}],
             traps=[[0, 60, 'divided-by-3'], [0, 90, 'divided-by-2']],
             h=[t('x + 3x = 4x, а разом суміжні кути — 180°.', 'x + 3x = 4x, and adjacent angles make 180° together.'), '180° : 4 = ?'], ok='x = 45°'),
        dict(type='num', p=t('Більший кут:', 'The bigger angle:'), f=[{'pre': '3x =', 'post': '°', 'ans': 135, 'n': 'angle'}],
             h=[t('помнож x на 3.', 'multiply x by 3.'), '3 · 45° = ?'], ok='3x = 135°')],
        after=t('45° і 135°. Перевірка: 45° + 135° = 180°.', '45° and 135°. Check: 45° + 135° = 180°.'), label=t('Д/з №1а (утричі більший): 45° і 135°', 'Homework 1a (three times): 45° and 135°')))
    # c1 homework 1b: 20 less
    Ct.append(dict(teacher=True, q=t('Знайди суміжні кути, якщо один із них на 20° менший за другий.', 'Find two adjacent angles if one is 20° smaller than the other.'),
                   pics=[bar([('x', [(4, Pp, '')]), ('x + 20°', [(4, Y, ''), (1, H, '20°')])], cls='stg', label='x + x + 20° = 180°'),
                         bar([('80°', [(4, Pp, '')]), ('100°', [(4, Y, ''), (1, H, '20°')])], cls='stg', label='80°, 100°'), two_angles(100, 80)], steps=[
        dict(type='num', p=t('Менший кут — x, більший — x + 20°. Знайди менший:', 'The smaller angle is x and the bigger is x + 20°. Find the smaller:'), f=[{'pre': 'x =', 'post': '°', 'ans': 80, 'n': 'part'}],
             traps=[[0, 90, 'ignored-difference'], [0, 100, 'bigger-not-smaller'], [0, 160, 'not-halved']],
             h=[t('x + (x + 20°) = 180°, тобто 2x = 160°.', 'x + (x + 20°) = 180°, so 2x = 160°.'), '160° : 2 = ?'], ok='x = 80°'),
        dict(type='num', p=t('Більший кут:', 'The bigger angle:'), f=[{'pre': 'x + 20° =', 'post': '°', 'ans': 100, 'n': 'angle'}],
             h=[t('додай 20°.', 'add 20°.'), '80° + 20° = ?'], ok='100°')],
        after=t('80° і 100°. Перевірка: 80° + 100° = 180°, 100° − 80° = 20°.', '80° and 100°. Check: 80° + 100° = 180°, 100° − 80° = 20°.'), label=t('Д/з №1б (на 20° менший): 80° і 100°', 'Homework 1b (20° smaller): 80° and 100°')))
    # c2 Problem 3: (ABC − CBD) : CBD = 5 : 2
    Ct.append(dict(teacher=True, q=t('Різниця двох суміжних кутів відноситься до меншого з них як 5 : 2. Знайди ці кути.',
                                     'The difference between two adjacent angles is to the smaller one as 5 : 2. Find the angles.'),
                   pics=[bar([('∠CBD', [(2, Pp, '2 ' + pt_)]), ('∠ABC', [(2, Pp, '2 ' + pt_), (5, H, t('5 ч. різниця', '5 p. diff.'))])], cls='stg', label='2 + 7 = 9 частин'),
                         bar([('∠CBD', [(2, Pp, '2 ' + pt_)]), ('∠ABC', [(2, Pp, '2 ' + pt_), (5, H, t('5 ч. різниця', '5 p. diff.'))])], cls='stg', label='',
                             note=t('2 + 7 = 9 частин = 180°', '2 + 7 = 9 parts = 180°')),
                         bar([('∠CBD', [(2, Pp, '40°')]), ('∠ABC', [(7, Y, '140°')])], cls='stg', label='40°, 140°'), two_angles(140, 40)], steps=[
        dict(type='num', p=t('Менший кут — 2 частини, різниця — 5 частин. Скільки частин у більшому куті?', 'The smaller angle is 2 parts and the difference is 5 parts. How many parts are in the bigger angle?'),
             f=[{'pre': '∠ABC =', 'post': ' ' + pt_, 'ans': 7, 'n': 'parts'}], traps=[[0, 5, 'difference-as-angle']],
             h=[t('більший кут = менший + різниця.', 'bigger angle = smaller + difference.'), '2 + 5 = ?'], ok=t('∠ABC — 7 частин', '∠ABC is 7 parts')),
        dict(type='num', p=t('Разом 2 + 7 = 9 частин = 180°. Одна частина:', 'Together 2 + 7 = 9 parts = 180°. One part:'), f=[{'pre': t('1 ч. =', '1 p. ='), 'post': '°', 'ans': 20, 'n': 'part'}],
             traps=[[0, 25.71428571428571, 'used-7-parts']], h=[t('поділи 180° на 9.', 'divide 180° by 9.'), '180° : 9 = ?'], ok=t('1 частина = 20°', '1 part = 20°')),
        dict(type='num', p=t('Тепер кути:', 'Now the angles:'), f=[ang('∠CBD', 40), dict(ang('∠ABC', 140), pre='<span class="gap"></span>∠ABC =')],
             h=[t('менший — 2 частини, більший — 7 частин.', 'the smaller is 2 parts and the bigger is 7 parts.'), '2 · 20° = ?; 7 · 20° = ?'], ok='40° ' + t('і', 'and') + ' 140°')],
        after=t('Перевірка: 140° − 40° = 100°, і 100 : 40 = 5 : 2.', 'Check: 140° − 40° = 100°, and 100 : 40 = 5 : 2.'), label=t('Задача 3 (5 : 2): 40° і 140°', 'Problem 3 (5 : 2): 40° and 140°')))
    # c3 №103: M : N = 2 : 5, adjacent to one is 140
    Ct.append(dict(teacher=True, q=t('Гострий кут M і тупий кут N відносяться як 2 : 5. Кут, суміжний з одним із них, дорівнює 140°. Знайди ∠M і ∠N.',
                                     'Acute angle M and obtuse angle N are in the ratio 2 : 5. The partner of one of them is 140°. Find ∠M and ∠N.'),
                   pics=[two_angles(140, 40), bar([('∠M', [(2, Pp, '40°')]), ('∠N', [(5, 'cell', '5 ' + pt_)])], cls='stg', label='∠M = 40°'),
                         bar([('∠M', [(2, Pp, '40°')]), ('∠N', [(5, 'cell', '5 ' + pt_)])], cls='stg', label='x = 20°', note=t('2 частини = 40°', '2 parts = 40°')),
                         bar([('∠M', [(2, Pp, '40°')]), ('∠N', [(5, Y, '100°')])], cls='stg', label='∠N = 100°')], steps=[
        dict(type='num', p=t('Суміжний 140° — тупий. Отже, він суміжний із гострим кутом M. Знайди ∠M:', 'The partner 140° is obtuse, so it belongs to the acute angle M. Find ∠M:'),
             f=[ang('∠M', 40)], traps=[[0, 140, 'copied-angle']], h=[t('∠M і кут 140° — суміжні.', '∠M and the 140° angle are adjacent.'), '180° − 140° = ?'], ok='∠M = 40°'),
        dict(type='num', p=t('∠M — 2 частини. Одна частина x:', '∠M is 2 parts. One part x:'), f=[{'pre': 'x =', 'post': '°', 'ans': 20, 'n': 'part'}],
             h=[t('2x = 40°.', '2x = 40°.'), '40° : 2 = ?'], ok='x = 20°'),
        dict(type='num', p=t('∠N — 5 частин:', '∠N is 5 parts:'), f=[ang('∠N', 100)], traps=[[0, 140, 'added-not-multiplied']], h=[t('5x.', '5x.'), '5 · 20° = ?'], ok='∠N = 100°')],
        after=t('∠M = 40°, ∠N = 100°. Перевірка: 40 : 100 = 2 : 5.', '∠M = 40°, ∠N = 100°. Check: 40 : 100 = 2 : 5.'), label=t('№103 (2 : 5, 140°): 40° і 100°', 'No. 103 (2 : 5, 140°): 40° and 100°')))
    # c4 №106: A : B = 1 : 2, partners 7 : 5
    Ct.append(dict(teacher=True, q=t('Два кути відносяться як 1 : 2, а суміжні з ними — як 7 : 5. Знайди ці кути.',
                                     'Two angles are in the ratio 1 : 2, and their partners are in the ratio 7 : 5. Find the two angles.'),
                   pics=[bar([('∠A', [(1, Pp, 'x')]), ('∠B', [(2, Y, '2x')])], cls='stg', label='∠A = x, ∠B = 2x', note=t('∠C = 180° − x, ∠D = 180° − 2x', '∠C = 180° − x, ∠D = 180° − 2x')),
                         bar([('∠A', [(1, Pp, '40°')]), ('∠B', [(2, Y, '80°')])], cls='stg', label='40°, 80°'),
                         bar([('∠A', [(1, Pp, '40°')]), ('∠B', [(2, Y, '80°')])], cls='stg', label='40°, 80°', note=t('∠C = 140°, ∠D = 100°: 7 : 5 ✓', '∠C = 140°, ∠D = 100°: 7 : 5 ✓'))], steps=[
        dict(type='num', p=t('5(180° − x) = 7(180° − 2x). Знайди x = ∠A:', '5(180° − x) = 7(180° − 2x). Find x = ∠A:'), f=[{'pre': 'x =', 'post': '°', 'ans': 40, 'n': 'part'}],
             h=[t('розкрий дужки: 900° − 5x = 1260° − 14x. Перенеси x ліворуч, числа праворуч.', 'expand the brackets: 900° − 5x = 1260° − 14x. Move the x terms left and the numbers right.'),
                '14x − 5x = 1260° − 900° → 9x = 360°'], ok='x = 40°'),
        dict(type='num', p=t('Тоді ∠B = 2x:', 'Then ∠B = 2x:'), f=[ang('∠B', 80)], h=[t('удвічі більший за ∠A.', 'twice ∠A.'), '2 · 40° = ?'], ok='∠B = 80°')],
        after=t('Перевірка: суміжні 140° і 100°, а 140 : 100 = 7 : 5.', 'Check: the partners are 140° and 100°, and 140 : 100 = 7 : 5.'), label=t('№106 (1 : 2 і 7 : 5): 40° і 80°', 'No. 106 (1 : 2 and 7 : 5): 40° and 80°')))
    # ours
    for a, b_, k in ((4, 11, 12), (1, 5, 30)):
        Ct.append(dict(teacher=False, q=t(f'Суміжні кути відносяться як {a} : {b_}. Знайди їх.', f'Two adjacent angles are in the ratio {a} : {b_}. Find them.'),
                       pics=[bar([('', [(a, Pp, f'{a} ' + pt_), (b_, Y, f'{b_} ' + pt_)])], total='180°', cls='stg', label=f'{a} : {b_}'),
                             bar([('', [(a, Pp, f'{a * k}°'), (b_, Y, f'{b_ * k}°')])], total='180°', cls='stg', label=f'{a * k}°, {b_ * k}°'),
                             two_angles(b_ * k, a * k)], steps=[
            dict(type='num', p=t(f'Скільки градусів в одній частині?', 'How many degrees are in one part?'), f=[{'pre': t('1 ч. =', '1 p. ='), 'post': '°', 'ans': k, 'n': 'part'}],
                 traps=[[0, 180 / b_, 'divided-by-one-part'], [0, 180 / a, 'divided-by-one-part']],
                 h=[t('спершу порахуй усі частини разом.', 'first count all the parts together.'), f'{a} + {b_} = {a + b_}; 180° : {a + b_} = ?'], ok=t(f'1 частина = {k}°', f'1 part = {k}°')),
            dict(type='num', p=t('Тепер кути:', 'Now the angles:'), f=[{'pre': t('менший =', 'smaller ='), 'post': '°', 'ans': a * k, 'n': 'small'},
                                                                 {'pre': '<span class="gap"></span>' + t('більший =', 'bigger ='), 'post': '°', 'ans': b_ * k, 'n': 'big'}],
                 h=[t('помнож кількість частин на градуси в одній частині.', 'multiply the number of parts by the degrees in one part.'), f'{a} · {k}° = ?; {b_} · {k}° = ?'],
                 ok=f'{a * k}° ' + t('і', 'and') + f' {b_ * k}°')],
            after=t(f'Перевірка: {a * k}° + {b_ * k}° = 180°.', f'Check: {a * k}° + {b_ * k}° = 180°.'), label=f'{a} : {b_} → {a * k}° ' + t('і', 'and') + f' {b_ * k}°'))
    Ct.insert(6, dict(teacher=False, q=t('Один із суміжних кутів на 50° більший за другий. Знайди їх.', 'One of two adjacent angles is 50° bigger than the other. Find them.'),
                      pics=[bar([('x', [(5, Pp, '')]), ('x + 50°', [(5, Y, ''), (2, H, '50°')])], cls='stg', label='x + x + 50° = 180°'),
                            bar([('65°', [(5, Pp, '')]), ('115°', [(5, Y, ''), (2, H, '50°')])], cls='stg', label='65°, 115°'), two_angles(115, 65)], steps=[
        dict(type='num', p=t('Менший кут x:', 'The smaller angle x:'), f=[{'pre': 'x =', 'post': '°', 'ans': 65, 'n': 'part'}], traps=[[0, 90, 'ignored-difference'], [0, 130, 'not-halved']],
             h=[t('x + (x + 50°) = 180°, тобто 2x = 130°.', 'x + (x + 50°) = 180°, so 2x = 130°.'), '130° : 2 = ?'], ok='x = 65°'),
        dict(type='num', p=t('Більший кут:', 'The bigger angle:'), f=[{'pre': 'x + 50° =', 'post': '°', 'ans': 115, 'n': 'angle'}], h=[t('додай 50°.', 'add 50°.'), '65° + 50° = ?'], ok='115°')],
        after=t('65° і 115°. Перевірка: 115° − 65° = 50°.', '65° and 115°. Check: 115° − 65° = 50°.'), label=t('На 50° більший: 65° і 115°', '50° bigger: 65° and 115°')))
    for i, c in enumerate(Ct):
        c['label'] = t(f'Задача {i + 1}: ', f'Problem {i + 1}: ') + c['label']
        for s in c['steps']:
            s.setdefault('traps', [])
    # en: decimal points / multiplication sign in hints and prompts
    if lang == 'en':
        for L in (A, Bt, Ct):
            for task in L:
                for s in task['steps']:
                    s['h'] = [h.replace(' · ', ' × ').replace(' : ', ' ÷ ') if (' · ' in h or ('° : ' in h)) else h for h in s['h']]
    return {'a': {'tasks': A}, 'b': {'tasks': Bt}, 'c': {'tasks': Ct}}


STAGE_JS = r"""
function picOf(c){const t=c.t;if(!t||!t.pics)return '';const k=c.solved?t.pics.length-1:Math.min(c.sub,t.pics.length-1);return t.pics[k]}
function stageA(c){
  if(c.finished&&!c.solved)return `<div class="say">${c.SVGR('hostA')}<p class="bubble">${c.S.aQuip}</p></div>`;
  return `${picOf(c)}<div class="say">${c.SVGR('messy')}<p class="hand">${c.S.aStageL}</p></div><p class="count">${c.S.count(c.i,c.n)}</p>`;
}
function stageB(c){
  if(c.finished&&!c.solved)return `<div class="say">${c.SVGR('tidy')}<p class="bubble">${c.S.bQuip}</p></div>`;
  return `${picOf(c)}<div class="say">${c.SVGR('tidy')}<p class="hand">${c.S.bStageL}</p></div><p class="count">${c.S.count(c.i,c.n)}</p>`;
}
function stageC(c){
  if(c.finished&&!c.solved)return `<div class="say">${c.SVGR('hostB')}<p class="bubble">${c.S.cQuip}</p></div>`;
  return `${picOf(c)}<div class="say">${c.SVGR('hostB')}<p class="hand">${c.S.cStageL}</p></div><p class="count">${c.S.count(c.i,c.n)}</p>`;
}
const STAGE={a:stageA,b:stageB,c:stageC};
/* the drawing follows the solution: after a right answer show the next picture */
"""

EXTRA_CSS = """
.stage .stg{max-width:340px}
"""


def texts(lang, edition):
    t = lambda uk, en: uk if lang == 'uk' else en
    home = edition == 'home'
    common = dict(
        h1={'meadow': t('Суміжні кути <span>на лузі</span>', 'Adjacent angles <span>in the meadow</span>'),
            'space': t('Суміжні кути <span>у космосі</span>', 'Adjacent angles <span>in space</span>'),
            'bricks': t('Суміжні кути <span>з цеглинок</span>', 'Adjacent angles <span>made of bricks</span>')},
        lH=t('Урок: суміжні кути', 'Lesson: adjacent angles'),
        lIntro=t('Дев’ять карток за уроком 6. Роздивляйся кольорові дуги: однаковий колір — один і той самий кут.',
                 'Nine cards based on lesson 6. Look at the coloured arcs: the same colour means the same angle.'),
        lBye=t('{hostA} каже: знайшов кут — перевір! Суміжні кути разом мають дати рівно 180°.', '{hostA} says: found an angle? Check it! Two adjacent angles must add up to exactly 180°.'),
        toA=t('До першого рівня', 'Go to level 1'),
        dipH=t('Диплом {me:знавця:знавчині:знавця} кутів', 'Angle Expert Certificate'),
        teacherTag=t('з уроку Ігоря Петровича', 'from Mr Pasika’s lesson') if home else t('з уроку 6', 'from lesson 6'),
        rIntro=(t('Тут видно, що {me:ти вже пройшов:ти вже пройшла:вже пройдено}. Натисни кнопку, скопіюй звіт і надішли татові.',
                  'Here’s everything you’ve done so far. Copy the report and send it to Dad.') if home else
                t('Тут видно, що {me:ти вже пройшов:ти вже пройшла:вже пройдено}. Натисни «Надіслати звіт» і вибери Viber, Telegram чи пошту. Або скопіюй звіт і встав у повідомлення вчителеві чи батькам.',
                  'Here’s everything you’ve done so far. Tap "Send my report" and choose WhatsApp, Viber or email. Or copy the report and paste it into a message to your teacher or parents.')),
        copied=t('Скопійовано! Встав звіт у повідомлення.', 'Copied! Paste it into a message.'),
        repHead=(t('Тату, ось мій звіт про суміжні кути.', 'Hi Dad, here is my adjacent angles report.') if home else t('Ось мій звіт про суміжні кути.', 'Here is my adjacent angles report.')),
    )
    W = {}
    W['meadow'] = dict(
        intro=t('{tidy} креслить план нового будиночка для морських свинок, а {messy} весь час питає: «А цей кут скільки?» Прочитай урок і пройди три рівні: розпізнай суміжні кути, добудуй креслення й поділи пряжу між двома кольорами.',
                '{tidy} is drawing a plan for a new guinea pig house, and {messy} keeps asking: "How big is this angle?" Read the lesson, then play three levels: spot adjacent angles, finish the drawings and share out the yarn between two colours.'),
        tabA=t('1. Хто сусіди', '1. Who are partners'), tabB=t('2. Креслення', '2. Drawings'), tabC=t('3. Пряжа', '3. Yarn'),
        aH=t('Рівень 1. Хто тут сусіди?', 'Level 1. Who are the partners?'),
        aIntro=t('Дивись на малюнок: чи суміжні кути, і скільки градусів у сусіда.', 'Look at the picture: are the angles adjacent, and how big is the partner?'),
        bH=t('Рівень 2. Креслення будиночка', 'Level 2. Drawing the house'),
        bIntro=t('Задачі з уроку: промені, бісектриси й кілька кутів одразу. Кожна правильна відповідь з’являється на кресленні.',
                 'Problems from the lesson: rays, bisectors and several angles at once. Every right answer appears on the drawing.'),
        cH=t('Рівень 3. Пряжа на 180 петель', 'Level 3. Yarn for 180 stitches'),
        cIntro=t('Розгорнутий кут — як ряд на 180 петель, який треба поділити між двома кольорами. Смужка покаже частини.',
                 'A straight angle is like a row of 180 stitches shared between two colours. The strip shows the parts.'),
        aGood=t('Так!', 'Yes!'), bGood=t('Креслення доповнено!', 'The drawing is complete!'), cGood=t('Петлі поділено!', 'The stitches are shared out!'),
        aStageL=t('{messy} уважно дивиться', '{messy} is watching closely'), bStageL=t('Креслимо разом', 'Drawing together'), cStageL=t('Ділимо 180 петель', 'Sharing out 180 stitches'),
        aQuip=t('Усі сусіди знайдені!', 'All the partners are found!'), bQuip=t('Креслення готове — можна будувати!', 'The plan is ready: time to build!'), cQuip=t('Шарф буде двоколірний!', 'The scarf will have two colours!'),
        aDoneH=t('Сусідів знайдено!', 'All partners found!'),
        aDoneP=t('{messy} тепер сам {g:messy:показує:показує} суміжні кути на всіх парканах. Перша зірка твоя!', '{messy} now points out adjacent angles on every fence. Your first star!'),
        bDoneH=t('Креслення готове!', 'The plan is finished!'),
        bDoneP=t('{tidy} {g:tidy:поправив:поправила} окуляри: усе пораховано до градуса. Друга зірка твоя!', '{tidy} straightened her glasses: every angle is worked out to the degree. Your second star!'),
        cDoneH=t('Пряжу поділено!', 'The yarn is shared out!'),
        cDoneP=t('З такими частинами вийде гарний смугастий шарф. Третя зірка твоя!', 'With these parts you can knit a lovely stripy scarf. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі власноруч зв’язаний транспортир, а {messy} — моркву.', 'All three levels complete! {tidy} gives you a hand-knitted protractor, and {messy} gives you a carrot.'),
        meet=[['hostA', t('Руда пляма, любить моркву і пояснювати.', 'Ginger patch. Loves carrots and explaining things.')],
              ['hostB', t('Темна пляма, придумує підказки-віршики.', 'Dark patch. Makes up rhymes to help you remember.')],
              ['tidy', t('Їжачиха-охайниця. Креслить план будиночка.', 'A very tidy hedgehog. Drawing a plan for the house.')],
              ['messy', t('Єнот. Усе змішує, але хоче навчитись міряти кути.', 'A raccoon. Mixes things up, but wants to learn to measure angles.')]],
    )
    W['space'] = dict(
        intro=t('{tidy} прокладає курс корабля, а прибулець {messy} крутить антену радара туди-сюди. Прочитай урок і пройди три рівні: впізнай суміжні кути на радарі, проклади курс і поділи паливо між двома баками.',
                '{tidy} is plotting the ship’s course, and {messy} the alien keeps spinning the radar dish. Read the lesson, then play three levels: spot adjacent angles on the radar, plot the course and share the fuel between two tanks.'),
        tabA=t('1. Радар', '1. Radar'), tabB=t('2. Курс', '2. Course'), tabC=t('3. Паливо', '3. Fuel'),
        aH=t('Рівень 1. Радар', 'Level 1. The radar'), aIntro=t('Дивись на екран радара: чи суміжні кути, і скільки градусів у сусіда.', 'Look at the radar screen: are the angles adjacent, and how big is the partner?'),
        bH=t('Рівень 2. Прокладаємо курс', 'Level 2. Plotting the course'),
        bIntro=t('Задачі з уроку: промені, бісектриси й кілька кутів одразу. Кожна правильна відповідь з’являється на карті.', 'Problems from the lesson: rays, bisectors and several angles at once. Every right answer appears on the map.'),
        cH=t('Рівень 3. Паливо на 180 одиниць', 'Level 3. 180 units of fuel'),
        cIntro=t('Розгорнутий кут — як 180 одиниць палива для двох баків. Смужка покаже, скільки в кожному.', 'A straight angle is like 180 units of fuel for two tanks. The strip shows how much goes in each.'),
        aGood=t('Так!', 'Yes!'), bGood=t('Курс уточнено!', 'Course corrected!'), cGood=t('Баки заправлено!', 'The tanks are filled!'),
        aStageL=t('{messy} крутить антену', '{messy} is spinning the dish'), bStageL=t('Прокладаємо курс', 'Plotting the course'), cStageL=t('Ділимо паливо', 'Sharing out the fuel'),
        aQuip=t('Радар бачить усіх сусідів!', 'The radar sees every partner!'), bQuip=t('Курс прокладено. Летимо!', 'Course plotted. Let’s fly!'), cQuip=t('Обидва баки повні!', 'Both tanks are full!'),
        aDoneH=t('Радар налаштовано!', 'The radar is tuned!'), aDoneP=t('{messy} {g:messy:навчився:навчилася} бачити суміжні кути з першого погляду. Перша зірка твоя!', '{messy} can now spot adjacent angles at a glance. Your first star!'),
        bDoneH=t('Курс готовий!', 'The course is ready!'), bDoneP=t('{tidy} задоволено пискнув: жодного зайвого градуса. Друга зірка твоя!', '{tidy} beeped happily: not a single degree out. Your second star!'),
        cDoneH=t('Баки заправлено!', 'The tanks are filled!'), cDoneP=t('Паливо поділено точно. Ракета готова до старту. Третя зірка твоя!', 'The fuel is shared exactly. The rocket is ready for launch. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі значок «Штурман кутів», а {messy} обіцяє більше не крутити радар без потреби.', 'All three levels complete! {tidy} gives you an "Angle Navigator" badge, and {messy} promises not to spin the radar for no reason.'),
        meet=[['hostA', t('Керує станцією і пояснює уроки.', 'Runs the station and explains the lessons.')], ['hostB', t('Водить ракету й придумує віршики.', 'Flies the rocket and makes up rhymes.')],
              ['tidy', t('Робот. Прокладає курс до градуса.', 'A robot. Plots the course to the degree.')], ['messy', t('Прибулець. Любить крутити антену радара.', 'An alien. Loves spinning the radar dish.')]],
    )
    W['bricks'] = dict(
        intro=t('{tidy} креслить міст, а песик {messy} перевіряє кожну балку носом. Прочитай урок і пройди три рівні: перевір кути, добудуй креслення мосту й поділи балку на дві частини.',
                '{tidy} is drawing a bridge, and {messy} the puppy checks every beam with his nose. Read the lesson, then play three levels: check the angles, finish the bridge drawings and split a beam into two parts.'),
        tabA=t('1. Перевірка', '1. Inspection'), tabB=t('2. Креслення', '2. Drawings'), tabC=t('3. Балка', '3. Beam'),
        aH=t('Рівень 1. Перевірка кутів', 'Level 1. Angle inspection'), aIntro=t('Дивись на креслення: чи суміжні кути, і скільки градусів у сусіда.', 'Look at the drawing: are the angles adjacent, and how big is the partner?'),
        bH=t('Рівень 2. Креслення мосту', 'Level 2. The bridge drawings'),
        bIntro=t('Задачі з уроку: промені, бісектриси й кілька кутів одразу. Кожна правильна відповідь з’являється на кресленні.', 'Problems from the lesson: rays, bisectors and several angles at once. Every right answer appears on the drawing.'),
        cH=t('Рівень 3. Балка на 180 сантиметрів', 'Level 3. A beam 180 centimetres long'),
        cIntro=t('Розгорнутий кут — як балка завдовжки 180, яку ріжуть на дві частини. Смужка покаже частини.', 'A straight angle is like a 180-long beam cut into two pieces. The strip shows the parts.'),
        aGood=t('Так!', 'Yes!'), bGood=t('Креслення доповнено!', 'The drawing is complete!'), cGood=t('Балку розпиляно!', 'The beam is cut!'),
        aStageL=t('{messy} обнюхує креслення', '{messy} is sniffing the drawing'), bStageL=t('Креслимо міст', 'Drawing the bridge'), cStageL=t('Ріжемо балку', 'Cutting the beam'),
        aQuip=t('Усі кути перевірено!', 'Every angle is checked!'), bQuip=t('Міст можна будувати!', 'The bridge can be built!'), cQuip=t('Частини точно по мірці!', 'The pieces fit exactly!'),
        aDoneH=t('Перевірку пройдено!', 'Inspection passed!'), aDoneP=t('{messy} радісно {g:messy:гавкнув:гавкнула}: жодної помилки. Перша зірка твоя!', '{messy} barked happily: not a single mistake. Your first star!'),
        bDoneH=t('Креслення готове!', 'The drawings are finished!'), bDoneP=t('{tidy} {g:tidy:поміряв:поміряла} кожен кут і {g:tidy:кивнув:кивнула}. Друга зірка твоя!', '{tidy} measured every angle and nodded. Your second star!'),
        cDoneH=t('Балки готові!', 'The beams are ready!'), cDoneP=t('Усі частини точно по мірці. Третя зірка твоя!', 'Every piece is cut to size. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі медаль «Знавець кутів», а {messy} приносить найкращу кісточку.', 'All three levels complete! {tidy} gives you an "Angle Expert" medal, and {messy} brings you the best bone.'),
        meet=[['hostA', t('Будує мости й пояснює уроки.', 'Builds bridges and explains the lessons.')], ['hostB', t('Будує вежі й придумує віршики.', 'Builds towers and makes up rhymes.')],
              ['tidy', t('Робот-інженерка. Креслить міст.', 'A robot engineer. Drawing a bridge.')], ['messy', t('Песик. Перевіряє все носом.', 'A puppy. Checks everything with his nose.')]],
    )
    common['worlds'] = W
    return common


def rights():
    return [
        (14, 'Земля є основним національним багатством, що перебуває під особливою охороною держави.',
         'Межі земельних ділянок на мапах креслять кутами й відрізками.',
         'Land is the country’s main national treasure and is under the special protection of the state.', 'The borders of plots of land are drawn on maps with angles and lines.'),
        (33, 'Кожному, хто на законних підставах перебуває на території України, гарантується свобода пересування…',
         'Можна вільно подорожувати країною. А кути допоможуть читати мапу.',
         'Everyone who is lawfully in Ukraine has freedom of movement.', 'You can travel freely around the country. Angles help you read the map.'),
        (30, 'Кожному гарантується недоторканність житла.', 'Твій дім — під захистом закону.',
         'Everyone’s home is protected from intrusion.', 'Your home is protected by law.'),
        (47, 'Кожен має право на житло.', 'Будинки будують за кресленнями, де кожен кут пораховано.',
         'Everyone has the right to housing.', 'Houses are built from plans where every angle is worked out.'),
        (41, 'Кожен має право володіти, користуватися і розпоряджатися своєю власністю, результатами своєї інтелектуальної, творчої діяльності.',
         'Твої речі й твої малюнки — твої.', 'Everyone has the right to own, use and manage their property and the results of their creative work.', 'Your things and your drawings belong to you.'),
        (13, 'Земля, її надра, атмосферне повітря, водні та інші природні ресурси, які знаходяться в межах території України…',
         'Річки, ліси й повітря — спільне багатство всього народу.',
         'The land, what lies under it, the air, the water and other natural resources within Ukraine…', 'Rivers, forests and air belong to the whole nation.'),
        (66, 'Кожен зобов’язаний не заподіювати шкоду природі, культурній спадщині, відшкодовувати завдані ним збитки.',
         'Права йдуть разом з обов’язками: бережи парк, де гуляєш.',
         'Everyone must not harm nature or cultural heritage, and must make up for any damage they cause.', 'Rights come with duties: look after the park you play in.'),
        (39, 'Громадяни мають право збиратися мирно, без зброї і проводити збори, мітинги, походи і демонстрації…',
         'Люди можуть мирно зібратися, щоб сказати, що для них важливо.',
         'Citizens have the right to gather peacefully, without weapons, and to hold meetings, rallies, marches and demonstrations.', 'People can gather peacefully to say what matters to them.'),
        (50, 'Кожен має право на безпечне для життя і здоров’я довкілля та на відшкодування завданої порушенням цього права шкоди.',
         'Чисте повітря й вода — теж твоє право.', 'Everyone has the right to an environment that is safe for life and health.', 'Clean air and water are your right too.'),
    ]


def why(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    return {'items': [
        (t('Кути навколо тебе.', 'Angles are all around you.'),
         t('Будівельники, штурмани й розробники ігор щодня рахують кути. Знаєш один кут на прямій — знаєш і сусідній.',
           'Builders, navigators and game designers work with angles every day. Know one angle on a straight line, and you know its partner.')),
        (t('Перевіряй себе.', 'Check yourself.'),
         t('Сума суміжних кутів завжди 180°. Вийшло інакше — десь помилка. Така самоперевірка допомагає й поза математикою: чи сходяться цифри в новині?',
           'Adjacent angles always add up to 180°. If yours don’t, there’s a mistake somewhere. Checking like this helps outside maths too: do the numbers in a news story add up?')),
        (t('Твої права.', 'Your rights.'),
         t('Стаття 14 Конституції України: «Земля є основним національним багатством, що перебуває під особливою охороною держави». Межі ділянок на мапах креслять кутами й відрізками.',
           'Article 14 of the Constitution of Ukraine says land is the country’s main national treasure, under the special protection of the state. Plot borders on maps are drawn with angles and lines.')),
    ], 'dip': t('Тепер ти вмієш знаходити невідомі кути з одного відомого.', 'Now you can find unknown angles from one known angle.')}
