"""Small SVG toolkit for the living cheat-sheet cards: exact glyph widths (Comfortaa, Caveat, Nunito), coloured runs
with superscripts, arrows with shared markers and geometry helpers for angle drawings."""
import math
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = {}


def _font(name):
    if name not in FONTS:
        path, w = {'d': ('/root/.fonts/Comfortaa%5Bwght%5D.ttf', 700), 'h': ('/root/.fonts/Caveat%5Bwght%5D.ttf', 600),
                   'b': ('/root/.fonts/Nunito%5Bwght%5D.ttf', 700)}[name]
        f = instancer.instantiateVariableFont(TTFont(path), {'wght': w})
        FONTS[name] = (f.getBestCmap(), f['hmtx'].metrics, f['head'].unitsPerEm)
    return FONTS[name]


def width(text, size, font='d'):
    cmap, hm, upm = _font(font)
    w = 0
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord('?'))
        w += hm[g][0]
    return w * size / upm


C = dict(y='var(--yarn)', p='var(--plum)', s='var(--sky)', l='var(--leaf)', h='var(--hay)', i='var(--ink)',
         m='var(--muted)', b='var(--bad)', k='var(--marker-ink)', g='var(--good)', w='var(--paper)')
MK = {'y': 'ah-y', 'p': 'ah-p', 'l': 'ah-l', 'i': 'ah-i', 's': 'ah-s', 'h': 'ah-h', 'b': 'ah-b', 'k': 'ah-k',
      'm': 'ah-i', 'g': 'ah-l'}


def f1(v):
    return f'{v:.1f}'


def text(x, y, s, size=20, col='i', cls='d', anchor=None, extra=''):
    a = f' text-anchor="{anchor}"' if anchor else ''
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'<text x="{f1(x)}" y="{f1(y)}"{a} font-size="{size:g}" class="{cls}" fill="{C.get(col, col)}"{extra}>{s}</text>'


def hand(x, y, s, size=22, col='m', anchor='middle'):
    return text(x, y, s, size, col, 'h', anchor)


class Run:
    """pieces: (text, colour key, 'n'|'s'); superscripts are 0.6 size and raised. Use run.svg, run.w, run.span(i)."""

    def __init__(self, pieces, x, y, size=30, anchor='start', font='d', gap=0.0):
        self.size = size
        ws = []
        for t, c, k in pieces:
            sz = size * (0.6 if k == 's' else 1)
            ws.append(width(t, sz, font) + (size * 0.04 if k == 's' else 0))
        tot = sum(ws) + gap * (len(pieces) - 1)
        x0 = x - (tot / 2 if anchor == 'middle' else tot if anchor == 'end' else 0)
        self.w, self.x0, self.y = tot, x0, y
        out, self.spans = [], []
        cx = x0
        for (t, c, k), w in zip(pieces, ws):
            if k == 's':
                sz, yy = size * 0.6, y - size * 0.42
            else:
                sz, yy = size, y
            if t.strip():
                lead = width(t[:len(t) - len(t.lstrip())], sz, font)
                out.append(text(cx + lead + (size * 0.02 if k == 's' else 0), yy, t.strip(), round(sz, 1), c, 'h' if font == 'h' else 'd'))
            self.spans.append((cx, cx + w, yy - sz * 0.72, yy))
            cx += w + gap
        self.svg = ''.join(out)

    def span(self, i):
        return self.spans[i]

    def cx(self, i):
        a, b, _, _ = self.spans[i]
        return (a + b) / 2

    def top(self, i):
        return self.spans[i][2]

    def bot(self, i):
        return self.spans[i][3]


def arrow(x1, y1, x2, y2, col='i', bend=0.25, w=2.6, dash=False, start=False, end=True):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    qx, qy = mx - dy * bend, my + dx * bend
    d = ' stroke-dasharray="5 5"' if dash else ''
    m = (f' marker-end="url(#{MK[col]})"' if end else '') + (f' marker-start="url(#{MK[col]})"' if start else '')
    return (f'<path d="M{f1(x1)} {f1(y1)} Q{f1(qx)} {f1(qy)} {f1(x2)} {f1(y2)}" stroke="{C[col]}" stroke-width="{w}" '
            f'fill="none" stroke-linecap="round"{d}{m}/>')


def line(x1, y1, x2, y2, col='i', w=2.5, dash=None, cap='round'):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f1(x1)}" y1="{f1(y1)}" x2="{f1(x2)}" y2="{f1(y2)}" stroke="{C.get(col, col)}" stroke-width="{w}" stroke-linecap="{cap}"{d}/>'


def circle(cx, cy, r, fill='none', stroke='i', w=2.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<circle cx="{f1(cx)}" cy="{f1(cy)}" r="{f1(r)}" fill="{C.get(fill, fill)}" stroke="{C.get(stroke, stroke)}" stroke-width="{w}"{d}/>'


def rect(x, y, w, h, fill='var(--cell)', stroke='l', sw=2.5, rx=10, dash=None, extra=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" rx="{rx}" fill="{C.get(fill, fill)}" stroke="{C.get(stroke, stroke)}" stroke-width="{sw}"{d}{extra}/>'


def path(d, col='i', w=2.5, fill='none', dash=None, extra=''):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="{C.get(col, col)}" stroke-width="{w}" fill="{C.get(fill, fill)}" stroke-linecap="round" stroke-linejoin="round"{ds}{extra}/>'


# ---------- angles (degrees, maths orientation: 0° to the right, counter-clockwise, SVG y down) ----------
def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def ray(cx, cy, deg, r, col='i', w=3, arrowhead=True):
    x, y = pt(cx, cy, r, deg)
    m = f' marker-end="url(#{MK[col]})"' if arrowhead else ''
    return f'<path d="M{f1(cx)} {f1(cy)} L{f1(x)} {f1(y)}" stroke="{C[col]}" stroke-width="{w}" fill="none" stroke-linecap="round"{m}/>'


def arc(cx, cy, r, a1, a2, col='y', w=3, fill=None, dash=None):
    """arc from angle a1 to a2 counter-clockwise (a2 > a1)."""
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    large = 1 if (a2 - a1) % 360 > 180 else 0
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    if fill:
        return (f'<path d="M{f1(cx)} {f1(cy)} L{f1(x1)} {f1(y1)} A{r} {r} 0 {large} 0 {f1(x2)} {f1(y2)} Z" fill="{C.get(fill, fill)}" '
                f'opacity=".22" stroke="none"/>'
                f'<path d="M{f1(x1)} {f1(y1)} A{r} {r} 0 {large} 0 {f1(x2)} {f1(y2)}" stroke="{C[col]}" stroke-width="{w}" fill="none"{ds}/>')
    return f'<path d="M{f1(x1)} {f1(y1)} A{r} {r} 0 {large} 0 {f1(x2)} {f1(y2)}" stroke="{C[col]}" stroke-width="{w}" fill="none"{ds}/>'


def svg(vb_w, vb_h, body, label, cls='viz'):
    lab = label.replace('"', '&quot;')
    return f'<svg viewBox="0 0 {vb_w} {vb_h}" class="{cls}" role="img" aria-label="{lab}">{body}</svg>'
