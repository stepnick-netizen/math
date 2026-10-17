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
}
PIC_EN = {'влада': 'power', '30 днів': '30 days', 'ПДВ': 'VAT'}

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
         ('Експерти, які допомагають державі ставати кращою',
          'Громадські організації не лише допомагають людям, а й підказують державі, як працювати краще. Наприклад, Центр політико-правових реформ — громадська організація, яка постала в 1996 році, того ж року, що й Конституція. Її юристи пропонують, як зробити зручнішими адміністративні послуги, сильнішим місцеве самоврядування, чеснішою роботу влади, і готують Україну до вступу в Європейський Союз.',
          None, None),
         ('Experts who help the country get better',
          'Civic organisations do not only help people: they also show the state how to work better. For example, the Centre of Policy and Legal Reform is a civic organisation founded in 1996, the same year as the Constitution. Its lawyers propose how to make public services easier to use, local self-government stronger and the work of the authorities more honest, and they help prepare Ukraine to join the European Union.',
          None, None)),
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
          'З 2015 року Україна змінює устрій: більше прав і грошей отримали громади — міста, селища й села, що об’єдналися. Тепер їх 1469. Ідея проста: про ремонт школи чи дороги краще вирішувати тим, хто там живе, а не далекому кабінету в столиці. Це називають децентралізацією.',
          None, None),
         ('Strong communities',
          'Since 2015 Ukraine has been changing how it is organised: communities, towns and villages that joined together, have gained more rights and money. There are now 1,469 of them. The idea is simple: repairing a school or a road is best decided by the people who live there, not by a distant office in the capital. This is called decentralisation.',
          None, None)),
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
               src='Розділ підготовлено за матеріалами Центру політико-правових реформ (pravo.org.ua) і Конституції України.'),
    'en': dict(title='This is our country', h1='This is <span>our</span> country', file='civic-en.html', other='civic.html', other_l='Українська версія',
               lead='A country is not just the government in the capital. It is us: the rules we set, the money we collect together and the decisions we can change. Here is how it works and what you can do right now.',
               check='Try it', home='The Maths Apiary', idx='index-en.html', crumb='Our country',
               src='Based on materials of the Centre of Policy and Legal Reform (pravo.org.ua) and the Constitution of Ukraine.'),
}

CSS = """/* civic */.wrap>nav.site-home{justify-self:stretch;width:100%}.civ-head{display:grid;gap:10px}
.civ-nav{display:flex;flex-wrap:wrap;gap:8px}.civ-nav a{font:700 14.5px var(--body);color:var(--ink);text-decoration:none;background:var(--paper);border:1.5px solid var(--line);border-left:4px solid var(--sky);border-radius:10px;padding:6px 11px}
.civ-sec{display:grid;gap:12px;scroll-margin-top:12px}.civ-sec>h2{display:flex;align-items:center;gap:10px}
.civ-sec>h2::before{content:"";width:16px;height:18px;flex:none;background:linear-gradient(#0057B7 0 50%,#FFD700 50% 100%);clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.civ-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px;align-items:start}
.civ{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:16px;box-shadow:0 3px 0 var(--shadow);display:grid;grid-template-columns:140px 1fr;gap:14px}
.civ svg{width:140px;height:auto}.civ-body{display:grid;gap:8px;min-width:0;align-content:start}.civ h3{font:700 19px/1.3 var(--display);margin:0}.civ p{margin:0;font-size:15.5px}
.civ details{background:var(--cell);border-radius:12px;padding:8px 12px}.civ summary{cursor:pointer;font-weight:800;color:var(--sky)}.civ details p{margin-top:6px}
.civ-src{color:var(--muted);font-size:14px;border-top:1px solid var(--line);padding-top:10px}
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
    body = (f'<body>\n<div class="wrap">\n<nav class="site-home" aria-label="breadcrumb"><a href="{tx["idx"]}">← {tx["home"]}</a><span class="sep">›</span><span class="here">{tx["crumb"]}</span></nav>'
            f'<header class="civ-head"><h1>{tx["h1"]}</h1><p>{tx["lead"]}</p><p style="font-size:15px"><a href="{tx["other"]}">{tx["other_l"]}</a></p></header>'
            f'<nav class="civ-nav">{nav}</nav>{secs}<p class="civ-src">{tx["src"]}</p>\n</div>\n')
    (ROOT / tx['file']).write_text(head + body + foot)


if __name__ == '__main__':
    build('uk')
    build('en')
    print('ok')
