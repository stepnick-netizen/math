#!/usr/bin/env python3
"""«Це наша держава» / «This is our country»: civic.html and civic-en.html.

Run from the repo root:  python3 tools/civic.py   (then python3 tools/add_theme_toggle.py)
Same look as the home page (head, palette, footer, stats are taken from index.html).

Sources, checked 17.10.2026:
- Constitution of Ukraine (president.gov.ua): art. 1 «Україна є суверенна і незалежна, демократична, соціальна, правова держава.»;
  art. 5 «Носієм суверенітету і єдиним джерелом влади в Україні є народ.»; art. 36, 38, 40 (opening words verbatim, the rest retold).
- Ihor Koliushko, «Принципи правовладдя», CPLR, 2025 (pravo.org.ua): six principles after the Venice Commission (2011).
- CPLR facts (founded 1996, mission, vision): CPLR reference file.
- Law «Про звернення громадян»: an answer within one month (art. 20). Youth = 14–35 (Law «Про основні засади молодіжної політики», 2021).
- 1469 territorial hromadas since 2020; VAT 20 % (price 30 → VAT 5); Plast founded 1911; «Повернись живим» since 2014;
  EU candidate status 23.06.2022, accession talks opened 25.06.2024.
"""
import re, html
from pathlib import Path
from _inject import put_style

ROOT = Path(__file__).resolve().parent.parent


def t(x, y, s, size=14, col='--ink', w=700, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Comfortaa,Nunito,sans-serif" font-weight="{w}" font-size="{size}" fill="var({col})">{s}</text>'


def svg(body):
    return f'<svg viewBox="0 0 160 112" aria-hidden="true">{body}</svg>'


PICS = {
    # people at the top of a pyramid: the people are the source of power
    'people': ''.join(f'<circle cx="{30 + i * 25}" cy="78" r="8" fill="var(--sky)"/><path d="M{18 + i * 25} 104 Q{30 + i * 25} 84 {42 + i * 25} 104 Z" fill="var(--sky)"/>' for i in range(5))
              + '<path d="M80 12 L112 56 H48 Z" fill="var(--hay)"/>' + t(80, 50, 'влада', 11, '--marker-ink'),
    'rules': '<rect x="40" y="10" width="80" height="92" rx="6" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
             + ''.join(f'<line x1="52" y1="{30 + k * 14}" x2="108" y2="{30 + k * 14}" stroke="var(--muted)" stroke-width="2"/>' for k in range(5))
             + '<circle cx="114" cy="92" r="14" fill="var(--yarn)"/><path d="M107 92 l5 5 l9 -10" stroke="#fff" stroke-width="3" fill="none"/>',
    'referee': '<rect x="20" y="20" width="120" height="76" rx="6" fill="var(--leaf)" opacity=".85"/><line x1="80" y1="20" x2="80" y2="96" stroke="#fff" stroke-width="2"/>'
               '<circle cx="80" cy="58" r="12" fill="none" stroke="#fff" stroke-width="2"/><rect x="100" y="30" width="16" height="22" rx="2" fill="var(--hay)" transform="rotate(12 108 41)"/>',
    'hands': ''.join(f'<path d="M{24 + i * 28} 100 V{60 - (i % 2) * 10} q 0 -8 6 -8 q 6 0 6 8 V100 Z" fill="var({c})"/>' for i, c in enumerate(('--yarn', '--hay', '--sky', '--leaf', '--plum')))
             + '<path d="M14 100 H150" stroke="var(--ink)" stroke-width="3"/>',
    'letter': '<rect x="26" y="26" width="108" height="70" rx="6" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/><path d="M26 30 L80 66 L134 30" fill="none" stroke="var(--ink)" stroke-width="2.5"/>'
              + t(80, 18, '30 днів', 13, '--yarn'),
    'vote': '<rect x="40" y="46" width="80" height="54" rx="6" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/><rect x="62" y="44" width="36" height="6" rx="2" fill="var(--ink)"/>'
            '<rect x="64" y="12" width="32" height="40" rx="3" fill="var(--hay)" transform="rotate(-8 80 32)"/><path d="M70 30 l6 6 l12 -12" stroke="var(--marker-ink)" stroke-width="3" fill="none" transform="rotate(-8 80 32)"/>',
    'school': '<path d="M30 54 L80 22 L130 54 Z" fill="var(--yarn)"/><rect x="38" y="54" width="84" height="46" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
              + ''.join(f'<rect x="{48 + k * 22}" y="64" width="14" height="14" fill="var(--sky)"/>' for k in range(3)) + '<rect x="72" y="82" width="16" height="18" fill="var(--hay)"/>',
    'honest': '<rect x="36" y="24" width="88" height="70" rx="6" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>' + t(80, 70, '12', 34, '--leaf')
              + '<circle cx="120" cy="28" r="14" fill="var(--leaf)"/><path d="M113 28 l5 5 l9 -10" stroke="#fff" stroke-width="3" fill="none"/>',
    'map': '<path d="M14 60 Q30 30 60 36 Q80 18 108 30 Q140 30 146 56 Q150 84 118 88 Q96 102 66 94 Q30 100 18 82 Z" fill="var(--cell)" stroke="var(--ink)" stroke-width="2.5"/>'
           + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="var(--yarn)"/>' for x, y in ((40, 62), (62, 50), (88, 44), (110, 58), (128, 70), (74, 76), (98, 80), (52, 82))) + t(80, 108, '1469', 13, '--yarn'),
    'icecream': '<path d="M60 58 L80 104 L100 58 Z" fill="var(--hay)"/><circle cx="80" cy="46" r="22" fill="var(--yarn)"/><circle cx="70" cy="40" r="5" fill="#fff" opacity=".5"/>'
                + t(128, 40, '30 ₴', 15, '--ink') + t(128, 64, '5 ₴', 15, '--sky') + t(128, 80, 'ПДВ', 11, '--sky'),
    'eu': ''.join(f'<polygon points="{80 + 34 * __import__("math").cos(__import__("math").radians(k * 30)):.1f},{56 + 34 * __import__("math").sin(__import__("math").radians(k * 30)) - 5:.1f} '
                  f'{80 + 34 * __import__("math").cos(__import__("math").radians(k * 30)) + 4:.1f},{56 + 34 * __import__("math").sin(__import__("math").radians(k * 30)) + 3:.1f} '
                  f'{80 + 34 * __import__("math").cos(__import__("math").radians(k * 30)) - 4:.1f},{56 + 34 * __import__("math").sin(__import__("math").radians(k * 30)) + 3:.1f}" fill="var(--hay)"/>' for k in range(12))
          + '<rect x="66" y="44" width="28" height="12" fill="#0057B7"/><rect x="66" y="56" width="28" height="12" fill="#FFD700"/>',
    # --- from CPLR materials (17.10.2026) ---
    'book': '<rect x="36" y="10" width="88" height="92" rx="6" fill="var(--sky)"/><rect x="44" y="16" width="74" height="80" rx="3" fill="var(--paper)"/>'
            + t(81, 62, '30', 36, '--sky') + t(81, 84, '1996 → 2026', 11, '--muted'),
    'screen': '<rect x="28" y="16" width="104" height="66" rx="5" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/><path d="M16 90 H144 L136 100 H24 Z" fill="var(--ink)"/>'
              + ''.join(f'<line x1="40" y1="{32 + k * 11}" x2="{100 - (k % 2) * 18}" y2="{32 + k * 11}" stroke="var(--muted)" stroke-width="2.5"/>' for k in range(4))
              + '<circle cx="112" cy="58" r="12" fill="none" stroke="var(--sky)" stroke-width="4"/><path d="M121 67 l10 10" stroke="var(--sky)" stroke-width="5" stroke-linecap="round"/>',
    'office': '<path d="M24 44 L80 14 L136 44 Z" fill="var(--sky)"/><rect x="32" y="44" width="96" height="58" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
              + t(80, 38, 'ЦНАП', 12, '--paper') + ''.join(f'<circle cx="{46 + k * 23}" cy="60" r="7" fill="var({c})"/>' for k, c in enumerate(('--yarn', '--hay', '--leaf', '--plum')))
              + '<rect x="70" y="76" width="20" height="26" fill="var(--hay)"/>',
    'coins': ''.join(f'<ellipse cx="50" cy="{96 - k * 9}" rx="24" ry="7" fill="var(--hay)" stroke="var(--marker-ink)" stroke-width="1.5"/>' for k in range(6))
             + '<circle cx="114" cy="54" r="30" fill="var(--cell)" stroke="var(--ink)" stroke-width="2"/><path d="M114 54 V24 A30 30 0 0 1 142.5 63.3 Z" fill="var(--yarn)"/>' + t(114, 100, '30 %', 14, '--yarn'),
    'talk': '<path d="M14 18 H90 a8 8 0 0 1 8 8 V58 a8 8 0 0 1 -8 8 H40 L26 80 V66 H14 a8 8 0 0 1 -8 -8 V26 a8 8 0 0 1 8 -8 Z" fill="var(--sky)" opacity=".9"/>' + t(52, 52, '?', 30, '--paper')
            + '<path d="M70 46 H146 a8 8 0 0 1 8 8 V86 a8 8 0 0 1 -8 8 H134 V108 L120 94 H70 a8 8 0 0 1 -8 -8 V54 a8 8 0 0 1 8 -8 Z" fill="var(--hay)"/>' + t(108, 80, '!', 30, '--marker-ink'),
    'backpack': '<rect x="44" y="30" width="72" height="76" rx="16" fill="var(--leaf)"/><path d="M62 30 V22 a18 12 0 0 1 36 0 V30" fill="none" stroke="var(--ink)" stroke-width="4"/>'
                '<rect x="56" y="66" width="48" height="28" rx="6" fill="var(--paper)" opacity=".85"/><path d="M80 90 C64 80 66 70 73 70 C77 70 80 74 80 74 C80 74 83 70 87 70 C94 70 96 80 80 90 Z" fill="var(--yarn)"/>',
    'dome': '<path d="M50 40 A30 24 0 0 1 110 40 Z" fill="var(--sky)"/><rect x="34" y="40" width="92" height="8" fill="var(--ink)"/>'
            + ''.join(f'<rect x="{40 + k * 16}" y="50" width="8" height="38" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>' for k in range(6))
            + '<rect x="28" y="88" width="104" height="10" fill="var(--ink)"/>' + t(80, 30, '226', 14, '--paper'),
    'link': ''.join(f'<circle cx="{40 + k * 40}" cy="{56 + (k % 2) * 10 - 5}" r="24" fill="none" stroke="var({c})" stroke-width="7"/>' for k, c in enumerate(('--sky', '--hay', '--leaf'))),
    'search': '<rect x="26" y="12" width="74" height="92" rx="5" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
              + ''.join(f'<line x1="38" y1="{30 + k * 12}" x2="88" y2="{30 + k * 12}" stroke="var(--muted)" stroke-width="2.5"/>' for k in range(4))
              + '<circle cx="104" cy="70" r="20" fill="var(--cell)" stroke="var(--sky)" stroke-width="5"/><path d="M118 84 l18 18" stroke="var(--sky)" stroke-width="7" stroke-linecap="round"/>' + t(104, 78, '5', 22, '--yarn'),
    'petition': '<rect x="40" y="8" width="80" height="98" rx="5" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
                + ''.join(f'<path d="M50 {28 + k * 13} l4 4 l7 -8" stroke="var(--leaf)" stroke-width="2.5" fill="none"/><path d="M66 {28 + k * 13} q8 -6 16 0 t16 0" stroke="var(--sky)" stroke-width="2" fill="none"/>' for k in range(5))
                + t(80, 100, '25 000', 12, '--yarn'),
    'poll': '<path d="M20 100 H144" stroke="var(--ink)" stroke-width="3"/>' + ''.join(
                f'<rect x="{30 + k * 40}" y="{100 - h}" width="28" height="{h}" rx="3" fill="var({c})"/>' + t(44 + k * 40, 94 - h, f'{p} %', 12, c)
                for k, (h, p, c) in enumerate(((66, 55, '--leaf'), (42, 35, '--yarn'), (12, 10, '--muted')))),
    'tower': '<rect x="56" y="34" width="48" height="70" fill="var(--hay)" stroke="var(--marker-ink)" stroke-width="2"/><path d="M50 34 L80 10 L110 34 Z" fill="var(--yarn)"/>'
             + '<path d="M70 104 V82 a10 10 0 0 1 20 0 V104 Z" fill="var(--ink)"/>'
             '<rect x="74" y="48" width="12" height="16" rx="6" fill="var(--paper)"/><rect x="18" y="64" width="38" height="40" fill="var(--cell)" stroke="var(--ink)" stroke-width="2"/><rect x="104" y="64" width="38" height="40" fill="var(--cell)" stroke="var(--ink)" stroke-width="2"/>'
             '<path d="M80 10 V0" stroke="var(--ink)" stroke-width="2"/>',
    'broom': '<path d="M44 16 L96 70" stroke="var(--ink)" stroke-width="6" stroke-linecap="round"/><path d="M90 62 L114 50 L132 92 L108 104 Z" fill="var(--hay)"/>'
             + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--muted)" opacity=".55"/>' for x, y, r in ((30, 98, 5), (46, 92, 3), (58, 100, 4), (140, 102, 3), (20, 88, 2.5), (70, 94, 2))),
    'checklist': '<rect x="22" y="8" width="84" height="98" rx="5" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
                 + ''.join(f'<rect x="30" y="{15 + k * 13}" width="9" height="9" rx="2" fill="none" stroke="var(--ink)" stroke-width="1.5"/><line x1="46" y1="{20 + k * 13}" x2="96" y2="{20 + k * 13}" stroke="var(--muted)" stroke-width="2"/>' for k in range(7))
                 + ''.join(f'<path d="M31 {19 + k * 13} l3 3 l6 -7" stroke="var(--leaf)" stroke-width="2.5" fill="none"/>' for k in range(4))
                 + '<circle cx="128" cy="78" r="22" fill="#0057B7"/>' + ''.join(
                     f'<circle cx="{128 + 14 * __import__("math").cos(__import__("math").radians(k * 30)):.1f}" cy="{78 + 14 * __import__("math").sin(__import__("math").radians(k * 30)):.1f}" r="2" fill="#FFD700"/>' for k in range(12)),
}
PIC_EN = {'влада': 'power', '30 днів': '30 days', 'ПДВ': 'VAT', 'ЦНАП': 'ASC'}

# (id, picture, uk(title, text, question, answer), en(...))
SECTIONS = [
    ('who', 'Хто в державі головний?', 'Who is in charge of a country?', [
        ('people', 'people',
         ('Головний — народ, тобто ми',
          'Стаття 5 Конституції України: «Носієм суверенітету і єдиним джерелом влади в Україні є народ». Президент, депутати, міністри, мер — це люди, яким ми доручили роботу на певний час. Ми їх обираємо, ми платимо їм зарплату з наших податків, і вони мають звітувати перед нами.',
          'Чому депутата обирають лише на кілька років, а не назавжди?',
          'Щоб народ міг перевірити його роботу: якщо працював погано, на наступних виборах його можна не обрати. Влада — це доручення, а не власність.'),
         ('The people are in charge: that means us',
          'Article 5 of the Constitution of Ukraine says that the people are the bearer of sovereignty and the only source of power in Ukraine. The President, MPs, ministers and the mayor are people we have given a job for a fixed time. We elect them, we pay their salaries from our taxes, and they must answer to us.',
          'Why is an MP elected for a few years and not for ever?',
          'So that the people can check their work: if they did a bad job, they need not be elected next time. Power is a task entrusted to someone, not their property.')),
        ('class', 'school',
         ('Твій клас — маленька держава',
          'У класі є правила, які діють для всіх (як Конституція й закони). Є староста, якого обирають (як вибори). Є спільні гроші на екскурсію (як бюджет). А якщо виникла суперечка, її розглядає той, хто не на боці жодної сторони (як суд). Добрий клас — це коли правила чесні, а кожен голос чують.',
          'Староста сам вирішив витратити гроші класу на подарунок собі. Що не так?',
          'Спільні гроші належать усім, і витрачати їх можна лише так, як домовилися всі. Це і є підзвітність — головна вимога до будь-якої влади.'),
         ('Your class is a small country',
          'A class has rules that apply to everyone (like the Constitution and laws). It has a class captain who is elected (like elections). It has shared money for a trip (like a budget). And if there is a dispute, it is settled by someone who is on neither side (like a court). A good class is one where the rules are fair and every voice is heard.',
          'The class captain decided on their own to spend the class money on a present for themselves. What is wrong?',
          'Shared money belongs to everyone and can only be spent as everyone agreed. That is accountability, the key requirement for any power.')),
        ('constitution', 'book',
         ('Конституції — 30 років',
          'Конституцію України ухвалили 28 червня 1996 року, тож цього року їй виповнилося 30. Це головні правила країни: усі інші закони мають з нею узгоджуватися, так само як правила класу не можуть суперечити статуту школи. Змінювати Конституцію можна, але відкрито й після обговорення з людьми. Того ж 1996 року, після ухвалення Конституції, з’явився Центр політико-правових реформ — про нього нижче.',
          'У якому році Конституції виповниться 50? А скільки тоді буде тобі?',
          '1996 + 50 = 2046. Якщо ти народився у 2014 році, то у 2046-му тобі буде 2046 − 2014 = 32 роки.'),
         ('The Constitution is 30',
          'The Constitution of Ukraine was adopted on 28 June 1996, so it turned 30 this year. It holds the country’s main rules: every other law must agree with it, just as class rules cannot contradict the school charter. The Constitution can be changed, but openly and after discussion with the people. In the same year, 1996, after the Constitution was adopted, the Centre of Policy and Legal Reform was founded: more about it below.',
          'In what year will the Constitution turn 50? And how old will you be then?',
          '1996 + 50 = 2046. If you were born in 2014, in 2046 you will be 2046 − 2014 = 32.')),
    ]),
    ('law', 'Правовладдя: правила однакові для всіх', 'The rule of law: the same rules for everyone', [
        ('ruleoflaw', 'rules',
         ('Шість принципів правовладдя',
          'Голова правління Центру політико-правових реформ Ігор Коліушко пояснює правовладдя через шість принципів. Простими словами: 1) влада діє лише за законом; 2) закони зрозумілі, і їх знають наперед; 3) ніхто не може діяти свавільно, «як захотілося»; 4) права людини справді захищені; 5) закон однаковий для всіх — і для учня, і для міністра; 6) у будь-якій суперечці можна звернутися до суду.',
          'Директор школи оголосив нове правило вже після контрольної й покарав за нього учнів. Який принцип порушено?',
          'Юридична визначеність: правила мають бути відомі заздалегідь. Не можна карати за правило, якого ще не було.'),
         ('Six principles of the rule of law',
          'Ihor Koliushko, chair of the board of the Centre of Policy and Legal Reform, explains the rule of law through six principles. In plain words: 1) those in power act only according to the law; 2) laws are clear and known in advance; 3) no one may act arbitrarily, “just because they felt like it”; 4) human rights are really protected; 5) the law is the same for everyone, for a pupil and for a minister; 6) in any dispute you can go to court.',
          'A head teacher announced a new rule after a test and punished pupils for breaking it. Which principle was broken?',
          'Legal certainty: rules must be known in advance. You cannot punish someone under a rule that did not exist yet.')),
        ('referee', 'referee',
         ('Суд — як чесний суддя на футболі',
          'Уяви матч, де суддя грає за одну команду. Грати немає сенсу! Тому суд має бути незалежним: він не слухається ні президента, ні багатих, ні друзів. Сильна держава — та, де суд однаково справедливий до всіх.',
          None, None),
         ('A court is like a fair football referee',
          'Imagine a match where the referee plays for one team. There would be no point in playing! That is why courts must be independent: they take orders from no president, no rich people and no friends. A strong country is one where the court is equally fair to everyone.',
          None, None)),
        ('opencourt', 'screen',
         ('Рішення суду може прочитати кожен',
          'Чесний суд не ховається. З 2005 року діє закон «Про доступ до судових рішень», проєкт якого підготував Центр політико-правових реформ. Відтоді рішення судів публікують у Єдиному державному реєстрі судових рішень, і кожен може безкоштовно прочитати їх в інтернеті. Того ж року з’явилися адміністративні суди, які розглядають суперечки людини з владою. Їхню концепцію і Кодекс адміністративного судочинства теж розробив ЦППР.',
          'Сусід зламав ваш паркан — це суперечка між людьми. А якщо міська рада незаконно відмовила твоїй родині в документі, до якого суду звертатися?',
          'До адміністративного: він розглядає суперечки людини з владою. Влада теж відповідає перед судом.'),
         ('Anyone can read a court’s decision',
          'A fair court does not hide. Since 2005 Ukraine has had a law on access to court decisions, drafted by the Centre of Policy and Legal Reform. Since then court decisions have been published in the Unified State Register of Court Decisions, and anyone can read them online for free. In the same year administrative courts appeared: they settle disputes between a person and the authorities. Their concept and the Code of Administrative Procedure were also drafted by the CPLR.',
          'A neighbour broke your fence: that is a dispute between people. But if the town council unlawfully refused your family a document, which court do you go to?',
          'The administrative court: it settles disputes between a person and the authorities. Those in power answer to the court too.')),
    ]),
    ('service', 'Держава, яка служить тобі', 'A country that serves you', [
        ('cnap', 'office',
         ('ЦНАП: усе в одному місці',
          'Паспорт, реєстрація народження, довідка — це адміністративні послуги. Колись по них доводилося ходити різними кабінетами, а тепер є ЦНАП — центр надання адміністративних послуг, де багато справ можна залагодити в одному місці. Центр політико-правових реформ розробив концепцію реформи адмінпослуг (уряд схвалив її у 2006 році) і допомагав створювати перші ЦНАП, а у 2012 році ухвалили закон «Про адміністративні послуги». Навіть у прифронтовому Харкові восени 2022 року ЦНАП попри обстріли відновив основні послуги.',
          'За день ЦНАП надав 200 послуг, 90 % із них — безоплатні. Скільки послуг були платними?',
          '100 % − 90 % = 10 %. 10 % від 200 = 200 : 10 = 20 послуг.'),
         ('The service centre: everything in one place',
          'A passport, registering a birth, a certificate: these are administrative services. People used to go from office to office for them, but now there are Administrative Service Centres (ASC, «ЦНАП» in Ukrainian) where many things can be sorted out in one place. The Centre of Policy and Legal Reform drafted the concept for reforming these services (the government approved it in 2006) and helped set up the first centres, and in 2012 the Law on Administrative Services was passed. Even in Kharkiv, close to the front line, the centre restored its main services in autumn 2022 despite the shelling.',
          'In one day a service centre provided 200 services, and 90% of them were free. How many were paid?',
          '100% − 90% = 10%. 10% of 200 = 200 ÷ 10 = 20 services.')),
        ('procedure', 'talk',
         ('Тебе мають вислухати й пояснити',
          'Коли влада ухвалює рішення щодо людини, вона мусить дотримуватися закону «Про адміністративну процедуру»: вислухати людину, дати їй ознайомитися з документами, а якщо відмовляє — пояснити чому і як це рішення оскаржити. Над цим законом Центр політико-правових реформ працював з 1999 року. Парламент ухвалив його 17 лютого 2022 року, а запрацював він 15 грудня 2023-го. Наполегливість теж перемагає!',
          'Скільки років минуло від початку роботи над законом до його ухвалення?',
          '2022 − 1999 = 23 роки — майже вдвічі довше, ніж ти вчитимешся в школі (12 років).'),
         ('They must hear you out and explain',
          'When the authorities make a decision about a person, they must follow the Law on Administrative Procedure: hear the person out, let them see the documents and, if they say no, explain why and how to appeal. The Centre of Policy and Legal Reform worked on this law from 1999. Parliament passed it on 17 February 2022, and it came into force on 15 December 2023. Persistence wins too!',
          'How many years passed from the start of work on the law to its adoption?',
          '2022 − 1999 = 23 years, almost twice as long as you will spend at school (12 years).')),
        ('free', 'coins',
         ('Безоплатного не буває',
          '«Усі розуміють, що нічого безоплатного не буває», — каже експерт ЦППР Віктор Тимощук. У більшості ЦНАП 90 % послуг для людей безоплатні, а плата за решту покриває в середньому лише близько 30 % витрат на роботу ЦНАП. Реєстрація шлюбу, наприклад, коштує 85 копійок! Решту доплачує громада, тобто всі ми з наших податків. Тому ЦППР пропонує ухвалити закон про адміністративний збір, щоб кожна послуга мала чесну й зрозумілу ціну.',
          'Утримання ЦНАП коштує 1 000 000 грн на рік, а плата за послуги покриває 30 %. Скільки має доплатити громада?',
          '30 % від 1 000 000 = 300 000 грн. Доплатити треба 1 000 000 − 300 000 = 700 000 грн.'),
         ('Nothing is really free',
          '“Everyone understands that nothing is free,” says CPLR expert Viktor Tymoshchuk. In most service centres 90% of services are free for people, and the fees for the rest cover on average only about 30% of what it costs to run the centre. Registering a marriage, for example, costs 85 kopecks! The community pays the rest, which means all of us through our taxes. That is why the CPLR proposes a law on administrative fees, so that every service has a fair and clear price.',
          'Running a service centre costs 1,000,000 UAH a year, and fees cover 30%. How much does the community have to add?',
          '30% of 1,000,000 = 300,000 UAH. The community adds 1,000,000 − 300,000 = 700,000 UAH.')),
        ('newpupil', 'backpack',
         ('Новенька з Харківщини',
          'У клас прийшла дівчинка, родина якої переїхала через війну. Такі люди — внутрішньо переміщені особи (ВПО) — мають ті самі права, що й усі, і можуть отримати послуги на новому місці, наприклад довідку в місцевому ЦНАП. Для них ЦППР видав «Порадник для ВПО». А клас може допомогти по-своєму: показати школу, бібліотеку й гуртки. Коли наші землі звільнять, там доведеться відновити не лише будинки, а й школи, ЦНАП і місцеву владу. Експерти ЦППР разом із партнерами вже готують, як це зробити.',
          'У школі 600 учнів, із них 45 — з родин ВПО. Яку частку це становить у відсотках?',
          '45 : 600 · 100 % = 7,5 %. Тобто приблизно кожен тринадцятий учень.'),
         ('The new girl from the Kharkiv region',
          'A girl has joined the class whose family had to move because of the war. Such people are internally displaced persons (IDPs): they have the same rights as everyone and can get services in their new home, for example a certificate at the local service centre. The CPLR published a guide for them. And the class can help in its own way: show her the school, the library and the clubs. When our land is liberated, it will need more than new houses: schools, service centres and local government will have to be rebuilt too. CPLR experts and their partners are already preparing how to do it.',
          'A school has 600 pupils, and 45 of them come from displaced families. What percentage is that?',
          '45 ÷ 600 × 100% = 7.5%. That is about one pupil in thirteen.')),
    ]),
    ('laws', 'Як народжується закон', 'How a law is born', [
        ('rada', 'dome',
         ('226 із 450',
          'Верховна Рада — парламент України — має 450 народних депутатів. Закон ухвалено, якщо «за» проголосували щонайменше 226, тобто більше половини (статті 76 і 91 Конституції). Добрий закон народжується так: спершу описують проблему, потім обговорюють варіанти з людьми, а вже тоді голосують. Центр політико-правових реформ у «Білій книзі законодавчого процесу» (2023) показав, що буває інакше: закони ухвалюють поспіхом і без аналізу проблеми, а законопроєктів так багато, що їх не встигають перевірити. Експерти називають це «законодавчим спамом».',
          'У класі 28 учнів. За нове правило проголосували 15, проти — 9, решта утрималися. Правило ухвалено, якщо «за» більше половини всього класу. Ухвалили?',
          'Половина від 28 — це 14. 15 більше за 14, тож ухвалили. Так само в Раді: половина від 450 — це 225, тому потрібно щонайменше 226.'),
         ('226 out of 450',
          'The Verkhovna Rada, Ukraine’s parliament, has 450 MPs. A law is passed if at least 226 vote for it, that is, more than half (Articles 76 and 91 of the Constitution). A good law is born like this: first the problem is described, then the options are discussed with people, and only then comes the vote. In its White Book of the Law-Making Process (2023), the Centre of Policy and Legal Reform showed that things often go differently: laws are passed in a hurry without analysing the problem, and there are so many bills that nobody has time to check them. The experts call this “legislative spam”.',
          'A class has 28 pupils. 15 voted for a new rule, 9 against, and the rest abstained. The rule passes if more than half of the whole class votes for it. Did it pass?',
          'Half of 28 is 14. 15 is more than 14, so it passed. Parliament works the same way: half of 450 is 225, so at least 226 votes are needed.')),
        ('referendum', 'vote',
         ('Референдум: вирішує кожен',
          'Стаття 38 Конституції гарантує громадянам право брати участь у референдумах, коли рішення ухвалюють не депутати, а самі люди. У 2021 році ухвалили новий закон «Про всеукраїнський референдум», за який ЦППР провів адвокаційну кампанію. А от закону про місцевий референдум, де вирішують жителі громади, немає з 2012 року. Робоча група ЦППР розробила його проєкт і обговорила на 96 публічних заходах, а у 2021 році 112 депутатів внесли його до парламенту.',
          'Проєкт обговорили на 96 заходах. Скільки тижнів це триватиме, якщо проводити по 2 заходи на тиждень?',
          '96 : 2 = 48 тижнів — майже цілий рік.'),
         ('Referendum: everyone decides',
          'Article 38 of the Constitution gives citizens the right to take part in referendums, where decisions are made by the people themselves rather than by MPs. In 2021 a new law on national referendums was passed after an advocacy campaign by the CPLR. But there has been no law on local referendums, where residents of a community decide, since 2012. A CPLR working group drafted one and discussed it at 96 public events, and in 2021 112 MPs submitted it to parliament.',
          'The draft was discussed at 96 events. How many weeks would that take at 2 events a week?',
          '96 ÷ 2 = 48 weeks, almost a whole year.')),
    ]),
    ('society', 'Громадянське суспільство — це ми', 'Civil society is us', [
        ('together', 'hands',
         ('Коли люди об’єднуються самі',
          'Громадянське суспільство — це люди, які самі, без наказу згори, об’єднуються, щоб розв’язати спільну проблему. Стаття 36 Конституції: «Громадяни України мають право на свободу об’єднання у політичні партії та громадські організації». Пласт — українська скаутська організація — діє з 1911 року. Волонтери фонду «Повернись живим» допомагають армії з 2014 року. А з 2022 року мільйони українців стали волонтерами.',
          'Назви три об’єднання, які є біля тебе: у школі, у місті, в інтернеті.',
          'Наприклад: учнівське самоврядування, спортивний клуб, гурток, притулок для тварин, волонтерський чат, читацький клуб. Усе це — громадянське суспільство.'),
         ('When people join forces themselves',
          'Civil society is people joining forces on their own, without orders from above, to solve a shared problem. Article 36 of the Constitution gives citizens the right to freedom of association in political parties and civic organisations. Plast, the Ukrainian scout organisation, has been active since 1911. The Come Back Alive foundation has helped the army since 2014. And since 2022 millions of Ukrainians have become volunteers.',
          'Name three groups near you: at school, in your town, online.',
          'For example: the school council, a sports club, an after-school club, an animal shelter, a volunteer chat, a book club. All of that is civil society.')),
        ('cplr', 'rules',
         ('Як громадська організація змінює закони',
          'Центр політико-правових реформ — громадська організація юристів, заснована в 1996 році, після ухвалення Конституції. Такі організації називають аналітичними центрами: вони вивчають проблему, пишуть пропозиції й проєкти законів, пояснюють їх людям і переконують владу. Це називають адвокацією. Ось кілька законів, проєкти яких готували експерти ЦППР: 2005 — «Про доступ до судових рішень», 2011 — «Про доступ до публічної інформації», 2022 — «Про адміністративну процедуру». Між ідеєю і законом інколи минає понад 20 років.',
          'Що спільного в цих трьох законах?',
          'Усі вони роблять владу відкритішою для людини: можна прочитати рішення суду, дізнатися, що робить влада, і почути, чому тобі відмовили.'),
         ('How a civic organisation changes laws',
          'The Centre of Policy and Legal Reform is a civic organisation of lawyers founded in 1996, after the Constitution was adopted. Organisations like this are called think tanks: they study a problem, write proposals and draft laws, explain them to people and persuade those in power. This is called advocacy. Here are some laws drafted by CPLR experts: 2005, access to court decisions; 2011, access to public information; 2022, administrative procedure. Sometimes more than 20 years pass between an idea and a law.',
          'What do these three laws have in common?',
          'They all make power more open to people: you can read a court’s decision, find out what the authorities are doing and hear why you were refused.')),
        ('coalition', 'link',
         ('Сила — в об’єднанні',
          'Одну організацію почути важко. Тому в березні 2014 року, після Революції Гідності, громадські організації й експерти об’єдналися в коаліцію «Реанімаційний пакет реформ»; ЦППР — один із її засновників. А у 2023 році ЦППР провів у Львові Молодіжний аналітичний форум: 184 учасники з 23 регіонів. Коли йдеться про підготовку законів до вступу в ЄС, «тут має бути саме провідна роль молоді», — каже членкиня правління ЦППР Юлія Кириченко.',
          '184 учасники приїхали з 23 регіонів. Скільки в середньому з одного регіону?',
          '184 : 23 = 8 учасників.'),
         ('Strength in unity',
          'One organisation is hard to hear. So in March 2014, after the Revolution of Dignity, civic organisations and experts joined forces in the Reanimation Package of Reforms coalition; the CPLR is one of its founders. And in 2023 the CPLR held a Youth Analytical Forum in Lviv: 184 participants from 23 regions. When it comes to preparing Ukraine’s laws for joining the EU, “young people should play the leading role here,” says CPLR board member Yuliia Kyrychenko.',
          '184 participants came from 23 regions. How many per region on average?',
          '184 ÷ 23 = 8 participants.')),
    ]),
    ('you', 'Що ти можеш уже зараз', 'What you can do right now', [
        ('council', 'school',
         ('Учнівське самоврядування',
          'Закон «Про освіту» дає учням право на учнівське самоврядування. Це шанс уже в школі навчитися домовлятися, обирати й бути обраним, звітувати перед однокласниками. Запропонуй ідею: лавки на подвір’ї, клуб настільних ігор, шкільний ярмарок для ЗСУ.',
          None, None),
         ('The school council',
          'The Law on Education gives pupils the right to self-government at school. It is a chance to learn, already at school, how to agree, how to elect and be elected and how to report back to your classmates. Suggest an idea: benches in the yard, a board-games club, a school fair for the army.',
          None, None)),
        ('letter', 'letter',
         ('Напиши звернення — тобі мусять відповісти',
          'Стаття 40 Конституції: «Усі мають право направляти індивідуальні чи колективні письмові звернення» до органів влади, а посадовці зобов’язані їх розглянути й відповісти у строк, установлений законом, — зазвичай до одного місяця. Бачиш розбитий перехід чи темну зупинку? Напиши до громади разом із батьками.',
          'Як почати звернення?',
          'Наприклад: «Шановний голово громади! Біля школи № 5 немає світла на пішохідному переході. Взимку діти йдуть до школи в темряві. Прошу встановити ліхтар. Дякую». Додай своє ім’я, адресу й дату.'),
         ('Write a request: they must answer',
          'Article 40 of the Constitution says that everyone has the right to send individual or collective written requests to the authorities, and officials must consider them and reply within the time set by law, usually up to one month. Spot a broken crossing or a dark bus stop? Write to your local council together with your parents.',
          'How do you start a request?',
          'For example: “Dear Head of the Council! The pedestrian crossing by School No. 5 has no light. In winter children walk to school in the dark. Please install a street light. Thank you.” Add your name, address and the date.')),
        ('askinfo', 'search',
         ('Спитай владу — відповідь за 5 днів',
          'Хочеш знати, скільки коштуватиме ремонт спортмайданчика біля школи чи коли відкриють нове укриття? Надішли запит на публічну інформацію — можна разом із батьками. За законом «Про доступ до публічної інформації» (2011), проєкт якого підготував Центр політико-правових реформ, відповісти мають не пізніше ніж за 5 робочих днів. Пояснювати, навіщо тобі ця інформація, не треба.',
          'Ти надіслав запит у понеділок, і його того ж дня отримали. До якого дня мають відповісти?',
          'Рахуємо робочі дні з наступного дня: вівторок, середа, четвер, п’ятниця (субота й неділя — вихідні) і понеділок. Відповідь — до наступного понеділка.'),
         ('Ask the authorities: an answer within 5 days',
          'Want to know how much repairing the sports ground by your school will cost, or when the new shelter will open? Send a request for public information, together with your parents if you like. Under the 2011 Law on Access to Public Information, drafted by the Centre of Policy and Legal Reform, they must answer within 5 working days. You do not have to explain why you want to know.',
          'You sent a request on Monday and it was received the same day. By what day must they answer?',
          'Count working days from the next day: Tuesday, Wednesday, Thursday, Friday (Saturday and Sunday are days off) and Monday. The answer is due by the following Monday.')),
        ('petition', 'petition',
         ('Петиція: коли голосів багато',
          'Петиція — це звернення, яке підписують багато людей. Електронні петиції в Україні можна подавати з 2015 року. Щоб Президент, Верховна Рада чи уряд мусили розглянути петицію, за 3 місяці її мають підписати щонайменше 25 000 людей. Скільки підписів потрібно для петиції до міської чи сільської ради, кожна громада вирішує сама у своєму статуті.',
          'Петиція до міської ради має зібрати 1 000 підписів за 60 днів. За перші 10 днів зібрали 240. Чи встигнуть, якщо темп не зміниться?',
          '240 : 10 = 24 підписи на день. За 60 днів: 24 · 60 = 1 440 — це більше за 1 000. Встигнуть, і навіть раніше: 1 000 : 24 ≈ 42 дні.'),
         ('A petition: when many voices join',
          'A petition is a request signed by many people. Ukrainians have been able to file e-petitions since 2015. For the President, parliament or the government to be obliged to consider a petition, at least 25,000 people must sign it within 3 months. How many signatures a petition to a town or village council needs is decided by each community in its own statute.',
          'A petition to the town council must collect 1,000 signatures in 60 days. In the first 10 days it got 240. Will it make it if the pace stays the same?',
          '240 ÷ 10 = 24 signatures a day. In 60 days: 24 × 60 = 1,440, which is more than 1,000. It will make it, even early: 1,000 ÷ 24 ≈ 42 days.')),
        ('consult', 'poll',
         ('Спершу порадитися, потім вирішувати',
          'Добра влада радиться з людьми до рішення, а не після. Це називають публічними консультаціями: спершу описують проблему («зелена книга»), обговорюють її, а потім пропонують рішення («біла книга»). Експерти ЦППР працювали над законом «Про публічні консультації» й обстоювали його. Закон ухвалили у 2024 році, і він запрацює через рік після завершення воєнного стану. А в школі консультацію можна провести вже сьогодні, наприклад опитування перед зміною шкільної форми.',
          'В опитуванні про шкільну форму взяли участь 320 учнів: 176 — «за», 112 — «проти», решта не визначилися. Скільки відсотків у кожній групі?',
          '176 : 320 = 0,55 → 55 %; 112 : 320 = 0,35 → 35 %; решта 32 учні — 10 %. Перевір: 55 + 35 + 10 = 100.'),
         ('Consult first, decide later',
          'Good government talks to people before a decision, not after. This is called public consultation: first the problem is described (a “green book”), then discussed, and then a solution is proposed (a “white book”). CPLR experts worked on the Law on Public Consultations and campaigned for it. It was passed in 2024 and will come into force a year after martial law ends. But at school you can hold a consultation today, for example a poll before the school uniform changes.',
          '320 pupils took part in a poll about the school uniform: 176 for, 112 against, the rest undecided. What percentage is each group?',
          '176 ÷ 320 = 0.55 → 55%; 112 ÷ 320 = 0.35 → 35%; the other 32 pupils are 10%. Check: 55 + 35 + 10 = 100.')),
        ('budget', 'vote',
         ('Громадський бюджет: ти вирішуєш, на що підуть гроші',
          'У багатьох громадах частину бюджету віддають на проєкти, які пропонують і обирають самі мешканці: спортмайданчик, велодоріжка, укриття. А в деяких школах є шкільний громадський бюджет, де проєкти пропонують і обирають учні. Правила свої в кожній громаді — спитай у школі чи в міській раді.',
          'За проєкт «Турнік на подвір’ї» проголосували 312 учнів, за «Шахи в коридорі» — 309. Наскільки важливий кожен голос?',
          'Різниця — лише 3 голоси. Якби троє прихильників турніка лишилися вдома, була б нічия 309 : 309, а якби четверо — перемогли б шахи. Кожен голос вирішує!'),
         ('Participatory budget: you decide what the money is for',
          'In many communities part of the budget goes to projects that residents themselves propose and choose: a sports ground, a cycle lane, a shelter. And some schools have a school participatory budget where pupils propose and choose the projects. Each community has its own rules: ask at school or at the council.',
          '312 pupils voted for “A pull-up bar in the yard” and 309 for “Chess in the corridor”. How much does each vote matter?',
          'The gap is only 3 votes. If three pull-up fans had stayed at home it would be a 309 : 309 tie, and if four had, chess would have won. Every vote counts!')),
        ('honest', 'honest',
         ('Чесність починається з малого',
          'Корупція — це коли хтось використовує свою посаду чи владу для власної вигоди: бере «подарунок» за оцінку, влаштовує друга на роботу без конкурсу, краде спільні гроші. Країна стає сильною, коли люди звикають чесно: не списувати, не давати й не брати «подяк» за те, що й так належить, дотримувати обіцянок.',
          'Що з цього — корупція: а) учень списав контрольну; б) батьки дали вчителеві гроші за вищу оцінку; в) клас скинувся на подарунок учителеві на свято?',
          'Корупція — б): гроші за оцінку, яку мали поставити чесно. Списування (а) — нечесність, з якої починаються погані звички. Спільний подарунок на свято (в) — не за оцінку, тож це не корупція.'),
         ('Honesty starts small',
          'Corruption is when someone uses their position or power for their own gain: taking a “present” for a mark, giving a friend a job without fair selection, stealing shared money. A country grows strong when people get used to honesty: not cheating, not giving or taking “thank-yous” for what is due anyway, keeping promises.',
          'Which of these is corruption: a) a pupil copied in a test; b) parents gave a teacher money for a higher mark; c) the class chipped in for a holiday present for the teacher?',
          'Corruption is b): money for a mark that should have been given fairly. Copying (a) is dishonesty, which is where bad habits begin. A shared holiday present (c) is not for a mark, so it is not corruption.')),
        ('youth', 'hands',
         ('Молодь — з 14 років',
          'Закон називає молоддю людей від 14 до 35 років. У багатьох громадах діють молодіжні ради, де підлітки пропонують, що змінити в місті: від афіш для молоді до місць, де можна провести час. А волонтерити можна вже зараз: у притулку для тварин, на шкільному ярмарку, у бібліотеці.',
          None, None),
         ('Youth starts at 14',
          'Ukrainian law calls people aged 14 to 35 “youth”. Many communities have youth councils where teenagers suggest what to change in their town, from events for young people to places to spend time. And you can volunteer right now: at an animal shelter, a school fair or a library.',
          None, None)),
    ]),
    ('build', 'Яку державу ми будуємо', 'What kind of country we are building', [
        ('taxes', 'icecream',
         ('Податки — це наші спільні гроші',
          'Купуєш морозиво за 30 гривень? У ціні вже є податок на додану вартість (ПДВ) — 20 %. Тобто 25 грн коштує саме морозиво, а 5 грн іде до бюджету: 25 + 20 % = 25 + 5 = 30. З таких грошей платять учителям і лікарям, будують укриття й захищають країну. Тож і ти вже платник податків!',
          'Скільки ПДВ у шоколадці за 60 грн?',
          '60 : 120 · 20 = 10 грн. Перевір: 50 + 20 % від 50 = 50 + 10 = 60.'),
         ('Taxes are our shared money',
          'Buying an ice cream for 30 hryvnias? The price already includes value added tax (VAT) of 20%. So the ice cream itself costs 25 UAH and 5 UAH goes to the budget: 25 + 20% = 25 + 5 = 30. That money pays teachers and doctors, builds shelters and defends the country. So you are a taxpayer already!',
          'How much VAT is there in a 60-hryvnia chocolate bar?',
          '60 ÷ 120 × 20 = 10 UAH. Check: 50 + 20% of 50 = 50 + 10 = 60.')),
        ('hromada', 'map',
         ('Сильні громади',
          'З 2014 року Україна змінює устрій: більше прав і грошей отримали громади — міста, селища й села, що об’єдналися. Тепер їх 1469. Ідея проста: про ремонт школи чи дороги краще вирішувати тим, хто там живе, а не далекому кабінету в столиці. Це називають децентралізацією. Експерти ЦППР Ігор Коліушко й Олександр Бовш називають цю реформу «однією з найбільш успішних за весь період новітньої історії України».',
          'Бюджет громади — 50 млн грн: 40 % іде на освіту, 15 % — на дороги. Скільки грошей на кожне і скільки лишається на інше?',
          '40 % від 50 млн = 20 млн грн; 15 % від 50 млн = 7,5 млн грн. Лишається 50 − 20 − 7,5 = 22,5 млн грн, тобто 45 %.'),
         ('Strong communities',
          'Since 2014 Ukraine has been changing how it is organised: communities, towns and villages that joined together, have gained more rights and money. There are now 1,469 of them. The idea is simple: repairing a school or a road is best decided by the people who live there, not by a distant office in the capital. This is called decentralisation. CPLR experts Ihor Koliushko and Oleksandr Bovsh call it one of the most successful reforms in Ukraine’s modern history.',
          'A community budget is 50 million UAH: 40% goes to education and 15% to roads. How much is that for each, and how much is left for everything else?',
          '40% of 50 million = 20 million UAH; 15% of 50 million = 7.5 million UAH. That leaves 50 − 20 − 7.5 = 22.5 million UAH, or 45%.')),
        ('magdeburg', 'tower',
         ('Самоврядування — наша давня традиція',
          'Ще в середньовіччі українські міста отримували магдебурзьке право — право самим обирати міську владу, судити й вирішувати свої справи. Львів отримав його в 1356 році, Київ — наприкінці XV століття. Міста мали статути, тобто власні «правила гри». Експерти ЦППР вивчили історію статутів громад і розробили проєкт закону «Про самоврядування громади», щоб і сучасні громади мали сильні права.',
          'Скільки повних століть минуло від 1356 року до 2026-го?',
          '2026 − 1356 = 670 років, тобто 6 повних століть і ще 70 років.'),
         ('Self-government is an old tradition of ours',
          'As early as the Middle Ages, Ukrainian towns received Magdeburg rights: the right to elect their own town government, hold their own courts and run their own affairs. Lviv received them in 1356 and Kyiv at the end of the 15th century. Towns had charters, their own “rules of the game”. CPLR experts studied the history of community charters and drafted a law on community self-government so that today’s communities have strong rights too.',
          'How many full centuries passed from 1356 to 2026?',
          '2026 − 1356 = 670 years, that is, 6 full centuries and 70 more years.')),
        ('dust', 'broom',
         ('Корупція — як пил',
          '«Корупція, як пил: якщо регулярно не прибирати, то її кількість лише зростає і шкодить нормальному життю», — каже експертка ЦППР Ольга Піскунова. Тому з нею треба боротися постійно. В Індексі сприйняття корупції, де 100 балів має дуже чесна країна, Україна у 2021 році мала 32 бали, а у 2025-му — 36. Експерти ЦППР брали участь у підготовці закону про Національне антикорупційне бюро (2014) і обстоювали створення Вищого антикорупційного суду.',
          'З 2021 до 2025 року показник України зріс з 32 до 36 балів. На скільки відсотків?',
          '36 − 32 = 4 бали. 4 : 32 = 0,125 → на 12,5 %.'),
         ('Corruption is like dust',
          '“Corruption is like dust: if you don’t clean regularly, it only builds up and spoils normal life,” says CPLR expert Olha Piskunova. That is why it has to be fought all the time. In the Corruption Perceptions Index, where a very honest country scores 100, Ukraine had 32 points in 2021 and 36 in 2025. CPLR experts took part in preparing the law on the National Anti-Corruption Bureau (2014) and campaigned for the High Anti-Corruption Court.',
          'From 2021 to 2025 Ukraine’s score rose from 32 to 36. By what percentage?',
          '36 − 32 = 4 points. 4 ÷ 32 = 0.125 → by 12.5%.')),
        ('exam', 'checklist',
         ('Вступний іспит до ЄС',
          'Коли у 2022 році Україна стала кандидатом на вступ до Європейського Союзу, вона мала виконати 7 рекомендацій Європейської комісії: про суди, боротьбу з корупцією, права національних меншин, медіа та інше. Експерти ЦППР пояснили їх у виданні «Вступний іспит для України» і стежать, як Україна його складає. «Фактично ці реформи — другий фронт, без успіхів на якому нам буде важко перемогти на фронті військовому», — каже голова правління ЦППР Ігор Коліушко.',
          'Уяви: із 7 рекомендацій 4 виконано повністю, а 2 — частково (рахуємо як половину). На скільки відсотків виконано «домашнє завдання»?',
          '4 + 2 · 0,5 = 5 із 7. 5 : 7 ≈ 0,71 → приблизно 71 %.'),
         ('The entrance exam for the EU',
          'When Ukraine became a candidate to join the European Union in 2022, it had to carry out 7 recommendations from the European Commission: on the courts, fighting corruption, the rights of national minorities, the media and more. CPLR experts explained them in a publication called “An Entrance Exam for Ukraine” and follow how Ukraine is passing it. “In fact these reforms are a second front, and without success on it we will find it hard to win on the military front,” says CPLR board chair Ihor Koliushko.',
          'Imagine 4 of the 7 recommendations are fully done and 2 are half done (count them as a half each). What percentage of the “homework” is done?',
          '4 + 2 × 0.5 = 5 out of 7. 5 ÷ 7 ≈ 0.71 → about 71%.')),
        ('europe', 'eu',
         ('Європейська, демократична, правова',
          'Стаття 1 Конституції: «Україна є суверенна і незалежна, демократична, соціальна, правова держава». У червні 2022 року Україна стала кандидатом на вступ до Європейського Союзу, а в червні 2024-го почалися переговори про вступ. Щоб вступити, ми маємо зробити суди чесними, владу — підзвітною, а послуги — зручними. Це наша держава, і будувати її — нам.',
          None, None),
         ('European, democratic, governed by law',
          'Article 1 of the Constitution says Ukraine is a sovereign and independent, democratic, social, law-governed state. In June 2022 Ukraine became a candidate to join the European Union, and in June 2024 accession talks began. To join, we must make courts fair, those in power accountable and public services easy to use. This is our country, and building it is up to us.',
          None, None)),
    ]),
]

TXT = {
    'uk': dict(title='Це наша держава', h1='Це <span>наша</span> держава', file='civic.html', other='civic-en.html', other_l='English version',
               lead='Держава — це не лише влада в столиці. Це ми: правила, які ми встановлюємо, гроші, які ми разом збираємо, і рішення, які ми можемо змінити. Тут — як це працює і що ти можеш зробити вже зараз.',
               check='Спробуй сам', home='Математична пасіка', idx='index.html', crumb='Наша держава',
               src='Розділ підготовлено за матеріалами Центру політико-правових реформ (pravo.org.ua) і Конституції України.',
               read='Для вчителів і батьків: що почитати (матеріали ЦППР)'),
    'en': dict(title='This is our country', h1='This is <span>our</span> country', file='civic-en.html', other='civic.html', other_l='Українська версія',
               lead='A country is not just the government in the capital. It is us: the rules we set, the money we collect together and the decisions we can change. Here is how it works and what you can do right now.',
               check='Try it', home='The Maths Apiary', idx='index-en.html', crumb='Our country',
               src='Based on materials of the Centre of Policy and Legal Reform (pravo.org.ua) and the Constitution of Ukraine.',
               read='For teachers and parents: further reading (CPLR materials, in Ukrainian)'),
}

READ = [  # CPLR publications for teachers and parents (Ukrainian)
    ('Вступний іспит для України. Що маємо зробити для виконання рекомендацій ЄС', 'https://pravo.org.ua/books/vstupnyj-ispyt-dlya-ukrayiny-shho-mayemo-zrobyty-dlya-vykonannya-rekomendatsij-yes/'),
    ('Біла книга законодавчого процесу', 'https://pravo.org.ua/books/bila-knyga-zakonodavchogo-protsesu/'),
    ('Всеукраїнський та місцевий референдум в Україні: що? де? коли?', 'https://pravo.org.ua/blogs/vseukrayinskyj-ta-mistsevyj-referendum-v-ukrayini-shho-de-koly/'),
    ('Як змінилася робота ЦНАП в умовах війни', 'https://pravo.org.ua/analytical-materials/yak-zminylasya-robota-cznap-v-umovah-vijny-rezultaty-doslidzhennya/'),
    ('Інфографіка. Чому необхідно ухвалити закон про адміністративний збір', 'https://pravo.org.ua/analytical-materials/infografika-chomu-neobhidno-uhvalyty-zakon-pro-administratyvnyj-zbir/'),
    ('Порадник для ВПО: корисна інформація', 'https://pravo.org.ua/books/poradnyk-dlya-vpo-korysna-informatsiya/'),
    ('Довідник із запобігання корупції в органах місцевого самоврядування', 'https://pravo.org.ua/books/dovidnyk-iz-zapobigannya-koruptsiyi-v-organah-mistsevogo-samovryaduvannya/'),
    ('Статути громад в Україні: історія та спроба актуалізації', 'https://pravo.org.ua/blogs/statuty-gromad-v-ukrayini-istoriya-ta-sproba-aktualizacziyi/'),
    ('Молодь у майбутньому України. Підсумки Молодіжного аналітичного форуму', 'https://pravo.org.ua/molod-u-majbutnomu-ukrayiny-pidsumky-molodizhnogo-analitychnogo-forumu/'),
    ('Центр політико-правових реформ: 16 кроків за 16 років', 'https://pravo.org.ua/tsentr-polityko-pravovyh-reform-16-krokiv-za-16-rokiv/'),
    ('Річний звіт ЦППР 2023', 'https://dev.pravo.org.ua/wp-content/uploads/2024/11/czppr_richnyj_zvit_2023.pdf'),
    ('Конституція України', 'https://zakon.rada.gov.ua/laws/show/254%D0%BA/96-%D0%B2%D1%80'),
]

CSS = """/* civic */.wrap>nav.site-home{justify-self:stretch;width:100%}.civ-head{display:grid;gap:10px}
.civ-nav{display:flex;flex-wrap:wrap;gap:8px}.civ-nav a{font:700 14.5px var(--body);color:var(--ink);text-decoration:none;background:var(--paper);border:1.5px solid var(--line);border-left:4px solid var(--sky);border-radius:10px;padding:6px 11px}
.civ-sec{display:grid;gap:12px;scroll-margin-top:12px}.civ-sec>h2{display:flex;align-items:center;gap:10px}
.civ-sec>h2::before{content:"";width:16px;height:18px;flex:none;background:linear-gradient(#0057B7 0 50%,#FFD700 50% 100%);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.civ-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px;align-items:start}
.civ{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:0 3px 0 var(--shadow);display:grid;grid-template-columns:140px 1fr;gap:14px}
.civ svg{width:140px;height:auto}.civ-body{display:grid;gap:8px;min-width:0;align-content:start}.civ h3{font:700 19px/1.3 var(--display);margin:0}.civ p{margin:0;font-size:15.5px}
.civ details{background:var(--cell);border-radius:12px;padding:8px 12px}.civ summary{cursor:pointer;font-weight:800;color:var(--sky)}.civ details p{margin-top:6px}
.civ-src{color:var(--muted);font-size:14px;border-top:1px solid var(--line);padding-top:10px}
.civ-read{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:10px 14px}.civ-read summary{cursor:pointer;font-weight:800;color:var(--sky)}.civ-read ul{margin:8px 0 2px;padding-left:20px;display:grid;gap:4px;font-size:15px}
@media (max-width:560px){.civ{grid-template-columns:1fr}.civ svg{width:160px;justify-self:center}}"""


def build(lang):
    tx = TXT[lang]
    tpl = (ROOT / tx['idx']).read_text()
    head = tpl[:tpl.index('<body')]
    head = re.sub(r'<title>.*?</title>', f'<title>{tx["title"]} · {tx["home"]}</title>', head, count=1)
    head = put_style(head, 'civic', CSS)
    foot = tpl[tpl.index('<footer class="site-copy"'):]
    for pat in (r'<script>/\* toc \*/.*?</script>', r'<script>/\* theme switch \*/.*?</script>', r'<script>\s*\(function\(\)\{var K=.ponya-bulya-profile-v1.*?</script>'):
        foot = re.sub(pat, '', foot, flags=re.S)
    nav = ''.join(f'<a href="#{sid}">{su if lang == "uk" else se}</a>' for sid, su, se, _ in SECTIONS)
    secs = ''
    for sid, su, se, cards in SECTIONS:
        cs = ''
        for cid, pk, uk, en in cards:
            title, text, q, a = uk if lang == 'uk' else en
            pic = PICS[pk]
            if lang == 'en':
                for k, v in PIC_EN.items():
                    pic = pic.replace(k, v)
            body = f'<h3>{html.escape(title)}</h3><p>{html.escape(text)}</p>'
            if q:
                body += f'<details><summary>{tx["check"]}: {html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
            cs += f'<article class="civ" id="{cid}">{svg(pic)}<div class="civ-body">{body}</div></article>'
        secs += f'<section class="civ-sec" id="{sid}"><h2>{su if lang == "uk" else se}</h2><div class="civ-grid">{cs}</div></section>'
    read = ('<details class="civ-read"><summary>' + tx['read'] + '</summary><ul>'
            + ''.join(f'<li><a href="{u}" target="_blank" rel="noopener"{"" if lang == "uk" else " hreflang=uk"}>{html.escape(n)}</a></li>' for n, u in READ) + '</ul></details>')
    body = (f'<body>\n<div class="wrap">\n<nav class="site-home" aria-label="breadcrumb"><a href="{tx["idx"]}">← {tx["home"]}</a><span class="sep">›</span><span class="here">{tx["crumb"]}</span></nav>'
            f'<header class="civ-head"><h1>{tx["h1"]}</h1><p>{tx["lead"]}</p><p style="font-size:15px"><a href="{tx["other"]}">{tx["other_l"]}</a></p></header>'
            f'<nav class="civ-nav">{nav}</nav>{secs}{read}<p class="civ-src">{tx["src"]}</p>\n</div>\n')
    (ROOT / tx['file']).write_text(head + body + foot)


if __name__ == '__main__':
    build('uk')
    build('en')
    print('ok')
