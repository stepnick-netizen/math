"""Topic: powers (Урок №9.1 Ігоря Петровича) — lesson cards, cheat sheet, three levels, world texts."""
from svgkit import Run, text, hand, arrow, line, circle, rect, path, svg, width, C
from fmt import X, P, num
from common import ROLE_SVG, pig

KEY = 'powers'
LESSON_NO = '9.1'


def say(world, role, s, flip=False):
    return f'<div class="say">{pig(ROLE_SVG[world][role], flip)}<p class="hand">{s}</p></div>'


def pw(b, e, cb='p', ce='y'):
    return [(b, cb, 'n'), (e, ce, 's')]


def op(s, c='i'):
    return [(s, c, 'n')]


# ---------------------------------------------------------------- lesson cards
def cards(lang, world, sheet=False):
    t = lambda uk, en: uk if lang == 'uk' else en
    MUL = '·' if lang == 'uk' else '×'
    DV = ':' if lang == 'uk' else '÷'
    out = []

    # 1. what a power is
    r = Run(pw('2', '5'), 64, 86, 60)
    b = ''
    b += r.svg
    b += hand(52, 150, t('основа', 'base'), 26, 'p')
    b += arrow(r.cx(0) - 4, r.bot(0) + 10, 58, 128, 'p', -0.25)
    b += hand(214, 36, t('показник', 'index'), 26, 'y')
    b += arrow(170, 34, r.cx(1) + 9, r.top(1) + 2, 'y', 0.2)
    xs = [34 + i * 48 for i in range(5)]
    for i, x in enumerate(xs):
        b += circle(x, 196, 18, 'var(--cell)', 'p', 2.5) + text(x, 203, '2', 20, 'p', anchor='middle')
        if i < 4:
            b += text(x + 24, 202, MUL, 20, 'm', anchor='middle')
    b += path('M18 222 Q130 242 242 222', 'y', 2.5)
    b += hand(130, 262, t('5 однакових множників', '5 equal factors'), 22, 'y')
    b += text(262, 204, '=', 26, 'i') + text(284, 205, '32', 30, 'l')
    b += arrow(r.cx(1) + 10, r.bot(1) - 6, 150, 168, 'y', -0.2, dash=True)
    s1 = svg(340, 272, b, '2⁵ = 2·2·2·2·2 = 32')
    out.append(('', t('Що таке степінь', 'What a power is'),
                t('Степінь — короткий запис множення однакових множників: <b>aⁿ = a · a · … · a</b> (n разів).',
                  'A power is a short way to write repeated multiplication: <b>aⁿ = a × a × … × a</b> (n times).'),
                s1, f'<p class="tail">{t("a¹ = a: один множник — це саме число. Читаємо: «два в п’ятому степені».", "a¹ = a: one factor is just the number. Say it: “two to the power of five”.")}</p>'))

    # 2. minus and brackets
    b = ''
    rows = [(op('(−2)', 'p') + [('2', 'y', 's')], '4', 'l', t('парний — плюс', 'even → plus')),
            (op('(−2)', 'p') + [('3', 'y', 's')], '−8', 'y', t('непарний — мінус', 'odd → minus')),
            (op('−', 'i') + pw('2', '2'), '−4', 'y', t('мінус окремо!', 'minus outside!'))]
    for k, (pcs, res, rc, note) in enumerate(rows):
        y = 52 + k * 62
        r = Run(pcs + op(' = ') + [(res, rc, 'n')], 20, y, 30)
        b += r.svg + hand(332, y - 4, note, 23, 'm', 'end')
        if k == 2:
            x0, x1 = r.span(0)[0], r.span(2)[1]
            b += rect(x0 - 6, y - 32, x1 - x0 + 9, 44, 'none', 'h', 2.5, 12, '6 5')
    s2 = svg(340, 200, b, '(−2)² = 4, (−2)³ = −8, −2² = −4')
    out.append(('', t('Мінус і дужки', 'Minus signs and brackets'),
                t('Від’ємне число в <b>парному</b> степені стає додатним, у <b>непарному</b> лишається від’ємним.',
                  'A negative number to an <b>even</b> power turns positive; to an <b>odd</b> power it stays negative.'),
                s2, f'<p class="tail">{t("−2² — це −(2²): степінь стосується лише двійки. Хочеш, щоб і мінуса, — бери в дужки.", "−2² means −(2²): the power only belongs to the 2. To include the minus, use brackets.")}</p>'
                + say(world, 'hostB', t('Дужки — як обійми: що всередині, те й у степені.', 'Brackets are like a hug: everything inside gets the power.'), True)))

    # 3. KEY: multiplying powers
    b = ''
    r = Run(pw('2', '3') + op(f' {MUL} ', 'k') + pw('2', '2') + op(' =', 'k'), 18, 42, 30)
    b += r.svg
    cx = [32, 64, 96, 146, 178]
    for i, x in enumerate(cx):
        b += circle(x, 96, 14, 'var(--paper)', 'p', 2.5) + text(x, 103, '2', 18, 'p', anchor='middle')
    b += text(121, 102, MUL, 20, 'k', anchor='middle')
    b += path('M24 118 Q64 140 104 118', 'y', 2.5) + path('M138 118 Q162 136 186 118', 'y', 2.5)
    b += text(64, 156, '3', 22, 'y', anchor='middle') + text(162, 152, '2', 22, 'y', anchor='middle')
    b += arrow(204, 96, 246, 96, 'k', 0)
    r2 = Run(pw('2', '5'), 262, 110, 40)
    b += r2.svg + hand(290, 152, '3 + 2 = 5', 26, 'l')
    b += hand(170, 200, t(f'перевірка: 8 · 4 = 32 = 2⁵ ✓', f'check: 8 × 4 = 32 = 2⁵ ✓'), 23, 'k')
    s3 = svg(340, 212, b, '2³ · 2² = 2⁵')
    out.append(('key wide two', t('Головне: множимо степені', 'Key rule: multiplying powers'),
                t('<b>Основа та сама — показники додаємо: aᵐ · aⁿ = aᵐ⁺ⁿ.</b>', '<b>Same base? Add the indices: aᵐ × aⁿ = aᵐ⁺ⁿ.</b>'),
                s3, f'<p class="more">{t("Працює лише для однакових основ: 2³ · 5² так не скоротиш.", "This only works for the same base: you can’t do it with 2³ × 5².")}</p>'
                + say(world, 'tidy', t('Однакова основа — збери всіх в одну компанію й порахуй!', 'Same base? Put them all in one group and count!'))))

    # 4. dividing powers
    b = ''
    r = Run(pw('3', '5') + op(f' {DV} ') + pw('3', '2') + op(' = ') + pw('3', '3') + op(' = 27'), 170, 38, 26, 'middle')
    b += r.svg
    xs = [70 + i * 40 for i in range(5)]
    for i, x in enumerate(xs):
        b += circle(x, 92, 15, 'var(--cell)', 'p', 2.5) + text(x, 99, '3', 18, 'p', anchor='middle')
    b += line(44, 120, 256, 120, 'i', 3)
    for i, x in enumerate([130, 170]):
        b += circle(x, 148, 15, 'var(--cell)', 'p', 2.5) + text(x, 155, '3', 18, 'p', anchor='middle')
    for x in (70, 110):
        b += line(x - 14, 106, x + 14, 78, 'b', 3)
    for x in (130, 170):
        b += line(x - 14, 162, x + 14, 134, 'b', 3)
    b += path('M146 76 Q190 60 234 76', 'y', 2.5) + text(190, 66, '3', 18, 'y', anchor='middle')
    b += hand(290, 104, '5 − 2 = 3', 26, 'l')
    b += hand(170, 200, t('пари згори й знизу скорочуються', 'pairs on top and bottom cancel'), 23, 'm')
    s4 = svg(340, 212, b, '3⁵ : 3² = 3³ = 27')
    out.append(('', t('Ділимо степені', 'Dividing powers'),
                t('Основа та сама — <b>показники віднімаємо</b>: aᵐ : aⁿ = aᵐ⁻ⁿ (a ≠ 0).', 'Same base? <b>Subtract the indices</b>: aᵐ ÷ aⁿ = aᵐ⁻ⁿ (a ≠ 0).'),
                s4, f'<p class="tail">{t("Перевірка: 243 : 9 = 27.", "Check: 243 ÷ 9 = 27.")}</p>'
                + say(world, 'messy', t('Скоротив пари — і роботи поменшало!', 'Cancel the pairs and there’s less work to do!'), True)))

    # 5. power of a power
    b = ''
    r = Run(op('(') + pw('a', '2') + op(')') + [('3', 's', 's')] + op(' ='), 20, 44, 30)
    b += r.svg
    for i, x in enumerate([26, 116, 206]):
        b += rect(x, 70, 70, 50, 'var(--cell)', 'p', 2.5, 12)
        rr = Run(pw('a', '2'), x + 35, 106, 28, 'middle')
        b += rr.svg
        if i < 2:
            b += text(x + 80, 103, MUL, 22, 'm', anchor='middle')
    b += path('M26 132 Q151 162 276 132', 's', 2.5) + hand(151, 176, t('3 рази', '3 times'), 24, 's')
    b += arrow(286, 96, 300, 150, 'i', -0.3)
    r2 = Run(pw('a', '6'), 290, 196, 38, 'middle')
    b += r2.svg + hand(196, 214, t('2 · 3 = 6', '2 × 3 = 6'), 24, 'l')
    s5 = svg(340, 224, b, '(a²)³ = a⁶')
    out.append(('', t('Степінь степеня', 'A power of a power'),
                t('Степінь підносимо ще до степеня — <b>показники множимо</b>: (aᵐ)ⁿ = aᵐⁿ.', 'Raise a power to a power? <b>Multiply the indices</b>: (aᵐ)ⁿ = aᵐⁿ.'),
                s5, f'<p class="tail">{t("Не плутай: a² · a³ = a⁵ (додаємо), а (a²)³ = a⁶ (множимо).", "Don’t mix them up: a² × a³ = a⁵ (add), but (a²)³ = a⁶ (multiply).")}</p>'))

    # 6. power of a product (umbrella)
    b = ''
    r = Run(op('(') + op('2', 'y') + op(f' {MUL} ') + op('5', 'p') + op(')') + [('3', 's', 's')], 150, 98, 40, 'middle')
    b += r.svg
    ex, ey = r.cx(5) + 4, r.top(5) - 4
    b += arrow(ex, ey, r.cx(1), r.top(1) - 6, 's', 0.45, 2.2) + arrow(ex, ey, r.cx(3), r.top(3) - 6, 's', 0.35, 2.2)
    b += hand(ex + 58, 44, t('парасолька', 'umbrella'), 22, 'h')
    r2 = Run(pw('2', '3', 'y', 's') + op(f' {MUL} ') + pw('5', '3', 'p', 's') + op(' = 8 ' + MUL + ' 125 = ') + op('1000', 'l'), 170, 180, 26, 'middle')
    b += r2.svg
    b += arrow(r.cx(1), r.bot(1) + 6, r2.cx(0), r2.top(0) - 6, 'y', 0.12) + arrow(r.cx(3), r.bot(3) + 6, r2.cx(3), r2.top(3) - 6, 'p', -0.12)
    b += hand(170, 224, t('перевірка: 10³ = 1000 ✓', 'check: 10³ = 1000 ✓'), 23, 'm')
    s6 = svg(340, 234, b, '(2·5)³ = 2³·5³ = 1000')
    out.append(('wide two', t('Степінь добутку', 'A power of a product'),
                t('Показник за дужкою дістається <b>кожному</b> множнику: (ab)ⁿ = aⁿbⁿ.', 'The index outside the brackets goes to <b>every</b> factor: (ab)ⁿ = aⁿbⁿ.'),
                s6, f'<p class="more">{t("Працює й навпаки: 25² · 4² = (25 · 4)² = 100² = 10&nbsp;000. Однакові показники — збирай під одну дужку.", "It works backwards too: 25² × 4² = (25 × 4)² = 100² = 10,000. Same index? Put them under one bracket.")}</p>'
                + say(world, 'hostB', t('Показник за дужкою — як парасолька над усіма.', 'The index outside is an umbrella over everyone.'))))

    # 7. same base ladder
    b = ''
    vals = [2, 4, 8, 16, 32, 64]
    for i, v in enumerate(vals):
        x = 30 + i * 56
        b += circle(x, 66, 22, 'var(--cell)', 'p', 2.5) + text(x, 73, str(v), 18 if v < 10 else 16, 'p', anchor='middle')
        rr = Run(pw('2', str(i + 1)), x, 124, 22, 'middle')
        b += rr.svg + line(x, 92, x, 104, 'm', 1.5, '3 3')
        if i < 5:
            b += arrow(x + 12, 40, x + 44, 40, 'h', -0.35, 2.2) + hand(x + 28, 22, '×2', 19, 'h')
    b += hand(170, 166, t('кожен крок — ще раз помножити на 2', 'each step: multiply by 2 once more'), 22, 'm')
    s7 = svg(340, 178, b, '2, 4, 8, 16, 32, 64 = 2¹ … 2⁶')
    out.append(('', t('Зведи до однієї основи', 'Change to the same base'),
                t('Різні числа часто — степені однієї основи. Переклади їх, і правила знову працюють.', 'Different numbers are often powers of the same base. Rewrite them, and the rules work again.'),
                s7, f'<p class="more">{X("8² · 4 = ({2|3})² · {2|2} = {2|6} · {2|2} = {2|8} = 256", lang)}</p>'
                + f'<p class="tail">{t("Корисно знати: 9 = 3², 27 = 3³, 49 = 7², 100 = 10², 1000 = 10³.", "Handy to know: 9 = 3², 27 = 3³, 49 = 7², 100 = 10², 1000 = 10³.")}</p>'))

    # 8. simplify first
    b = ''
    r = Run(pw('7', '5') + op(f' {MUL} ') + pw('7', '3') + op(f' {DV} ') + pw('7', '6'), 170, 40, 30, 'middle')
    r2 = Run(pw('7', '8') + op(f' {DV} ') + pw('7', '6'), 170, 116, 30, 'middle')
    r3 = Run(pw('7', '2') + op(' = ') + op('49', 'l'), 170, 192, 34, 'middle')
    b += r.svg + r2.svg + r3.svg
    b += arrow(170, 54, 170, 88, 'y', 0) + hand(160, 78, '① 5 + 3 = 8', 23, 'y', 'end')
    b += arrow(170, 130, 170, 160, 'y', 0) + hand(182, 150, '② 8 − 6 = 2', 23, 'y', 'start')
    s8 = svg(340, 206, b, '7⁵·7³:7⁶ = 7² = 49')
    out.append(('', t('Спершу спрости, потім рахуй', 'Simplify first, then work it out'),
                t('Не перемножуй велетенські числа. Спершу збери показники, а рахуй уже маленький степінь.', 'Don’t multiply out huge numbers. Combine the indices first, then work out a small power.'),
                s8, say(world, 'hostA', t('7⁸ — це понад 5 мільйонів. Навіщо, якщо відповідь 49?', '7⁸ is over 5 million. Why bother, when the answer is 49?'))))

    # 9. folding paper
    b = ''
    layers = [1, 2, 4, 8, 16, 32]
    for i, n in enumerate(layers):
        x = 22 + i * 52
        h = n * 3.6 + 4
        b += rect(x, 150 - h, 36, h, 'var(--cell)', 's', 2, 3)
        for k in range(1, min(n, 32)):
            yy = 150 - h + k * (h / n)
            if n <= 16 or k % 2 == 0:
                b += line(x + 3, yy, x + 33, yy, 'var(--line)', 0.9, cap='butt')
        b += text(x + 18, 174, str(n), 18, 'p', anchor='middle')
    b += hand(170, 198, t('шарів після 0, 1, 2, 3, 4, 5 складань', 'layers after 0, 1, 2, 3, 4, 5 folds'), 20, 'm')
    b += hand(110, 34, t('щоразу вдвічі більше', 'twice as many each time'), 22, 'h')
    s9 = svg(340, 204, b, '1, 2, 4, 8, 16, 32 шари')
    out.append(('wide two', t('Степені в житті', 'Powers in real life'),
                t('Склади аркуш навпіл — шарів удвічі більше. Ще раз — знову вдвічі.', 'Fold a sheet of paper in half and there are twice as many layers. Fold again: twice as many again.'),
                s9, f'<p class="tail">{t("П’ять складань — 2⁵ = 32 шари. Десять — уже 2¹⁰ = 1024. Так само швидко розлітаються чутки, якщо кожен перекаже двом.", "Five folds make 2⁵ = 32 layers. Ten make 2¹⁰ = 1024. Rumours spread just as fast when everyone tells two friends.")}</p>'))

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
        title=t('Шпаргалка: степені', 'Cheat sheet: powers'),
        h1=t('Степені <span>на одній сторінці</span>', 'Powers <span>on one page</span>'),
        bubble=t('Привіт! Тут усе головне про степені: що це таке і три правила, які роблять складне простим. Стрілочки підкажуть, що куди йде.',
                 'Hi! Here is everything important about powers: what they are and three rules that make hard sums easy. Follow the arrows.'),
        cast=[pig(ROLE_SVG[w][r], r == 'hostB') for r in ('hostA', 'hostB', 'tidy', 'messy')],
        cards=cards(lang, w, True),
        final_svg=pig(ROLE_SVG[w]['tidy']),
        final=t('Самоперевірка: основа однакова? Множення — додай показники, ділення — відніми, степінь степеня — помнож.',
                'Check yourself: same base? Multiplying: add the indices. Dividing: subtract them. Power of a power: multiply them.'))


# ---------------------------------------------------------------- levels
RULE = {'add': ('Показники додаємо', 'Add the indices', '+'), 'sub': ('Показники віднімаємо', 'Subtract the indices', '−'),
        'mul': ('Показники множимо', 'Multiply the indices', '×')}
RULE_COL = {'add': 'var(--leaf)', 'sub': 'var(--sky)', 'mul': 'var(--plum)'}


def rule_icon(sign, col):
    return (f'<svg viewBox="0 0 70 60" aria-hidden="true"><rect x="6" y="6" width="58" height="48" rx="14" fill="var(--cell)" stroke="{col}" stroke-width="3"/>'
            f'<text x="35" y="44" text-anchor="middle" font-size="34" font-family="Comfortaa,sans-serif" font-weight="700" fill="{col}">{sign}</text></svg>')


def levels(lang, edition):
    t = lambda uk, en: uk if lang == 'uk' else en
    x = lambda s: X(s, lang)
    p = lambda s: P(s, lang)
    n = lambda v: num(v, lang)
    MUL = '·' if lang == 'uk' else '×'

    # ---- level A: which rule + index
    A = [  # (shown, base, rule, m, k, answer, teacher, hidden-one)
        ('{p|2}·{p|4}', 'p', 'add', 2, 4, 6, True, False),
        ('{m|9} : {m|5}', 'm', 'sub', 9, 5, 4, True, False),
        ('({a|4})^5', 'a', 'mul', 4, 5, 20, True, False),
        ('{4|}·{4|16}', '4', 'add', 1, 16, 17, True, True),
        ('{9|7} : {9|}', '9', 'sub', 7, 1, 6, True, True),
        ('({c|7})^2', 'c', 'mul', 7, 2, 14, True, False),
        ('{x|3}·{x|5}·{x|}', 'x', 'add', 3, 5, 9, False, True),
        ('({y|2})^6', 'y', 'mul', 2, 6, 12, False, False),
        ('{b|12} : {b|4}', 'b', 'sub', 12, 4, 8, False, False),
        ('{z|10} : {z|}', 'z', 'sub', 10, 1, 9, False, True),
    ]
    order = ['add', 'sub', 'mul']
    ta = []
    for i, (sh, base, rule, m, k, ans, teach, hid) in enumerate(A):
        if base == 'x':
            calc = '3 + 5 + 1'
        elif rule == 'add':
            calc = f'{m} + {k}'
        elif rule == 'sub':
            calc = f'{m} − {k}'
        else:
            calc = f'{m} {MUL} {k}'
        hid_note = t(f' Степінь без показника має показник 1.', ' A power with no index has an index of 1.') if hid else ''
        traps = []
        if rule == 'add':
            traps = [[0, m * k, 'exp-multiplied']] + ([[0, ans - 1, 'exp-forgot-hidden-1']] if hid else [])
        elif rule == 'sub':
            traps = [[0, m + k, 'exp-added']] + ([[0, m / k, 'exp-divided']] if k > 1 else []) + ([[0, m, 'exp-forgot-hidden-1']] if hid else [])
        else:
            traps = [[0, m + k, 'exp-added']]
        steps = [
            {'type': 'choice', 'style': 'doors', 'p': t('Яке правило тут працює?', 'Which rule works here?'),
             'opts': [[r, t(RULE[r][0], RULE[r][1])] for r in order], 'ans': rule,
             'icons': [rule_icon(RULE[r][2], RULE_COL[r]) for r in order], 'colors': [RULE_COL[r] for r in order],
             'tag': {r: f'rule-{rule}-as-{r}' for r in order},
             'h': [t('дивись на дію між степенями. Множення — показники додаємо, ділення — віднімаємо, степінь у дужках ще в степені — множимо.',
                     'look at what is happening between the powers. Multiplying: add the indices. Dividing: subtract. A power in brackets raised to another power: multiply.'),
                   {'add': t('тут степені з однаковою основою множать один на одного.', 'here powers with the same base are multiplied together.'),
                    'sub': t('тут степінь ділять на степінь з тією самою основою.', 'here a power is divided by a power with the same base.'),
                    'mul': t('тут степінь стоїть у дужках, а за дужками ще один показник.', 'here a power is inside brackets, with another index outside.')}[rule]],
             'ok': t(RULE[rule][0], RULE[rule][1])},
            {'type': 'num', 'p': t('Який показник вийде?', 'What is the new index?'),
             'f': [{'pre': x(sh) + ' = ' + f'<span class="b">{base}</span>', 'sup': True, 'ans': ans, 'n': 'exp', 'aria': t('показник', 'index')}],
             'traps': traps,
             'h': [t('основа лишається та сама, змінюється лише показник.', 'the base stays the same; only the index changes.') + hid_note,
                   f'{calc} = ?'],
             'ok': x(sh + ' = {' + base + '|' + str(ans) + '}')}
        ]
        ta.append({'teacher': teach, 'show': x(sh), 'steps': steps, 'rule': rule,
                   'after': x(sh + ' = {' + base + '|' + str(ans) + '}'),
                   'label': t(f'Картка {i + 1}: ', f'Card {i + 1}: ') + p(sh + ' = {' + base + '|' + str(ans) + '}')})

    # ---- level B: one power, then the value
    B = [  # shown, base, steps calc, exponent, value, value hint, teacher, traps for exponent
        ('{9|10} : {9|8}', '9', '10 − 8', 2, 81, '9 · 9 = ?', True, [[0, 18, 'exp-added'], [0, 1.25, 'exp-divided']]),
        ('{0,4|17} : {0,4|14}', '0,4', '17 − 14', 3, 0.064, '0,4 · 0,4 = 0,16; 0,16 · 0,4 = ?', True, [[0, 31, 'exp-added']]),
        ('{5|4}·{5|12} : {5|13}', '5', '4 + 12 − 13', 3, 125, '5 · 5 = 25; 25 · 5 = ?', True, [[0, 29, 'exp-all-added'], [0, 35, 'exp-other']]),
        ('{37|12} : ({37|5}·{37|6})', '37', '12 − (5 + 6)', 1, 37, '37¹ = ?', True, [[0, 23, 'exp-other'], [0, 13, 'exp-brackets-ignored']]),
        ('{6|17}·{6|8} : {6|22}', '6', '17 + 8 − 22', 3, 216, '6 · 6 = 36; 36 · 6 = ?', True, [[0, 47, 'exp-all-added']]),
        ('{0,7|3}·{0,7|16} : ({0,7|12}·{0,7|5})', '0,7', '3 + 16 − (12 + 5)', 2, 0.49, '0,7 · 0,7 = ?', True, [[0, 36, 'exp-all-added'], [0, 12, 'exp-brackets-ignored']]),
        ('{10|6}·{10|2} : {10|5}', '10', '6 + 2 − 5', 3, 1000, '10 · 10 · 10 = ?', False, [[0, 13, 'exp-all-added']]),
        ('{(−2)|5} : {(−2)|2}', '(−2)', '5 − 2', 3, -8, '(−2) · (−2) = 4; 4 · (−2) = ?', False, [[0, 7, 'exp-added']]),
    ]
    tb = []
    for i, (sh, base, calc, e, val, vh, teach, traps) in enumerate(B):
        powv = '{' + base + '|' + str(e) + '}'
        valtraps = []
        try:
            bnum = float(base.replace(',', '.').replace('(', '').replace(')', '').replace('−', '-'))
            valtraps = [[0, bnum * e, 'value-times-n']]
        except ValueError:
            pass
        if val < 0:
            valtraps.append([0, -val, 'value-sign'])
        steps = [
            {'type': 'num', 'p': t('Запиши одним степенем:', 'Write it as one power:'),
             'f': [{'pre': x(sh) + ' = ' + f'<span class="b">{x(base)}</span>', 'sup': True, 'ans': e, 'n': 'exp', 'aria': t('показник', 'index')}],
             'traps': traps,
             'h': [t('основа скрізь однакова. Множення — показники додаємо, ділення — віднімаємо. Дужки — спершу.', 'the base is the same everywhere. Multiplying: add the indices; dividing: subtract. Brackets first.'),
                   f'{x(calc)} = ?'],
             'ok': x(sh + ' = ' + powv)},
            {'type': 'num', 'p': t('Тепер обчисли значення:', 'Now work out the value:'),
             'f': [{'pre': x(powv) + ' =', 'wide': True, 'ans': val, 'n': 'value', 'aria': t('значення', 'value')}],
             'traps': valtraps,
             'h': [t('степінь — це множення однакових множників, а не множення основи на показник.', 'a power is repeated multiplication, not the base times the index.'),
                   x(vh)],
             'ok': x(powv + ' = ' + n(val))}
        ]
        tb.append({'teacher': teach, 'show': x(sh), 'steps': steps,
                   'after': x(sh + ' = ' + powv + ' = ' + n(val)),
                   'label': t(f'Замок {i + 1}: ', f'Lock {i + 1}: ') + p(sh + ' = ' + n(val))})

    # ---- level C: same base, power of a product
    sup = lambda pre, ans, name='exp': {'pre': pre, 'sup': True, 'ans': ans, 'n': name, 'aria': t('показник', 'index')}
    numf = lambda pre, ans, name='value', post='': {'pre': pre, 'wide': True, 'ans': ans, 'n': name, 'post': post, 'aria': t('число', 'number')}
    tr_h = t('підбери показник: скільки разів треба помножити основу саму на себе?', 'find the index: how many times do you multiply the base by itself?')
    combine_h = t('степінь степеня — показники множимо; добуток — додаємо; частка — віднімаємо.', 'power of a power: multiply the indices; multiplying: add; dividing: subtract.')
    NL = '<span class="gap"></span>'
    TC = []
    # c0 8^9·4^5
    TC.append(dict(teacher=True, show='{8|9}·{4|5} = {2|?}', steps=[
        dict(type='num', p=t('Переклади числа в степені двійки:', 'Write the numbers as powers of 2:'),
             f=[sup('8 = <span class="b">2</span>', 3), sup(NL + '4 = <span class="b">2</span>', 2)],
             h=[tr_h, '2 · 2 · 2 = 8; 2 · 2 = 4'], ok=x('8 = {2|3}, 4 = {2|2}')),
        dict(type='num', p=t('Тепер один степінь:', 'Now one power:'),
             f=[sup(x('({2|3})^9·({2|2})^5 = ') + '<span class="b">2</span>', 37)], traps=[[0, 19, 'exp-added-not-multiplied'], [0, 14, 'exp-other']],
             h=[combine_h, '3 · 9 + 2 · 5 = ?'], ok=x('{2|27}·{2|10} = {2|37}'))],
        after=x('{8|9}·{4|5} = {2|27}·{2|10} = {2|37}'), label=x('8⁹·4⁵ = 2³⁷')))
    # c1 32·16^6·64^3
    TC.append(dict(teacher=True, show='32·{16|6}·{64|3} = {2|?}', steps=[
        dict(type='num', p=t('Переклади числа в степені двійки:', 'Write the numbers as powers of 2:'),
             f=[sup('32 = <span class="b">2</span>', 5), sup(NL + '16 = <span class="b">2</span>', 4), sup(NL + '64 = <span class="b">2</span>', 6)],
             h=[tr_h, '2 · 2 · 2 · 2 = 16; 16 · 2 = 32; 32 · 2 = 64'], ok=x('32 = {2|5}, 16 = {2|4}, 64 = {2|6}')),
        dict(type='num', p=t('Тепер один степінь:', 'Now one power:'),
             f=[sup(x('{2|5}·({2|4})^6·({2|6})^3 = ') + '<span class="b">2</span>', 47)], traps=[[0, 24, 'exp-added-not-multiplied']],
             h=[combine_h, '5 + 4 · 6 + 6 · 3 = ?'], ok=x('{2|5}·{2|24}·{2|18} = {2|47}'))],
        after=x('32·{16|6}·{64|3} = {2|5}·{2|24}·{2|18} = {2|47}'), label=x('32·16⁶·64³ = 2⁴⁷')))
    # c2 100^5 : 1000^2
    TC.append(dict(teacher=True, show='{100|5} : {1000|2}', steps=[
        dict(type='num', p=t('Переклади в степені десятки:', 'Write them as powers of 10:'),
             f=[sup('100 = <span class="b">10</span>', 2), sup(NL + '1000 = <span class="b">10</span>', 3)],
             h=[t('порахуй нулі: скільки нулів — такий показник у десятки.', 'count the zeros: the number of zeros is the index of 10.'), '100 = 10 · 10'], ok=x('100 = {10|2}, 1000 = {10|3}')),
        dict(type='num', p=t('Один степінь:', 'One power:'),
             f=[sup(x('{10|10} : {10|6} = ') + '<span class="b">10</span>', 4)], traps=[[0, 16, 'exp-added']],
             h=[combine_h, '2 · 5 − 3 · 2 = ?'], ok=x('{10|10} : {10|6} = {10|4}')),
        dict(type='num', p=t('Значення:', 'The value:'), f=[numf(x('{10|4} ='), 10000)], traps=[[0, 40, 'value-times-n']],
             h=[t('10⁴ — одиниця і чотири нулі.', '10⁴ is 1 followed by four zeros.'), '10 · 10 · 10 · 10 = ?'], ok=x('{10|4} = 10 000') if lang == 'uk' else x('{10|4} = 10,000'))],
        after=x('{100|5} : {1000|2} = {10|10} : {10|6} = {10|4} = ') + ('10 000' if lang == 'uk' else '10,000'), label=p('100⁵ : 1000² = ') + ('10 000' if lang == 'uk' else '10,000')))
    # c3 7^9·49^8 : 343^8
    TC.append(dict(teacher=True, show='{7|9}·{49|8} : {343|8}', steps=[
        dict(type='num', p=t('Переклади в степені сімки:', 'Write them as powers of 7:'),
             f=[sup('49 = <span class="b">7</span>', 2), sup(NL + '343 = <span class="b">7</span>', 3)],
             h=[tr_h, '7 · 7 = 49; 49 · 7 = 343'], ok=x('49 = {7|2}, 343 = {7|3}')),
        dict(type='num', p=t('Один степінь:', 'One power:'),
             f=[sup(x('{7|9}·{7|16} : {7|24} = ') + '<span class="b">7</span>', 1)], traps=[[0, 49, 'exp-all-added']],
             h=[combine_h, '9 + 2 · 8 − 3 · 8 = ?'], ok=x('{7|25} : {7|24} = {7|1}')),
        dict(type='num', p=t('Значення:', 'The value:'), f=[numf(x('{7|1} ='), 7)], h=[t('a¹ = a.', 'a¹ = a.'), t('сім у першому степені — це просто 7.', 'seven to the power of one is just 7.')], ok='= 7')],
        after=x('{7|9}·{7|16} : {7|24} = {7|1} = 7'), label=p('7⁹·49⁸ : 343⁸ = 7')))
    # c4 6^12 : (2^10·3^11)
    TC.append(dict(teacher=True, show='{6|12} : ({2|10}·{3|11})', steps=[
        dict(type='num', p=t('6 = 2 · 3. Піднеси добуток до степеня:', '6 = 2 × 3. Raise the product to the power:'),
             f=[sup(x('{6|12} = ') + '<span class="b">2</span>', 12), sup(MUL + ' <span class="b">3</span>', 12)],
             h=[t('показник за дужкою дістається кожному множнику: (2 · 3)¹² = 2¹² · 3¹².', 'the index outside the bracket goes to every factor: (2 × 3)¹² = 2¹² × 3¹².'), '(2 · 3)¹² = ?'],
             ok=x('{6|12} = {2|12}·{3|12}')),
        dict(type='num', p=t('Поділи двійки на двійки, трійки на трійки:', 'Divide the 2s by the 2s and the 3s by the 3s:'),
             f=[sup('= <span class="b">2</span>', 2), sup(MUL + ' <span class="b">3</span>', 1)], traps=[[0, 22, 'exp-added'], [1, 23, 'exp-added']],
             h=[t('у кожної основи свої показники: віднімай окремо.', 'each base has its own indices: subtract them separately.'), '12 − 10 = ?; 12 − 11 = ?'],
             ok=x('{2|2}·{3|1}')),
        dict(type='num', p=t('Значення:', 'The value:'), f=[numf(x('{2|2}·{3|} ='), 12)], traps=[[0, 7, 'value-added']],
             h=[t('2² = 4, а 3¹ = 3.', '2² = 4 and 3¹ = 3.'), '4 · 3 = ?'], ok='= 12')],
        after=x('{6|12} : ({2|10}·{3|11}) = {2|2}·{3|1} = 12'), label=p('6¹² : (2¹⁰·3¹¹) = 12')))
    # c5 12,5^3·8^3
    TC.append(dict(teacher=True, show='{12,5|3}·{8|3}', steps=[
        dict(type='num', p=t('Однакові показники — збери під одну дужку:', 'Same index? Put them under one bracket:'),
             f=[numf(x('({12,5|}·{8|})^3 = (') , 100, 'product', ')<sup>3</sup>')],
             h=[t('aⁿ · bⁿ = (a · b)ⁿ. Спершу перемнож основи.', 'aⁿ × bⁿ = (a × b)ⁿ. Multiply the bases first.'), x('12,5 · 8 = ?')], traps=[[0, 20.5, 'added-bases']],
             ok=x('({12,5|}·{8|})^3 = 100^3')),
        dict(type='num', p=t('Значення:', 'The value:'), f=[numf('100<sup>3</sup> =', 1000000)], traps=[[0, 300, 'value-times-n'], [0, 10000, 'value-square']],
             h=[t('100³ = 100 · 100 · 100.', '100³ = 100 × 100 × 100.'), t('100 · 100 = 10 000; ще раз на 100 — допиши два нулі.', '100 × 100 = 10,000; times 100 again: add two more zeros.')],
             ok='= ' + ('1 000 000' if lang == 'uk' else '1,000,000'))],
        after=x('{12,5|3}·{8|3} = (12,5·8)^3 = 100^3 = ') + ('1 000 000' if lang == 'uk' else '1,000,000'), label=p('12,5³·8³ = ') + ('1 000 000' if lang == 'uk' else '1,000,000')))
    # c6 a^3 b^6 = (a^? b^?)^3
    TC.append(dict(teacher=True, q=t('Запиши у вигляді степеня з показником 3:', 'Write it as a power with index 3:'), show='{a|3}{b|6} = (?)^3', steps=[
        dict(type='num', p=t('Що стоїть у дужках?', 'What goes in the brackets?'),
             f=[sup('(<span class="b">a</span>', 1), sup('<span class="b">b</span>', 2, 'exp2')], traps=[[1, 3, 'exp-subtracted'], [1, 18, 'exp-multiplied']],
             h=[t('(…)³ — показники в дужках помножаться на 3. Тож поділи кожен показник на 3.', '(…)³ multiplies every index inside by 3. So divide each index by 3.'), '3 : 3 = ?; 6 : 3 = ?'],
             ok=x('{a|3}{b|6} = ({a|}{b|2})^3'))],
        after=x('{a|3}{b|6} = ({a|}{b|2})^3'), label=p('a³b⁶ = (ab²)³')))
    TC[-1]['steps'][0]['f'][1]['post'] = ')<sup>3</sup>'
    # c7 x^9 y^15 = (x^? y^?)^3
    TC.append(dict(teacher=True, q=t('Запиши у вигляді степеня з показником 3:', 'Write it as a power with index 3:'), show='{x|9}{y|15} = (?)^3', steps=[
        dict(type='num', p=t('Що стоїть у дужках?', 'What goes in the brackets?'),
             f=[sup('(<span class="b">x</span>', 3), dict(sup('<span class="b">y</span>', 5, 'exp2'), post=')<sup>3</sup>')], traps=[[0, 6, 'exp-subtracted'], [1, 12, 'exp-subtracted']],
             h=[t('кожен показник у дужках помножиться на 3. Поділи на 3.', 'every index inside gets multiplied by 3. Divide by 3.'), '9 : 3 = ?; 15 : 3 = ?'],
             ok=x('({x|3}{y|5})^3'))],
        after=x('{x|9}{y|15} = ({x|3}{y|5})^3'), label=p('x⁹y¹⁵ = (x³y⁵)³')))
    # c8 ours 27^2·9 : 3^5
    TC.append(dict(teacher=False, show='{27|2}·9 : {3|5}', steps=[
        dict(type='num', p=t('Переклади в степені трійки:', 'Write them as powers of 3:'),
             f=[sup('27 = <span class="b">3</span>', 3), sup(NL + '9 = <span class="b">3</span>', 2)],
             h=[tr_h, '3 · 3 = 9; 9 · 3 = 27'], ok=x('27 = {3|3}, 9 = {3|2}')),
        dict(type='num', p=t('Один степінь:', 'One power:'),
             f=[sup(x('{3|6}·{3|2} : {3|5} = ') + '<span class="b">3</span>', 3)], traps=[[0, 13, 'exp-all-added']],
             h=[combine_h, '3 · 2 + 2 − 5 = ?'], ok=x('{3|8} : {3|5} = {3|3}')),
        dict(type='num', p=t('Значення:', 'The value:'), f=[numf(x('{3|3} ='), 27)], traps=[[0, 9, 'value-times-n']], h=[t('3³ = 3 · 3 · 3.', '3³ = 3 × 3 × 3.'), '9 · 3 = ?'], ok='= 27')],
        after=x('{27|2}·9 : {3|5} = {3|8} : {3|5} = {3|3} = 27'), label=p('27²·9 : 3⁵ = 27')))
    for i, tc in enumerate(TC):
        tc['show'] = x(tc['show']) if not tc['show'].startswith('<') else tc['show']
        tc['label'] = t(f'Крок {i + 1}: ', f'Step {i + 1}: ') + tc['label']
        for s in tc['steps']:
            s.setdefault('traps', [])
    # localise numbers inside field prefixes of C
    return {'a': {'tasks': ta}, 'b': {'tasks': tb}, 'c': {'tasks': TC}}


# ---------------------------------------------------------------- stages (JS)
STAGE_JS = r"""
/* level A: three doors with the cards already sorted */
const DOOR={add:['+','var(--leaf)'],sub:['−','var(--sky)'],mul:['×','var(--plum)']};
function stageA(c){
  const solved=LV.a.tasks.slice(0,c.i);
  const doors=['add','sub','mul'].map(r=>{const [sg,col]=DOOR[r];const chips=solved.map((t,k)=>t.rule===r?`<span class="chip">${LV.a.tasks[k].after}</span>`:'').join('');
    return `<div class="door" style="--c:${col}">${ICONS[c.W.icon||'basket'](col)}<b>${sg}</b><div class="chips">${chips}</div></div>`}).join('');
  const top=c.finished?`<div class="say">${c.SVGR('messy')}<p class="bubble">${c.S.aQuip}</p></div>`
    :`<div class="say">${c.SVGR('messy')}</div><div class="expcard pop">${c.t.show}</div><p class="count">${c.S.heap(c.n-c.i)}</p>`;
  return top+`<div class="doors">${doors}</div>`;
}
/* level B: a door with padlocks; each right answer opens one */
function lockSVG(open,x,y){
  const sh=open?`<path d="M${x-9} ${y-2} V${y-20} a9 9 0 0 1 18 0 V${y-14}" stroke="var(--leaf)" stroke-width="4" fill="none" transform="translate(0,-8)"/>`
                :`<path d="M${x-9} ${y} V${y-12} a9 9 0 0 1 18 0 V${y}" stroke="var(--hay)" stroke-width="4" fill="none"/>`;
  return sh+`<rect x="${x-14}" y="${y}" width="28" height="22" rx="5" fill="${open?'var(--leaf)':'var(--hay)'}"/><circle cx="${x}" cy="${y+10}" r="3.5" fill="var(--paper)"/>`;
}
function stageB(c){
  const n=c.n,k=Math.min(c.i,n),cols=4,rows=Math.ceil(n/cols);
  const shape={meadow:`<path d="M30 220 V70 Q160 -10 290 70 V220 Z" fill="var(--cell)" stroke="var(--hay)" stroke-width="4"/>`,
    space:`<rect x="30" y="20" width="260" height="200" rx="60" fill="var(--cell)" stroke="var(--sky)" stroke-width="4"/>`,
    bricks:`<rect x="30" y="40" width="260" height="180" rx="10" fill="var(--cell)" stroke="var(--yarn)" stroke-width="4"/><path d="M30 90 H290" stroke="var(--yarn)" stroke-width="3"/>`}[P.world];
  let locks='';for(let j=0;j<n;j++){const r=Math.floor(j/cols),q=j%cols;locks+=lockSVG(j<k,80+q*54,108+r*58)}
  const prize=c.finished?`<text x="160" y="214" text-anchor="middle" class="h" font-size="26" fill="var(--leaf)">${c.S.bOpen}</text>`:'';
  return `<svg viewBox="0 0 320 236" class="stg" role="img" aria-label="${c.S.count(k,n)}">${shape}${locks}${prize}</svg>
    <div class="say">${c.SVGR(c.finished?'hostA':'tidy')}<p class="hand">${c.finished?c.S.bQuip:c.S.bStageL}</p></div><p class="count">${c.S.count(k,n)}</p>`;
}
/* level C: something grows: carrots in the meadow, stars in space, a wall of bricks */
function growSVG(k,n){
  let s='';
  if(P.world==='meadow'){
    s+=`<rect x="10" y="150" width="300" height="34" rx="10" fill="#8A6542" opacity=".55"/>`;
    for(let j=0;j<n;j++){const x=30+j*(260/(n-1));const on=j<k;
      s+= on?`<path d="M${x} 152 L${x-8} 120 Q${x} 112 ${x+8} 120 Z" fill="#E7792B"/><path d="M${x} 118 q-10 -22 -4 -30 M${x} 118 q0 -24 6 -30 M${x} 118 q8 -18 16 -20" stroke="var(--leaf)" stroke-width="4" fill="none" stroke-linecap="round"/>`
             :`<circle cx="${x}" cy="160" r="4" fill="var(--paper)" opacity=".7"/>`}
  }else if(P.world==='space'){
    const pts=[];for(let j=0;j<n;j++){const a=Math.PI*(0.95-0.9*j/(n-1));pts.push([160+130*Math.cos(a),160-110*Math.sin(a)])}
    for(let j=1;j<k;j++)s+=`<line x1="${pts[j-1][0]}" y1="${pts[j-1][1]}" x2="${pts[j][0]}" y2="${pts[j][1]}" stroke="var(--hay)" stroke-width="2" stroke-dasharray="4 4"/>`;
    pts.forEach(([x,y],j)=>{const on=j<k;const r=on?11:6;let d='';for(let q=0;q<10;q++){const a=Math.PI/5*q-Math.PI/2,rr=q%2?r*.45:r;d+=(q?'L':'M')+(x+rr*Math.cos(a)).toFixed(1)+' '+(y+rr*Math.sin(a)).toFixed(1)}
      s+=`<path d="${d}Z" fill="${on?'var(--hay)':'var(--line)'}"/>`});
  }else{
    for(let j=0;j<n;j++){const row=Math.floor(j/3),q=j%3;const x=70+q*62+(row%2?31:0),y=170-row*34;const on=j<k;
      s+=`<rect x="${x}" y="${y}" width="58" height="30" rx="4" fill="${on?'var(--yarn)':'none'}" stroke="${on?'var(--yarn)':'var(--line)'}" stroke-width="2.5" ${on?'':'stroke-dasharray="5 4"'}/>`}
  }
  return `<svg viewBox="0 36 320 164" class="stg" role="img" aria-label="${k}/${n}">${s}</svg>`;
}
function stageC(c){
  const k=Math.min(c.i,c.n);
  return `${growSVG(k,c.n)}<div class="say">${c.SVGR(c.finished?'messy':'hostB')}<p class="hand">${c.finished?c.S.cQuip:c.S.cStageL}</p></div><p class="count">${c.S.count(k,c.n)}</p>`;
}
const STAGE={a:stageA,b:stageB,c:stageC};
"""

EXTRA_CSS = """
.doors{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;width:100%}
.door{display:grid;gap:4px;justify-items:center;align-content:start;border:2px solid var(--c);border-radius:14px;padding:8px 4px;background:var(--paper);min-width:0}
.door svg{width:60px;height:auto}
.door b{font:700 22px var(--display);color:var(--c)}
.door .chip{font-size:12.5px}
.expcard{font:700 clamp(26px,7vw,36px) var(--display);background:var(--paper);border:3px solid var(--hay);border-radius:16px;padding:12px 20px;box-shadow:0 4px 0 var(--shadow);transform:rotate(-2deg);white-space:nowrap}
"""


# ---------------------------------------------------------------- texts
def texts(lang, edition):
    t = lambda uk, en: uk if lang == 'uk' else en
    home = edition == 'home'
    common = dict(
        h1={'meadow': t('Степені <span>на лузі</span>', 'Powers <span>in the meadow</span>'),
            'space': t('Степені <span>у космосі</span>', 'Powers <span>in space</span>'),
            'bricks': t('Степені <span>з цеглинок</span>', 'Powers <span>made of bricks</span>')},
        lH=t('Урок: степені', 'Lesson: powers'),
        lIntro=t('Дев’ять коротких карток за уроком 9.1. Читай по черзі й дивись на стрілочки: вони показують, що куди йде.',
                 'Nine short cards based on lesson 9.1. Read them in order and follow the arrows: they show what goes where.'),
        lBye=t('{hostA} каже: перш ніж рахувати, глянь на основи. Однакові? Тоді працюють правила, і великі числа стають маленькими.',
               '{hostA} says: before you calculate, look at the bases. Are they the same? Then the rules work, and big numbers become small.'),
        toA=t('До першого рівня', 'Go to level 1'),
        dipH=t('Диплом {me:майстра:майстрині:майстра} степенів', 'Powers Master Certificate'),
        teacherTag=t('з уроку Ігоря Петровича', 'from Mr Pasika’s lesson') if home else t('з уроку 9.1', 'from lesson 9.1'),
        rIntro=(t('Тут видно, що {me:ти вже пройшов:ти вже пройшла:вже пройдено}. Натисни кнопку, скопіюй звіт і надішли татові.',
                  'Here’s everything you’ve done so far. Copy the report and send it to Dad.') if home else
                t('Тут видно, що {me:ти вже пройшов:ти вже пройшла:вже пройдено}. Натисни «Надіслати звіт» і вибери Viber, Telegram чи пошту. Або скопіюй звіт і встав у повідомлення вчителеві чи батькам.',
                  'Here’s everything you’ve done so far. Tap "Send my report" and choose WhatsApp, Viber or email. Or copy the report and paste it into a message to your teacher or parents.')),
        copied=t('Скопійовано! Встав звіт у повідомлення.', 'Copied! Paste it into a message.'),
        repHead=(t('Тату, ось мій звіт про степені.', 'Hi Dad, here is my powers report.') if home else t('Ось мій звіт про степені.', 'Here is my powers report.')),
    )
    W = {}
    W['meadow'] = dict(
        intro=t('{messy} знову все {g:messy:переплутав:переплутала}: картки зі степенями розсипались, а комору з морквою хтось замкнув на вісім замків. Прочитай урок і пройди три рівні: розклади картки по нірках, відімкни комору й посади морквяну грядку.',
                '{messy} has mixed everything up again: the power cards are scattered, and someone has locked the carrot pantry with eight padlocks. Read the lesson, then play three levels: sort the cards into burrows, unlock the pantry and plant a carrot patch.'),
        tabA=t('1. Нірки', '1. Burrows'), tabB=t('2. Комора', '2. Pantry'), tabC=t('3. Грядка', '3. Carrot patch'),
        aH=t('Рівень 1. Три нірки', 'Level 1. Three burrows'),
        aIntro=t('У кожній нірці живе своє правило: показники додаємо, віднімаємо або множимо. Вибери нірку для картки, а потім запиши новий показник.',
                 'Each burrow has its own rule: add, subtract or multiply the indices. Choose the burrow for each card, then write the new index.'),
        bH=t('Рівень 2. Комора з морквою', 'Level 2. The carrot pantry'),
        bIntro=t('{messy} {g:messy:замкнув:замкнула} комору на вісім замків. Кожен вираз спершу запиши одним степенем, потім обчисли — і замок відімкнеться.',
                 '{messy} has locked the pantry with eight padlocks. Write each expression as one power, then work out its value, and a padlock opens.'),
        cH=t('Рівень 3. Морквяна грядка', 'Level 3. The carrot patch'),
        cIntro=t('Тут числа різні, але основа одна. Переклади їх у степені однієї основи — і за кожну відповідь виросте морквина.',
                 'The numbers look different, but they share a base. Rewrite them as powers of the same base, and a carrot grows for every answer.'),
        aGood=t('Так!', 'Yes!'), bGood=t('Клац! Замок відімкнено.', 'Click! A padlock opens.'), cGood=t('Виросла ще одна морквина!', 'Another carrot has grown!'),
        aQuip=t('Усі картки по нірках. Як охайно!', 'All the cards are in their burrows. So tidy!'),
        bStageL=t('Відмикаємо замки по одному', 'One padlock at a time'), bOpen=t('Комора відчинена!', 'The pantry is open!'),
        bQuip=t('Морква для всіх! Дякуємо!', 'Carrots for everyone! Thank you!'),
        cStageL=t('Садимо грядку', 'Planting the patch'), cQuip=t('Яка грядка! {messy} вже несе кошик.', 'What a patch! {messy} is bringing a basket.'),
        aDoneH=t('Усі картки розкладено!', 'All the cards are sorted!'),
        aDoneP=t('{messy} аж {g:messy:присвиснув:присвиснула}: правила тепер на своїх місцях. Перша зірка твоя!', '{messy} whistled in surprise: every rule is in its place. Your first star!'),
        bDoneH=t('Комору відчинено!', 'The pantry is open!'),
        bDoneP=t('{tidy} {g:tidy:розклав:розклала} моркву по кошиках і {g:tidy:вручив:вручила} тобі найбільшу. Друга зірка твоя!', '{tidy} shared the carrots out and gave you the biggest one. Your second star!'),
        cDoneH=t('Грядка готова!', 'The patch is ready!'),
        cDoneP=t('Дев’ять морквин у рядочок. {messy} {g:messy:пообіцяв:пообіцяла} більше нічого не плутати. Третя зірка твоя!', 'Nine carrots in a row. {messy} has promised never to mix things up again. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі медаль «Майстер степенів», а {messy} — найсмачнішу морквину.',
               'All three levels complete! {tidy} presents you with a "Powers Master" medal, and {messy} gives you the tastiest carrot.'),
        meet=[['hostA', t('Руда пляма, любить моркву і пояснювати.', 'Ginger patch. Loves carrots and explaining things.')],
              ['hostB', t('Темна пляма, придумує підказки-віршики.', 'Dark patch. Makes up rhymes to help you remember.')],
              ['tidy', t('Їжачиха-охайниця. Знає, де живе кожне правило.', 'A very tidy hedgehog. Knows where every rule lives.')],
              ['messy', t('Єнот. Усе змішує, але дуже хоче навчитись.', 'A raccoon. Mixes everything up, but really wants to learn.')]],
    )
    W['space'] = dict(
        intro=t('Прибулець {messy} {g:messy:розсипав:розсипала} картки зі степенями по всій станції, а сейф із паливом сам замкнувся на вісім замків. Прочитай урок і пройди три рівні: розсортуй картки по шлюзах, відімкни сейф і запали зоряну карту.',
                '{messy} the alien has scattered the power cards all over the station, and the fuel safe has locked itself with eight padlocks. Read the lesson, then play three levels: sort the cards into airlocks, open the safe and light up the star map.'),
        tabA=t('1. Шлюзи', '1. Airlocks'), tabB=t('2. Сейф', '2. Safe'), tabC=t('3. Зорі', '3. Star map'),
        aH=t('Рівень 1. Три шлюзи', 'Level 1. Three airlocks'),
        aIntro=t('Кожен шлюз пропускає лише своє правило: показники додаємо, віднімаємо або множимо. Відправ картку в потрібний шлюз і запиши новий показник.',
                 'Each airlock lets through only its own rule: add, subtract or multiply the indices. Send each card to the right airlock and write the new index.'),
        bH=t('Рівень 2. Сейф із паливом', 'Level 2. The fuel safe'),
        bIntro=t('Сейф замкнено на вісім замків. Кожен вираз запиши одним степенем, потім обчисли — і замок відімкнеться.',
                 'The safe has eight padlocks. Write each expression as one power, then work out its value, and a padlock opens.'),
        cH=t('Рівень 3. Зоряна карта', 'Level 3. The star map'),
        cIntro=t('Числа різні, а основа одна. Переклади їх у степені однієї основи — і на карті засвітиться нова зоря.',
                 'The numbers look different, but they share a base. Rewrite them as powers of the same base, and a new star lights up on the map.'),
        aGood=t('Так!', 'Yes!'), bGood=t('Клац! Замок відімкнено.', 'Click! A padlock opens.'), cGood=t('Засвітилась нова зоря!', 'A new star lights up!'),
        aQuip=t('Станція сяє!', 'The station is gleaming!'),
        bStageL=t('Відмикаємо замки по одному', 'One padlock at a time'), bOpen=t('Сейф відчинено!', 'The safe is open!'),
        bQuip=t('Палива вистачить до самої Альфи Центавра!', 'Enough fuel to reach Alpha Centauri!'),
        cStageL=t('Малюємо сузір’я', 'Drawing a constellation'), cQuip=t('Тепер {messy} знає дорогу додому!', 'Now {messy} knows the way home!'),
        aDoneH=t('Усі картки в шлюзах!', 'All the cards are in their airlocks!'),
        aDoneP=t('{messy} здивовано {g:messy:заблимав:заблимала} всіма трьома очима. Перша зірка твоя!', '{messy} blinked all three eyes in surprise. Your first star!'),
        bDoneH=t('Сейф відчинено!', 'The safe is open!'),
        bDoneP=t('{tidy} заправив ракету й радісно пискнув. Друга зірка твоя!', '{tidy} fuelled the rocket and beeped happily. Your second star!'),
        cDoneH=t('Карта світиться!', 'The map is lit up!'),
        cDoneP=t('Дев’ять зір склались у сузір’я. Третя зірка твоя — справжня!', 'Nine stars make a constellation. Your third star is a real one!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі значок «Майстер степенів», а {messy} обіцяє назвати на твою честь зорю.',
               'All three levels complete! {tidy} presents you with a "Powers Master" badge, and {messy} promises to name a star after you.'),
        meet=[['hostA', t('Керує станцією і пояснює уроки.', 'Runs the station and explains the lessons.')],
              ['hostB', t('Водить ракету й придумує підказки-віршики.', 'Flies the rocket and makes up rhymes.')],
              ['tidy', t('Робот. Любить, коли все по поличках.', 'A robot. Likes everything in its place.')],
              ['messy', t('Прибулець. Плутає все, але дуже допитливий.', 'An alien. Mixes everything up, but is very curious.')]],
    )
    W['bricks'] = dict(
        intro=t('Песик {messy} {g:messy:розкидав:розкидала} картки зі степенями по майданчику, а скриня з інструментами замкнена на вісім замків. Прочитай урок і пройди три рівні: розклади картки по ящиках, відімкни скриню й збудуй стіну.',
                '{messy} the puppy has scattered the power cards all over the building site, and the toolbox is locked with eight padlocks. Read the lesson, then play three levels: sort the cards into crates, unlock the toolbox and build a wall.'),
        tabA=t('1. Ящики', '1. Crates'), tabB=t('2. Скриня', '2. Toolbox'), tabC=t('3. Стіна', '3. Wall'),
        aH=t('Рівень 1. Три ящики', 'Level 1. Three crates'),
        aIntro=t('На кожному ящику написано правило: показники додаємо, віднімаємо або множимо. Поклади картку в потрібний ящик і запиши новий показник.',
                 'Each crate has a rule written on it: add, subtract or multiply the indices. Put each card in the right crate and write the new index.'),
        bH=t('Рівень 2. Скриня з інструментами', 'Level 2. The toolbox'),
        bIntro=t('Скриню замкнено на вісім замків. Кожен вираз запиши одним степенем, потім обчисли — і замок відімкнеться.',
                 'The toolbox has eight padlocks. Write each expression as one power, then work out its value, and a padlock opens.'),
        cH=t('Рівень 3. Стіна з цеглинок', 'Level 3. A brick wall'),
        cIntro=t('Числа різні, а основа одна. Переклади їх у степені однієї основи — і в стіні з’явиться нова цеглинка.',
                 'The numbers look different, but they share a base. Rewrite them as powers of the same base, and a new brick goes into the wall.'),
        aGood=t('Так!', 'Yes!'), bGood=t('Клац! Замок відімкнено.', 'Click! A padlock opens.'), cGood=t('Ще одна цеглинка на місці!', 'Another brick in place!'),
        aQuip=t('Майданчик блищить!', 'The site is spotless!'),
        bStageL=t('Відмикаємо замки по одному', 'One padlock at a time'), bOpen=t('Скриню відчинено!', 'The toolbox is open!'),
        bQuip=t('Тепер є всі інструменти!', 'Now we have every tool!'),
        cStageL=t('Кладемо стіну', 'Building the wall'), cQuip=t('Міцна стіна! {messy} махає хвостом.', 'A strong wall! {messy} is wagging.'),
        aDoneH=t('Усі картки в ящиках!', 'All the cards are in their crates!'),
        aDoneP=t('{messy} радісно {g:messy:гавкнув:гавкнула}: так охайно тут ще не було. Перша зірка твоя!', '{messy} barked happily: the site has never been this tidy. Your first star!'),
        bDoneH=t('Скриню відчинено!', 'The toolbox is open!'),
        bDoneP=t('{tidy} {g:tidy:поміряв:поміряла} кожен інструмент і {g:tidy:кивнув:кивнула}. Друга зірка твоя!', '{tidy} measured every tool and nodded. Your second star!'),
        cDoneH=t('Стіна готова!', 'The wall is finished!'),
        cDoneP=t('Дев’ять цеглинок рівно лягли одна на одну. Третя зірка твоя!', 'Nine bricks sit neatly on top of each other. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі медаль «Майстер степенів», а {messy} приносить найкращу кісточку.',
               'All three levels complete! {tidy} presents you with a "Powers Master" medal, and {messy} brings you the best bone.'),
        meet=[['hostA', t('Будує мости й пояснює уроки.', 'Builds bridges and explains the lessons.')],
              ['hostB', t('Будує вежі й придумує віршики.', 'Builds towers and makes up rhymes.')],
              ['tidy', t('Робот-інженерка. Усе міряє і рахує.', 'A robot engineer. Measures and counts everything.')],
              ['messy', t('Песик. Розкидає все, але дуже старається.', 'A puppy. Scatters everything, but tries really hard.')]],
    )
    common['worlds'] = W
    return common




def rights():
    return [
        (34, 'Кожному гарантується право на свободу думки і слова, на вільне вираження своїх поглядів і переконань.',
         'Ти можеш казати, що думаєш. А перш ніж поширювати, перевір, чи це правда.',
         'Everyone has the right to freedom of thought and speech, and to express their views and beliefs freely.',
         'You can say what you think. Before you share something, check that it’s true.'),
        (57, 'Кожному гарантується право знати свої права і обов’язки.',
         'Знання множиться, як степінь, коли ним діляться.',
         'Everyone has the right to know their rights and duties.', 'Knowledge multiplies like a power when people share it.'),
        (31, 'Кожному гарантується таємниця листування, телефонних розмов, телеграфної та іншої кореспонденції.',
         'Твої повідомлення — лише твої. Чужі теж не читай без дозволу.',
         'Everyone’s letters, phone calls and other messages are private.', 'Your messages are yours alone. Don’t read other people’s without asking.'),
        (53, 'Кожен має право на освіту.', 'Кожна розв’язана задача — це твоє право в дії.',
         'Everyone has the right to education.', 'Every problem you solve is that right in action.'),
        (34, 'Кожен має право вільно збирати, зберігати, використовувати і поширювати інформацію усно, письмово або в інший спосіб…',
         'Інформація розлітається, як степінь. Поширюй лише перевірене.',
         'Everyone has the right to collect, keep, use and share information freely, by word of mouth, in writing or in any other way.',
         'Information spreads like a power. Only share what you have checked.'),
        (28, 'Кожен має право на повагу до його гідності.',
         'Образа в мережі не стає меншою, коли її перешлють тисячу разів. Поважай інших.',
         'Everyone has the right to respect for their dignity.', 'An insult online doesn’t get smaller when it’s shared a thousand times. Respect others.'),
        (54, 'Громадянам гарантується свобода літературної, художньої, наукової і технічної творчості…',
         'Малювати, програмувати, винаходити — твоє право. А чужі малюнки без дозволу не поширюють.',
         'Citizens are guaranteed freedom of literary, artistic, scientific and technical creativity.',
         'Drawing, coding and inventing are your right. And you don’t share other people’s drawings without asking.'),
        (32, 'Ніхто не може зазнавати втручання в його особисте і сімейне життя, крім випадків, передбачених Конституцією України.',
         'Особисте — це особисте. Не викладай чужі фото без дозволу.',
         'No one’s private or family life may be interfered with, except in cases set out in the Constitution of Ukraine.',
         'Private means private. Don’t post other people’s photos without asking.'),
        (22, 'Права і свободи людини і громадянина, закріплені цією Конституцією, не є вичерпними.',
         'Права не лише ті, що записані в Конституції: цей список не закритий.',
         'The rights and freedoms set out in this Constitution are not the only ones.', 'Your rights aren’t limited to the ones written down: the list isn’t closed.'),
    ]


def why(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    return {'items': [
        (t('Чутки ростуть як степінь.', 'Rumours grow like powers.'),
         t('Якщо кожен перешле новину двом друзям, за 10 кроків її отримають 2¹⁰ = 1024 людини. Перш ніж пересилати, перевір, чи це правда.',
           'If everyone forwards a story to two friends, after 10 steps 2¹⁰ = 1024 people get it. Before you forward something, check that it’s true.')),
        (t('Великі числа — коротко.', 'Big numbers, written short.'),
         t('10⁶ — це мільйон. Степенями записують відстані в космосі й обсяг пам’яті в телефоні.',
           '10⁶ is a million. Powers are used to write distances in space and the memory in your phone.')),
        (t('Твої права.', 'Your rights.'),
         t('Стаття 57 Конституції України: «Кожному гарантується право знати свої права і обов’язки». Знання, як і степінь, швидко множиться, коли ним діляться.',
           'Article 57 of the Constitution of Ukraine says everyone has the right to know their rights and duties. Knowledge, like a power, multiplies fast when it is shared.')),
    ], 'dip': t('Тепер ти вмієш рахувати степені розумно і бачиш, як швидко росте те, що подвоюється.',
                'Now you can work with powers cleverly and see how fast anything that doubles grows.')}
