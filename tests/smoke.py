from playwright.sync_api import sync_playwright
import json
from pathlib import Path
import tempfile
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(accept_downloads=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://localhost:18761');page.wait_for_function('document.querySelector("#pitch").width > 0')
 page.evaluate('navigator.serviceWorker.ready');page.reload();page.wait_for_timeout(500)
 assert page.locator('#boardTabs button').count()==1
 page.locator('#addBoard').click();assert page.locator('#boardTabs button').count()==2
 name=page.locator('#boardName');name.fill('Mijn training');name.press('Tab');page.wait_for_timeout(750)
 assert page.evaluate('JSON.parse(localStorage.getItem("ppa-tactical-personal-v1")).boards.length')==2
 page.reload();page.wait_for_timeout(750)
 assert page.locator('#boardTabs button').count()==2
 assert page.locator('#boardName').input_value()=='Mijn training'
 with page.expect_download() as info:page.locator('#save').click()
 download=info.value;data=json.load(open(download.path()));assert len(data['boards'])==2
 with page.expect_download() as info:page.locator('#png').click()
 assert open(info.value.path(),'rb').read(8)==b'\x89PNG\r\n\x1a\n'
 page.locator('#present').click();assert page.locator('#presentationOverlay').is_visible();page.keyboard.press('Escape');page.wait_for_timeout(200)
 context.set_offline(True);page.reload();page.wait_for_timeout(700);assert page.locator('#boardName').input_value()=='Mijn training'
 context.set_offline(False)
 for width,height in [(390,844),(768,1024),(1440,1000)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(150)
  overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth')
  print('Viewport',width,height,'horizontal overflow',overflow)
  assert not overflow
  page.screenshot(path=str(Path(tempfile.gettempdir()) / f'ppa-screen-{width}.png'),full_page=True)
 assert not errors,errors
 print('PASS: initial board, add board, rename, autosave, reload restore, JSON export, PNG export, presentation, offline reload, responsive widths; no JS errors')
 browser.close()
