"""Topic: identities and whole expressions (Урок №11, узагальнення) — lesson cards, cheat sheet, three levels, world texts."""
from svgkit import Run, text, hand, arrow, line, circle, rect, path, svg, width, C
from fmt import X, P
from common import ROLE_SVG, pig

KEY = 'identities'


def say(world, role, s, flip=False):
    return f'<div class="say">{pig(ROLE_SVG[world][role], flip)}<p class="hand">{s}</p></div>'


def chip(x, y, s, ok, size=19):
    w = width(s, size) + 22
    col = 'l' if ok else 'b'
    return rect(x - w / 2, y - 22, w, 32, 'var(--cell)', col, 2.2, 10, None if ok else '6 4') + text(x, y, s, size, 'i', 'd', 'middle')


# ---------------------------------------------------------------- lesson cards
def cards(lang, world):
    t = lambda uk, en: uk if lang == 'uk' else en
    MUL = '·' if lang == 'uk' else '×'
    DV = ':' if lang == 'uk' else '÷'
    dec = (lambda s: s) if lang == 'uk' else (lambda s: s.replace(',', '.'))
    out = []
    # 1. whole expressions
    b = hand(86, 26, t('цілі вирази', 'whole expressions'), 23, 'l') + hand(254, 26, t('не цілі', 'not whole'), 23, 'b')
    for k, s in enumerate(['3a² − 5b', f'(x + 1) {DV} 2', dec('0,5m³ + 7')]):
        b += chip(86, 70 + k * 46, s, True)
    for k, s in enumerate([f'5 {DV} x', f'7 {DV} (a + b)', f'a² {DV} b']):
        b += chip(254, 70 + k * 46, s, False)
    b += line(170, 44, 170, 170, 'line', 1.5, '4 4')
    b += hand(170, 200, t('ділимо на букву — уже не цілий', 'divide by a letter: not whole any more'), 21, 'm')
    s1 = svg(340, 210, b, t('цілі й не цілі вирази', 'whole and not whole expressions'))
    out.append(('', t('Цілі вирази', 'Whole expressions'),
                t('<b>Цілий вираз</b> складають із чисел і букв за допомогою +, −, ·, степенів і ділення <b>на число</b>.',
                  'A <b>whole expression</b> is built from numbers and letters with +, −, ×, powers and division <b>by a number</b>.'),
                s1, f'<p class="tail">{t("Одночлен — найпростіший цілий вираз: лише множення.", "A monomial is the simplest whole expression: multiplication only.")}</p>'))
    # 2. identity table
    b = ''
    hdr = ['a', '2(a + 3)', '2a + 6']
    xs = [50, 150, 260]
    for x, h in zip(xs, hdr):
        b += text(x, 34, h, 20, 'p' if h == 'a' else 'i', 'd', 'middle')
    b += line(16, 46, 324, 46, 'line', 2)
    for k, a in enumerate([1, 2, 5]):
        y = 80 + k * 38
        v = 2 * (a + 3)
        b += text(50, y, str(a), 20, 'p', 'd', 'middle') + text(150, y, str(v), 20, 'y', 'd', 'middle') + text(260, y, str(2 * a + 6), 20, 'y', 'd', 'middle')
        b += text(205, y, '=', 20, 'l', 'd', 'middle')
    b += hand(170, 200, t('для будь-якого a — однаково!', 'the same for any a!'), 23, 'l')
    s2 = svg(340, 212, b, '2(a + 3) = 2a + 6')
    out.append(('', t('Тотожність', 'An identity'),
                t('<b>Тотожність</b> — рівність, правильна за <b>будь-яких</b> значень букв. Наприклад, 2(a + 3) = 2a + 6.',
                  'An <b>identity</b> is an equation that is true for <b>every</b> value of the letters. For example, 2(a + 3) = 2a + 6.'),
                s2, f'<p class="tail">{t("У британських підручниках тотожність позначають знаком ≡.", "In UK textbooks an identity is written with the sign ≡.")}</p>'
                + say(world, 'hostB', t('Таблиця — лише перевірка. Довести можна тільки перетвореннями.', 'A table is only a check. You prove it by changing the expression.'), True)))
    # 3. KEY: how to prove
    b = ''
    r1 = Run([('3(x − y) + 2(x + y) − x', 'k', 'n')], 170, 36, 24, 'middle')
    r2 = Run([('3x − 3y + 2x + 2y − x', 'k', 'n')], 170, 106, 24, 'middle')
    r3 = Run([('4x', 'y', 'n'), (' − ', 'k', 'n'), ('y', 'p', 'n')], 170, 176, 30, 'middle')
    b += r1.svg + r2.svg + r3.svg
    b += arrow(170, 48, 170, 84, 'y', 0) + hand(180, 72, t('① розкрий дужки', '① expand the brackets'), 21, 'y', 'start')
    b += arrow(170, 118, 170, 150, 'y', 0) + hand(180, 140, t('② зведи подібні', '② collect like terms'), 21, 'y', 'start')
    b += hand(58, 170, '3x + 2x − x = 4x', 17, 'k') + hand(58, 192, '−3y + 2y = −y', 17, 'k')
    s3 = svg(340, 202, b, '3(x − y) + 2(x + y) − x = 4x − y')
    out.append(('key wide two', t('Головне: як довести тотожність', 'Key rule: how to prove an identity'),
                t('<b>Перетворюй одну частину, доки вона не стане такою, як інша.</b> ① Розкрий дужки. ② Зведи подібні доданки.',
                  '<b>Change one side step by step until it looks exactly like the other.</b> ① Expand the brackets. ② Collect like terms.'),
                s3, say(world, 'tidy', t('Крок за кроком, без стрибків — і ніхто не засумнівається!', 'Step by step, no jumps, and nobody can doubt it!'))))
    # 4. counterexample
    b = Run([('(a + b)', 'i', 'n'), ('2', 'y', 's'), (' = a', 'i', 'n'), ('2', 'y', 's'), (' + b', 'i', 'n'), ('2', 'y', 's'), (' ?', 'h', 'n')], 170, 38, 26, 'middle').svg
    b += hand(170, 76, t('візьмемо a = 1, b = 1', 'try a = 1, b = 1'), 22, 'm')
    b += text(90, 120, '(1 + 1)² = 4', 22, 'y', 'd', 'middle') + text(250, 120, '1² + 1² = 2', 22, 'p', 'd', 'middle')
    b += text(170, 122, '≠', 30, 'b', 'd', 'middle')
    b += hand(170, 166, t('4 ≠ 2 — не тотожність!', '4 ≠ 2: not an identity!'), 25, 'b')
    s4 = svg(340, 180, b, '(a + b)² ≠ a² + b²')
    out.append(('', t('Одного контрприкладу досить', 'One counterexample is enough'),
                t('Щоб показати, що рівність <b>не</b> тотожність, досить одного набору чисел, де вона хибна.',
                  'To show an equation is <b>not</b> an identity, one set of numbers where it fails is enough.'),
                s4, say(world, 'messy', t('Я думав, (a + b)² = a² + b². Одне число — і все ясно!', 'I thought (a + b)² = a² + b². One example, and it’s clear!'), True)))
    # 5. block
    b = rect(110, 14, 120, 44, 'var(--cell)', 'h', 3, 12) + text(170, 44, '2ab = 7', 22, 'h', 'd', 'middle')
    b += text(90, 112, f'6ab = 3 {MUL} (2ab)', 20, 'i', 'd', 'middle') + text(90, 146, f'= 3 {MUL} 7 = 21', 20, 'l', 'd', 'middle')
    b += text(252, 112, '4a²b² = (2ab)²', 20, 'i', 'd', 'middle') + text(252, 146, '= 7² = 49', 20, 'l', 'd', 'middle')
    b += arrow(140, 60, 100, 92, 'h', 0.15) + arrow(200, 60, 242, 92, 'h', -0.15)
    b += hand(170, 186, t('a і b шукати не треба!', 'no need to find a and b!'), 22, 'm')
    s5 = svg(340, 198, b, '2ab = 7')
    out.append(('', t('Рахуй блоком', 'Use the block'),
                t('Знаєш значення цілого «блоку»? Склади з нього потрібний вираз: помнож або піднеси до степеня.',
                  'Know the value of a whole "block"? Build the expression you need from it: multiply it or raise it to a power.'),
                s5, f'<p class="tail">{t("Щоб побачити блок, розклади числа: 4 = 2², 6 = 3 · 2.", "To spot the block, split the numbers: 4 = 2², 6 = 3 × 2.")}</p>'))
    # 6. smallest value
    b = ''
    for k, (lab, base) in enumerate([('(x − 1)²', 0), ('(x − 1)² + 3', 3)]):
        y = 56 + k * 74
        b += line(30, y, 320, y, 'i', 2.5) + text(18, y - 16, lab, 18, 'p', 'd', 'start')
        for v in range(0, 7):
            x = 50 + v * 42
            b += line(x, y - 6, x, y + 6, 'i', 2) + text(x, y + 26, str(v), 15, 'm', 'd', 'middle')
        x0 = 50 + base * 42
        b += circle(x0, y, 7, 'var(--yarn)', 'y', 0) + path(f'M{x0} {y} H316', 'y', 6, extra=' opacity=".45"')
    b += arrow(50, 70, 176, 118, 'h', -0.2) + hand(150, 96, '+3', 22, 'h')
    b += hand(170, 196, t('найменше значення 3 — коли x = 1', 'smallest value 3, when x = 1'), 22, 'l')
    s6 = svg(340, 206, b, '(x − 1)² + 3 ≥ 3')
    out.append(('wide two', t('Найменше значення', 'The smallest value'),
                t('Квадрат (і будь-який парний степінь) не буває від’ємним: <b>x² ≥ 0</b>. Тож (x − 1)² + 3 ≥ 3.',
                  'A square (and any even power) is never negative: <b>x² ≥ 0</b>. So (x − 1)² + 3 ≥ 3.'),
                s6, f'<p class="tail">{t("Найменше значення досягається, коли дужка дорівнює нулю: x = 1.", "The smallest value happens when the bracket is zero: x = 1.")}</p>'))
    # 7. comparing powers
    b = Run([('2', 'p', 'n'), ('15', 'y', 's'), ('  ?  ', 'h', 'n'), ('3', 'p', 'n'), ('10', 'y', 's')], 170, 40, 30, 'middle').svg
    b += text(90, 104, '(2³)⁵ = 8⁵', 22, 'i', 'd', 'middle') + text(250, 104, '(3²)⁵ = 9⁵', 22, 'i', 'd', 'middle')
    b += arrow(126, 50, 104, 82, 'p', 0.1) + arrow(214, 50, 236, 82, 'p', -0.1)
    b += text(170, 160, '8⁵ < 9⁵', 30, 'l', 'd', 'middle')
    b += hand(170, 194, t('показники однакові — порівнюй основи', 'same index? compare the bases'), 21, 'm')
    s7 = svg(340, 204, b, '2¹⁵ < 3¹⁰')
    out.append(('', t('Порівняння степенів', 'Comparing powers'),
                t('Зведи степені до <b>однакового показника</b> (або однакової основи) — і порівнювати стане легко.',
                  'Rewrite the powers with the <b>same index</b> (or the same base), and comparing becomes easy.'),
                s7, f'<p class="tail">{t("Отже, 2¹⁵ < 3¹⁰. Перевірка: 32 768 < 59 049.", "So 2¹⁵ < 3¹⁰. Check: 32,768 < 59,049.")}</p>'))
    # 8. divisibility
    b = Run([('n', 'p', 'n'), (' + ', 'i', 'n'), ('(n + 1)', 'p', 'n'), (' + ', 'i', 'n'), ('(n + 2)', 'p', 'n')], 170, 40, 24, 'middle').svg
    b += arrow(170, 52, 170, 84, 'y', 0) + text(170, 110, '= 3n + 3', 26, 'i', 'd', 'middle')
    b += arrow(170, 120, 170, 148, 'y', 0) + Run([('= ', 'i', 'n'), ('3', 'l', 'n'), ('(n + 1)', 'i', 'n')], 170, 176, 30, 'middle').svg
    b += hand(270, 150, t('множник 3!', 'a factor of 3!'), 23, 'l')
    s8 = svg(340, 190, b, 'n + (n + 1) + (n + 2) = 3(n + 1)')
    out.append(('', t('Доведення подільності', 'Proving divisibility'),
                t('Сума трьох послідовних натуральних чисел ділиться на 3. Доводимо для <b>будь-якого</b> n, а не для кількох прикладів.',
                  'The sum of three consecutive whole numbers is divisible by 3. We prove it for <b>any</b> n, not just a few examples.'),
                s8, f'<p class="tail">{t("Винесли спільний множник 3 — отже, ділиться на 3.", "We took out the common factor 3, so it divides by 3.")}</p>'))
    # 9. fence
    b = rect(70, 50, 200, 100, 'var(--cell)', 'l', 3, 8)
    b += text(170, 40, 'a', 22, 'p', 'd', 'middle') + text(170, 176, 'a', 22, 'p', 'd', 'middle')
    b += text(54, 108, 'b', 22, 's', 'd', 'middle') + text(286, 108, 'b', 22, 's', 'd', 'middle')
    b += text(170, 96, '2(a + b)', 22, 'y', 'd', 'middle') + text(170, 124, '= 2a + 2b', 22, 'y', 'd', 'middle')
    s9 = svg(340, 190, b, 'P = 2(a + b) = 2a + 2b')
    out.append(('wide two', t('Тотожності в житті', 'Identities in real life'),
                t('Паркан для вольєра: можна обійти «довжина + ширина» двічі, а можна додати дві довжини й дві ширини. Відповідь та сама — це тотожність.',
                  'A fence round a pen: you can go "length + width" twice, or add two lengths and two widths. Same answer: that’s an identity.'),
                s9, f'<p class="tail">{t("Тотожності дозволяють рахувати зручнішим способом і бути певними, що відповідь не зміниться.", "Identities let you choose the easier way and be sure the answer won’t change.")}</p>'))
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
        title=t('Шпаргалка: тотожності й вирази', 'Cheat sheet: identities'),
        h1=t('Тотожності й вирази <span>на одній сторінці</span>', 'Identities and expressions <span>on one page</span>'),
        bubble=t('Привіт! Тут повторення перед контрольною: тотожності, рахунок «блоком», найменше значення, порівняння степенів і доведення.',
                 'Hi! Here is the revision before the test: identities, using a "block", the smallest value, comparing powers and proofs.'),
        cast=[pig(ROLE_SVG[w][r], r == 'hostB') for r in ('hostA', 'hostB', 'tidy', 'messy')],
        cards=cards(lang, w), final_svg=pig(ROLE_SVG[w]['tidy']),
        final=t('Самоперевірка: підстав у відповідь одне-два числа. Не збіглося — шукай помилку. Збіглося — доведи перетвореннями.',
                'Check yourself: put one or two numbers into your answer. Don’t match? Look for the mistake. Match? Prove it by rewriting.'))


# ---------------------------------------------------------------- levels
def levels(lang, edition):
    t = lambda uk, en: uk if lang == 'uk' else en
    x = lambda s: X(s, lang)
    p = lambda s: P(s, lang)
    MUL = '·' if lang == 'uk' else '×'
    NL = '<span class="gap"></span>'
    # ---- level A: identity or not
    A = [  # left, right, values text, left value, right value, identity?, proof/counter text, teacher
        ('2(a + b − c) + 3(a − c) − 2b', '5(a − c)', 'a = 3, b = 1, c = 1', 10, 10, True,
         '2a + 2b − 2c + 3a − 3c − 2b = 5a − 5c = 5(a − c)', True,
         t('ліва: 2 · (3 + 1 − 1) + 3 · (3 − 1) − 2 · 1', 'left: 2 · (3 + 1 − 1) + 3 · (3 − 1) − 2 · 1')),
        ('(a + b)^2', 'a^2 + b^2', 'a = 1, b = 2', 9, 5, False, '', False, t('ліва: (1 + 2)² = 3²; права: 1 + 4', 'left: (1 + 2)² = 3²; right: 1 + 4')),
        ('3(x − 2)', '3x − 6', 'x = 5', 9, 9, True, '3(x − 2) = 3 · x − 3 · 2 = 3x − 6', False, t('ліва: 3 · (5 − 2); права: 3 · 5 − 6', 'left: 3 · (5 − 2); right: 3 · 5 − 6')),
        ('x^3 · x^2', 'x^6', 'x = 2', 32, 64, False, '', False, t('ліва: 8 · 4; права: 2⁶ = 64', 'left: 8 · 4; right: 2⁶ = 64')),
        ('(2a)^3', '8a^3', 'a = −1', -8, -8, True, '(2a)³ = 2³ · a³ = 8a³', False, t('ліва: (2 · (−1))³ = (−2)³; права: 8 · (−1)³', 'left: (2 · (−1))³ = (−2)³; right: 8 · (−1)³')),
        ('−a^2', '(−a)^2', 'a = 3', -9, 9, False, '', False, t('ліва: −(3²) = −9; права: (−3)² = (−3) · (−3)', 'left: −(3²) = −9; right: (−3)² = (−3) · (−3)')),
        ('4(m + 1) − 4', '4m', 'm = 7', 28, 28, True, '4(m + 1) − 4 = 4m + 4 − 4 = 4m', False, t('ліва: 4 · 8 − 4; права: 4 · 7', 'left: 4 · 8 − 4; right: 4 · 7')),
        ('(x^2)^3', 'x^5', 'x = 2', 64, 32, False, '', False, t('ліва: (2²)³ = 4³; права: 2⁵', 'left: (2²)³ = 4³; right: 2⁵')),
    ]
    TA = []
    for i, (l, r, vals, lv, rv, ident, proof, teach, h2) in enumerate(A):
        h2 = h2.replace(' · ', f' {MUL} ')
        after = (t('Тотожність. Доведення: ', 'An identity. Proof: ') + x(l) + ' = ' + x(proof.split(' = ', 1)[1]) if ident else
                 t(f'Не тотожність: за {vals} ліва частина {lv}, а права {rv}.', f'Not an identity: when {vals}, the left side is {lv} and the right side is {rv}.').replace('-', '−'))
        TA.append(dict(teacher=teach, q=t('Чи є рівність тотожністю?', 'Is this equation an identity?'), show=x(l + ' = ' + r), steps=[
            dict(type='num', p=t(f'Перевір числами: {vals}.', f'Test it with numbers: {vals}.'),
                 f=[{'pre': '<span class="lbl">' + t('ліва частина', 'left side') + '</span> =', 'ans': lv, 'n': 'left', 'aria': t('ліва частина', 'left side')},
                    {'pre': NL + '<span class="lbl">' + t('права частина', 'right side') + '</span> =', 'ans': rv, 'n': 'right', 'aria': t('права частина', 'right side')}],
                 traps=[[0, -lv, 'left-sign'], [1, -rv, 'right-sign']] if lv and rv else [],
                 h=[t('підстав числа замість букв і рахуй кожну частину окремо. Спершу дужки й степені.', 'put the numbers in place of the letters and work out each side separately. Brackets and powers first.'), h2],
                 ok=t(f'ліва = {lv}, права = {rv}', f'left = {lv}, right = {rv}').replace('-', '−')),
            dict(type='choice', style='pills', p=t('Тож чи тотожність?', 'So is it an identity?'),
                 opts=[['yes', t('Тотожність', 'Identity')], ['no', t('Не тотожність', 'Not an identity')]], ans='yes' if ident else 'no',
                 tag={'yes': 'not-identity-as-identity', 'no': 'identity-as-not'},
                 h=[t('різні значення — точно не тотожність. Однакові — ще не доказ: перевір перетворенням.', 'different values: definitely not an identity. The same: not proof yet, so check by rewriting.'),
                    (t('спробуй розкрити дужки в лівій частині.', 'try expanding the brackets on the left.') if ident else t('ти вже бачиш різні числа зліва й справа.', 'you can already see different numbers on the two sides.'))],
                 ok=t('Тотожність', 'Identity') if ident else t('Не тотожність', 'Not an identity'))],
            after=after, label=p(l + ' = ' + r) + ' — ' + (t('тотожність', 'identity') if ident else t('ні', 'not an identity'))))
    # ---- level B: the block
    block_f = lambda blk: [{'pre': x('='), 'ans': None, 'n': 'k', 'aria': t('множник', 'factor')}]
    B = [  # block, value, target, k (list of accepted), n, result (list), teacher, k hint, value hint
        ('5xy^2', 9, 'xy^2', [0.2], 1, [1.8], True, t('xy² — це п’ята частина від 5xy².', 'xy² is one fifth of 5xy².'), '9 : 5 = ?'),
        ('5xy^2', 9, '7xy^2', [1.4], 1, [12.6], True, t('7xy² = 7 : 5 · (5xy²). Множник 7/5.', '7xy² = 7 ÷ 5 × (5xy²). The factor is 7/5.'), '7/5 · 9 = 63/5 = ?'),
        ('5xy^2', 9, '−25x^2y^4', [-1], 2, [-81], True, t('25x²y⁴ = (5xy²)², а мінус лишається спереду: −1 · (…)².', '25x²y⁴ = (5xy²)², and the minus stays in front: −1 × (…)².'), '−(9²) = ?'),
        ('5xy^2', 9, '125x^3y^6', [1], 3, [729], True, t('125 = 5³, а показники x і y — утричі більші.', '125 = 5³, and the indices of x and y are three times bigger.'), '9³ = 9 · 9 · 9 = ?'),
        ('4m^2n', 9, '12m^2n', [3], 1, [27], True, t('12 = 3 · 4.', '12 = 3 × 4.'), '3 · 9 = ?'),
        ('4m^2n', 9, '4m^4n^2', [0.25], 2, [20.25], True, t('(4m²n)² = 16m⁴n². А нам треба 4m⁴n² — це чверть.', '(4m²n)² = 16m⁴n². We need 4m⁴n², which is a quarter of it.'), '81 : 4 = ?'),
        ('5x^2y^4', 6, '25x^4y^8', [1], 2, [36], True, t('25 = 5², а показники вдвічі більші.', '25 = 5², and the indices are twice as big.'), '6² = ?'),
        ('3a^2b', 4, '−6a^2b', [-2], 1, [-8], False, t('−6 = −2 · 3.', '−6 = −2 × 3.'), '−2 · 4 = ?'),
    ]
    TB = []
    for i, (blk, val, tgt, k, n, res, teach, kh, vh) in enumerate(B):
        kh, vh = kh.replace(' · ', f' {MUL} '), vh.replace(' · ', f' {MUL} ').replace(' : ', ' ÷ ' if lang == 'en' else ' : ')
        kk = k[0]
        kstr = {0.2: '1/5', 1.4: '7/5', 0.25: '1/4'}.get(kk, str(kk))
        if lang == 'uk':
            kstr2 = {0.2: '0,2', 1.4: '1,4', 0.25: '0,25'}.get(kk, kstr)
        else:
            kstr2 = {0.2: '0.2', 1.4: '1.4', 0.25: '0.25'}.get(kk, kstr)
        rs = str(res[0]).replace('.0', '') if float(res[0]).is_integer() else (str(res[0]).replace('.', ',') if lang == 'uk' else str(res[0]))
        rs = rs.replace('-', '−')
        TB.append(dict(teacher=teach, q=t('Відомо: ', 'We know: ') + x(f'{blk} = {val}') + t('. Знайди значення виразу:', '. Find the value of:'), show=x(tgt),
                       block=x(f'{blk} = {val}'), steps=[
            dict(type='num', p=t('Склади вираз із блоку:', 'Build it from the block:'),
                 f=[{'pre': x(tgt) + ' =', 'ans': k + ([round(kk)] if False else []), 'n': 'k', 'aria': t('множник', 'factor')},
                    {'pre': MUL + ' (' + x(blk) + ')', 'sup': True, 'ans': n, 'n': 'n', 'aria': t('показник', 'index')}],
                 traps=[[1, 1, 'power-missed']] if n > 1 else [[0, 1, 'factor-missed']],
                 tip=t('Дріб можна писати так: 1/5 або 0,2.', 'You can type a fraction like 1/5 or 0.2.'),
                 h=[t('подивись, у скільки разів більші числа й показники, ніж у блоці.', 'look at how many times bigger the number and the indices are than in the block.'), kh],
                 ok=x(tgt) + ' = ' + (f'{kstr2} {MUL} ' if kk != 1 else ('−' if False else '')) + ('(' + x(blk) + ')' + (f'<sup>{n}</sup>' if n > 1 else ''))),
            dict(type='num', p=t('Тепер підстав значення блоку:', 'Now put in the value of the block:'),
                 f=[{'pre': x(tgt) + ' =', 'ans': res, 'wide': True, 'n': 'value', 'aria': t('значення', 'value')}],
                 traps=[[0, -res[0], 'value-sign']] if res[0] else [],
                 h=[t('блок дорівнює ', 'the block equals ') + str(val) + t('. Підстав і порахуй.', '. Put it in and work it out.'), vh],
                 ok=x(tgt) + ' = ' + rs)],
            after=x(tgt) + ' = ' + rs + '.', label=p(f'{blk} = {val} → {tgt} = ') + rs))
    # fix the "−1 ·" display for k = −1 in the ok text
    for tb in TB:
        tb['steps'][0]['ok'] = tb['steps'][0]['ok'].replace(f'−1 {MUL} ', '−')
    # ---- level C: proofs workshop
    mono = lambda coef, letters: [{'pre': '', 'ans': coef, 'n': 'coef', 'aria': t('коефіцієнт', 'coefficient')}] + \
        [{'pre': f'<span class="b">{l}</span>', 'sup': True, 'ans': e, 'n': 'exp-' + l, 'aria': t('показник', 'index')} for l, e in letters]
    TC = []
    TC.append(dict(teacher=True, q=t('Якого найменшого значення може набувати вираз?', 'What is the smallest value of this expression?'), show=x('m^4 − 12'), steps=[
        dict(type='num', p=t('Найменше значення:', 'The smallest value:'), f=[{'pre': '', 'ans': -12, 'n': 'min', 'aria': t('значення', 'value')}], traps=[[0, 12, 'sign'], [0, 0, 'zero']],
             h=[t('m⁴ ≥ 0 за будь-якого m. Яке найменше значення m⁴?', 'm⁴ ≥ 0 for any m. What is the smallest value of m⁴?'), t('найменше m⁴ = 0, тоді 0 − 12 = ?', 'the smallest m⁴ is 0, so 0 − 12 = ?')], ok='−12')],
        after=t('m⁴ ≥ 0, тож m⁴ − 12 ≥ −12. Найменше значення −12 (коли m = 0).', 'm⁴ ≥ 0, so m⁴ − 12 ≥ −12. The smallest value is −12 (when m = 0).'), label=p('m^4 − 12: min = −12')))
    TC.append(dict(teacher=True, q=t('Якого найменшого значення може набувати вираз?', 'What is the smallest value of this expression?'), show=x('(a + 2)^8 + 7'), steps=[
        dict(type='num', p=t('Найменше значення:', 'The smallest value:'), f=[{'pre': '', 'ans': 7, 'n': 'min', 'aria': t('значення', 'value')}], traps=[[0, 9, 'added-2'], [0, 0, 'zero']],
             h=[t('(a + 2)⁸ — парний степінь, він ≥ 0.', '(a + 2)⁸ is an even power, so it is ≥ 0.'), '0 + 7 = ?'], ok='7'),
        dict(type='num', p=t('А за якого a це буває?', 'And for which a does it happen?'), f=[{'pre': 'a =', 'ans': -2, 'n': 'a', 'aria': 'a'}], traps=[[0, 2, 'sign']],
             h=[t('коли дужка дорівнює нулю.', 'when the bracket is zero.'), 'a + 2 = 0 → a = ?'], ok='a = −2')],
        after=t('(a + 2)⁸ + 7 ≥ 7, найменше значення 7 — коли a = −2.', '(a + 2)⁸ + 7 ≥ 7; the smallest value is 7, when a = −2.'), label=p('(a + 2)^8 + 7: min = 7')))
    cmp_opts = [['lt', '&lt;'], ['eq', '='], ['gt', '&gt;']]
    TC.append(dict(teacher=True, q=t('Порівняй вирази:', 'Compare the expressions:'), show=x('{5|12}  і  {25|6}') if lang == 'uk' else x('{5|12}  and  {25|6}'), steps=[
        dict(type='num', p=t('Переклади 25⁶ у степінь п’ятірки:', 'Write 25⁶ as a power of 5:'), f=[{'pre': x('{25|6} = (5^2)^6 = ') + '<span class="b">5</span>', 'sup': True, 'ans': 12, 'n': 'exp'}],
             traps=[[0, 8, 'exp-added']], h=[t('25 = 5², а степінь степеня — показники множимо.', '25 = 5², and for a power of a power you multiply the indices.'), '2 · 6 = ?'], ok=x('{25|6} = {5|12}')),
        dict(type='choice', style='pills big', p=x('{5|12}  ?  {25|6}'), opts=cmp_opts, ans='eq', h=[t('порівняй 5¹² і 5¹².', 'compare 5¹² with 5¹².'), t('це той самий степінь.', 'it’s the same power.')], ok='5¹² = 25⁶')],
        after='5¹² = 25⁶.', label=p('5^12 = 25^6')))
    TC.append(dict(teacher=True, q=t('Порівняй вирази:', 'Compare the expressions:'), show=x('{2|30}  і  {3|20}') if lang == 'uk' else x('{2|30}  and  {3|20}'), steps=[
        dict(type='num', p=t('Зведи до однакового показника 10:', 'Rewrite both with the index 10:'),
             f=[{'pre': x('{2|30} = ({2|3})^10 = ') + '<span class="b">8</span>', 'sup': True, 'ans': 10, 'n': 'exp1'},
                {'pre': NL + x('{3|20} = ({3|2})^10 = ') + '<span class="b">9</span>', 'sup': True, 'ans': 10, 'n': 'exp2'}],
             h=[t('2³ = 8, 3² = 9. Показники множимо.', '2³ = 8 and 3² = 9. Multiply the indices.'), '3 · 10 = 30; 2 · 10 = 20'], ok=x('{8|10} і {9|10}') if lang == 'uk' else x('{8|10} and {9|10}')),
        dict(type='choice', style='pills big', p=x('{2|30}  ?  {3|20}'), opts=cmp_opts, ans='lt',
             h=[t('показники однакові (10), тож порівняй основи 8 і 9.', 'the indices are the same (10), so compare the bases 8 and 9.'), t('8 менше за 9.', '8 is less than 9.')], ok='2³⁰ &lt; 3²⁰')],
        after=t('8¹⁰ < 9¹⁰, отже 2³⁰ < 3²⁰.', '8¹⁰ < 9¹⁰, so 2³⁰ < 3²⁰.'), label=p('2^30 < 3^20')))
    cards_odd = [t('Нехай числа: 2n + 1, 2n + 3, 2n + 5', 'Let the numbers be 2n + 1, 2n + 3, 2n + 5'),
                 t('Сума: (2n + 1) + (2n + 3) + (2n + 5)', 'Sum: (2n + 1) + (2n + 3) + (2n + 5)'), '= 6n + 9', '= 3(2n + 3)',
                 t('Є множник 3, тож сума ділиться на 3', 'There is a factor of 3, so the sum divides by 3')]
    TC.append(dict(teacher=True, q=t('Доведи: сума трьох послідовних непарних натуральних чисел ділиться на 3.', 'Prove: the sum of three consecutive odd whole numbers is divisible by 3.'), show='', steps=[
        dict(type='order', p=t('Склади доведення: натискай картки по черзі.', 'Build the proof: tap the cards in order.'), cards=cards_odd, mix=[2, 4, 0, 3, 1],
             h=[t('спершу познач числа буквою, потім запиши суму, спрости й винеси множник.', 'first name the numbers with a letter, then write the sum, simplify and take out the factor.'),
                t('перша картка — «Нехай числа…», остання — висновок.', 'the first card is "Let the numbers be…", the last is the conclusion.')], ok=t('Доведено!', 'Proved!'))],
        after=t('2n + 1 + 2n + 3 + 2n + 5 = 6n + 9 = 3(2n + 3).', '2n + 1 + 2n + 3 + 2n + 5 = 6n + 9 = 3(2n + 3).'), label=t('Доведення: сума трьох непарних ділиться на 3', 'Proof: three odd numbers sum to a multiple of 3')))
    TC.append(dict(teacher=True, q=t('Спрости вираз:', 'Simplify:'), show=x('0,2a^2b · (−10ab^3)^2'), steps=[
        dict(type='num', p=t('Спершу дужка в квадраті:', 'First the bracket squared:'), f=[dict(mono(100, [('a', 2), ('b', 6)])[0], pre=x('(−10ab^3)^2 =') + NL), *mono(100, [('a', 2), ('b', 6)])[1:]],
             traps=[[0, -100, 'coef-sign'], [0, -20, 'coef-times-n'], [2, 5, 'exp-added']],
             h=[t('квадрат кожного множника: (−10)², a², (b³)².', 'square every factor: (−10)², a², (b³)².'), t('(−10)² = 100; показник у b: 3 · 2', '(−10)² = 100; index of b: 3 × 2')], ok=x('(−10ab^3)^2 = 100a^2b^6')),
        dict(type='num', p=t('Тепер перемнож:', 'Now multiply:'), f=[dict(mono(20, [('a', 4), ('b', 7)])[0], pre=x('0,2a^2b · 100a^2b^6 =') + NL), *mono(20, [('a', 4), ('b', 7)])[1:]],
             traps=[[2, 6, 'exp-forgot-hidden-1']],
             h=[t('числа множимо, показники однакових букв додаємо.', 'multiply the numbers and add the indices of matching letters.'), t('0,2 · 100 = 20; a: 2 + 2; b: 1 + 6', '0.2 × 100 = 20; a: 2 + 2; b: 1 + 6')], ok=x('20a^4b^7'))],
        after=x('0,2a^2b · 100a^2b^6 = 20a^4b^7'), label=p('0,2a^2b · (−10ab^3)^2 = 20a^4b^7')))
    TC.append(dict(teacher=True, q=t('Який одночлен стандартного вигляду треба записати замість зірочки?', 'Which monomial in simplest form should replace the star?'), show=x('* · 3m^2n^3 = 15m^3n^8'), steps=[
        dict(type='num', p='', f=[dict(mono(5, [('m', 1), ('n', 5)])[0], pre='* ='), *mono(5, [('m', 1), ('n', 5)])[1:]], traps=[[0, 45, 'coef-multiplied'], [0, 12, 'coef-subtracted'], [2, 11, 'exp-added']],
             h=[t('* = добуток : відомий множник. Числа ділимо, показники віднімаємо.', '* = product ÷ known factor. Divide the numbers, subtract the indices.'), t('15 : 3; m: 3 − 2; n: 8 − 3', '15 ÷ 3; m: 3 − 2; n: 8 − 3')], ok=x('* = 5mn^5'))],
        after=x('5mn^5 · 3m^2n^3 = 15m^3n^8 ✓'), label=p('* · 3m^2n^3 = 15m^3n^8 → * = 5mn^5')))
    TC.append(dict(teacher=True, q=t('Спрости вираз:', 'Simplify:'), show=x('(10m^2n)^2 · (3mn^2)^3'), steps=[
        dict(type='num', p=t('Кожну дужку окремо:', 'Each bracket separately:'),
             f=[dict(mono(100, [('m', 4), ('n', 2)])[0], pre=x('(10m^2n)^2 =') + NL), *mono(100, [('m', 4), ('n', 2)])[1:],
                dict(mono(27, [('m', 3), ('n', 6)])[0], pre=NL + x('(3mn^2)^3 =') + NL), *mono(27, [('m', 3), ('n', 6)])[1:]],
             traps=[[0, 20, 'coef-times-n'], [3, 9, 'coef-times-n']],
             h=[t('показник за дужкою — кожному множнику: число в степінь, показники букв множимо.', 'the index outside goes to every factor: raise the number, multiply the letters’ indices.'), '10² = 100; 3³ = 27'], ok=x('100m^4n^2 · 27m^3n^6')),
        dict(type='num', p=t('Тепер перемнож:', 'Now multiply:'), f=[dict(mono(2700, [('m', 7), ('n', 8)])[0], pre=x('100m^4n^2 · 27m^3n^6 =') + NL), *mono(2700, [('m', 7), ('n', 8)])[1:]], traps=[[0, 127, 'coef-added']],
             h=[t('числа множимо, показники додаємо.', 'multiply the numbers, add the indices.'), t('100 · 27; m: 4 + 3; n: 2 + 6', '100 × 27; m: 4 + 3; n: 2 + 6')], ok=x('2700m^7n^8'))],
        after=x('(10m^2n)^2 · (3mn^2)^3 = 2700m^7n^8'), label=p('(10m^2n)^2 · (3mn^2)^3 = 2700m^7n^8')))
    cards_two = [t('Нехай числа: 2n + 1 і 2n + 3', 'Let the numbers be 2n + 1 and 2n + 3'), t('Сума: (2n + 1) + (2n + 3)', 'Sum: (2n + 1) + (2n + 3)'),
                 '= 4n + 4', '= 4(n + 1)', t('Є множник 4, тож сума ділиться на 4', 'There is a factor of 4, so the sum divides by 4')]
    TC.append(dict(teacher=False, q=t('Доведи: сума двох послідовних непарних чисел ділиться на 4.', 'Prove: the sum of two consecutive odd numbers is divisible by 4.'), show='', steps=[
        dict(type='order', p=t('Склади доведення: натискай картки по черзі.', 'Build the proof: tap the cards in order.'), cards=cards_two, mix=[3, 0, 4, 2, 1],
             h=[t('так само, як у попередньому доведенні.', 'just like the previous proof.'), t('після «Нехай…» іде сума, далі спрощення.', 'after "Let…" comes the sum, then simplifying.')], ok=t('Доведено!', 'Proved!'))],
        after=t('(2n + 1) + (2n + 3) = 4n + 4 = 4(n + 1).', '(2n + 1) + (2n + 3) = 4n + 4 = 4(n + 1).'), label=t('Доведення: сума двох непарних ділиться на 4', 'Proof: two odd numbers sum to a multiple of 4')))
    for L in (TA, TB, TC):
        for s in [s for tk in L for s in tk['steps']]:
            s.setdefault('traps', [])
    for i, tk in enumerate(TA):
        tk['label'] = t(f'Справа {i + 1}: ', f'Case {i + 1}: ') + tk['label']
    for i, tk in enumerate(TB):
        tk['label'] = t(f'Блок {i + 1}: ', f'Block {i + 1}: ') + tk['label']
    for i, tk in enumerate(TC):
        tk['label'] = t(f'Завдання {i + 1}: ', f'Task {i + 1}: ') + tk['label']
    return {'a': {'tasks': TA, 'word': t('ДОВЕДЕНО', 'IDENTITY')}, 'b': {'tasks': TB}, 'c': {'tasks': TC}}


STAGE_JS = r"""
function stageA(c){
  const w=LV.a.word,k=Math.min(c.i,c.n);
  const tiles=[...w].map((ch,j)=>`<span class="${j<k?'on':''}">${j<k?ch:'?'}</span>`).join('');
  return `<div class="word" aria-label="${k}/${c.n}">${tiles}</div><div class="say">${c.SVGR(c.finished?'hostA':'tidy')}<p class="hand">${c.finished?c.S.aQuip:c.S.aStageL}</p></div><p class="count">${c.S.count(k,c.n)}</p>`;
}
function stageB(c){
  const k=Math.min(c.i,c.n);
  const blk=c.t&&!c.finished?`<div class="blockcard"><small>${c.S.bKey}</small><b>${c.t.block}</b></div>`:'';
  const done=LV.b.tasks.slice(0,k).map(t=>`<span class="chip">${t.after.replace(/\.$/,'')}</span>`).join('');
  return `${blk}<div class="say">${c.SVGR('hostB')}<p class="hand">${c.finished?c.S.bQuip:c.S.bStageL}</p></div><div class="chips">${done}</div><p class="count">${c.S.count(k,c.n)}</p>`;
}
function bloomSVG(k,n){
  let s='';
  if(P.world==='meadow'){
    s+=`<path d="M10 180 Q160 160 310 180 L310 200 L10 200 Z" fill="var(--leaf)" opacity=".35"/>`;
    for(let j=0;j<n;j++){const x=26+j*(268/(n-1)),on=j<k,h=on?60+(j%3)*12:18;
      s+=`<path d="M${x} 186 V${186-h}" stroke="var(--leaf)" stroke-width="3"/>`;
      if(on){const cy=186-h;const col=['var(--yarn)','var(--plum)','var(--hay)','var(--sky)'][j%4];
        for(let q=0;q<5;q++){const a=q*72*Math.PI/180;s+=`<circle cx="${(x+9*Math.cos(a)).toFixed(1)}" cy="${(cy+9*Math.sin(a)).toFixed(1)}" r="7" fill="${col}"/>`}
        s+=`<circle cx="${x}" cy="${cy}" r="5" fill="var(--marker)"/>`}
      else s+=`<circle cx="${x}" cy="${186-h}" r="4" fill="var(--leaf)"/>`}
  }else if(P.world==='space'){
    const pts=[];for(let j=0;j<n;j++){const a=Math.PI*(0.92-0.84*j/(n-1));pts.push([160+125*Math.cos(a),186-120*Math.sin(a)])}
    for(let j=1;j<k;j++)s+=`<line x1="${pts[j-1][0]}" y1="${pts[j-1][1]}" x2="${pts[j][0]}" y2="${pts[j][1]}" stroke="var(--sky)" stroke-width="2" stroke-dasharray="4 4"/>`;
    pts.forEach(([x,y],j)=>{const on=j<k;s+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${on?9:5}" fill="${on?'var(--sky)':'var(--line)'}"/>`+(on?`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="14" fill="var(--sky)" opacity=".2"/>`:'')});
  }else{
    for(let j=0;j<n;j++){const x=30+j*30,h=24+j*14,on=j<k;
      s+=`<rect x="${x}" y="${190-h}" width="26" height="${h}" rx="3" fill="${on?'var(--hay)':'none'}" stroke="${on?'var(--hay)':'var(--line)'}" stroke-width="2.5" ${on?'':'stroke-dasharray="5 4"'}/>`}
  }
  return `<svg viewBox="0 50 320 150" class="stg" role="img" aria-label="${k}/${n}">${s}</svg>`;
}
function stageC(c){
  const k=Math.min(c.i,c.n);
  return `${bloomSVG(k,c.n)}<div class="say">${c.SVGR(c.finished?'messy':'tidy')}<p class="hand">${c.finished?c.S.cQuip:c.S.cStageL}</p></div><p class="count">${c.S.count(k,c.n)}</p>`;
}
const STAGE={a:stageA,b:stageB,c:stageC};
"""

EXTRA_CSS = """
.blockcard{display:grid;gap:2px;justify-items:center;background:var(--cell);border:3px solid var(--hay);border-radius:16px;padding:10px 18px;box-shadow:0 4px 0 var(--shadow)}
.blockcard small{font:700 13px var(--body);color:var(--muted);letter-spacing:.05em;text-transform:uppercase}
.blockcard b{font:700 clamp(24px,6vw,30px) var(--display)}
.stage .chips .chip{font-size:13px}
.opts.big .opt{font:700 30px var(--display);min-width:72px}
"""


def texts(lang, edition):
    t = lambda uk, en: uk if lang == 'uk' else en
    home = edition == 'home'
    common = dict(
        h1={'meadow': t('Тотожності <span>на лузі</span>', 'Identities <span>in the meadow</span>'),
            'space': t('Тотожності <span>у космосі</span>', 'Identities <span>in space</span>'),
            'bricks': t('Тотожності <span>з цеглинок</span>', 'Identities <span>made of bricks</span>')},
        lH=t('Урок: тотожності й вирази', 'Lesson: identities and expressions'),
        lIntro=t('Повторення перед контрольною за уроком 11: дев’ять карток, кожна з малюнком-схемою.', 'Revision before the test, based on lesson 11: nine cards, each with a diagram.'),
        lBye=t('{hostA} каже: перевіряй числами, а доводь перетвореннями. Так роблять справжні математики.', '{hostA} says: test with numbers, prove by rewriting. That’s what real mathematicians do.'),
        toA=t('До першого рівня', 'Go to level 1'),
        dipH=t('Диплом {me:майстра:майстрині:майстра} доведень', 'Master of Proof Certificate'),
        teacherTag=t('з уроку Ігоря Петровича', 'from Mr Pasika’s lesson') if home else t('з уроку 11', 'from lesson 11'),
        rIntro=(t('Тут видно, що {me:ти вже пройшов:ти вже пройшла:вже пройдено}. Натисни кнопку, скопіюй звіт і надішли татові.',
                  'Here’s everything you’ve done so far. Copy the report and send it to Dad.') if home else
                t('Тут видно, що {me:ти вже пройшов:ти вже пройшла:вже пройдено}. Натисни «Надіслати звіт» і вибери Viber, Telegram чи пошту. Або скопіюй звіт і встав у повідомлення вчителеві чи батькам.',
                  'Here’s everything you’ve done so far. Tap "Send my report" and choose WhatsApp, Viber or email. Or copy the report and paste it into a message to your teacher or parents.')),
        copied=t('Скопійовано! Встав звіт у повідомлення.', 'Copied! Paste it into a message.'),
        repHead=(t('Тату, ось мій звіт про тотожності.', 'Hi Dad, here is my identities report.') if home else t('Ось мій звіт про тотожності.', 'Here is my identities report.')),
    )
    W = {}
    W['meadow'] = dict(
        intro=t('{messy} стверджує, що всі рівності на лузі — тотожності, а {tidy} просить доказів. Прочитай урок і пройди три рівні: розкрий справи детектива, порахуй тюки сіна блоками й збери букет доведень.',
                '{messy} claims every equation in the meadow is an identity, and {tidy} wants proof. Read the lesson, then play three levels: crack the detective cases, count hay bales in blocks and grow a bouquet of proofs.'),
        tabA=t('1. Детектив', '1. Detective'), tabB=t('2. Тюки сіна', '2. Hay bales'), tabC=t('3. Майстерня', '3. Workshop'),
        aH=t('Рівень 1. Детектив тотожностей', 'Level 1. The identity detective'),
        aIntro=t('Перевір кожну рівність числами й виріши: тотожність чи ні. Кожна розкрита справа відкриває букву в слові-розгадці.',
                 'Test each equation with numbers and decide: identity or not? Every solved case reveals a letter of the secret word.'),
        bH=t('Рівень 2. Рахуємо тюками', 'Level 2. Counting in bales'),
        bIntro=t('Тюк сіна — це «блок», значення якого відоме. Склади з тюків потрібний вираз і порахуй, не шукаючи x та y.',
                 'A hay bale is a "block" whose value you know. Build the expression from bales and work it out without finding x or y.'),
        cH=t('Рівень 3. Майстерня доведень', 'Level 3. The proof workshop'),
        cIntro=t('Найменші значення, порівняння степенів, спрощення й справжні доведення. За кожну відповідь розквітає квітка.',
                 'Smallest values, comparing powers, simplifying and real proofs. A flower blooms for every answer.'),
        aGood=t('Справу розкрито!', 'Case closed!'), bGood=t('Тюк на місці!', 'Bale stacked!'), cGood=t('Розквітла ще одна квітка!', 'Another flower blooms!'),
        aStageL=t('{tidy} гортає справи', '{tidy} is going through the cases'), bStageL=t('Складаємо тюки', 'Stacking the bales'), bKey=t('Ключ', 'Key'),
        cStageL=t('Збираємо букет', 'Growing a bouquet'),
        aQuip=t('Усі справи розкрито!', 'Every case is closed!'), bQuip=t('Сіна вистачить на всю зиму!', 'Enough hay for the whole winter!'), cQuip=t('Який букет! {messy} аж почервонів.', 'What a bouquet! {messy} is blushing.'),
        aDoneH=t('Усі справи розкрито!', 'Every case is closed!'),
        aDoneP=t('{messy} {g:messy:визнав:визнала}: не кожна рівність — тотожність. Перша зірка твоя!', '{messy} admits that not every equation is an identity. Your first star!'),
        bDoneH=t('Усі тюки пораховано!', 'All the bales are counted!'),
        bDoneP=t('Жодного разу не довелося шукати x та y. Друга зірка твоя!', 'You never had to find x or y. Your second star!'),
        cDoneH=t('Букет доведень готовий!', 'The bouquet of proofs is ready!'),
        cDoneP=t('{tidy} {g:tidy:вклонився:вклонилася}: такі доведення не стидно показати вчителеві. Третя зірка твоя!', '{tidy} bows: these proofs are good enough to show your teacher. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі значок «Майстер доведень», а {messy} обіцяє тепер перевіряти, перш ніж стверджувати.',
               'All three levels complete! {tidy} gives you a "Master of Proof" badge, and {messy} promises to check before claiming things.'),
        meet=[['hostA', t('Руда пляма, любить моркву і пояснювати.', 'Ginger patch. Loves carrots and explaining things.')],
              ['hostB', t('Темна пляма, придумує підказки-віршики.', 'Dark patch. Makes up rhymes to help you remember.')],
              ['tidy', t('Їжачиха-детектив. Без доказів не вірить.', 'A hedgehog detective. Believes nothing without proof.')],
              ['messy', t('Єнот. Любить гучні твердження.', 'A raccoon. Loves bold claims.')]],
    )
    W['space'] = dict(
        intro=t('Прибулець {messy} надсилає на станцію сигнали з рівностями, а {tidy} перевіряє, які з них правдиві. Прочитай урок і пройди три рівні: розшифруй сигнали, порахуй паливні блоки й збери сузір’я доведень.',
                '{messy} the alien sends equations to the station, and {tidy} checks which ones are true. Read the lesson, then play three levels: decode the signals, count the fuel blocks and build a constellation of proofs.'),
        tabA=t('1. Сигнали', '1. Signals'), tabB=t('2. Паливні блоки', '2. Fuel blocks'), tabC=t('3. Майстерня', '3. Workshop'),
        aH=t('Рівень 1. Розшифруй сигнали', 'Level 1. Decode the signals'),
        aIntro=t('Перевір кожну рівність числами й виріши: тотожність чи ні. Кожен розшифрований сигнал відкриває букву.', 'Test each equation with numbers and decide: identity or not? Every decoded signal reveals a letter.'),
        bH=t('Рівень 2. Паливні блоки', 'Level 2. Fuel blocks'),
        bIntro=t('Паливний блок — це вираз, значення якого відоме. Склади з блоків потрібний вираз і порахуй.', 'A fuel block is an expression whose value you know. Build the expression from blocks and work it out.'),
        cH=t('Рівень 3. Майстерня доведень', 'Level 3. The proof workshop'),
        cIntro=t('Найменші значення, порівняння степенів, спрощення й доведення. За кожну відповідь засвічується зоря.', 'Smallest values, comparing powers, simplifying and proofs. A star lights up for every answer.'),
        aGood=t('Сигнал розшифровано!', 'Signal decoded!'), bGood=t('Блок завантажено!', 'Block loaded!'), cGood=t('Засвітилась зоря!', 'A star lights up!'),
        aStageL=t('{tidy} слухає ефір', '{tidy} is listening'), bStageL=t('Завантажуємо блоки', 'Loading the blocks'), bKey=t('Ключ', 'Key'), cStageL=t('Збираємо сузір’я', 'Building a constellation'),
        aQuip=t('Усі сигнали розшифровано!', 'Every signal is decoded!'), bQuip=t('Ракета заправлена!', 'The rocket is fuelled!'), cQuip=t('Нове сузір’я! {messy} назве його твоїм ім’ям.', 'A new constellation! {messy} will name it after you.'),
        aDoneH=t('Ефір чистий!', 'All signals clear!'), aDoneP=t('{messy} тепер перевіряє кожен сигнал, перш ніж надіслати. Перша зірка твоя!', '{messy} now checks every signal before sending it. Your first star!'),
        bDoneH=t('Блоки завантажено!', 'Blocks loaded!'), bDoneP=t('Жодного разу не довелося шукати x та y. Друга зірка твоя!', 'You never had to find x or y. Your second star!'),
        cDoneH=t('Сузір’я доведень готове!', 'The constellation of proofs is ready!'), cDoneP=t('{tidy} записав усі доведення в бортовий журнал. Третя зірка твоя!', '{tidy} has logged every proof. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі значок «Майстер доведень», а {messy} обіцяє перевіряти, перш ніж стверджувати.', 'All three levels complete! {tidy} gives you a "Master of Proof" badge, and {messy} promises to check before claiming things.'),
        meet=[['hostA', t('Керує станцією і пояснює уроки.', 'Runs the station and explains the lessons.')], ['hostB', t('Водить ракету й придумує віршики.', 'Flies the rocket and makes up rhymes.')],
              ['tidy', t('Робот. Перевіряє кожен сигнал.', 'A robot. Checks every signal.')], ['messy', t('Прибулець. Надсилає гучні твердження.', 'An alien. Sends bold claims.')]],
    )
    W['bricks'] = dict(
        intro=t('Песик {messy} приніс креслення з рівностями, а {tidy} перевіряє, чи можна за ними будувати. Прочитай урок і пройди три рівні: перевір креслення, порахуй будівельні блоки й зведи вежу доведень.',
                '{messy} the puppy has brought plans full of equations, and {tidy} checks whether you can build from them. Read the lesson, then play three levels: inspect the plans, count building blocks and raise a tower of proofs.'),
        tabA=t('1. Перевірка', '1. Inspection'), tabB=t('2. Блоки', '2. Blocks'), tabC=t('3. Майстерня', '3. Workshop'),
        aH=t('Рівень 1. Перевірка креслень', 'Level 1. Inspecting the plans'),
        aIntro=t('Перевір кожну рівність числами й виріши: тотожність чи ні. Кожне перевірене креслення відкриває букву.', 'Test each equation with numbers and decide: identity or not? Every plan you check reveals a letter.'),
        bH=t('Рівень 2. Будівельні блоки', 'Level 2. Building blocks'),
        bIntro=t('Блок — це вираз, значення якого відоме. Склади з блоків потрібний вираз і порахуй.', 'A block is an expression whose value you know. Build the expression from blocks and work it out.'),
        cH=t('Рівень 3. Майстерня доведень', 'Level 3. The proof workshop'),
        cIntro=t('Найменші значення, порівняння степенів, спрощення й доведення. За кожну відповідь вежа росте.', 'Smallest values, comparing powers, simplifying and proofs. The tower grows with every answer.'),
        aGood=t('Креслення перевірено!', 'Plan checked!'), bGood=t('Блок на місці!', 'Block in place!'), cGood=t('Вежа виросла!', 'The tower grows!'),
        aStageL=t('{tidy} переглядає креслення', '{tidy} is checking the plans'), bStageL=t('Складаємо блоки', 'Stacking the blocks'), bKey=t('Ключ', 'Key'), cStageL=t('Зводимо вежу', 'Raising the tower'),
        aQuip=t('Усі креслення перевірено!', 'Every plan is checked!'), bQuip=t('Блоки складено рівненько!', 'The blocks are stacked neatly!'), cQuip=t('Вежа доведень! {messy} гавкає з самого верху.', 'A tower of proofs! {messy} is barking from the top.'),
        aDoneH=t('Перевірку завершено!', 'Inspection finished!'), aDoneP=t('{messy} {g:messy:зрозумів:зрозуміла}: не кожна рівність — тотожність. Перша зірка твоя!', '{messy} understands: not every equation is an identity. Your first star!'),
        bDoneH=t('Блоки пораховано!', 'Blocks counted!'), bDoneP=t('Жодного разу не довелося шукати x та y. Друга зірка твоя!', 'You never had to find x or y. Your second star!'),
        cDoneH=t('Вежа доведень готова!', 'The tower of proofs is ready!'), cDoneP=t('{tidy} {g:tidy:поміряв:поміряла} кожен поверх: усе рівно. Третя зірка твоя!', '{tidy} measured every floor: all level. Your third star!'),
        dipP=t('Усі три рівні пройдено! {tidy} вручає тобі медаль «Майстер доведень», а {messy} приносить найкращу кісточку.', 'All three levels complete! {tidy} gives you a "Master of Proof" medal, and {messy} brings you the best bone.'),
        meet=[['hostA', t('Будує мости й пояснює уроки.', 'Builds bridges and explains the lessons.')], ['hostB', t('Будує вежі й придумує віршики.', 'Builds towers and makes up rhymes.')],
              ['tidy', t('Робот-інженерка. Без перевірки не будує.', 'A robot engineer. Never builds without checking.')], ['messy', t('Песик. Приносить креслення в зубах.', 'A puppy. Carries the plans in his mouth.')]],
    )
    common['worlds'] = W
    return common


def rights():
    return [
        (62, 'Особа вважається невинуватою у вчиненні злочину і не може бути піддана кримінальному покаранню, доки її вину не буде доведено в законному порядку і встановлено обвинувальним вироком суду.',
         'Як і в математиці: твердження стає правдою, лише коли його доведено.',
         'A person is innocent of a crime until their guilt is proved lawfully and confirmed by a court.', 'Just like in maths: a claim only becomes true once it has been proved.'),
        (24, 'Громадяни мають рівні конституційні права і свободи та є рівними перед законом.',
         'Рівність перед законом — як тотожність: правильна для кожного.', 'Citizens have equal constitutional rights and freedoms and are equal before the law.', 'Equality before the law is like an identity: it holds for everyone.'),
        (8, 'В Україні визнається і діє принцип верховенства права.', 'Правила однакові для всіх, і влада теж мусить їх виконувати.',
         'Ukraine recognises and follows the rule of law.', 'The rules are the same for everyone, and those in power must follow them too.'),
        (55, 'Права і свободи людини і громадянина захищаються судом.', 'Якщо права порушили, у суді це доводять доказами, а не криком.',
         'Human and civil rights and freedoms are protected by the courts.', 'If someone’s rights are broken, the court decides with evidence, not shouting.'),
        (34, 'Кожному гарантується право на свободу думки і слова, на вільне вираження своїх поглядів і переконань.',
         'Можеш не погоджуватися. А доказ допоможе переконати.', 'Everyone has the right to freedom of thought and speech, and to express their views and beliefs freely.', 'You can disagree. Good proof helps you persuade others.'),
        (59, 'Кожен має право на професійну правничу допомогу.', 'Юрист допомагає довести свою правоту, як підказка до складної задачі.',
         'Everyone has the right to professional legal help.', 'A lawyer helps you prove you are right, like a hint for a hard problem.'),
        (63, 'Особа не несе відповідальності за відмову давати показання або пояснення щодо себе, членів сім’ї чи близьких родичів…',
         'Ніхто не мусить свідчити проти себе чи своєї родини.', 'No one can be punished for refusing to give evidence about themselves or their close family.', 'No one has to give evidence against themselves or their family.'),
        (28, 'Кожен має право на повагу до його гідності.', 'Сперечайся аргументами й поважай співрозмовника, навіть коли він помиляється.',
         'Everyone has the right to respect for their dignity.', 'Argue with reasons and respect the other person, even when they are wrong.'),
        (58, 'Закони та інші нормативно-правові акти не мають зворотної дії в часі…', 'Нове правило діє з дня, коли його ухвалили, а не заднім числом.',
         'Laws do not apply backwards in time.', 'A new rule applies from the day it is made, not to things that happened before.'),
    ]


def why(lang):
    t = lambda uk, en: uk if lang == 'uk' else en
    return {'items': [
        (t('Доказ, а не віра на слово.', 'Proof, not just taking someone’s word.'),
         t('Одна підстановка може спростувати твердження, але довести його можна лише міркуванням. Так само з новинами: один факт проти — і заголовок під сумнівом.',
           'One example can disprove a claim, but only reasoning can prove it. It’s the same with news: one fact against it, and the headline is in doubt.')),
        (t('Розумний рахунок.', 'Clever counting.'),
         t('Якщо 5xy² = 9, то 25x²y⁴ = 81, і x та y шукати не треба. Помічати готовий «блок» корисно і в задачах, і в житті.',
           'If 5xy² = 9, then 25x²y⁴ = 81, with no need to find x or y. Spotting a ready-made "block" helps in problems and in life.')),
        (t('Твої права.', 'Your rights.'),
         t('Стаття 62 Конституції України: людина невинувата, «доки її вину не буде доведено в законному порядку». Як і в математиці: твердження стає правдою, лише коли його доведено.',
           'Article 62 of the Constitution of Ukraine says a person is innocent until their guilt is proved lawfully. Just like in maths: a claim becomes true only when it is proved.')),
    ], 'dip': t('Тепер ти вмієш доводити тотожності й перевіряти твердження.', 'Now you can prove identities and test claims.')}
