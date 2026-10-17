#!/usr/bin/env python3
"""«Це наша держава» / «This is our country»: civic.html and civic-en.html.

Run from the repo root:  python3 tools/civic.py   (then python3 tools/add_theme_toggle.py)
Same look as the home page (head, palette, footer, stats are taken from index.html).

Rebuilt 17.10.2026 from documents Mykola sent (CPLR):
- «Як громадяни можуть забезпечити розвиток своєї країни (набір ідей для суспільного договору)», draft 2025 —
  presented as a DRAFT for discussion; contested proposals (voting age 20–70, compulsory training, life-cycle table) NOT used.
- CPLR profile (2024): vision, mission, values, 9 directions, goals, «основні досягнення»; transparency 2016; UPLAN since 2017, 68 experts in 6 oblasts.
- CPLR strategic plan 2024–2025 (goals are goals, not results).
- Anti-corruption direction report 2026 (results only: Prosecutor General bill registered 22.06.2026, proposals in draft
  Anti-Corruption Strategy 2026–2030, HACC trainings, student moot court; new Criminal Code — Khavroniuk's participation in
  the presidential working group, not institutional). Plans, projects, donors, risks NOT used.
- «Бачення України — 2030»: coalition «Україна після перемоги» (end of March 2022), document June 2022 (pravo.org.ua PDF);
  CPLR event 9.03.2023: 7 concepts (Sept 2022 – March 2023); socio-humanitarian chapter (NaUKMA + RPR): 2030 targets 95 % / 75 %.
  The page pravo.org.ua/bachennya-ukrayiny-2030/ itself could not be fetched automatically.
- Also: Constitution art. 70 (vote at 18); CPI 2021 = 32, 2025 = 36 (mind.ua); Khavroniuk quote (CPLR annual report 2023);
  «Вступний іспит для України»; CPLR registered 18.11.1996 (Koliushko presentation 29.05.2025).
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

    # --- 2026 rebuild: social contract, Vision 2030, CPLR profile ---
    'scroll': '<path d="M36 18 H118 a10 10 0 0 1 0 20 H112 V96 a10 10 0 0 1 -10 10 H44 a10 10 0 0 1 0 -20 H48 V28 a10 10 0 0 0 -12 -10 Z" fill="var(--paper)" stroke="var(--ink)" stroke-width="2.5"/>'
              + ''.join(f'<line x1="58" y1="{44 + k * 10}" x2="102" y2="{44 + k * 10}" stroke="var(--muted)" stroke-width="2"/>' for k in range(3))
              + '<path d="M58 80 q8 -8 14 0 t14 0 t14 0" stroke="var(--sky)" stroke-width="2.5" fill="none"/><path d="M120 60 L142 30 l6 4 L126 64 Z" fill="var(--hay)"/><path d="M120 60 l-3 9 l8 -5" fill="var(--ink)"/>',
    'timeline': '<path d="M10 64 H150" stroke="var(--ink)" stroke-width="3"/>' + ''.join(
                f'<circle cx="{x}" cy="64" r="{r}" fill="var({c})"/>' + t(x, 48 if k % 2 else 92, lab, 10.5, '--ink')
                for k, (x, r, c, lab) in enumerate(((20, 6, '--sky', 'Русь'), (52, 6, '--leaf', 'Козаки'), (84, 6, '--yarn', '1918'), (114, 7, '--hay', '1991'), (142, 7, '--sky', '1996')))),
    'identity': '<circle cx="62" cy="58" r="34" fill="#0057B7"/><path d="M28 58 A34 34 0 0 0 96 58 Z" fill="#FFD700"/>'
                '<circle cx="104" cy="58" r="34" fill="none" stroke="#0057B7" stroke-width="4"/>' + ''.join(
                f'<circle cx="{104 + 22 * __import__("math").cos(__import__("math").radians(k * 30)):.1f}" cy="{58 + 22 * __import__("math").sin(__import__("math").radians(k * 30)):.1f}" r="2.6" fill="#FFD700"/>' for k in range(12)),
    'net': (lambda pts: ''.join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="var(--sky)" stroke-width="1.6" opacity=".7"/>' for i, a in enumerate(pts) for b in pts[i + 1:])
            + ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="var({c})"/>' for (x, y), c in zip(pts, ('--yarn', '--hay', '--leaf', '--plum', '--sky', '--yarn', '--hay')))
            )([(80, 14), (124, 34), (134, 78), (100, 104), (56, 104), (26, 78), (36, 34)]),
    'spread': '<circle cx="80" cy="14" r="7" fill="var(--yarn)"/>' + ''.join(
                f'<line x1="80" y1="14" x2="{x}" y2="50" stroke="var(--muted)" stroke-width="1.5"/><circle cx="{x}" cy="50" r="6" fill="var(--hay)"/>'
                + ''.join(f'<line x1="{x}" y1="50" x2="{x + d}" y2="92" stroke="var(--muted)" stroke-width="1.2"/><circle cx="{x + d}" cy="92" r="4.5" fill="var(--sky)"/>' for d in (-16, 0, 16))
                for x in (32, 80, 128)) + t(80, 110, '3 → 9 → 27', 11, '--muted'),
    'tree': '<rect x="74" y="66" width="12" height="38" fill="#8a5a2b"/><circle cx="80" cy="46" r="30" fill="var(--leaf)"/><circle cx="58" cy="60" r="18" fill="var(--leaf)"/><circle cx="102" cy="60" r="18" fill="var(--leaf)"/>'
            '<path d="M20 104 H140" stroke="var(--ink)" stroke-width="3"/><circle cx="66" cy="38" r="4" fill="var(--yarn)"/><circle cx="96" cy="50" r="4" fill="var(--yarn)"/><circle cx="80" cy="28" r="4" fill="var(--yarn)"/>',
    'shield': '<path d="M80 8 L128 24 V58 C128 84 106 100 80 108 C54 100 32 84 32 58 V24 Z" fill="#0057B7"/><path d="M80 58 V108 C54 100 32 84 32 58 Z" fill="#FFD700"/><path d="M80 58 H128 C128 84 106 100 80 108 Z" fill="#FFD700"/>'
              '<path d="M80 8 L128 24 V58 H32 V24 Z" fill="#0057B7"/>' + '<text x="80" y="50" text-anchor="middle" font-family="Comfortaa,Nunito,sans-serif" font-weight="700" font-size="18" fill="#fff">18+</text>',
    'levels': '<rect x="16" y="14" width="128" height="90" rx="10" fill="var(--cell)" stroke="var(--sky)" stroke-width="2.5"/><rect x="34" y="34" width="92" height="64" rx="8" fill="var(--paper)" stroke="var(--leaf)" stroke-width="2.5"/>'
              '<rect x="54" y="54" width="52" height="40" rx="6" fill="var(--hay)"/>' + t(80, 29, 'держава', 11, '--sky') + t(80, 48, 'регіон', 11, '--leaf') + t(80, 79, 'громада', 11, '--marker-ink'),
    'grid12': ''.join(f'<rect x="{22 + (k % 4) * 30}" y="{14 + (k // 4) * 30}" width="24" height="24" rx="5" fill="var({c})"/>' + t(34 + (k % 4) * 30, 31 + (k // 4) * 30, str(k + 1), 11, '--paper')
                      for k, c in enumerate(['--sky', '--leaf', '--hay', '--yarn', '--plum', '--sky', '--leaf', '--hay', '--yarn', '--plum', '--sky', '--leaf'])),
    'sunrise': '<path d="M14 84 H146" stroke="var(--ink)" stroke-width="3"/><path d="M40 84 A40 40 0 0 1 120 84 Z" fill="var(--hay)"/>'
               + ''.join(f'<line x1="{80 + 48 * __import__("math").cos(__import__("math").radians(a)):.1f}" y1="{84 - 48 * __import__("math").sin(__import__("math").radians(a)):.1f}" x2="{80 + 60 * __import__("math").cos(__import__("math").radians(a)):.1f}" y2="{84 - 60 * __import__("math").sin(__import__("math").radians(a)):.1f}" stroke="var(--hay)" stroke-width="3" stroke-linecap="round"/>' for a in (20, 50, 80, 110, 140, 160))
               + t(80, 76, '2030', 18, '--marker-ink') + '<path d="M14 96 H146" stroke="var(--sky)" stroke-width="3" opacity=".6"/>',
    'seven': ''.join(f'<polygon points="{" ".join(f"{cx + 15 * __import__("math").cos(__import__("math").radians(60 * j + 30)):.1f},{cy + 15 * __import__("math").sin(__import__("math").radians(60 * j + 30)):.1f}" for j in range(6))}" fill="var({c})"/>' + t(cx, cy + 5, str(n), 13, '--paper')
                     for n, (cx, cy, c) in enumerate(((80, 58, '--yarn'), (80, 31, '--sky'), (103.4, 44.5, '--leaf'), (103.4, 71.5, '--hay'), (80, 85, '--plum'), (56.6, 71.5, '--sky'), (56.6, 44.5, '--leaf')), 1)),
    'hexa': '<polygon points="80,10 122,34 122,82 80,106 38,82 38,34" fill="var(--sky)"/><polygon points="80,22 112,40 112,76 80,94 48,76 48,40" fill="var(--paper)"/>' + t(80, 56, '1996', 16, '--sky') + t(80, 76, '30', 16, '--yarn'),
    'target': ''.join(f'<circle cx="80" cy="58" r="{r}" fill="var({c})"/>' for r, c in ((46, '--yarn'), (34, '--paper'), (22, '--yarn'), (10, '--paper')))
              + '<path d="M80 58 L136 12" stroke="var(--ink)" stroke-width="3"/><path d="M136 12 l-12 2 l4 4 l4 4 Z" fill="var(--ink)"/>' + t(28, 108, '9', 16, '--sky', anchor='start'),
}
PIC_EN = {'влада': 'power', '30 днів': '30 days', 'ПДВ': 'VAT', 'ЦНАП': 'ASC', 'Русь': 'Rus', 'Козаки': 'Cossacks', 'держава': 'state', 'регіон': 'region', 'громада': 'community'}

# (id, picture, uk(title, text, question, answer), en(...))
SECTIONS = [
    ('contract', 'Суспільний договір: як ми домовляємося жити разом', 'The social contract: how we agree to live together', [
        ('what', 'scroll',
         ('Що таке суспільний договір',
          'Ідея суспільного договору з’явилася у XVII–XVIII століттях: держава постає не з волі короля, а з домовленості людей. Суспільний договір — це набір принципів і правил поведінки, які більшість людей вважає корисними для всіх. Якщо їх дотримуватися, країна розвивається швидше. У 2025 році група українських науковців і суспільних авторитетів підготувала проєкт «Суспільного договору для України» — набір ідей для обговорення. Головна думка: «Українська держава… є і буде тепер завжди! Якою вона буде, залежить від Українського народу».',
          'Хто бере участь у суспільному договорі: лише ті, хто живе зараз?',
          'Ні. За проєктом, у ньому «участь поколінь померлих і ненароджених»: від попередніх поколінь ми успадкували країну, а нашим нащадкам маємо її зберегти й примножити.'),
         ('What a social contract is',
          'The idea of a social contract appeared in the 17th and 18th centuries: a state comes not from a king’s will but from an agreement between people. A social contract is a set of principles and rules of behaviour that most people find useful for everyone. If people follow them, the country develops faster. In 2025 a group of Ukrainian scholars and respected public figures drafted a “Social Contract for Ukraine”, a set of ideas for discussion. Its main thought: the Ukrainian state exists and will exist for ever, and what it will be like depends on the Ukrainian people.',
          'Who takes part in the social contract: only the people alive now?',
          'No. According to the draft, it includes the generations who have died and those not yet born: we inherited the country from earlier generations and must keep it and make it better for those who come after us.')),
        ('heirs', 'timeline',
         ('Ми — спадкоємці',
          'Сучасна Україна — спадкоємиця Руської держави з центром у Києві (IX–XIII ст.), Галицько-Волинської держави (XIII–XIV ст.), Козацької держави (XVII–XVIII ст.), УНР, Української Держави і ЗУНР (1918–1920). 22 січня 1918 року проголосили незалежність УНР, 24 серпня 1991 року — незалежність України, 1 грудня 1991 року її підтвердили на всеукраїнському референдумі, а 28 червня 1996 року ухвалили Конституцію. У 2014 році Росія напала на Україну — окупувала Крим і частину Донбасу, а у 2022 році почала повномасштабне вторгнення. Ми не здалися.',
          'Скільки років минуло від проголошення незалежності УНР 22 січня 1918 року до 24 серпня 1991 року?',
          '1991 − 1918 = 73 роки (і ще 7 місяців). Майже три покоління боролися за те, щоб держава повернулася.'),
         ('We are heirs',
          'Modern Ukraine is the heir of the Rus state centred on Kyiv (9th–13th centuries), the Galician-Volhynian state (13th–14th), the Cossack state (17th–18th), and the Ukrainian People’s Republic, the Ukrainian State and the West Ukrainian People’s Republic (1918–1920). Independence of the Ukrainian People’s Republic was proclaimed on 22 January 1918, Ukraine’s independence on 24 August 1991, confirmed in a national referendum on 1 December 1991, and the Constitution was adopted on 28 June 1996. In 2014 Russia attacked Ukraine, occupying Crimea and part of Donbas, and in 2022 it launched a full-scale invasion. We did not give up.',
          'How many years passed between the proclamation of independence on 22 January 1918 and 24 August 1991?',
          '1991 − 1918 = 73 years (and 7 more months). Almost three generations fought for the state to come back.')),
        ('identity', 'identity',
         ('Ми — українці. Ми — європейці',
          'Український народ — політична нація: це громадяни України, які незалежно від етнічного походження вважають себе спадкоємцями історії Українського народу і пов’язують своє майбутнє з Україною. Бути українцем, за проєктом суспільного договору, означає знати й шанувати свою історію, знати українську мову й користуватися нею, будувати спільне майбутнє в Українській державі. Кримські татари — корінний народ Криму і частина Українського народу. А ще ми — європейці: поділяємо права людини, демократію й правовладдя. «Від інших народів і держав ми прагнемо поваги за наші успіхи і досягнення, а не страху через нашу силу».',
          'Чи може бути українцем людина, чиї бабуся й дідусь приїхали з іншої країни?',
          'Так. Політична нація — це не про походження, а про вибір: громадянин, який вважає історію України своєю і пов’язує з нею майбутнє, — українець.'),
         ('We are Ukrainians. We are Europeans',
          'The Ukrainian people is a political nation: citizens of Ukraine who, whatever their ethnic origin, see themselves as heirs to the history of the Ukrainian people and link their future with Ukraine. According to the draft social contract, being Ukrainian means knowing and honouring our history, knowing and using the Ukrainian language and building our shared future in the Ukrainian state. The Crimean Tatars are the indigenous people of Crimea and part of the Ukrainian people. And we are Europeans too: we share human rights, democracy and the rule of law. “From other nations and states we seek respect for our successes and achievements, not fear of our strength.”',
          'Can someone whose grandparents came from another country be Ukrainian?',
          'Yes. A political nation is about choice, not origin: a citizen who sees Ukraine’s history as their own and links their future with it is Ukrainian.')),
        ('trust', 'net',
         ('Довіра — швидкий шлях уперед',
          'Проєкт суспільного договору наголошує: «швидкий розвиток країни можливий лише в умовах довіри громадян один до одного та до створених ними інституцій». А довіра можлива, коли люди відмовляються збагачуватися нечесно за рахунок інших і не застосовують силу, щоб розв’язати суперечки між собою. У класі так само: якщо ніхто не бере чужого й не б’ється, можна разом робити великі справи.',
          'У класі 28 учнів. Скільки пар «я довіряю тобі — ти довіряєш мені» може бути, якщо довіряють усі всім?',
          'Кожен із 28 учнів утворює пару з 27 іншими: 28 · 27 = 756, але так кожну пару пораховано двічі. 756 : 2 = 378 пар. Що більше довіри, то більше зв’язків!'),
         ('Trust is the fast way forward',
          'The draft social contract stresses that a country can develop fast only when citizens trust one another and the institutions they create. And trust is possible when people refuse to get rich dishonestly at others’ expense and do not use force to settle arguments among themselves. A class works the same way: if nobody takes what is not theirs and nobody fights, you can do big things together.',
          'A class has 28 pupils. How many “I trust you, you trust me” pairs can there be if everyone trusts everyone?',
          'Each of the 28 pupils pairs with 27 others: 28 × 27 = 756, but that counts every pair twice. 756 ÷ 2 = 378 pairs. The more trust, the more connections!')),
    ]),
    ('citizen', 'Звички громадянина, які роблять країну сильною', 'Citizen habits that make a country strong', [
        ('honesty', 'honest',
         ('Чесність і чесна праця',
          'Перші принципи громадянина в проєкті суспільного договору — давні й прості: не вбивати, не красти, не свідчити неправдиво, не жадати чужого. А ще — дотримуватися законів, поважати гідність інших і сплачувати податки. «Ми цінуємо багатство, здобуте чесною працею і талантом, оскільки з багатства окремих громадян складається багатство суспільства». У школі чесна праця — це власна контрольна без списування.',
          'Що з цього — нечесне збагачення за рахунок інших: а) продати власний малюнок на шкільному ярмарку; б) забрати чужий обід; в) отримати приз за перемогу в олімпіаді?',
          'б): це взяти чуже. Малюнок (а) і приз (в) здобуті власною працею й талантом — таким багатством можна пишатися.'),
         ('Honesty and honest work',
          'The first principles of a citizen in the draft social contract are old and simple: do not kill, do not steal, do not bear false witness, do not covet what belongs to others. And also: obey the law, respect other people’s dignity and pay taxes. “We value wealth earned by honest work and talent, because the wealth of society is made up of the wealth of individual citizens.” At school, honest work means your own test with no copying.',
          'Which of these is getting rich dishonestly at others’ expense: a) selling your own drawing at the school fair; b) taking someone else’s lunch; c) winning a prize at a maths olympiad?',
          'b): that is taking what is not yours. The drawing (a) and the prize (c) were earned by your own work and talent, and that kind of wealth is something to be proud of.')),
        ('learn', 'book',
         ('Вчитися — все життя',
          'Ще один принцип громадянина: «Здобуваємо не менше середньої освіти і фах, розвиваємося впродовж усього життя». А серед справ держави проєкт називає розвиток освіти й науки, бо саме «рівень розвитку освіти й науки визначає темпи розвитку суспільства загалом». І окремо — «підтримання високого суспільного статусу вчителя». Тож коли ти розв’язуєш задачі на цьому сайті, ти теж будуєш країну.',
          'Якщо щодня позайматися 20 хвилин понад уроки, скільки годин набереться за 170 навчальних днів?',
          '20 · 170 = 3 400 хвилин. 3 400 : 60 ≈ 56,7 години — понад два повні тижні уроків математики!'),
         ('Learning for life',
          'Another citizen principle: we get at least a secondary education and a profession, and we keep developing all our lives. Among the state’s tasks the draft names education and science, because “the level of education and science sets the pace of development of society as a whole.” It also calls for keeping the high public standing of teachers. So when you solve problems on this site, you are building the country too.',
          'If you study for 20 minutes a day on top of lessons, how many hours is that over 170 school days?',
          '20 × 170 = 3,400 minutes. 3,400 ÷ 60 ≈ 56.7 hours, more than two full weeks of maths lessons!')),
        ('truth', 'spread',
         ('Поширюй лише правду',
          'Принцип громадянина з проєкту суспільного договору: «Споживаємо і поширюємо лише достовірну інформацію». Під час війни ворог навмисно запускає фейки, щоб посіяти паніку. Перш ніж переслати новину, перевір: хто автор, чи є офіційне джерело, чи пишуть про це надійні медіа.',
          'Ти переслав чутку 3 друзям, кожен із них — ще 3, і так 5 разів. Скільки людей її отримали?',
          '3 + 9 + 27 + 81 + 243 = 363 людини. Це степені числа 3: 3¹ + 3² + 3³ + 3⁴ + 3⁵. Ось чому одна неперевірена новина розлітається так швидко.'),
         ('Only share what is true',
          'A citizen principle from the draft social contract: we take in and pass on only reliable information. In wartime the enemy deliberately spreads fakes to cause panic. Before you forward a news story, check: who wrote it, is there an official source, are reliable media reporting it?',
          'You forwarded a rumour to 3 friends, each of them sent it to 3 more, and so on 5 times. How many people got it?',
          '3 + 9 + 27 + 81 + 243 = 363 people. These are powers of 3: 3¹ + 3² + 3³ + 3⁴ + 3⁵. That is why one unchecked story spreads so fast.')),
        ('together', 'hands',
         ('Самоорганізація: робимо разом',
          'Проєкт суспільного договору вважає самоорганізацію громадян запорукою свободи й розвитку держави. Люди об’єднуються, щоб домовлятися про справи свого будинку чи двору, займатися наукою, творчістю й спортом, допомагати через благодійні фонди й волонтерство, стежити за владою через аналітичні центри. Учнівське самоврядування, гурток, спортивна команда, шкільний ярмарок для ЗСУ — це теж громадянське суспільство.',
          'Учні хочуть відкрити клуб настільних ігор: потрібні 3 гри по 600 грн. Скинулися 24 учні. Скільки з кожного?',
          '3 · 600 = 1 800 грн. 1 800 : 24 = 75 грн з кожного. Разом — легко, самому — дорого.'),
         ('Self-organisation: doing things together',
          'The draft social contract sees citizens organising themselves as the key to freedom and to the state’s development. People join forces to agree on matters in their building or street, to pursue science, art and sport, to help through charities and volunteering, and to keep an eye on those in power through think tanks. A school council, an after-school club, a sports team, a school fair for the army: that is civil society too.',
          'Pupils want to start a board-games club: they need 3 games at 600 UAH each. 24 pupils chip in. How much each?',
          '3 × 600 = 1,800 UAH. 1,800 ÷ 24 = 75 UAH each. Easy together, expensive alone.')),
        ('nature', 'tree',
         ('Бережемо природу й спадщину',
          '«Оберігаємо довкілля та природу України та світу, історичну та культурну спадщину Українського народу» — ще одна звичка громадянина. Проєкт пояснює: збереження природи — запорука виживання у світі, де людство чекають зміни клімату й нестача води. Сортувати сміття, не смітити в лісі, берегти старовинні будинки й пам’ятки — усе це внесок у спільне майбутнє.',
          'Кожен із 28 учнів класу сортує 1 кг сміття на тиждень. Скільки кілограмів за 34 навчальні тижні?',
          '28 · 34 = 952 кг — майже тонна, і це лише один клас!'),
         ('Caring for nature and heritage',
          'Protecting the environment and nature of Ukraine and the world, and the historic and cultural heritage of the Ukrainian people, is another citizen habit. The draft explains that saving nature is key to survival in a world facing climate change and water shortages. Sorting rubbish, not littering in the woods, looking after old buildings and monuments: all of it is a contribution to our shared future.',
          'Each of the 28 pupils in a class sorts 1 kg of rubbish a week. How many kilograms over 34 school weeks?',
          '28 × 34 = 952 kg, almost a tonne, and that is just one class!')),
        ('defend', 'shield',
         ('Захищаємо Україну, обираємо свідомо',
          'Проєкт суспільного договору називає обов’язком громадянина відстоювати незалежність і територіальну цілісність України. А ще — голосувати на виборах і референдумах свідомо, поінформовано й самостійно, бо політика — це вибір шляху, яким піде країна. Голосувати в Україні можна з 18 років (стаття 70 Конституції). Поки ти молодший — допомагай захисникам, вчися й готуйся бути свідомим виборцем.',
          'Голосувати можна з 18 років. Якщо ти народився у 2014 році, у якому році ти вперше зможеш проголосувати?',
          '2014 + 18 = 2032. Якщо день народження пізніше за день виборів, то вже наступного разу.'),
         ('Defending Ukraine, voting wisely',
          'The draft social contract calls defending Ukraine’s independence and territorial integrity a citizen’s duty. It also asks citizens to vote in elections and referendums thoughtfully, well informed and independently, because politics is choosing the path the country will take. In Ukraine you can vote from the age of 18 (Article 70 of the Constitution). Until then, help the defenders, keep learning and get ready to be a thoughtful voter.',
          'You can vote from 18. If you were born in 2014, in what year will you first be able to vote?',
          '2014 + 18 = 2032. If your birthday comes after election day, it will be at the next election.')),
    ]),
    ('hromada', 'Громада: справи, які вирішують поруч із тобою', 'Your community: things decided close to home', [
        ('community', 'map',
         ('Що робить твоя громада',
          'Громада — це місто, селище чи село (або кілька, що об’єдналися), люди, які там живуть, і їхнє самоврядування. Проєкт суспільного договору перелічує її справи: дитячі садки, школи й гуртки, місцеві дороги й транспорт, порядок і безпека, житло й комунальні послуги, первинна медична допомога, культура, спорт і дозвілля, допомога тим, хто її потребує. Жителі обирають раду громади і голову. Центр політико-правових реформ пропонує, щоб громада мала права юридичної особи і сама відповідала за свої справи.',
          'Бюджет громади — 50 млн грн: 40 % іде на освіту, 15 % — на дороги. Скільки грошей на кожне і скільки лишається на інше?',
          '40 % від 50 млн = 20 млн грн; 15 % від 50 млн = 7,5 млн грн. Лишається 50 − 20 − 7,5 = 22,5 млн грн, тобто 45 %.'),
         ('What your community does',
          'A community (hromada) is a town or village, or several that have joined together, the people who live there and their self-government. The draft social contract lists its tasks: nurseries, schools and clubs, local roads and transport, order and safety, housing and utilities, primary healthcare, culture, sport and leisure, and help for those who need it. Residents elect the community council and its head. The Centre of Policy and Legal Reform proposes that a community should be a legal entity responsible for its own affairs.',
          'A community budget is 50 million UAH: 40% goes to education and 15% to roads. How much is that for each, and how much is left for everything else?',
          '40% of 50 million = 20 million UAH; 15% of 50 million = 7.5 million UAH. That leaves 50 − 20 − 7.5 = 22.5 million UAH, or 45%.')),
        ('levels', 'levels',
         ('Хто що вирішує: громада, регіон, держава',
          'Головне правило — вирішувати якомога ближче до людей (його називають принципом субсидіарності). Що може зробити громада, те робить громада. Що їй не під силу — регіон: лікарні, коледжі, дороги між містами. А те, що стосується всієї країни, — держава: армія, гривня, закони. Проєкт суспільного договору пропонує, щоб і регіони мали власне виборне самоврядування, а ЦППР розробив концепцію, як розподілити повноваження між громадами, районами, областями й державою.',
          'Розклади справи: шкільний автобус, лікарня швидкої допомоги на всю область, армія.',
          'Шкільний автобус — громада; обласна лікарня — регіон; армія — держава.'),
         ('Who decides what: community, region, state',
          'The main rule is to decide as close to people as possible (this is called the principle of subsidiarity). What a community can do, the community does. What it cannot manage goes to the region: hospitals, colleges, roads between towns. And what concerns the whole country is for the state: the army, the hryvnia, laws. The draft social contract proposes that regions should also have their own elected self-government, and the CPLR has drafted a concept for dividing powers between communities, districts, regions and the state.',
          'Sort these: a school bus, an emergency hospital for the whole region, the army.',
          'School bus: community; regional hospital: region; army: state.')),
    ]),
    ('state', 'Держава: 12 справ, які ми їй доручаємо', 'The state: 12 jobs we give it', [
        ('policies', 'grid12',
         ('Дванадцять державних політик',
          'Проєкт суспільного договору каже: громадяни доручають державі 12 справ (політик). Це правова політика; правопорядок і безпека; економіка; фінанси; розвиток регіонів; соціальний захист і здоров’я; освіта й наука; інфраструктура (світло, зв’язок, дороги); довкілля; культура й спорт; закордонні справи; оборона. Держава — політична організація нації і гарант прав і свобод людини.',
          'До якої з 12 політик належать: а) твоя школа; б) світло в будинку; в) ЗСУ?',
          'а) освіта й наука; б) інфраструктура (передача електроенергії); в) оборона.'),
         ('Twelve state policies',
          'The draft social contract says citizens give the state 12 jobs (policies): law; public order and safety; the economy; finance; regional development; social protection and health; education and science; infrastructure (power, communications, transport); the environment; culture and sport; foreign affairs; and defence. The state is “the political organisation of the nation” and the guarantor of human rights and freedoms.',
          'Which of the 12 policies do these belong to: a) your school; b) electricity at home; c) the Armed Forces?',
          'a) education and science; b) infrastructure (power transmission); c) defence.')),
        ('equal', 'rules',
         ('Закон однаковий для всіх',
          '«Справедливість законів та рівність громадян перед законом є основою суспільної злагоди, а відтак — запорукою розвитку», — сказано в проєкті суспільного договору. Влада теж мусить діяти лише за Конституцією й законами, без свавілля. Центр політико-правових реформ ставить собі за мету «підпорядкувати владу демократичній Конституції».',
          'Учень і директор школи обидва поставили велосипеди на газоні, де це заборонено. Кого мають попросити їх прибрати?',
          'Обох. Правило однакове для всіх — і для учня, і для директора. Якщо правило діє лише для слабших, його ніхто не поважає.'),
         ('The law is the same for everyone',
          '“Fair laws and the equality of citizens before the law are the basis of social harmony and therefore the key to development,” says the draft social contract. Those in power must also act only under the Constitution and the laws, never arbitrarily. The Centre of Policy and Legal Reform sets itself the goal of making power subject to a democratic Constitution.',
          'A pupil and the head teacher both left their bikes on the lawn where it is not allowed. Who should be asked to move them?',
          'Both. A rule is the same for everyone, for a pupil and for a head teacher. If a rule only applies to the weaker, nobody respects it.')),
        ('taxes', 'icecream',
         ('Податки — це наші спільні гроші',
          'Купуєш морозиво за 30 гривень? У ціні вже є податок на додану вартість (ПДВ) — 20 %. Тобто 25 грн коштує саме морозиво, а 5 грн іде до бюджету: 25 + 20 % = 25 + 5 = 30. Проєкт суспільного договору наголошує на «принципі рівності усіх перед обов’язком» сплачувати податки. З цих грошей платять учителям і лікарям, будують укриття й захищають країну. Тож і ти вже платник податків!',
          'Скільки ПДВ у шоколадці за 60 грн?',
          '60 : 120 · 20 = 10 грн. Перевір: 50 + 20 % від 50 = 50 + 10 = 60.'),
         ('Taxes are our shared money',
          'Buying an ice cream for 30 hryvnias? The price already includes value added tax (VAT) of 20%. So the ice cream itself costs 25 UAH and 5 UAH goes to the budget: 25 + 20% = 25 + 5 = 30. The draft social contract stresses that everyone is equally obliged to pay taxes. That money pays teachers and doctors, builds shelters and defends the country. So you are a taxpayer already!',
          'How much VAT is there in a 60-hryvnia chocolate bar?',
          '60 ÷ 120 × 20 = 10 UAH. Check: 50 + 20% of 50 = 50 + 10 = 60.')),
    ]),
    ('vision', 'Бачення України — 2030', 'Vision for Ukraine 2030', [
        ('vision2030', 'sunrise',
         ('Якою може бути Україна у 2030 році',
          'Наприкінці березня 2022 року, у перші тижні повномасштабної війни, науковці й громадські експерти об’єдналися в коаліцію «Україна після перемоги». Уже в червні 2022 року вони представили документ «Бачення України — 2030». Його головна мета: Україна має стати «спроможною, висококонкурентною і невід’ємною, інтегрованою частиною розвиненого світу». Основа — демократія, правовладдя, належне врядування й вільна ринкова економіка.',
          'Скільки тобі буде у 2030 році, якщо ти народився у 2014-му?',
          '2030 − 2014 = 16 років. Тобто Україну-2030 будуватимуть, зокрема, нинішні семикласники.'),
         ('What Ukraine could be like in 2030',
          'At the end of March 2022, in the first weeks of the full-scale war, scholars and civic experts joined forces in the “Ukraine after Victory” coalition. By June 2022 they had presented the document “Vision for Ukraine 2030”. Its main goal: Ukraine should become “a capable, highly competitive and inseparable, integrated part of the developed world.” Its foundations are democracy, the rule of law, good governance and a free market economy.',
          'How old will you be in 2030 if you were born in 2014?',
          '2030 − 2014 = 16. So today’s Year 7 pupils will be among those building Ukraine 2030.')),
        ('seven', 'seven',
         ('Сім реформ від ЦППР',
          'Щоб «Бачення» стало планом, Центр політико-правових реформ разом із партнерами з вересня 2022 до березня 2023 року розробив концепції реформ у семи сферах. Конституція: збалансувати повноваження Президента, парламенту й уряду. Парламент: сильні комітети, які контролюють уряд. Уряд: міністерства планують політику, інші органи її виконують. Послуги: базові послуги — у ЦНАП біля дому, простіше й цифрово. Суди: чесні й прозорі. Правоохоронці: керівників обирають за конкурсом, а не з політичних міркувань. Регіони: власне самоврядування.',
          'Яку з семи реформ ти почав би першою і чому?',
          'Однієї правильної відповіді немає. Експерти теж сперечаються! Важливо пояснити свій вибір: наприклад, «спершу суди, бо без чесного суду не працюють інші закони».'),
         ('Seven reforms from the CPLR',
          'To turn the Vision into a plan, the Centre of Policy and Legal Reform and its partners drafted reform concepts in seven areas between September 2022 and March 2023. Constitution: balance the powers of the President, parliament and government. Parliament: strong committees that hold the government to account. Government: ministries plan policy and other bodies carry it out. Services: basic services at a service centre near home, simpler and digital. Courts: honest and transparent. Law enforcement: leaders chosen by open competition, not for political reasons. Regions: their own self-government.',
          'Which of the seven reforms would you start with, and why?',
          'There is no single right answer. Experts argue about it too! What matters is explaining your choice, for example: “courts first, because without fair courts no other law works.”')),
        ('languages', 'talk',
         ('Мови, які відкривають світ',
          'Частину «Бачення України — 2030» про суспільство й гуманітарну політику підготували Школа політичної аналітики НаУКМА та коаліція «Реанімаційний пакет реформ». Вони ставлять цілі на 2030 рік: 95 % дорослих вільно володіють українською мовою (рівень C1–C2), а 75 % — англійською на рівні B2–C1. Мова — ключ і до спільної країни, і до всього світу.',
          'У класі 28 учнів. Скільки з них мали б вільно знати англійську, щоб клас досяг цілі 75 %?',
          '75 % — це три чверті. 28 : 4 · 3 = 21 учень.'),
         ('Languages that open up the world',
          'The part of “Vision for Ukraine 2030” on society and the humanities was prepared by the School of Policy Analysis at Kyiv-Mohyla Academy and the Reanimation Package of Reforms coalition. They set goals for 2030: 95% of adults fluent in Ukrainian (level C1–C2) and 75% speaking English at level B2–C1. Language is the key both to our shared country and to the whole world.',
          'A class has 28 pupils. How many should speak English well for the class to reach the 75% goal?',
          '75% is three quarters. 28 ÷ 4 × 3 = 21 pupils.')),
        ('exam', 'checklist',
         ('Вступний іспит до ЄС',
          'Коли у 2022 році Україна стала кандидатом на вступ до Європейського Союзу, вона мала виконати 7 рекомендацій Європейської комісії: про суди, боротьбу з корупцією, права національних меншин, медіа та інше. Експерти ЦППР разом із колегами з партнерських організацій пояснили їх у документі «Вступний іспит для України», а потім оцінювали, як Україна виконує вимоги щодо судової реформи й реформи органів правопорядку. Мета ЦППР у цьому напрямі звучить коротко: вступ України до Європейського Союзу.',
          'Уяви: із 7 рекомендацій 4 виконано повністю, а 2 — частково (рахуємо як половину). На скільки відсотків виконано «домашнє завдання»?',
          '4 + 2 · 0,5 = 5 із 7. 5 : 7 ≈ 0,71 → приблизно 71 %.'),
         ('The entrance exam for the EU',
          'When Ukraine became a candidate to join the European Union in 2022, it had to carry out 7 recommendations from the European Commission: on the courts, fighting corruption, the rights of national minorities, the media and more. CPLR experts and colleagues from partner organisations explained them in “An Entrance Exam for Ukraine” and then assessed how Ukraine was meeting the requirements on judicial and law-enforcement reform. The CPLR’s goal in this area is short: Ukraine joining the European Union.',
          'Imagine 4 of the 7 recommendations are fully done and 2 are half done (count them as a half each). What percentage of the “homework” is done?',
          '4 + 2 × 0.5 = 5 out of 7. 5 ÷ 7 ≈ 0.71 → about 71%.')),
    ]),
    ('cplr', 'Хто допомагає будувати: Центр політико-правових реформ', 'Who helps build it: the Centre of Policy and Legal Reform', [
        ('who', 'hexa',
         ('Аналітичний центр, якому 30 років',
          'Центр політико-правових реформ (ЦППР) — неурядовий аналітичний центр, зареєстрований 18 листопада 1996 року, того ж року, коли ухвалили Конституцію. Його бачення: «Україна — європейська держава, побудована на принципах демократії, правовладдя, належного врядування». Цінності ЦППР: патріотизм та історична тяглість; доброчесність і прозорість; фаховість та інноваційність; незалежність і неупередженість; проактивність і поступ. У 2016 році ЦППР визнали одним із найпрозоріших аналітичних центрів, а з 2017 року він створює мережу регіональних аналітичних центрів UPLAN: тепер вона має 68 експертів у шести областях.',
          'Скільки років ЦППР і Конституції у 2026 році?',
          '2026 − 1996 = 30 років — обом однаково.'),
         ('A think tank turning 30',
          'The Centre of Policy and Legal Reform (CPLR) is a non-governmental think tank registered on 18 November 1996, the year the Constitution was adopted. Its vision: “Ukraine is a European state built on the principles of democracy, the rule of law and good governance.” Its values: patriotism and historical continuity; integrity and transparency; expertise and innovation; independence and impartiality; initiative and progress. In 2016 the CPLR was recognised as one of the most transparent think tanks, and since 2017 it has been building UPLAN, a network of regional think tanks that now has 68 experts in six regions.',
          'How old are the CPLR and the Constitution in 2026?',
          '2026 − 1996 = 30 years, the same for both.')),
        ('goals', 'target',
         ('Дев’ять цілей',
          'ЦППР працює в дев’яти напрямах, і в кожного є своя мета. Влада підпорядкована демократичній Конституції. Належне урядування. Державні послуги — якісні й доброзичливі. Сильні громади й регіони. Справедливий суд. Захищеність від злочинів. Відчутне зниження корупції. Вступ України до ЄС. Розвинуте громадянське суспільство. Це цілі, а не готові результати: до них іде робота роками.',
          'Яка з дев’яти цілей найбільше стосується твоєї школи?',
          'Наприклад, «сильні громади»: саме громада утримує школу. А ще «державні послуги» — коли батьки оформлюють тобі документи.'),
         ('Nine goals',
          'The CPLR works in nine areas, each with its own goal. Power subject to a democratic Constitution. Good governance. Public services that are good and friendly. Strong communities and regions. Fair courts. Protection from crime. A real fall in corruption. Ukraine joining the EU. A well-developed civil society. These are goals, not finished results: reaching them takes years of work.',
          'Which of the nine goals matters most for your school?',
          'For example, “strong communities”: it is the community that runs your school. And “public services”, when your parents get documents for you.')),
        ('done', 'rules',
         ('Що вже вдалося',
          'Ось кілька прикладів того, що зробили експерти ЦППР. Розробили концепцію ЦНАП і брали участь у підготовці закону «Про адміністративні послуги». Над законом «Про адміністративну процедуру» працювали з 1999 року, брали участь у його підготовці й адвокації, а потім — у навчанні службовців, як його застосовувати. Провели адвокаційну кампанію за закон «Про всеукраїнський референдум» і за конкурсний відбір суддів Конституційного Суду. Підготували проєкт закону «Про місцевий референдум». Уперше оцінили українські суди за методикою, якою ЄС порівнює суди своїх країн. Видали «Довідник із запобігання корупції в органах місцевого самоврядування».',
          'Закон «Про адміністративну процедуру» ухвалили у 2022 році. Скільки років тривала робота, якщо почали у 1999-му?',
          '2022 − 1999 = 23 роки. Наполегливість — теж частина громадянської активності.'),
         ('What has been achieved',
          'Here are some examples of what CPLR experts have done. They drafted the concept of service centres and took part in preparing the Law on Administrative Services. They worked on the Law on Administrative Procedure from 1999, took part in drafting it and campaigning for it, and then in training officials to apply it. They ran advocacy campaigns for the Law on National Referendums and for open competitions to select Constitutional Court judges. They drafted a law on local referendums. For the first time they assessed Ukraine’s courts by the method the EU uses to compare its members’ courts. And they published a handbook on preventing corruption in local government.',
          'The Law on Administrative Procedure was passed in 2022. How many years did the work take if it started in 1999?',
          '2022 − 1999 = 23 years. Persistence is part of being an active citizen too.')),
        ('integrity', 'broom',
         ('Проти корупції: що зроблено у 2026 році',
          'Мета антикорупційного напряму ЦППР — відчутне зниження рівня корупції. У 2026 році експерти ЦППР підготували законопроєкт про посилення незалежності Генерального прокурора, який зареєстрували у Верховній Раді, а їхні пропозиції врахували в проєкті Антикорупційної стратегії на 2026–2030 роки. Член правління ЦППР Микола Хавронюк у робочій групі при Президентові бере участь у підготовці проєкту нового Кримінального кодексу з новими підходами до покарання за корупцію. Вони навчали суддів Вищого антикорупційного суду і судили студентський змагальний суд (муткорт) із суддівської етики. Микола Хавронюк наголошує: «зусиллями самої лише антикорупційної інфраструктури неможливо забезпечити доброчесність в усіх сферах». Тобто чесність — справа кожного.',
          'В Індексі сприйняття корупції (100 балів має дуже чесна країна) Україна у 2021 році мала 32 бали, а у 2025-му — 36. На скільки відсотків зріс показник?',
          '36 − 32 = 4 бали. 4 : 32 = 0,125 → на 12,5 %.'),
         ('Against corruption: what was done in 2026',
          'The goal of the CPLR’s anti-corruption work is a real fall in corruption. In 2026 CPLR experts drafted a bill to strengthen the independence of the Prosecutor General, which was registered in parliament, and their proposals were taken into account in the draft Anti-Corruption Strategy for 2026–2030. CPLR board member Mykola Khavroniuk is taking part, in a working group under the President, in drafting a new Criminal Code with new approaches to punishing corruption. They trained judges of the High Anti-Corruption Court and judged a student moot court on judicial ethics. Khavroniuk stresses that anti-corruption bodies alone cannot make every area of life honest. So honesty is everyone’s job.',
          'In the Corruption Perceptions Index (a very honest country scores 100) Ukraine had 32 points in 2021 and 36 in 2025. By what percentage did the score rise?',
          '36 − 32 = 4 points. 4 ÷ 32 = 0.125 → by 12.5%.')),
    ]),
]

TXT = {
    'uk': dict(title='Це наша держава', h1='Це <span>наша</span> держава', file='civic.html', other='civic-en.html', other_l='English version',
               lead='Українська держава є і буде. А якою вона буде, залежить від нас. Тут — про суспільний договір, тобто як ми домовляємося жити разом, про звички громадянина, громаду й державу, про те, якою може бути Україна у 2030 році, і про людей, які допомагають її будувати.',
               check='Спробуй сам', home='Математична пасіка', idx='index.html', crumb='Наша держава',
               src='Розділ підготовлено за матеріалами Центру політико-правових реформ (pravo.org.ua): профіль і стратегічний план ЦППР, звіт антикорупційного напряму 2026 року, «Бачення України — 2030», а також за проєктом «Суспільного договору для України» (2025) і Конституцією України.',
               read='Для вчителів і батьків: що почитати'),
    'en': dict(title='This is our country', h1='This is <span>our</span> country', file='civic-en.html', other='civic.html', other_l='Українська версія',
               lead='The Ukrainian state exists and will go on existing. What it will be like depends on us. This page is about the social contract (how we agree to live together), citizen habits, your community and the state, what Ukraine could be like in 2030, and the people helping to build it.',
               check='Try it', home='The Maths Apiary', idx='index-en.html', crumb='Our country',
               src='Based on materials of the Centre of Policy and Legal Reform (pravo.org.ua): the CPLR profile and strategic plan, its 2026 anti-corruption report and “Vision for Ukraine 2030”, as well as the draft “Social Contract for Ukraine” (2025) and the Constitution of Ukraine.',
               read='For teachers and parents: further reading (in Ukrainian)'),
}

READ = [  # for teachers and parents (Ukrainian)
    ('Бачення України — 2030 (сторінка ЦППР)', 'https://pravo.org.ua/bachennya-ukrayiny-2030/'),
    ('Україна після перемоги. Бачення України 2030 (документ коаліції, 2022)', 'https://pravo.org.ua/wp-content/uploads/2022/07/bachennya-ukr-2030.pdf'),
    ('Бачення України — 2030: соціально-гуманітарна сфера', 'https://dev.pravo.org.ua/wp-content/uploads/2024/10/bachennya-ukrayiny-2030_sotsialno-gumanitarna-sfera.pdf'),
    ('Концепція конституційної реформи', 'https://dev.pravo.org.ua/wp-content/uploads/2024/11/ua-constitutional-reform-concept-.pdf'),
    ('Концепція реформи системи правосуддя', 'https://dev.pravo.org.ua/wp-content/uploads/2024/11/kontseptsiya_systemy_reformy_pravosuddya.pdf'),
    ('Вступний іспит для України. Що маємо зробити для виконання рекомендацій ЄС', 'https://pravo.org.ua/books/vstupnyj-ispyt-dlya-ukrayiny-shho-mayemo-zrobyty-dlya-vykonannya-rekomendatsij-yes/'),
    ('Довідник із запобігання корупції в органах місцевого самоврядування', 'https://pravo.org.ua/books/dovidnyk-iz-zapobigannya-koruptsiyi-v-organah-mistsevogo-samovryaduvannya/'),
    ('ЦППР: бачення, місія і цінності', 'https://pravo.org.ua/vision/'),
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
