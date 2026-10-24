let installPrompt;
const installButton=document.getElementById('installApp');
window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();installPrompt=event;installButton.hidden=false;});
installButton.addEventListener('click',async()=>{if(!installPrompt)return;await installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;installButton.hidden=true;});
window.addEventListener('appinstalled',()=>{installButton.hidden=true;});
if('serviceWorker' in navigator&&location.protocol!=='file:')navigator.serviceWorker.register('./sw.js').catch(()=>{document.getElementById('autosaveStatus').textContent='Offline laden niet beschikbaar · JSON-back-up aanbevolen';});

// A new worker may replace an old offline version. Autosave runs on pagehide.
if('serviceWorker' in navigator){const previouslyControlled=!!navigator.serviceWorker.controller;let reloading=false;navigator.serviceWorker.addEventListener('controllerchange',()=>{if(previouslyControlled&&!reloading){reloading=true;location.reload();}});}
