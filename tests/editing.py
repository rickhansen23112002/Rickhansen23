from playwright.sync_api import sync_playwright, expect
import os, json
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(service_workers='block');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(os.environ.get('PPA_TEST_URL','http://localhost:18761'))
 fixture={'version':'PPA-Tactical-v5','idSeq':200,'activeBoard':0,'boards':[{'id':'b1','title':'Hoge druk','orientation':'h','settings':{},'frames':[]}]}
 frame={'t':0,'label':'Start','ball':None,'players':[{'id':'p1','team':'red','number':7,'x':.2,'y':.2}], 'objects':[{'id':'g1','type':'trainingGoal','a':{'x':.5,'y':.3},'size':.1,'rotation':0,'color':'#ffffff'},{'id':'c1','type':'cone','a':{'x':.75,'y':.7},'color':'#f3bd56'},{'id':'t1','type':'text','a':{'x':.7,'y':.4},'text':'Druk zetten','color':'#f3bd56'}]}
 fixture['boards'][0]['frames']=[frame,{**frame,'t':3,'label':'Stap 2'}]
 assert page.evaluate('async d=>await window.ppaProjects.open(new File([JSON.stringify(d)],"test.json"))',fixture)
 def dbl(x,y):
  box=page.locator('#pitch').bounding_box();page.locator('#pitch').dblclick(position={'x':(45+x*1010)/1100*box['width'],'y':(25+y*590)/640*box['height']})
 dbl(.5,.3);expect(page.locator('#shapeGoalControls')).to_be_visible()
 page.locator('[data-goal-size="20"]').click();page.locator('#shapeGoalRotation').select_option('90');page.locator('[data-color-target="shapeColor"][data-basic-color="#3498db"]').click();page.locator('#shapeSave').click()
 data=page.evaluate('window.ppaProjects.capture()')
 for f in data['boards'][0]['frames']:
  goal=f['objects'][0];assert goal['size']==.2 and goal['rotation']==90 and goal['color']=='#3498db'
 page.locator('#undo').click();assert page.evaluate('window.ppaProjects.capture().boards[0].frames[0].objects[0].size')==.1
 dbl(.75,.7);expect(page.locator('#shapeGoalControls')).to_be_hidden();assert page.locator('#shapePopup [data-basic-color]').count()==4
 page.locator('[data-color-target="shapeColor"][data-basic-color="#e74c5b"]').click();page.locator('#shapeSave').click();assert page.evaluate('window.ppaProjects.capture().boards[0].frames[0].objects[1].color')=='#e74c5b'
 dbl(.2,.2);expect(page.locator('#magnetPopup')).to_be_visible();page.locator('[data-color-target="magnetColor"][data-basic-color="#3498db"]').click();page.locator('#magnetSave').click();assert page.evaluate('window.ppaProjects.capture().boards[0].frames[0].players[0].color')=='#3498db'
 dbl(.7,.4);expect(page.locator('#textPopup')).to_be_visible();page.locator('[data-color-target="textColor"][data-basic-color="#3498db"]').click();page.locator('#textPopupSave').click();assert page.evaluate('window.ppaProjects.capture().boards[0].frames[0].objects[2].color')=='#3498db'
 page.locator('#homeColor').evaluate('(el)=>{el.value="#3498db";el.dispatchEvent(new Event("input",{bubbles:true}));}')
 assert page.locator('#selectHomeDot').evaluate('el=>getComputedStyle(el).backgroundColor')=='rgb(52, 152, 219)'
 assert 'eigen team' in page.locator('#selectRed').inner_text()
 assert 'color' not in page.evaluate('window.ppaProjects.capture().boards[0].frames[0].players[0]')
 page.reload();page.wait_for_timeout(700);assert page.locator('#selectHomeDot').evaluate('el=>getComputedStyle(el).backgroundColor')=='rgb(52, 152, 219)'
 assert page.locator('#newProject').count()==0 and page.locator('#addBoard').count()==1 and page.locator('#quickPng').count()==0
 for width,height,title in [(1440,900,'Hoge druk'),(390,844,'Hoge druk'),(844,390,'Hoge druk'),(390,844,'Hoge druk · '+ 'Samen druk zetten en compact verdedigen '*2)]:
  page.set_viewport_size({'width':width,'height':height});page.locator('#boardName').fill(title[:90]);page.locator('#boardName').press('Tab');page.locator('#present').click();expect(page.locator('#presentationTitle')).to_have_text(title[:90]);page.wait_for_timeout(150)
  head=page.locator('.presentation-heading').bounding_box();canvas=page.locator('#presentationCanvas').bounding_box();assert head['y']+head['height']<=canvas['y'];assert canvas['y']+canvas['height']<=page.evaluate('innerHeight')+1;assert canvas['height']>50
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=f'/tmp/ppa-presentation-{width}-{height}.png')
  page.locator('#exitPresentation').click()
 assert not errors,errors
 print('PASS: actual canvas double-click goal size/rotation/colors, multi-frame save and undo, cone palette, player palette, dynamic team dot and restore, duplicate controls removed, presentation title outside field at desktop/mobile/landscape/long titles; no JS errors')
 browser.close()
