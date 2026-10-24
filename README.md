# PPA Tactical Studio — persoonlijke app

Je oorspronkelijke v2.2-tactiekbord met installatie als app, offline laden en automatisch lokaal projectherstel. Geen account of clouddienst nodig.

## Windows

1. Download de repository via **Code → Download ZIP** en pak de zip volledig uit.
2. Dubbelklik `PPA_Tactical_Studio_Windows.exe` (of `START_WINDOWS.bat`).
3. Je browser opent vanzelf. Houd het startervenster open tijdens gebruik.
4. In Chrome of Edge kun je via het browsermenu **App installeren** kiezen.

Python en andere installaties zijn niet nodig. De meegeleverde starter is bedoeld voor normale Windows-laptops met een Intel- of AMD-processor (x64). Het programma is niet digitaal ondertekend; Windows kan daarom een melding tonen. Op beheerde laptops kan beleid het uitvoeren blokkeren. Als programma’s niet mogen starten, kun je `index.html` rechtstreeks openen; de basisfuncties werken dan zonder server, maar app-installatie en sommige browserfuncties zijn beperkt.

De app werkt na het eerste laden ook offline via de browsercache. De starter is nodig voor de eerste installatie en updates. Bewaar de bestanden op dezelfde plek en gebruik steeds `http://localhost:18761`; een ander adres gebruikt andere lokale opslag.

## Projecten bewaren

Wijzigingen worden automatisch lokaal in dezelfde browser en hetzelfde profiel bewaard. Heropenen herstelt het laatste project. Dit is geen externe back-up: maak regelmatig een JSON-bestand met **Project opslaan**. Browsergegevens wissen kan je lokale project verwijderen. Bestaande JSON-projecten kun je via **Open project** laden. PNG en WebM-export blijven beschikbaar; browserondersteuning kan verschillen.

## Ontwikkelen

Gebruik de bestaande checkout; een extra Git-worktree is niet nodig.

```sh
cd /workspace/Rickhansen23
python3 -m http.server 18761 --bind 127.0.0.1
```

Geen npm-installatie of build nodig. De app kan ook op een HTTPS-host worden geplaatst. Installatie op een telefoon vereist HTTPS op een bereikbaar adres; de Windows-starter deelt de app niet met andere apparaten.

Bij updates: wijzig de cachenaam in `sw.js`. Sluit alle appvensters en open opnieuw om de nieuwe serviceworker te activeren. De appbestanden zitten ook in de Windows-starter ingebouwd. Na wijzigingen bouw je deze opnieuw met Go: `GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -trimpath -o PPA_Tactical_Studio_Windows.exe launcher.go`.

## Mijn bestanden: opslaan in de app

Klik op **Mijn bestanden**, vul een naam in en kies **Map maken**. Open de map, vul een projectnaam in en kies **Huidig project hier opslaan**. Je project staat nu in de app en blijft na afsluiten beschikbaar. Een opgeslagen project is een momentopname: sla het na aanpassingen opnieuw onder dezelfde naam op om het te vervangen.

Via **Bestanden toevoegen** kun je ook bestaande JSON-projecten, afbeeldingen, pdf’s en andere bestanden in een map bewaren. Herkende tactiekprojecten kun je rechtstreeks openen; andere bestanden kun je downloaden. Bestanden en mappen kun je hernoemen en verplaatsen. Alleen lege mappen kunnen worden verwijderd.

De bibliotheek is lokaal per browserprofiel en apparaat, zonder synchronisatie. Gebruik steeds dezelfde browser en hetzelfde adres. Wis je de browsergegevens, dan kan ook de bibliotheek verdwijnen. Bewaar belangrijke bestanden daarom ook als losse back-up.

### Bijwerken
Sluit alle PPA-app- en browservensters en de oude starter. Download de nieuwste zip, pak deze uit en start de nieuwe Windows-starter. Gebruik dezelfde browser en hetzelfde localhost-adres om je lokale projecten te behouden. Als nog de vorige versie verschijnt, sluit alle appvensters en open de app opnieuw zodat de bijgewerkte offlinecache kan activeren.
