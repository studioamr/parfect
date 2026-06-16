// Codifica frames (manifest: "path escala" por linea) a un MP4 H.264 vertical 4K.
// Uso: ./_encode manifest.txt salida.mp4
import Foundation
import AVFoundation
import CoreVideo
import CoreGraphics
import ImageIO

let args = CommandLine.arguments
guard args.count >= 3 else { print("uso: _encode manifest out.mp4"); exit(1) }
let manifestPath = args[1]
let outPath = args[2]
let W = 2160, H = 3840
let FPS: Int32 = 30

try? FileManager.default.removeItem(atPath: outPath)
let outURL = URL(fileURLWithPath: outPath)

guard let writer = try? AVAssetWriter(outputURL: outURL, fileType: .mp4) else {
    print("no se pudo crear el writer"); exit(1)
}
let settings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W,
    AVVideoHeightKey: H,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 30_000_000,
        AVVideoMaxKeyFrameIntervalKey: 60,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel
    ]
]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
input.expectsMediaDataInRealTime = false
let attrs: [String: Any] = [
    kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32BGRA),
    kCVPixelBufferWidthKey as String: W,
    kCVPixelBufferHeightKey as String: H
]
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: attrs)
writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

var cache = [String: CGImage]()
func loadImg(_ p: String) -> CGImage? {
    if let c = cache[p] { return c }
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { return nil }
    cache[p] = img
    return img
}

let cs = CGColorSpaceCreateDeviceRGB()
func makeBuffer(_ img: CGImage, scale: CGFloat) -> CVPixelBuffer? {
    var pb: CVPixelBuffer?
    if let pool = adaptor.pixelBufferPool {
        CVPixelBufferPoolCreatePixelBuffer(nil, pool, &pb)
    }
    if pb == nil {
        CVPixelBufferCreate(nil, W, H, kCVPixelFormatType_32BGRA, attrs as CFDictionary, &pb)
    }
    guard let buffer = pb else { return nil }
    CVPixelBufferLockBaseAddress(buffer, [])
    defer { CVPixelBufferUnlockBaseAddress(buffer, []) }
    guard let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buffer),
                              width: W, height: H, bitsPerComponent: 8,
                              bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
                              space: cs,
                              bitmapInfo: CGImageAlphaInfo.premultipliedFirst.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)
    else { return nil }
    ctx.interpolationQuality = .high
    let sw = CGFloat(W) * scale, sh = CGFloat(H) * scale
    let x = (CGFloat(W) - sw) / 2, y = (CGFloat(H) - sh) / 2
    ctx.draw(img, in: CGRect(x: x, y: y, width: sw, height: sh))
    return buffer
}

let content = (try? String(contentsOfFile: manifestPath, encoding: .utf8)) ?? ""
let lines = content.split(separator: "\n").map(String.init)
var frame = 0
for line in lines {
    let parts = line.split(separator: " ")
    guard let img = loadImg(String(parts[0])) else { print("falta", parts[0]); continue }
    let scale = parts.count > 1 ? CGFloat(Double(parts[1]) ?? 1.0) : 1.0
    while !input.isReadyForMoreMediaData { usleep(3000) }
    if let buf = makeBuffer(img, scale: scale) {
        adaptor.append(buf, withPresentationTime: CMTime(value: CMTimeValue(frame), timescale: FPS))
        frame += 1
    }
}
input.markAsFinished()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
print("MP4 escrito: \(outPath) | frames=\(frame) | status=\(writer.status.rawValue)")
if let e = writer.error { print("error:", e) }

// thumbnail de verificacion a los 8s
let asset = AVURLAsset(url: outURL)
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
if let cg = try? gen.copyCGImage(at: CMTime(seconds: 8, preferredTimescale: 600), actualTime: nil) {
    let turl = URL(fileURLWithPath: outPath + ".thumb.png")
    if let dest = CGImageDestinationCreateWithURL(turl as CFURL, "public.png" as CFString, 1, nil) {
        CGImageDestinationAddImage(dest, cg, nil)
        CGImageDestinationFinalize(dest)
        print("thumb:", turl.path)
    }
}
