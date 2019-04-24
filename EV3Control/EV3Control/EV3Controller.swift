//
//  EV3Controller.swift
//  EV3Control
//
//  Created by Masaki Hosono on 2018/11/09.
//

import Foundation
import CoreML
import Vision
import UIKit

class EV3Controller {
    static let sharedController = EV3Controller()
    
    private let base_url = "http://CHANGE_HERE_INTO_YOUR_ADDRESS:8080"
    
    private init() {
    }
    
    /**
     * Steering
     * -1 ... Left Max
     *  1 ... Right Max
     */
    func controlFrontWheel(amount: Float) {
        let urlstr = base_url + "?target=front&amount=\(amount)"
        let url = URL(string: urlstr)
        
        call(url!)
    }
    
    /**
     * Throttle
     * -1 ... Backward Max
     *  1 ... Forward Max
     */
    func controlBackWheel(amount: Float) {
        let urlstr = base_url + "?target=back&amount=\(amount)"
        let url = URL(string: urlstr)
        
        call(url!)
    }
    
    
    func sendPixels(pixbuff: CVPixelBuffer) {
        DispatchQueue.global(qos: .default).async {
            self.sendPixelsAsync(pixbuff: pixbuff)
        }
    }
    
    /**
     * Send Image
     */
    func sendPixelsAsync(pixbuff: CVPixelBuffer) {
        let image = CVPixelBufferGetUIImageData(pixbuff: pixbuff)
        
        let url = URL(string: base_url)
        var request = URLRequest(url: url!, cachePolicy: URLRequest.CachePolicy.reloadIgnoringLocalCacheData, timeoutInterval: 1.0)
        request.httpMethod = "POST"
        
        do {
            let data = try JSONSerialization.data(withJSONObject: ["image": image.jpegData(compressionQuality: 1.0)?.base64EncodedString(), "mimeType": "image/jpeg"], options: [])
            request.httpBody = data
            request.addValue("application/json", forHTTPHeaderField: "content-type")
            
            print(request)
            
        } catch let error {
            print(error)
        }
        
        let task = URLSession.shared.dataTask(with: request) { (response_data, response, error) in
            if error != nil {
                print("\(#function)")
                print(error!.localizedDescription)
            }
        }
        task.resume()
    }
    
    /**
     * Convert CVPixelBuffer into Grayscaled UIImage
     */
    func CVPixelBufferGetUIImageData(pixbuff: CVPixelBuffer) -> UIImage {
        let pixelBufferHeight = CGFloat(CVPixelBufferGetHeight(pixbuff))
        let pixelBufferWidth = CGFloat(CVPixelBufferGetWidth(pixbuff))
        var ciImage = CIImage(cvPixelBuffer: pixbuff)
        ciImage = ciImage.oriented(CGImagePropertyOrientation.right)
        
        // Grayscaling
        let ciFilter:CIFilter = CIFilter(name: "CIColorMonochrome")!
        ciFilter.setValue(ciImage, forKey: "inputImage")
        ciFilter.setValue(CIColor(red: 0.75, green: 0.75, blue: 0.75), forKey: "inputColor")
        ciFilter.setValue(1.0, forKey: "inputIntensity")
        let grayscaleImage: CIImage = ciFilter.outputImage!
        
        // Resizing
        let ciScaleFilter:CIFilter = CIFilter(name: "CILanczosScaleTransform")!
        ciScaleFilter.setValue(grayscaleImage, forKey: "inputImage")
        ciScaleFilter.setValue(176/pixelBufferHeight, forKey: "inputScale")
        ciScaleFilter.setValue(1.0, forKey: "inputAspectRatio")
        let resizedGrayscaleImage: CIImage = ciScaleFilter.outputImage!
        
        let imageRect:CGRect = CGRect(x: 0, y: pixelBufferWidth * 176/pixelBufferHeight - 176, width: 176, height: 176)
        let ciContext = CIContext.init()
        let cgimage = ciContext.createCGImage(resizedGrayscaleImage, from: imageRect)
        let image = UIImage(cgImage: cgimage!)
        
        return image
    }
    
    private func call(_ url: URL) {
        let request = URLRequest(url: url, cachePolicy: URLRequest.CachePolicy.reloadIgnoringLocalCacheData, timeoutInterval: 60.0)
        
        let task = URLSession.shared.dataTask(with: request) { (response_data, response, error) in
            if error != nil {
                print("\(#function)")
                print(error!.localizedDescription)
            }
        }
        task.resume()
    }
}

