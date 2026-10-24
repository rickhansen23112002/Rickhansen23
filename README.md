# PPA Tactical Studio — persoonlijke app

Je oorspronkelijke v2.2-tactiekbord met installatie als app, offline laden en automatisch lokaal projectherstel. Geen account of clouddienst nodig.

## Windows

1. Pak de volledige zip uit in een vaste map.
2. Installeer Python 3 via https://www.python.org/downloads/ als dit nog ontbreekt.
3. Dubbelklik `START_WINDOWS.bat`. Houd het servervenster open tijdens gebruik. Vernieuw de browser als deze eerder opent dan de server.
4. Open in Chrome of Edge het browsermenu en kies **App installeren** (of de installatieknop in de app wanneer beschikbaar).

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

Bij updates: wijzig de cachenaam in `sw.js`. Sluit alle appvensters en open opnieuw om de nieuwe serviceworker te activeren. De meegeleverde oorspronkelijke Windows-programma’s worden niet gebruikt.
