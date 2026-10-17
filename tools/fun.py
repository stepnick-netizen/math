#!/usr/bin/env python3
"""«Математичні цікавинки» / «Maths curiosities»: cikavynky.html and cikavynky-en.html.

Run from the repo root:  python3 tools/fun.py
The page reuses the look of index.html (same head, palette, footer, stats), so run it after index changes,
then python3 tools/add_theme_toggle.py. All numbers below were checked by computation (17.10.2026):
2^42*0.1 mm ≈ 439 805 km > 384 400 km; 2^64-1 = 18 446 744 073 709 551 615; 142857*7 = 999999;
732-237 = 495, 495+594 = 1089; 1+…+100 = 5050; pizzas 200π ≈ 628 vs 225π ≈ 707 cm² (×1.125);
birthday 23 → 50.7 %, 30 → 70.6 %, 40 → 89.1 %; 23*22/2 = 253; 365 + 97/400 = 365.2425.
Facts: Gallivan 12 folds 2002 (Guinness), googol 1920 Milton Sirotta (Wikipedia), Kravchuk arrested 1938,
died in Kolyma 1942, noticed young Korolyov (KPI), Ostrogradsky b. 1801 Poltava region, Cauchy's praise (osvita.ua).
"""
import math, re, html
from _inject import put_style
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATS = [('all', 'Усі', 'All'), ('pow', 'Степені', 'Powers'), ('num', 'Числа', 'Numbers'), ('geo', 'Геометрія', 'Geometry'),
        ('prob', 'Ймовірність', 'Chance'), ('ppl', 'Люди', 'People')]
L = {  # lesson links
    'pow': ('powers', 'урок 9.1 «Степінь з натуральним показником»', 'lesson 9.1 “Powers with natural indices”'),
    'id': ('identities', 'урок 11 «Узагальнення: цілі раціональні вирази»', 'lesson 11 “Review: algebraic expressions”'),
    'ang': ('angles', 'урок 6 «Суміжні кути та їх властивості»', 'lesson 6 “Adjacent angles”'),
    'pct': ('percentages', 'тему «Відсотки» (6 клас)', 'the topic “Percentages” (Grade 6)'),
}


def t(x, y, s, size=14, col='--ink', w=700, anchor='middle', fam='Comfortaa,Nunito,sans-serif'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{size}" fill="var({col})">{s}</text>'


def pic(kind):
    b = ''
    if kind == 'paper':
        for i, hgt in enumerate((2, 4, 8, 16, 32, 64)):
            b += f'<rect x="{14 + i * 18}" y="{100 - hgt}" width="13" height="{hgt}" rx="2" fill="var(--sky)" opacity="{0.45 + i * 0.1:.2f}"/>'
        b += '<circle cx="140" cy="26" r="16" fill="var(--hay)"/><circle cx="134" cy="22" r="3" fill="var(--paper)" opacity=".5"/><circle cx="146" cy="32" r="2" fill="var(--paper)" opacity=".5"/>'
        b += '<path d="M122 40 Q 112 60 116 84" stroke="var(--yarn)" stroke-width="2.2" fill="none" stroke-dasharray="4 4"/>' + t(70, 14, '2⁴² шарів', 13, '--yarn')
    elif kind == 'chess':
        for r in range(4):
            for c in range(4):
                b += f'<rect x="{30 + c * 25}" y="{4 + r * 25}" width="25" height="25" fill="var({"--cell" if (r + c) % 2 else "--line"})"/>'
        for c, n in enumerate((1, 2, 4, 8)):
            b += t(42.5 + c * 25, 21, n, 12, '--yarn')
        b += t(117, 96, '…', 14, '--muted') + '<rect x="30" y="4" width="100" height="100" fill="none" stroke="var(--ink)" stroke-width="2"/>'
    elif kind == 'googol':
        b += t(80, 52, '10<tspan font-size="18" dy="-14">100</tspan>', 40, '--plum') + t(80, 86, '1 і сто нулів', 13, '--muted', 600)
    elif kind == 'cyclic':
        b += '<circle cx="80" cy="54" r="40" fill="none" stroke="var(--line)" stroke-width="3"/>'
        for i, d in enumerate('142857'):
            a = math.radians(-90 + i * 60)
            b += f'<circle cx="{80 + 40 * math.cos(a):.1f}" cy="{54 + 40 * math.sin(a):.1f}" r="12" fill="var(--hay)"/>' + t(f'{80 + 40 * math.cos(a):.1f}', f'{59 + 40 * math.sin(a):.1f}', d, 14, '--ink')
        b += t(80, 59, '× 7', 14, '--yarn')
    elif kind == '1089':
        pts = ' '.join(f'{80 + 46 * math.cos(math.radians(90 + 60 * k)):.1f},{54 + 46 * math.sin(math.radians(90 + 60 * k)):.1f}' for k in range(6))
        b += f'<polygon points="{pts}" fill="var(--marker)" stroke="var(--hay)" stroke-width="4" stroke-linejoin="round"/>' + t(80, 63, '1089', 26, '--marker-ink')
    elif kind == 'gauss':
        xs = [16, 40, 64, 96, 120, 144]
        for x, n in zip(xs, ('1', '2', '3', '98', '99', '100')):
            b += t(x, 80, n, 12, '--ink')
        b += t(80, 80, '…', 12, '--muted')
        for (a, c), col in zip(((16, 144), (40, 120), (64, 96)), ('--yarn', '--sky', '--leaf')):
            b += f'<path d="M{a} 66 Q {(a + c) / 2} {66 - (c - a) * 0.45:.0f} {c} 66" stroke="var({col})" stroke-width="2.4" fill="none"/>'
        b += t(80, 102, '50 пар × 101', 13, '--yarn')
    elif kind == 'pizza':
        for cx in (30, 74):
            b += f'<circle cx="{cx}" cy="56" r="20" fill="var(--hay)" stroke="var(--yarn)" stroke-width="3"/>'
        b += '<circle cx="128" cy="56" r="30" fill="var(--hay)" stroke="var(--yarn)" stroke-width="3"/>'
        for cx, cy in ((24, 50), (36, 62), (68, 50), (80, 60), (118, 46), (138, 60), (126, 70), (136, 42)):
            b += f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="var(--yarn)"/>'
        b += t(52, 98, '20 + 20 см', 12, '--muted', 600) + t(128, 98, '30 см', 12, '--muted', 600)
    elif kind == 'snow':
        for k in range(6):
            a = math.radians(k * 60 - 90)
            x2, y2 = 80 + 42 * math.cos(a), 54 + 42 * math.sin(a)
            b += f'<line x1="80" y1="54" x2="{x2:.1f}" y2="{y2:.1f}" stroke="var(--sky)" stroke-width="4" stroke-linecap="round"/>'
            for s in (0.55, 0.8):
                mx, my = 80 + 42 * s * math.cos(a), 54 + 42 * s * math.sin(a)
                for d in (-1, 1):
                    a2 = a + d * math.radians(45)
                    b += f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{mx + 9 * math.cos(a2):.1f}" y2="{my + 9 * math.sin(a2):.1f}" stroke="var(--sky)" stroke-width="2.5" stroke-linecap="round"/>'
        b += '<path d="M80 34 A 20 20 0 0 1 97.3 44" stroke="var(--yarn)" stroke-width="2.5" fill="none"/>' + t(104, 30, '60°', 13, '--yarn')
    elif kind == 'rope':
        A, B, C = (30, 96), (126, 96), (30, 24)
        b += f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="var(--cell)" stroke="var(--hay)" stroke-width="3" stroke-linejoin="round"/>'
        for i in range(12):
            per = [(A, B, 4), (B, C, 5), (C, A, 3)]
            k = i
            for P, Q, n in per:
                if k < n:
                    x = P[0] + (Q[0] - P[0]) * k / n; y = P[1] + (Q[1] - P[1]) * k / n
                    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="var(--yarn)"/>'
                    break
                k -= n
        b += '<path d="M30 84 H42 V96" stroke="var(--ink)" stroke-width="2" fill="none"/>' + t(78, 112, '4', 13) + t(20, 64, '3', 13) + t(86, 56, '5', 13)
    elif kind == 'bday':
        for i in range(23):
            x, y = 20 + (i % 8) * 17, 22 + (i // 8) * 26
            hit = i in (5, 17)
            b += f'<circle cx="{x}" cy="{y}" r="7" fill="var({"--yarn" if hit else "--line"})"/>'
        b += '<path d="M105 22 C 118 40 118 56 105 74" stroke="var(--yarn)" stroke-width="2.4" fill="none" stroke-dasharray="4 3"/>' + t(80, 104, '23 → 50,7 %', 14, '--yarn')
    elif kind == 'leap':
        b += '<rect x="44" y="12" width="72" height="84" rx="8" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/><rect x="44" y="12" width="72" height="24" rx="8" fill="var(--yarn)"/><rect x="44" y="28" width="72" height="8" fill="var(--yarn)"/>'
        b += t(80, 29, 'ЛЮТИЙ', 12, '--paper') + t(80, 80, '29', 38, '--ink')
    elif kind == 'krav':
        pts = ' '.join(f'{12 + i * 136 / 60:.1f},{56 - 34 * math.sin(i / 60 * 3 * math.pi) * math.exp(-((i - 30) / 34) ** 2):.1f}' for i in range(61))
        b += '<line x1="10" y1="56" x2="150" y2="56" stroke="var(--line)" stroke-width="2"/>' + f'<polyline points="{pts}" fill="none" stroke="var(--plum)" stroke-width="3"/>'
        for i in range(0, 61, 10):
            b += f'<circle cx="{12 + i * 136 / 60:.1f}" cy="{56 - 34 * math.sin(i / 60 * 3 * math.pi) * math.exp(-((i - 30) / 34) ** 2):.1f}" r="4" fill="var(--yarn)"/>'
    elif kind == 'ostro':
        for x in range(14, 110, 16):
            b += f'<path d="M{x} 100 V44 L{x + 6} 36 L{x + 12} 44 V100 Z" fill="var(--hay)" stroke="var(--ink)" stroke-width="1.5"/>'
        b += '<line x1="10" y1="60" x2="114" y2="60" stroke="var(--ink)" stroke-width="2"/><line x1="10" y1="86" x2="114" y2="86" stroke="var(--ink)" stroke-width="2"/>'
        b += '<line x1="132" y1="20" x2="132" y2="88" stroke="var(--yarn)" stroke-width="2.5"/><path d="M124 88 h16 l-3 12 h-10 z" fill="var(--ink)"/><line x1="120" y1="20" x2="144" y2="20" stroke="var(--ink)" stroke-width="3"/>'
    return f'<svg viewBox="0 0 160 112" role="img" aria-hidden="true">{b}</svg>'


# id, category, picture, link, uk(title, story, question, answer), en(...)
ITEMS = [
    ('paper', 'pow', 'paper', 'pow',
     ('42 згини — і ти на Місяці',
      'Аркуш паперу має товщину приблизно 0,1 мм. Кожен згин подвоює товщину: 2, 4, 8, 16 шарів… Після 42 згинів шарів буде 2⁴² — понад чотири трильйони. Помнож на 0,1 мм, і вийде приблизно 440 000 км. А до Місяця в середньому 384 400 км! Насправді так багато скласти папір не вдасться: у 2002 році школярка Брітні Ґаллівен склала смугу паперу понад кілометр завдовжки 12 разів, і це світовий рекорд.',
      'Скільки шарів буде після 10 згинів і якої товщини стопка?',
      '2¹⁰ = 1024 шари. 1024 · 0,1 мм ≈ 102 мм — приблизно 10 см, як товста книжка.'),
     ('42 folds and you reach the Moon',
      'A sheet of paper is about 0.1 mm thick. Every fold doubles the thickness: 2, 4, 8, 16 layers… After 42 folds there are 2⁴² layers, over four trillion. Multiply by 0.1 mm and you get about 440,000 km. The Moon is on average 384,400 km away! In real life you cannot fold paper that many times: in 2002 the schoolgirl Britney Gallivan folded a strip of paper over a kilometre long 12 times, and that is the world record.',
      'How many layers after 10 folds, and how thick is the pile?',
      '2¹⁰ = 1024 layers. 1024 × 0.1 mm ≈ 102 mm: about 10 cm, like a thick book.')),
    ('chess', 'pow', 'chess', 'pow',
     ('Зернятка на шаховій дошці',
      'За легендою, мудрець, який винайшов шахи, попросив у правителя скромну нагороду: на першу клітинку дошки одну зернину, на другу — дві, на третю — чотири, і так далі, щоразу вдвічі більше. Правитель засміявся… а потім порахував. На 64-й клітинці мало б лежати 2⁶³ зернин, а на всій дошці — 2⁶⁴ − 1 = 18 446 744 073 709 551 615. Щоб зібрати стільки пшениці, всій Землі довелося б вирощувати її сотні років.',
      'Скільки зернин лежить на 10-й клітинці?',
      'На першій 2⁰ = 1, на другій 2¹ = 2, тож на 10-й — 2⁹ = 512 зернин.'),
     ('Grains on a chessboard',
      'Legend says the wise man who invented chess asked the ruler for a modest reward: one grain on the first square, two on the second, four on the third, and so on, doubling every time. The ruler laughed… and then did the sums. The 64th square alone would hold 2⁶³ grains, and the whole board 2⁶⁴ − 1 = 18,446,744,073,709,551,615. To grow that much wheat, the whole Earth would need hundreds of years.',
      'How many grains are on the 10th square?',
      'The first has 2⁰ = 1, the second 2¹ = 2, so the 10th has 2⁹ = 512 grains.')),
    ('googol', 'pow', 'googol', 'pow',
     ('Гугол і дев’ятирічний хлопчик',
      'У 1920 році американський математик Едвард Каснер спитав свого дев’ятирічного племінника Мілтона, як назвати число 10¹⁰⁰ — одиницю зі ста нулями. Хлопчик вигадав слово «гугол». Це число більше, ніж кількість атомів у всьому видимому Всесвіті (їх приблизно 10⁸⁰). А назва компанії Google — гра слів із «гуголом».',
      'Скільки нулів у числі 10¹⁰⁰ · 10²?',
      'Показники додаються: 10¹⁰⁰ · 10² = 10¹⁰², тобто 102 нулі.'),
     ('The googol and a nine-year-old',
      'In 1920 the American mathematician Edward Kasner asked his nine-year-old nephew Milton what to call 10¹⁰⁰, a one followed by a hundred zeros. The boy made up the word “googol”. It is bigger than the number of atoms in the whole visible universe (about 10⁸⁰). And the company name Google is a play on “googol”.',
      'How many zeros are there in 10¹⁰⁰ × 10²?',
      'The indices add up: 10¹⁰⁰ × 10² = 10¹⁰², so 102 zeros.')),
    ('cyclic', 'num', 'cyclic', None,
     ('Чарівне число 142857',
      'Помнож 142857 на 2, 3, 4, 5 або 6, і вийдуть ті самі цифри в тому самому порядку по колу, просто з іншого місця: 285714, 428571, 571428, 714285, 857142. А якщо помножити на 7, вийде 999999. Секрет у дробі 1/7 = 0,142857142857…: ці шість цифр повторюються без кінця.',
      'Обчисли 142857 · 7. А потім 142857 · 3.',
      '142857 · 7 = 999999; 142857 · 3 = 428571 — ті самі цифри по колу.'),
     ('The magic number 142857',
      'Multiply 142857 by 2, 3, 4, 5 or 6 and you get the same digits in the same order round a circle, just starting from a different place: 285714, 428571, 571428, 714285, 857142. Multiply by 7 and you get 999999. The secret is the fraction 1/7 = 0.142857142857…: those six digits repeat for ever.',
      'Work out 142857 × 7. Then 142857 × 3.',
      '142857 × 7 = 999999; 142857 × 3 = 428571: the same digits round the circle.')),
    ('1089', 'num', '1089', 'id',
     ('Фокус із числом 1089',
      'Задумай тризначне число, у якого перша й остання цифри різняться хоча б на 2, наприклад 732. Переверни його (237) і відніми менше від більшого: 732 − 237 = 495. Тепер переверни результат (594) і додай: 495 + 594 = 1089. Спробуй з іншим числом: завжди виходить 1089! Чому? Число abc — це 100a + 10b + c. Різниця з перевернутим: 100a + 10b + c − (100c + 10b + a) = 99(a − c). Тож різниця завжди кратна 99: 198, 297, …, 891, і кожна з них разом зі своїм «перевертнем» дає 1089.',
      'Перевір фокус на числі 841.',
      '841 − 148 = 693; 693 + 396 = 1089.'),
     ('The 1089 trick',
      'Think of a three-digit number whose first and last digits differ by at least 2, say 732. Reverse it (237) and take the smaller from the bigger: 732 − 237 = 495. Now reverse the answer (594) and add: 495 + 594 = 1089. Try another number: it is always 1089! Why? The number abc is 100a + 10b + c. Take away the reversed number: 100a + 10b + c − (100c + 10b + a) = 99(a − c). So the difference is always a multiple of 99: 198, 297, …, 891, and each of them plus its reverse makes 1089.',
      'Check the trick with 841.',
      '841 − 148 = 693; 693 + 396 = 1089.')),
    ('leap', 'num', 'leap', None,
     ('Чому високосний рік буває не кожні 4 роки',
      'Земля обходить Сонце приблизно за 365,2422 доби. Якщо додавати 29 лютого кожні 4 роки, рік у середньому триває 365,25 доби: трохи задовго, і за 400 років набігає зайвих 3 доби. Тому придумали правило: роки, що діляться на 100, не високосні, якщо тільки вони не діляться на 400. Так за 400 років буває 97 високосних, і рік у середньому триває 365 + 97/400 = 365,2425 доби — майже точно.',
      'Чи був високосним 2000 рік? А чи буде 2100-й?',
      '2000 ділиться на 400 — високосний. 2100 ділиться на 100, але не на 400 — не високосний.'),
     ('Why a leap year is not every 4 years',
      'The Earth goes round the Sun in about 365.2422 days. If we add 29 February every 4 years, the average year is 365.25 days: a little too long, and over 400 years we gain 3 extra days. So there is a rule: years divisible by 100 are not leap years, unless they are divisible by 400. That gives 97 leap years in every 400, and the average year is 365 + 97/400 = 365.2425 days: almost exact.',
      'Was 2000 a leap year? Will 2100 be one?',
      '2000 is divisible by 400, so it was a leap year. 2100 is divisible by 100 but not by 400, so it will not be.')),
    ('pizza', 'geo', 'pizza', 'pct',
     ('Дві середні піци чи одна велика?',
      'Що вигідніше: дві піци по 20 см у діаметрі чи одна на 30 см? Здається, що дві: 20 + 20 = 40 більше за 30. Але їмо ми площу! Площа круга — πr². Дві малі: 2 · π · 10² ≈ 628 см². Одна велика: π · 15² ≈ 707 см². Велика піца на 12,5 % більша, ніж дві середні разом.',
      'Діаметр піци збільшили вдвічі. У скільки разів більше стало піци?',
      'У 4 рази: радіус удвічі більший, а площа πr² залежить від квадрата радіуса — 2² = 4.'),
     ('Two medium pizzas or one large?',
      'Which is the better deal: two pizzas 20 cm across or one 30 cm pizza? Two seems bigger: 20 + 20 = 40 is more than 30. But what we eat is area! The area of a circle is πr². Two small ones: 2 × π × 10² ≈ 628 cm². One large: π × 15² ≈ 707 cm². The large pizza is 12.5% bigger than the two medium ones together.',
      'A pizza’s diameter is doubled. How many times more pizza is there?',
      '4 times: the radius doubles, and the area πr² depends on the square of the radius, 2² = 4.')),
    ('snow', 'geo', 'snow', 'ang',
     ('Чому в сніжинки шість променів',
      'Молекули води, замерзаючи, складаються в гратку з шестикутників — як бджолині соти. Тому сніжинка завжди росте шістьма променями, і кут між сусідніми променями — 60°. Дві однакові сніжинки знайти майже неможливо: кожна росте у своєму шляху крізь хмару, з іншою температурою й вологістю.',
      'Кут між сусідніми променями — 60°. Який кут суміжний з ним?',
      '180° − 60° = 120°.'),
     ('Why a snowflake has six arms',
      'When water freezes, its molecules line up in a lattice of hexagons, like a honeycomb. That is why a snowflake always grows six arms, and the angle between neighbouring arms is 60°. Finding two identical snowflakes is almost impossible: each one grows along its own path through the cloud, with different temperature and moisture.',
      'The angle between neighbouring arms is 60°. What is the angle on a straight line with it?',
      '180° − 60° = 120°.')),
    ('rope', 'geo', 'rope', None,
     ('Прямий кут з мотузки',
      'Як без косинця побудувати прямий кут, наприклад для фундаменту? Зав’яжи на мотузці 12 вузлів через однакові відстані й натягни трикутник зі сторонами 3, 4 і 5 проміжків. Кут між сторонами 3 і 4 вийде прямим! Причина — у рівності 3² + 4² = 5² (9 + 16 = 25). Це теорема Піфагора, яку ти вивчатимеш у 8 класі.',
      'Чи вийде прямий кут з трикутника зі сторонами 6, 8 і 10?',
      'Так: 6² + 8² = 36 + 64 = 100 = 10². Це той самий трикутник 3–4–5, тільки вдвічі більший.'),
     ('A right angle from a rope',
      'How do you make a right angle without a set square, say for a foundation? Tie 12 knots at equal distances along a rope and stretch it into a triangle with sides of 3, 4 and 5 gaps. The angle between the sides 3 and 4 is a right angle! The reason is that 3² + 4² = 5² (9 + 16 = 25). That is Pythagoras’ theorem, which you will learn later.',
      'Does a triangle with sides 6, 8 and 10 have a right angle?',
      'Yes: 6² + 8² = 36 + 64 = 100 = 10². It is the same 3–4–5 triangle, just twice as big.')),
    ('bday', 'prob', 'bday', None,
     ('23 учні — і вже, швидше за все, є спільний день народження',
      'У році 365 днів, тож здається, що для збігу днів народження треба дуже багато людей. Але вже серед 23 людей імовірність, що двоє народилися в один день, — 50,7 %. Серед 30 — 70,6 %, а серед 40 — 89,1 %. Секрет у тому, що порівнюємо не тебе з кожним, а всі пари між собою, а пар дуже багато.',
      'Скільки різних пар можна скласти з 23 учнів?',
      '23 · 22 : 2 = 253 пари. Кожна пара — ще один шанс на збіг.'),
     ('23 pupils: probably a shared birthday',
      'There are 365 days in a year, so it feels as if you would need lots of people for two to share a birthday. But with just 23 people the chance that two share a birthday is 50.7%. With 30 it is 70.6%, and with 40, 89.1%. The secret: we do not compare you with everyone, we compare every pair, and there are lots of pairs.',
      'How many different pairs can you make from 23 pupils?',
      '23 × 22 ÷ 2 = 253 pairs. Each pair is one more chance of a match.')),
    ('gauss', 'ppl', 'gauss', 'id',
     ('Як маленький Гаусс додав числа від 1 до 100',
      'Розповідають, що вчитель хотів зайняти клас надовго й звелів додати всі числа від 1 до 100. Маленький Карл Фрідріх Гаусс, майбутній великий математик, за хвилину приніс відповідь: 5050. Він помітив, що 1 + 100 = 101, 2 + 99 = 101, 3 + 98 = 101… Таких пар 50, отже сума 50 · 101 = 5050. У загальному вигляді: 1 + 2 + … + n = n(n + 1) : 2.',
      'Чому дорівнює сума 1 + 2 + … + 10?',
      '10 · 11 : 2 = 55.'),
     ('How young Gauss added the numbers from 1 to 100',
      'The story goes that a teacher wanted to keep the class busy and told them to add all the numbers from 1 to 100. Young Carl Friedrich Gauss, a future great mathematician, came back within a minute with the answer: 5050. He had noticed that 1 + 100 = 101, 2 + 99 = 101, 3 + 98 = 101… There are 50 such pairs, so the sum is 50 × 101 = 5050. In general: 1 + 2 + … + n = n(n + 1) ÷ 2.',
      'What is 1 + 2 + … + 10?',
      '10 × 11 ÷ 2 = 55.')),
    ('krav', 'ppl', 'krav', None,
     ('Михайло Кравчук: формули, що пережили свого автора',
      'Михайло Кравчук — український математик, академік, професор Київського політехнічного інституту. Він першим помітив талант юного студента Сергія Корольова, майбутнього конструктора космічних ракет. Многочлени Кравчука, які він описав у 1929 році, сьогодні використовують у теорії кодування — науці про те, як передавати повідомлення без помилок, — і в обробці зображень. У 1938 році радянська влада заарештувала Кравчука, і в 1942 році він загинув у таборі на Колимі. А його формули працюють досі.',
      None, None),
     ('Mykhailo Kravchuk: formulas that outlived their author',
      'Mykhailo Kravchuk was a Ukrainian mathematician, academician and professor at the Kyiv Polytechnic Institute. He was the first to notice the talent of a young student, Serhiy Korolyov, the future designer of space rockets. The Kravchuk polynomials he described in 1929 are used today in coding theory, the science of sending messages without errors, and in image processing. In 1938 the Soviet regime arrested Kravchuk, and in 1942 he died in a prison camp in Kolyma. His formulas are still at work.',
      None, None)),
    ('ostro', 'ppl', 'ostro', None,
     ('Михайло Остроградський: хлопчик з мотузкою',
      'Михайло Остроградський народився 1801 року на Полтавщині. У дитинстві він не любив звичайних ігор, зате ходив із мотузкою й тягарцем і вимірював усе довкола: висоту парканів, глибину криниць. Навчався в Полтавській гімназії й Харківському університеті, слухав лекції найкращих учених Парижа. Його іменем названо формулу Гаусса–Остроградського, якою фізики й інженери досі рахують потоки рідини, тепла й електричного поля.',
      None, None),
     ('Mykhailo Ostrohradsky: the boy with a rope',
      'Mykhailo Ostrohradsky was born in 1801 in the Poltava region. As a boy he did not care for ordinary games; instead he walked about with a rope and a weight and measured everything around him: the height of fences, the depth of wells. He studied at the Poltava gymnasium and Kharkiv University and attended lectures by the best scientists in Paris. The Gauss–Ostrohradsky formula is named after him, and physicists and engineers still use it to calculate flows of liquid, heat and electric fields.',
      None, None)),
]

TXT = {
    'uk': dict(title='Математичні цікавинки', h1='Математичні <span>цікавинки</span>', file='cikavynky.html', other='cikavynky-en.html', other_l='English version',
               lead='Короткі історії про числа, форми й людей, які їх відкривали. Кожну можна прочитати за хвилину, а в кінці — завдання «Перевір себе».',
               rnd='Випадкова цікавинка', check='Перевір себе', lesson='До теми: {t} →', home='Математична пасіка', idx='index.html', crumbs='Цікавинки'),
    'en': dict(title='Maths curiosities', h1='Maths <span>curiosities</span>', file='cikavynky-en.html', other='cikavynky.html', other_l='Українська версія',
               lead='Short stories about numbers, shapes and the people who discovered them. Each takes a minute to read and ends with a “Check yourself” question.',
               rnd='Random curiosity', check='Check yourself', lesson='Related: {t} →', home='The Maths Apiary', idx='index-en.html', crumbs='Curiosities'),
}
PIC_EN = {'2⁴² шарів': '2⁴² layers', '1 і сто нулів': '1 and 100 zeros', '50 пар × 101': '50 pairs × 101', '20 + 20 см': '20 + 20 cm',
          '30 см': '30 cm', 'ЛЮТИЙ': 'FEB', '23 → 50,7 %': '23 → 50.7%'}

CSS = """/* fun */.wrap>nav.site-home{justify-self:stretch;width:100%}.fun-head{display:grid;gap:10px}.fun-tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.fun-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px;align-items:start}
.fun{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:0 3px 0 var(--shadow);display:grid;grid-template-columns:150px 1fr;gap:14px;scroll-margin-top:16px;transition:box-shadow .3s}
.fun.flash{box-shadow:0 0 0 4px var(--hay)}.fun svg{width:150px;height:auto;display:block}.fun-body{display:grid;gap:8px;min-width:0;align-content:start}
.fun-cat{justify-self:start;font:800 12px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.fun h3{font:700 19px/1.3 var(--display);margin:0}.fun p{margin:0;font-size:15.5px}
.fun details{background:var(--cell);border-radius:12px;padding:8px 12px}.fun summary{cursor:pointer;font-weight:800;color:var(--leaf)}.fun details p{margin-top:6px}
.fun-link{font:800 14.5px var(--body);color:var(--sky)}.fun-n{color:var(--hay)}
.rnd{background:var(--hay);color:#2A1E00;border:0;border-radius:12px;font:800 15px var(--body);padding:9px 14px;cursor:pointer}
@media (max-width:560px){.fun{grid-template-columns:1fr}.fun svg{width:170px;justify-self:center}}"""

JS = r"""<script>/* fun */(function(){var chips=[].slice.call(document.querySelectorAll('.fun-tools .chip')),cards=[].slice.call(document.querySelectorAll('.fun'));
function show(c){chips.forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-cat')===c)});cards.forEach(function(k){k.hidden=!(c==='all'||k.getAttribute('data-cat')===c)})}
chips.forEach(function(x){x.addEventListener('click',function(){show(x.getAttribute('data-cat'))})});
var r=document.getElementById('rnd');if(r)r.addEventListener('click',function(){show('all');var k=cards[Math.floor(Math.random()*cards.length)];k.scrollIntoView({behavior:'smooth',block:'start'});
k.classList.add('flash');setTimeout(function(){k.classList.remove('flash')},1600);var d=k.querySelector('details');if(d)d.open=false});
if(location.hash){var k=document.getElementById(location.hash.slice(1));if(k){k.classList.add('flash');setTimeout(function(){k.classList.remove('flash')},1600)}}
show('all')})();</script>"""


def build(lang):
    tx = TXT[lang]
    tpl = (ROOT / tx['idx']).read_text()
    head = tpl[:tpl.index('<body')]
    head = re.sub(r'<title>.*?</title>', f'<title>{tx["title"]} · {tx["home"]}</title>', head, count=1)
    head = put_style(head + '</head>', 'fun', CSS, legacy=['fun'])[:-len('</head>')]
    foot = tpl[tpl.index('<footer class="site-copy"'):]
    # keep stats/theme/bug scripts, drop the home-page-only ones
    foot = re.sub(r'<script>/\* toc \*/.*?</script>', '', foot, flags=re.S)
    foot = re.sub(r'<script>/\* theme switch \*/.*?</script>', '', foot, flags=re.S)
    foot = re.sub(r'<script>\s*\(function\(\)\{var K=.ponya-bulya-profile-v1.*?</script>', '', foot, flags=re.S)
    chips = ''.join(f'<button type="button" class="chip" data-cat="{c}" aria-pressed="{"true" if c == "all" else "false"}">{u if lang == "uk" else e}</button>' for c, u, e in CATS)
    cards = ''
    for n, (cid, cat, pk, link, uk, en) in enumerate(ITEMS, 1):
        title, story, q, a = uk if lang == 'uk' else en
        svg = pic(pk)
        if lang == 'en':
            for k, v in PIC_EN.items():
                svg = svg.replace(k, v)
        catname = next(u if lang == 'uk' else e for c, u, e in CATS if c == cat)
        body = f'<span class="fun-cat"><span class="fun-n">№{n}</span> · {catname}</span><h3>{html.escape(title)}</h3><p>{html.escape(story)}</p>'
        if q:
            body += f'<details><summary>{tx["check"]}: {html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
        if link:
            folder, lu, le = L[link]
            body += f'<a class="fun-link" href="{folder}/{"uk" if lang == "uk" else "en"}.html">{tx["lesson"].format(t=lu if lang == "uk" else le)}</a>'
        cards += f'<article class="fun" id="{cid}" data-cat="{cat}">{svg}<div class="fun-body">{body}</div></article>'
    body = (f'<body>\n<div class="wrap">\n<nav class="site-home" aria-label="breadcrumb"><a href="{tx["idx"]}">← {tx["home"]}</a><span class="sep">›</span><span class="here">{tx["crumbs"]}</span></nav>'
            f'<header class="fun-head"><h1>{tx["h1"]}</h1><p>{tx["lead"]}</p><p style="font-size:15px"><a href="{tx["other"]}">{tx["other_l"]}</a></p></header>'
            f'<div class="fun-tools" role="group">{chips}<button type="button" class="rnd" id="rnd">🎲 {tx["rnd"]}</button></div>'
            f'<section class="fun-grid">{cards}</section>\n</div>\n')
    (ROOT / tx['file']).write_text(head + body + foot.replace('</body>', JS + '</body>'))


BANNER_CSS = ('/* fun banner */a.fun-banner{display:flex;align-items:center;gap:16px;background:var(--marker);color:var(--marker-ink)!important;text-decoration:none!important;'
              'border-radius:16px;border-top:6px solid var(--hay);padding:16px 18px;box-shadow:0 4px 14px rgba(0,0,0,.14);transition:transform .15s}'
              'a.fun-banner:hover{transform:translateY(-2px)}.fb-hex{flex:none;width:76px;height:86px;display:grid;place-items:center;background:var(--hay);color:#2A1E00;'
              'font:700 26px var(--display);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}'
              '.fb-text{display:grid;gap:5px;min-width:0}.fb-kicker{font:800 12.5px/1.2 var(--body);letter-spacing:.09em;text-transform:uppercase;opacity:.75}'
              '.fb-title{font:700 23px/1.15 var(--display)}.fb-sub{font:15px/1.4 var(--body)}.fb-cta{justify-self:start;background:var(--ink);color:var(--paper);'
              'font:800 16px var(--body);padding:9px 16px;border-radius:10px;margin-top:5px}.fb-cta i{font-style:normal;display:inline-block;animation:hbnudge 1.4s ease-in-out infinite}'
              '@media (prefers-reduced-motion:reduce){.fb-cta i{animation:none}}@media (max-width:480px){a.fun-banner{align-items:flex-start;padding:14px}.fb-hex{width:56px;height:64px;font-size:20px}.fb-title{font-size:20px}}')


def banner(lang):
    n = len(ITEMS)
    if lang == 'uk':
        k, t_, s_, c = ('Окремий розділ сайту', 'Математичні цікавинки',
                        f'{n} коротких історій: аркуш до Місяця, фокус з числом 1089, чесна піца, сніжинки, маленький Гаусс і українські математики', 'Тисни і читай')
        href = 'cikavynky.html'
    else:
        k, t_, s_, c = ('A separate section of this site', 'Maths curiosities',
                        f'{n} short stories: folding paper to the Moon, the 1089 trick, the fair pizza, snowflakes, young Gauss and Ukrainian mathematicians', 'Tap to read')
        href = 'cikavynky-en.html'
    return (f'<!--fun--><section class="fun-sec"><a class="fun-banner" href="{href}"><span class="fb-hex" aria-hidden="true">?!</span><span class="fb-text">'
            f'<span class="fb-kicker">{k}</span><span class="fb-title">{t_}</span><span class="fb-sub">{s_}</span><span class="fb-cta">{c} <i>→</i></span></span></a></section><!--/fun-->')


def index_banner(lang):
    p = ROOT / TXT[lang]['idx']
    s = p.read_text()
    s = re.sub(r'\s*<!--fun-->.*?<!--/fun-->', '', s, flags=re.S)
    k = s.index('<section class="how now">')
    s = s[:k] + banner(lang) + '\n ' + s[k:]
    s = put_style(s, 'funbanner', BANNER_CSS, legacy=['fun banner'])
    p.write_text(s)


# ---------------------------------------------------------------- «curiosities for this lesson» on topic pages
ALSO = {'monomials': ['googol', '1089'], 'proportions': ['pizza']}   # extra related cards for lessons without a direct link
LINKS_CSS = ('/* funlinks */.funlinks{max-width:920px;margin:24px auto 0;background:var(--paper,#fff);border:2px dashed var(--hay,#D99A1E);border-radius:16px;padding:14px 16px;display:grid;gap:8px}'
             '.funlinks h2{font:700 19px var(--display,sans-serif);margin:0;display:flex;align-items:center;gap:10px}'
             '.funlinks h2::before{content:"?!";display:grid;place-items:center;width:34px;height:38px;background:var(--hay,#D99A1E);color:#2A1E00;font-size:14px;'
             'clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}'
             '.funlinks ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}.funlinks a{font:700 16px var(--body,sans-serif);color:var(--sky,#3E7FB8)}'
             '.funlinks small{color:var(--muted,#666);font:700 13px var(--body,sans-serif)}')


def lesson_links():
    import glob
    lk_folder = {k: v[0] for k, v in L.items()}
    by = {}
    for n, (cid, cat, pk, link, uk, en) in enumerate(ITEMS, 1):
        if link:
            by.setdefault(lk_folder[link], []).append((n, cid, uk[0], en[0]))
    num = {cid: (n, uk[0], en[0]) for n, (cid, cat, pk, link, uk, en) in enumerate(ITEMS, 1)}
    for folder, ids in ALSO.items():
        for cid in ids:
            n, tu, te = num[cid]
            by.setdefault(folder, []).append((n, cid, tu, te))
    for folder in {f for f in (Path(x).parent.name for x in glob.glob(str(ROOT / '*' / 'uk.html')))}:
        for lang in ('uk', 'en'):
            p = ROOT / folder / f'{lang}.html'
            s = p.read_text()
            s = re.sub(r'<!--funlinks-->.*?<!--/funlinks-->\n?', '', s, flags=re.S)
            items = sorted(by.get(folder, []))
            if items:
                head = 'Цікавинки до цього уроку' if lang == 'uk' else 'Curiosities for this lesson'
                page = 'cikavynky.html' if lang == 'uk' else 'cikavynky-en.html'
                lis = ''.join(f'<li><a href="../{page}#{cid}">{html.escape(tu if lang == "uk" else te)} →</a> <small>№{n}</small></li>' for n, cid, tu, te in items)
                block = f'<!--funlinks--><aside class="funlinks"><h2>{head}</h2><ul>{lis}</ul></aside><!--/funlinks-->\n'
                k = s.find('<nav class="lesson-nav"')
                if k < 0:
                    k = s.index('<footer class="site-copy"')
                s = s[:k] + block + s[k:]
                s = put_style(s, 'funlinks', LINKS_CSS, legacy=['funlinks'])
            p.write_text(s)


if __name__ == '__main__':
    build('uk')
    build('en')
    index_banner('uk')
    index_banner('en')
    lesson_links()
    print('ok')
