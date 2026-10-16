"""Play every level through the UI: one wrong answer per task step 0 to see hints, then the right one."""
import sys, json
from playwright.sync_api import sync_playwright
url=sys.argv[1]; prefix=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 420
shots=set(sys.argv[4].split(',')) if len(sys.argv)>4 else set()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':900})
    errs=[]
    pg.on('pageerror', lambda e: errs.append('PAGEERR '+str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' and 'Failed to load' not in m.text else None)
    pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto(url); pg.wait_for_timeout(400)
    if pg.query_selector('#pfDone'): pg.click('#pfDone')
    for L in 'abc':
        pg.evaluate(f"show('{L}')")
        n=pg.evaluate(f"LV.{L}.tasks.length")
        for i in range(n):
            nsteps=pg.evaluate(f"LV.{L}.tasks[{i}].steps.length")
            for s in range(nsteps):
                sp=pg.evaluate(f"LV.{L}.tasks[{i}].steps[{s}]")
                mistake = (s==0)
                if sp['type']=='choice':
                    if mistake:
                        wrong=[o[0] for o in sp['opts'] if o[0]!=str(sp['ans'])][0]
                        pg.click(f'#{L}Task [data-opt="{wrong}"]'); pg.wait_for_timeout(100)
                        if mistake and i==0: pg.click(f'#{L}Task [data-opt="{wrong}"]')
                        if f'{L}{i}hint' in shots: pg.screenshot(path=f'{prefix}-{L}{i}-hint.png', full_page=True)
                    pg.click(f'#{L}Task [data-opt="{sp["ans"]}"]')
                elif sp['type']=='num':
                    if mistake:
                        for k,f in enumerate(sp['f']):
                            pg.fill(f'#{L}f{k}', '999')
                        pg.click(f'#{L}Check'); pg.wait_for_timeout(100)
                        pg.click(f'#{L}Check'); pg.wait_for_timeout(100)
                        if f'{L}{i}hint' in shots: pg.screenshot(path=f'{prefix}-{L}{i}-hint.png', full_page=True)
                    for k,f in enumerate(sp['f']):
                        a=f['ans'][0] if isinstance(f['ans'],list) else f['ans']
                        v=str(a)
                        if pg.evaluate('UK'): v=v.replace('.',',')
                        pg.fill(f'#{L}f{k}', v)
                    pg.click(f'#{L}Check')
                elif sp['type']=='order':
                    if mistake:
                        for k in sp['mix']: pg.click(f'#{L}Task [data-pk="{k}"]')
                        pg.click(f'#{L}Check'); pg.wait_for_timeout(100)
                        pg.click(f'#{L}OReset')
                    for k in range(len(sp['cards'])): pg.click(f'#{L}Task [data-pk="{k}"]')
                    pg.click(f'#{L}Check')
                pg.wait_for_timeout(900 if s<nsteps-1 else 150)
            if f'{L}{i}' in shots: pg.screenshot(path=f'{prefix}-{L}{i}.png', full_page=True)
            if i<n-1: pg.click(f'#{L}Go'); pg.wait_for_timeout(120)
            else:
                pg.click(f'#{L}Go'); pg.wait_for_timeout(200)
        st=pg.evaluate(f"state.done.{L}")
        print(L,'done',st)
        if f'{L}end' in shots: pg.screenshot(path=f'{prefix}-{L}end.png', full_page=True)
    pg.evaluate("show('report')"); pg.wait_for_timeout(200)
    if 'report' in shots: pg.screenshot(path=f'{prefix}-report.png', full_page=True)
    print('diploma hidden', pg.evaluate("document.getElementById('diploma').hidden"))
    print('scrollW', pg.evaluate('document.documentElement.scrollWidth'))
    print(pg.evaluate("document.getElementById('reportText').value")[:900])
    print('errors', errs)
    b.close()
