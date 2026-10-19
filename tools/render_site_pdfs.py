"""PDF шпаргалок для сайту: рендерить <тема>/cheatsheet-<мова>.html у <тема>/cheatsheet-<мова>.pdf.

Навігацію, перемикач теми, кнопку «Знайшли помилку?» ховаємо, а копірайт учителя лишаємо внизу останньої сторінки
(без рядка про статистику). Шрифти Comfortaa, Nunito, Caveat мають бути в ~/.fonts.
Запуск з кореня репозиторію: python3 tools/render_site_pdfs.py [тема ...]
"""
import io, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
topics = sys.argv[1:] or sorted(p.parent.name for p in ROOT.glob('*/cheatsheet-uk.html'))
HIDE = ('nav.site-home,.site-home,.links,.theme-row,.theme-sw,.bug-btn,.lesson-nav,.fun-more,[data-x="fun"]'
        '{display:none!important} body::after{display:none!important} .box{break-inside:avoid}'
        '.site-copy{break-inside:avoid;padding-bottom:0!important}.site-copy small:nth-of-type(2){display:none!important}')

with sync_playwright() as p:
    b = p.chromium.launch()
    for t in topics:
        for lang in ('uk', 'en'):
            src = ROOT / t / f'cheatsheet-{lang}.html'
            if not src.exists(): continue
            pg = b.new_page(viewport={'width': 860, 'height': 1200})
            pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
            pg.add_init_script("try{localStorage.setItem('apiary-theme','light')}catch(e){}")
            pg.goto(src.as_uri()); pg.add_style_tag(content=HIDE)
            pg.evaluate("document.documentElement.dataset.theme='light'")
            pg.emulate_media(media='screen', color_scheme='light'); pg.wait_for_timeout(500)
            best = None
            for sc in (0.74, 0.72, 0.70, 0.68, 0.66, 0.64, 0.62):
                pdf = pg.pdf(format='A4', scale=sc, print_background=True,
                             margin={'top': '10mm', 'bottom': '10mm', 'left': '8mm', 'right': '8mm'})
                n = len(PdfReader(io.BytesIO(pdf)).pages)
                best = (sc, n, pdf)
                if n <= 2: break
            (ROOT / t / f'cheatsheet-{lang}.pdf').write_bytes(best[2])
            print(t, lang, 'scale', best[0], 'pages', best[1])
            pg.close()
    b.close()
