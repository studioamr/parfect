/* PARFECT · prueba de humo
   Carga la app contra un servidor local, entra con la cuenta demo y recorre
   las vistas principales. Si cualquier vista lanza un error de JS, sale con
   código 1 y lista los errores. Úsala antes de hacer push:

     python3 -m http.server 4173 &        # en la raíz del repo
     swift tools/smoke.swift              # → "SMOKE OK" o lista de errores
*/
import WebKit
import AppKit

let app = NSApplication.shared
app.setActivationPolicy(.accessory)

let cfg = WKWebViewConfiguration()
cfg.websiteDataStore = .nonPersistent()
let early = WKUserScript(
  source: "window.__errs=[]; window.addEventListener('error', function(e){ window.__errs.push((e.message||'?')+' @ '+(e.filename||'').split('/').pop()+':'+e.lineno); });",
  injectionTime: .atDocumentStart, forMainFrameOnly: true)
cfg.userContentController.addUserScript(early)

let wv = WKWebView(frame: NSRect(x: 0, y: 0, width: 440, height: 956), configuration: cfg)
let win = NSWindow(contentRect: wv.frame, styleMask: [.borderless], backing: .buffered, defer: false)
win.contentView = wv

/* vistas a recorrer una vez dentro de la cuenta demo */
let views = ["inicio", "ronda", "trainer", "social", "perfil", "metrics"]
var exitCode: Int32 = 0

func js(_ code: String, _ done: @escaping (Any?) -> Void) {
  wv.evaluateJavaScript(code) { res, _ in done(res) }
}

func walk(_ idx: Int, _ done: @escaping () -> Void) {
  if idx >= views.count { done(); return }
  js("try { V.view='\(views[idx])'; render(); } catch(e) { window.__errs.push('render \(views[idx]): '+e.message); } 0") { _ in
    DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) { walk(idx + 1, done) }
  }
}

class Nav: NSObject, WKNavigationDelegate {
  func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
    DispatchQueue.main.asyncAfter(deadline: .now() + 2.5) {
      js("try { seedDemoAccount(); } catch(e) { window.__errs.push('seed: '+e.message); } 0") { _ in
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
          walk(0) {
            js("JSON.stringify(window.__errs)") { res in
              let raw = (res as? String) ?? "[]"
              if raw == "[]" {
                print("SMOKE OK · \(views.count) vistas sin errores")
              } else {
                print("SMOKE FALLÓ:")
                print(raw)
                exitCode = 1
              }
              exit(exitCode)
            }
          }
        }
      }
    }
  }
}

let nav = Nav()
wv.navigationDelegate = nav
wv.load(URLRequest(url: URL(string: "http://localhost:4173/index.html")!))
DispatchQueue.main.asyncAfter(deadline: .now() + 60) {
  print("SMOKE FALLÓ: timeout (¿está corriendo python3 -m http.server 4173?)")
  exit(1)
}
app.run()
