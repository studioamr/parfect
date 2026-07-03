import Cocoa
import WebKit
setbuf(stdout, nil)
let app = NSApplication.shared; app.setActivationPolicy(.regular)
let web = WKWebView(frame: NSRect(x: 0, y: 0, width: 440, height: 956))
let win = NSWindow(contentRect: NSRect(x: 120, y: 120, width: 440, height: 956), styleMask: [.titled], backing: .buffered, defer: false)
win.contentView = web; win.makeKeyAndOrderFront(nil)
DispatchQueue.main.asyncAfter(deadline: .now() + 25) { exit(2) }
final class Nav: NSObject, WKNavigationDelegate {
  func webView(_ w: WKWebView, didFinish n: WKNavigation!) {
    DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
      w.evaluateJavaScript("try{localStorage.clear();}catch(e){}; var el=document.querySelector('.lp-cantera'); if(el){el.scrollIntoView();} el? 'found':'MISSING'") { r, _ in
        print("waitlist:", r ?? "?")
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
          let sc = WKSnapshotConfiguration(); sc.afterScreenUpdates = true; sc.snapshotWidth = 900
          w.takeSnapshot(with: sc) { image, _ in
            if let img = image, let t = img.tiffRepresentation, let rep = NSBitmapImageRep(data: t),
               let png = rep.representation(using: .png, properties: [:]) {
              try? png.write(to: URL(fileURLWithPath: "/tmp/qc-cantera.png")); print("saved")
            }
            exit(0)
          }
        }
      }
    }
  }
}
let nav = Nav(); web.navigationDelegate = nav
web.load(URLRequest(url: URL(string: "http://localhost:4173/")!))
app.run()
