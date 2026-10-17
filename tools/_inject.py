"""Shared helpers for the site post-processing scripts (site_nav, add_bug_button, add_theme_toggle, fun).

Every script keeps its CSS in its own <style data-x="name"> tag right before </head>, so re-running one
script can never remove another script's styles. Older pages had the CSS appended inside an existing
<style> after a comment marker like /* toc */; put_style() also removes such a legacy block safely
(up to the next known marker or </style>).
"""
import re

MARKERS = ['toc', 'nav', 'bug button', 'theme switch', 'fun banner', 'history banner', 'history button', 'fun', 'funlinks']
_NEXT = r'(?=</style>|/\* (?:' + '|'.join(re.escape(m) for m in MARKERS) + r') \*/)'


def drop_legacy(s, marker):
    return re.sub(re.escape(f'/* {marker} */') + r'.*?' + _NEXT, '', s, flags=re.S)


def put_style(s, name, css, legacy=None):
    """Replace (or add) <style data-x="name"> before </head>; css may start with a /* marker */ comment."""
    s = re.sub(r'<style data-x="' + re.escape(name) + r'">.*?</style>', '', s, flags=re.S)
    for m in (legacy or []):
        s = drop_legacy(s, m)
    i = s.index('</head>')
    return s[:i] + f'<style data-x="{name}">{css}</style>' + s[i:]
