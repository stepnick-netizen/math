"""Expression markup shared by the topics.
{b|e}  -> power: base (plum) with index (pink);  {b|}  -> base only, coloured;  ^n -> plain superscript.
Language: en swaps · -> ×, : -> ÷ and decimal commas -> points."""
import re

SUP = str.maketrans('0123456789-+()', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾')


def loc(s, lang):
    if lang == 'en':
        s = re.sub(r'(\d),(\d)', r'\1.\2', s)
        s = s.replace('·', '×').replace(' : ', ' ÷ ')
    return s


def X(s, lang):
    """markup -> html (for the game)."""
    s = loc(s, lang)
    s = re.sub(r'\{([^|{}]*)\|([^{}]*)\}', lambda m: f'<span class="b">{m.group(1)}</span>' + (f'<sup class="e">{m.group(2)}</sup>' if m.group(2) else ''), s)
    s = re.sub(r'\^(\{[^}]*\}|[0-9]+)', lambda m: '<sup>' + m.group(1).strip('{}') + '</sup>', s)
    return s


def P(s, lang):
    """markup -> plain text with unicode superscripts (report, aria labels)."""
    s = loc(s, lang)
    s = re.sub(r'\{([^|{}]*)\|([^{}]*)\}', lambda m: m.group(1) + m.group(2).translate(SUP), s)
    s = re.sub(r'\^(\{[^}]*\}|[0-9]+)', lambda m: m.group(1).strip('{}').translate(SUP), s)
    return s


def num(v, lang):
    s = f'{v:g}' if isinstance(v, float) else str(v)
    if lang == 'uk':
        s = s.replace('.', ',')
    return s.replace('-', '−')


def sup_in(base_html):
    """field spec helper: base shown, index typed into a small raised box."""
    return {'pre': base_html, 'sup': True}
