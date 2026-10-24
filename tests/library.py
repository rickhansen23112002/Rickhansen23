from playwright.sync_api import sync_playwright, expect
import json, os
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(accept_downloads=True,service_workers='block')
 page=context.new_page();downloads=[];page.on('download',lambda download:downloads.append(download));errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(os.environ.get('PPA_TEST_URL','http://localhost:18761'));page.locator('#save').click();expect(page.locator('#fileLibrary')).to_be_visible()
 page.locator('#libraryName').fill('Trainingen');page.locator('#libraryFolder').click();page.get_by_role('button',name='Open map',exact=True).click()
 page.locator('#libraryName').fill('Dinsdag');page.locator('#librarySave').click();page.get_by_text('Dinsdag.json',exact=False).first.wait_for();assert not downloads, 'Opslaan in app must not trigger a download'
 page.locator('#libraryFiles').set_input_files({'name':'notities.txt','mimeType':'text/plain','buffer':b'Mijn training'})
 page.get_by_text('notities.txt',exact=False).first.wait_for();expect(page.locator('.library-row')).to_have_count(2)
 page.reload();page.locator('#openLibrary').click();page.get_by_role('button',name='Open map',exact=True).click();expect(page.locator('.library-row')).to_have_count(2)
 row=page.locator('.library-row').filter(has_text='notities.txt')
 with page.expect_download() as download:row.get_by_role('button',name='Download',exact=True).click()
 assert open(download.value.path(),'rb').read()==b'Mijn training'
 row.locator('select').select_option('root');page.get_by_role('button',name='Mijn bestanden',exact=True).click();expect(page.locator('.library-row')).to_have_count(2)
 page.on('dialog',lambda d:d.accept())
 page.locator('.library-row').filter(has_text='notities.txt').get_by_role('button',name='Hernoemen',exact=True).click()
 page.get_by_role('button',name='Open map',exact=True).click()
 page.get_by_role('button',name='Open project',exact=True).click();page.wait_for_function('!document.querySelector("#fileLibrary").open')
 page.locator('#openLibrary').click();page.get_by_role('button',name='Mijn bestanden',exact=True).click()
 page.locator('.library-row').filter(has=page.locator('.library-title',has_text='Trainingen')).get_by_role('button',name='Verwijderen',exact=True).click()
 assert 'inhoud' in page.locator('#libraryStatus').inner_text()
 page.get_by_role('button',name='Open map',exact=True).click();page.get_by_role('button',name='Verwijderen',exact=True).click();expect(page.locator('.library-row')).to_have_count(0)
 page.get_by_role('button',name='Mijn bestanden',exact=True).click();page.locator('.library-row').filter(has=page.locator('.library-title',has_text='Trainingen')).get_by_role('button',name='Verwijderen',exact=True).click();expect(page.locator('.library-row')).to_have_count(1)
 for width in (390,768,1440):
  page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.locator('#fileLibrary').evaluate('(d)=>d.scrollWidth<=d.clientWidth')
 assert not errors,errors
 print('PASS: folder creation, project save, generic file import, persistence after reload, exact-byte download, move, project open, nonempty folder protection, delete, responsive dialog; no JavaScript errors')
 browser.close()
