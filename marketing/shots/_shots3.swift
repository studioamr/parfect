// Flujo ENTRENAMIENTO: resumen -> tab Entrenamiento -> drill abierto -> marcado
import Cocoa
import WebKit
setbuf(stdout, nil)
let BASE = "http://localhost:4173/"
let OUT  = FileManager.default.currentDirectoryPath + "/shots"
try? FileManager.default.createDirectory(atPath: OUT, withIntermediateDirectories: true)
let steps: [(String, String, Double)] = [
  ("11-ronda", "document.querySelector(\"[data-view='ronda']\").click();", 1.8),
]
let app = NSApplication.shared
app.setActivationPolicy(.regular)
let W = 440, H = 956
let web = WKWebView(frame: NSRect(x: 0, y: 0, width: W, height: H), configuration: WKWebViewConfiguration())
let win = NSWindow(contentRect: NSRect(x: 120, y: 120, width: W, height: H), styleMask: [.titled], backing: .buffered, defer: false)
win.contentView = web
win.makeKeyAndOrderFront(nil)
app.activate(ignoringOtherApps: true)
DispatchQueue.main.asyncAfter(deadline: .now() + 30) { print("TIMEOUT"); exit(2) }
final class Nav: NSObject, WKNavigationDelegate {
  var cb: (() -> Void)?
  func webView(_ w: WKWebView, didFinish n: WKNavigation!) { cb?() }
}
let nav = Nav(); web.navigationDelegate = nav
func snap(_ name: String, _ done: @escaping () -> Void) {
  let sc = WKSnapshotConfiguration(); sc.afterScreenUpdates = true
  sc.snapshotWidth = NSNumber(value: 1080)
  web.takeSnapshot(with: sc) { image, err in
    if let img = image, let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
       let png = rep.representation(using: .png, properties: [:]) {
      try? png.write(to: URL(fileURLWithPath: "\(OUT)/\(name).png")); print("saved \(name)")
    } else { print("FAIL \(name): \(String(describing: err))") }
    done()
  }
}
func runStep(_ i: Int) {
  if i >= steps.count { print("done"); DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) { exit(0) }; return }
  let (name, js, wait) = steps[i]
  web.evaluateJavaScript(js) { _, _ in
    DispatchQueue.main.asyncAfter(deadline: .now() + wait) { snap(name) { runStep(i + 1) } }
  }
}
var seeded = false
nav.cb = {
  if !seeded { seeded = true; web.evaluateJavaScript("try{seedDemoAccount();}catch(e){}; location.reload();") { _, _ in } }
  else { DispatchQueue.main.asyncAfter(deadline: .now() + 1.2) { runStep(0) } }
}
web.load(URLRequest(url: URL(string: BASE)!))
app.run()
