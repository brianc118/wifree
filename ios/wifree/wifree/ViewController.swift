//
//  ViewController.swift
//  wifree
//
//  Created by Brian Chen on 30/9/17.
//  Copyright © 2017 wifree. All rights reserved.
//

import UIKit
import CoreLocation

class ViewController: UIViewController, CLLocationManagerDelegate, UIPickerViewDelegate, UIPickerViewDataSource {
    var locationManager: CLLocationManager!
    @IBOutlet weak var picker: UIPickerView!
    var pickerData: [String] = [String]()
    var currentPickerRow: Int!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager.requestWhenInUseAuthorization()
        
        self.picker.delegate = self
        self.picker.dataSource = self
        
        pickerData = ["walking", "driving", "transit"]
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func locationManager(_ manager: CLLocationManager, didChangeAuthorization status: CLAuthorizationStatus) {
        if status == .authorizedAlways {
            if CLLocationManager.isMonitoringAvailable(for: CLBeaconRegion.self) {
                if CLLocationManager.isRangingAvailable() {
                    // do stuff
                }
            }
        }
    }
    
    func sendWithMessenger(msg: String) {
        let phoneNumber = "4158531662"
        let text = msg
     
        guard let messageURL = URL(string: "sms:\(phoneNumber)&body=\(text)")
            else { return }
        if UIApplication.shared.canOpenURL(messageURL) {
            UIApplication.shared.openURL(messageURL)
        }
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return pickerData.count;
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return pickerData[row] as String
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        currentPickerRow = row
    }

    //MARK: Actions

    @IBAction func findWifi(_ sender: UIButton) {
        
        if( CLLocationManager.authorizationStatus() == CLAuthorizationStatus.authorizedWhenInUse ||
            CLLocationManager.authorizationStatus() == CLAuthorizationStatus.authorizedAlways){
            
            let currentLocation = locationManager.location!.coordinate
            let loctext:String = pickerData[currentPickerRow] + "," +  String(currentLocation.latitude) + "," + String(currentLocation.longitude)
            sendWithMessenger(msg: loctext)
        }
    }
}

