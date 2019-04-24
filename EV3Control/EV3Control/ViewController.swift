//
//  ViewController.swift
//  EV3Control
//
//  Created by Masaki Hosono on 2018/11/08.
//

import UIKit

class ViewController: UIViewController {
    let controller = EV3Controller.sharedController
    var currentFrontWheelState = 0.0
    
    @IBOutlet weak var horizontalSlider: UISlider!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func forwardButtonTapped(_ sender: Any) {
        controller.controlBackWheel(amount: 0.4)
    }
    
    @IBAction func backwardButtonTapped(_ sender: Any) {
        controller.controlBackWheel(amount: -0.4)
    }
    
    @IBAction func leftButtonTapped(_ sender: Any) {
        if (currentFrontWheelState != -1.0) {
            currentFrontWheelState -= 0.5
            controller.controlFrontWheel(amount: Float(currentFrontWheelState))
        }
    }
    
    @IBAction func rightButtonTapped(_ sender: Any) {
        if (currentFrontWheelState != 1.0) {
            currentFrontWheelState += 0.5
            controller.controlFrontWheel(amount: Float(currentFrontWheelState))
        }
    }
    
    @IBAction func stopButtonTapped(_ sender: Any) {
        currentFrontWheelState = 0.0
//        controller.controlFrontWheel(amount: Float(currentFrontWheelState))
        controller.controlBackWheel(amount: 0.0)
    }
    
    @IBAction func holizontalSliderValueChanged(_ sender: Any) {
        let amount = ceil(horizontalSlider.value * 15) / 15
        controller.controlFrontWheel(amount: amount)
    }

    @IBAction func button0Tapped(_ sender: Any) {
        controller.controlFrontWheel(amount: -1.0)
    }
    
    @IBAction func button1Tapped(_ sender: Any) {
        controller.controlFrontWheel(amount: -0.5)
    }
    
    @IBAction func button2Tapped(_ sender: Any) {
        controller.controlFrontWheel(amount: 0.0)
    }
    
    @IBAction func button3Tapped(_ sender: Any) {
        controller.controlFrontWheel(amount: 0.5)
    }
    
    @IBAction func button4Tapped(_ sender: Any) {
        controller.controlFrontWheel(amount: 1.0)
    }
}

