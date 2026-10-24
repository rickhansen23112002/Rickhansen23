// PPA Tactical Studio: standalone local launcher, no external runtime required.
package main

import (
 "embed"
 "flag"
 "fmt"
 "log"
 "net"
 "net/http"
 "os/exec"
 "runtime"
 "time"
)

//go:embed index.html app.css app.js library.js manifest.webmanifest sw.js icon.svg icon-192.png icon-512.png
var assets embed.FS

func main() {
 port := flag.Int("port",18761,"Local port")
 noBrowser := flag.Bool("no-browser",false,"Do not open the browser")
 flag.Parse()
 address := fmt.Sprintf("127.0.0.1:%d",*port)
 url := fmt.Sprintf("http://localhost:%d/",*port)
 listener,err := net.Listen("tcp",address)
 if err != nil {
  fmt.Println("Kan de app niet starten. Sluit een eerdere PPA-starter en probeer opnieuw.")
  fmt.Println(err)
  fmt.Println("Druk op Enter om te sluiten.")
  fmt.Scanln()
  return
 }
 handler := http.FileServer(http.FS(assets))
 server := &http.Server{ReadHeaderTimeout:5*time.Second,Handler:http.HandlerFunc(func(w http.ResponseWriter,r *http.Request){
  if r.Method != "GET" && r.Method != "HEAD" {http.Error(w,"Methode niet toegestaan",http.StatusMethodNotAllowed);return}
  w.Header().Set("X-Content-Type-Options","nosniff")
  w.Header().Set("X-Frame-Options","DENY")
  w.Header().Set("Cache-Control","no-cache")
  handler.ServeHTTP(w,r)
 })}
 fmt.Println("PPA Tactical Studio - persoonlijke app")
 fmt.Println("Je browser opent op",url)
 fmt.Println("Houd dit venster open tijdens gebruik. Sluit het venster om de app te stoppen.")
 if runtime.GOOS=="windows" && !*noBrowser {
  if err:=exec.Command("rundll32","url.dll,FileProtocolHandler",url).Start();err!=nil{fmt.Println("Open zelf je browser op",url)}
 }
 log.Fatal(server.Serve(listener))
}
