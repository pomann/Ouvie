//
//  LoginSplitController.swift
//  Ouvie
//
//  Created by Roman Prochazka on 05/05/2020.
//  Copyright © 2020 Roman Prochazka. All rights reserved.
//

import Cocoa

struct Responses: Codable {
    let code: String
    let status: String
    let data: [String]
}

class LoginSplitController: NSViewController {

    @IBOutlet weak var usernameField: NSTextField!
    @IBOutlet weak var pswdField: NSSecureTextField!
    @IBOutlet weak var usernameLabel: NSTextField!
    @IBOutlet weak var nameLabel: NSTextField!
    @IBOutlet weak var emailLable: NSTextField!
    
    @IBOutlet weak var loginStack: NSStackView!
    @IBOutlet weak var userDetailsStack: NSStackView!
    
    var token: String = ""
    var username: String = ""
    var email: String = ""
    var name: String = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do view setup here.
        self.userDetailsStack.isHidden = true
    }
    
    @IBAction func onLogin(_ sender: Any) {
        if (usernameField.stringValue != "" && pswdField.stringValue != "") {
            self.username = self.usernameField.stringValue
            sendRequest(api: "api/v1/auth/login?" + "user=" + usernameField.stringValue + "&password=" + pswdField.stringValue)
        }
    }
    
    @IBAction func onRegister(_ sender: Any) {
        if let url = URL(string: "http://localhost:4200/register") {
            NSWorkspace.shared.open(url)
        }
    }
    
    @IBAction func onLogout(_ sender: Any) {
        self.username = ""
        self.token = ""
        self.email = ""
        self.name = ""
        

        self.pswdField.stringValue = ""
        self.usernameField.stringValue = ""
        
        loginStack.isHidden = false
        userDetailsStack.isHidden = true
        

        let dashboard = parent?.children[0] as! DashboardController
        dashboard.onLogout()
        self.view.window?.contentViewController = parent as! ContainerController
    }
    
    func sendRequest(api: String) -> Void {
        let session = URLSession.shared;
        let url = URL(string: "http://127.0.0.1:5000/" + api)!
        
        let task = session.dataTask(with: url, completionHandler: { data, response, error in
        // Check the response
            if error != nil || data == nil {
                print("Seems like an error! error || data nil")
                return
            }
            
            guard let mime = response?.mimeType, mime == "application/json" else {
                print("Not a JSON!")
                return
            }
            
            guard let response = response as? HTTPURLResponse, (200...299).contains(response.statusCode) else {
                print("Server response error!")
                return
            }
            
            do {
                let json = try JSONDecoder().decode(Responses.self, from: data! )
                if (json.code == "OV1111") {
                    DispatchQueue.main.async {
                        self.email = json.data.first ?? ""
                        self.token = json.data.last ?? ""
                        self.name = "Roman Prochazka"
                        
                        self.showUserInfo()
                    }
                }
                    
                
            } catch {
                print("JSON error: \(error.localizedDescription)")
            }
        })
        task.resume()
    }
    
    func showUserInfo() -> Void {
        self.loginStack.isHidden = true
        self.userDetailsStack.isHidden = false
        
        self.usernameLabel.stringValue = "Hi " + self.username + " !"
        self.emailLable.stringValue = self.email
        self.nameLabel.stringValue = self.name

        let dashboard = parent?.children[0] as! DashboardController
        dashboard.onLogin(user: self.username, email: self.email, token: self.token)
        self.view.window?.contentViewController = parent as! ContainerController
    }
}
