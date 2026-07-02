import AVFoundation
import Foundation
let a=CommandLine.arguments
let videoURL=URL(fileURLWithPath:a[1])
let cues=try! JSONSerialization.jsonObject(with:Data(contentsOf:URL(fileURLWithPath:a[2]))) as! [[String:Any]]
let outURL=URL(fileURLWithPath:a[3]); try? FileManager.default.removeItem(at:outURL)
let comp=AVMutableComposition()
let vAsset=AVAsset(url:videoURL)
let vTrack=comp.addMutableTrack(withMediaType:.video,preferredTrackID:kCMPersistentTrackID_Invalid)!
let srcV=vAsset.tracks(withMediaType:.video)[0]
try! vTrack.insertTimeRange(CMTimeRange(start:.zero,duration:vAsset.duration),of:srcV,at:.zero)
for c in cues {
  let t=c["t"] as! Double; let wav=c["wav"] as! String
  let aAsset=AVAsset(url:URL(fileURLWithPath:wav))
  guard let srcA=aAsset.tracks(withMediaType:.audio).first else {continue}
  let aTrack=comp.addMutableTrack(withMediaType:.audio,preferredTrackID:kCMPersistentTrackID_Invalid)!
  try! aTrack.insertTimeRange(CMTimeRange(start:.zero,duration:aAsset.duration),of:srcA,at:CMTime(seconds:t,preferredTimescale:600))
}
let exp=AVAssetExportSession(asset:comp,presetName:AVAssetExportPresetHighestQuality)!
exp.outputURL = outURL; exp.outputFileType = .mp4
let sem=DispatchSemaphore(value:0)
exp.exportAsynchronously{sem.signal()}
sem.wait()
if exp.status == .completed {print("mux ok")} else {print("mux error:",exp.error as Any); exit(1)}
