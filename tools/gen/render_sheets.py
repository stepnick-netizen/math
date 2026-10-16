import sys, io
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
topics = sys.argv[1:] or ['powers','angles','identities']
HIDE = '.links,.site-home,.site-copy{display:none!important} .box{break-inside:avoid}'
with sync_playwright() as p:
    b = p.chromium.launch()
    for t in topics:
        for lang in ('uk','en'):
            url = f'file:///home/claude/work/out/art/{t}/sheet-{lang}.html'
            # PNG
            pg = b.new_page(viewport={'width':860,'height':1200}, device_scale_factor=2)
            pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
            pg.goto(url); pg.add_style_tag(content=HIDE); pg.wait_for_timeout(400)
            pg.screenshot(path=f'out/sheets/{t}-cheatsheet-{lang}.png', full_page=True)
            pg.close()
            # PDF
            pg = b.new_page(viewport={'width':860,'height':1200})
            pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
            pg.goto(url); pg.add_style_tag(content=HIDE); pg.emulate_media(media='screen'); pg.wait_for_timeout(400)
            best=None
            for sc in (0.74,0.72,0.70,0.68,0.66,0.64,0.62):
                pdf = pg.pdf(format='A4', scale=sc, print_background=True, margin={'top':'10mm','bottom':'10mm','left':'8mm','right':'8mm'})
                n = len(PdfReader(io.BytesIO(pdf)).pages)
                best=(sc,n,pdf)
                if n<=2: break
            open(f'out/sheets/{t}-cheatsheet-{lang}.pdf','wb').write(best[2])
            print(t, lang, 'scale', best[0], 'pages', best[1])
            pg.close()
    b.close()
