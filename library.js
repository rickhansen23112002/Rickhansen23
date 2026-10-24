(()=>{
'use strict';
const dialog=document.createElement('dialog');
dialog.id='fileLibrary';
dialog.innerHTML=`<div class="library-heading"><h2>Mijn bestanden</h2><button id="libraryClose" aria-label="Sluiten">✕ Sluiten</button></div>
<p class="mini">Jouw lokale bibliotheek op dit apparaat. Download belangrijke bestanden ook als back-up.</p>
<nav id="libraryPath" aria-label="Mappad"></nav>
<div class="library-toolbar"><label>Naam <input id="libraryName" placeholder="Bijvoorbeeld Training dinsdag" maxlength="120"></label><button id="libraryFolder">＋ Map maken</button><button id="librarySave" class="primary">Huidig project hier opslaan</button><button id="libraryImport">Bestanden toevoegen</button><input id="libraryFiles" type="file" multiple hidden></div>
<p id="libraryStatus" role="status" aria-live="polite"></p><div id="libraryItems"></div>`;
document.body.append(dialog);
const $=id=>document.getElementById(id);
let current=null,records=[],dbPromise;
function database(){
 if(!dbPromise)dbPromise=new Promise((resolve,reject)=>{
  const request=indexedDB.open('ppa-personal-library',1);
  request.onupgradeneeded=()=>request.result.createObjectStore('entries',{keyPath:'id'});
  request.onsuccess=()=>resolve(request.result);
  request.onerror=()=>reject(request.error);
 });
 return dbPromise;
}
async function transaction(mode,action){
 const db=await database();
 return new Promise((resolve,reject)=>{const tx=db.transaction('entries',mode);const request=action(tx.objectStore('entries'));tx.oncomplete=()=>resolve(request?.result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error||Error('Opslag afgebroken'));});
}
const status=text=>{$('libraryStatus').textContent=text;};
function button(text,action){const b=document.createElement('button');b.textContent=text;b.type='button';b.onclick=()=>run(action);return b;}
async function run(action){try{await action();}catch(error){status('Niet gelukt: '+(error?.message||'lokale opslag niet beschikbaar')+'. Download je project via Project opslaan als back-up.');}}
const folder=id=>records.find(x=>x.id===id&&x.kind==='folder');
function folderPath(id){const names=[];const seen=new Set();while(id&&!seen.has(id)){seen.add(id);const f=folder(id);if(!f)break;names.unshift(f.name);id=f.parent;}return ['Mijn bestanden',...names].join(' / ');}
async function refresh(){records=await transaction('readonly',store=>store.getAll());render();}
function render(){
 const path=$('libraryPath');path.replaceChildren(button('Mijn bestanden',async()=>{current=null;render();}));
 const chain=[];let f=folder(current);while(f){chain.unshift(f);f=folder(f.parent);}
 for(const item of chain)path.append(button('› '+item.name,async()=>{current=item.id;render();}));
 const host=$('libraryItems');host.replaceChildren();
 const items=records.filter(x=>x.parent===current).sort((a,b)=>(a.kind===b.kind?0:a.kind==='folder'?-1:1)||a.name.localeCompare(b.name,'nl'));
 if(!items.length){const empty=document.createElement('p');empty.textContent='Deze map is leeg. Maak een map, sla je project op of voeg bestanden toe.';host.append(empty);}
 for(const item of items){
  const row=document.createElement('div');row.className='library-row';
  const title=document.createElement('div');title.className='library-title';const strong=document.createElement('strong');strong.textContent=(item.kind==='folder'?'📁 ':'📄 ')+item.name;title.append(strong);
  const detail=document.createElement('small');detail.textContent=item.kind==='folder'?'Map':`${Math.max(1,Math.ceil(item.blob.size/1024))} KB · ${new Date(item.updated).toLocaleString('nl-NL')}`;title.append(detail);row.append(title);
  const actions=document.createElement('div');actions.className='library-row-actions';
  if(item.kind==='folder')actions.append(button('Open map',async()=>{current=item.id;render();}));
  else {
   if(item.project)actions.append(button('Open project',async()=>{if(!confirm('Dit project openen? Je huidige werk wordt vervangen. Sla het eerst in de bibliotheek op als je het wilt bewaren.'))return;const success=await window.ppaProjects.open(new File([item.blob],item.name,{type:'application/json'}));if(success)dialog.close();else status('Dit project kon niet worden geopend.');}));
   actions.append(button('Download',async()=>{const url=URL.createObjectURL(item.blob),a=document.createElement('a');a.href=url;a.download=item.name;a.click();setTimeout(()=>URL.revokeObjectURL(url),3000);}));
  }
  actions.append(button('Hernoemen',async()=>{const value=prompt('Nieuwe naam:',item.name)?.trim();if(!value)return;if(duplicate(value,item.parent,item.id))throw Error('Deze naam bestaat al in deze map');await transaction('readwrite',store=>store.put({...item,name:value.slice(0,120),updated:Date.now()}));await refresh();status('Naam gewijzigd.');}));
  const move=document.createElement('select');move.setAttribute('aria-label','Verplaats '+item.name);const placeholder=new Option('Verplaatsen naar…','');move.append(placeholder);
  for(const target of [{id:null,name:'Mijn bestanden'},...records.filter(x=>x.kind==='folder')]){
   if(target.id===item.parent||target.id===item.id||isDescendant(target.id,item.id))continue;
   move.append(new Option(folderPath(target.id),target.id||'root'));
  }
  move.onchange=()=>run(async()=>{const target=move.value==='root'?null:move.value;move.value='';if(duplicate(item.name,target,item.id))throw Error('Deze naam bestaat al in de doelmap');await transaction('readwrite',store=>store.put({...item,parent:target,updated:Date.now()}));await refresh();status('Verplaatst.');});actions.append(move);
  actions.append(button('Verwijderen',async()=>{if(item.kind==='folder'&&records.some(x=>x.parent===item.id))throw Error('Verplaats of verwijder eerst de inhoud van deze map');if(!confirm('“'+item.name+'” definitief uit de bibliotheek verwijderen?'))return;await transaction('readwrite',store=>store.delete(item.id));await refresh();status('Verwijderd.');}));
  row.append(actions);host.append(row);
 }
}
function isDescendant(id,ancestor){const seen=new Set();while(id&&!seen.has(id)){if(id===ancestor)return true;seen.add(id);id=folder(id)?.parent;}return false;}
function duplicate(name,parent,except){return records.some(x=>x.id!==except&&x.parent===parent&&x.name.toLocaleLowerCase()===name.toLocaleLowerCase());}
function id(){return crypto.randomUUID?crypto.randomUUID():Date.now().toString(36)+Math.random().toString(36).slice(2);}
async function putFile(name,blob,project){
 name=name.slice(0,120);const existing=records.find(x=>x.parent===current&&x.name.toLocaleLowerCase()===name.toLocaleLowerCase());
 if(existing?.kind==='folder')throw Error('Er bestaat al een map met deze naam');
 if(existing&&!confirm('“'+name+'” bestaat al. Dit bestand vervangen?'))return false;
 await transaction('readwrite',store=>store.put({id:existing?.id||id(),name,parent:current,kind:'file',blob,project,updated:Date.now()}));await refresh();return true;
}
$('openLibrary').onclick=()=>{dialog.showModal();status('Bibliotheek laden…');run(async()=>{await refresh();status('');});};
$('libraryClose').onclick=()=>dialog.close();
$('libraryFolder').onclick=()=>run(async()=>{const name=$('libraryName').value.trim();if(!name)throw Error('Vul eerst een naam in');if(duplicate(name,current))throw Error('Deze naam bestaat al');await transaction('readwrite',store=>store.put({id:id(),kind:'folder',name,parent:current,updated:Date.now()}));$('libraryName').value='';await refresh();status('Map gemaakt.');});
$('librarySave').onclick=()=>run(async()=>{let name=$('libraryName').value.trim();if(!name)throw Error('Vul eerst een projectnaam in');if(!name.toLowerCase().endsWith('.json'))name+='.json';const blob=new Blob([JSON.stringify(window.ppaProjects.capture(),null,2)],{type:'application/json'});if(await putFile(name,blob,true)){status('Project opgeslagen in '+folderPath(current)+'.');$('libraryName').value='';}});
$('libraryImport').onclick=()=>$('libraryFiles').click();
$('libraryFiles').onchange=()=>run(async()=>{const files=[...$('libraryFiles').files];let count=0;try{for(const file of files){let project=false;if(file.name.toLowerCase().endsWith('.json')){try{const d=JSON.parse(await file.text());project=!!((Array.isArray(d.boards)&&d.boards.length&&d.boards.every(b=>Array.isArray(b.frames)&&b.frames.length&&Array.isArray(b.frames[0].players)))||(Array.isArray(d.frames)&&d.frames.length&&Array.isArray(d.frames[0].players)));}catch{}}if(await putFile(file.name,file,project))count++;}status(count+' bestand(en) toegevoegd.');}finally{$('libraryFiles').value='';}});
})();
