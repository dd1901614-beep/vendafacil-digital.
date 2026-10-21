from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
root=Path(__file__).resolve().parents[1]
(root/'screenshots').mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width,height,label in [(390,844,'celular'),(1440,900,'computador')]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto((root/'index.html').as_uri())
        page.screenshot(path=str(root/'screenshots'/f'{label}.png'),full_page=True)
        assert page.locator('.service').count()==9, 'Catalogo incompleto'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Rolagem horizontal'
        page.locator('#business').fill('Loja Exemplo')
        page.locator('#headline').fill('Oferta especial')
        page.locator('#format').select_option('story')
        page.locator('#make').click()
        assert page.locator('#art').evaluate('(c)=>c.width===1080&&c.height===1920'), 'Formato Story incorreto'
        assert page.locator('#download').is_enabled(), 'Download indisponivel'
        page.locator('#format').select_option('square')
        page.locator('#make').click()
        assert page.locator('#art').evaluate('(c)=>c.width===1080&&c.height===1080'), 'Formato quadrado incorreto'
        page.locator('#suggest').click()
        assert page.locator('#headline').input_value(), 'Sugestao nao gerada'
        page.locator('#headline').fill('Nova promocao')
        assert not page.locator('#download').is_enabled(), 'Download antigo nao bloqueado'
        page.locator('#make').click()
        assert page.locator('#download').is_enabled(), 'Download nao reativado'
        assert page.locator('#photo').count()==1, 'Campo de foto ausente'
        assert page.locator('#photo').get_attribute('accept')=='image/png,image/jpeg,image/webp', 'Tipos de foto incorretos'
        assert not errors, 'Erros JavaScript: '+str(errors)
        print(label, 'PASSOU: catalogo, largura, formatos, sugestao e download')
        page.close()
    browser.close()
