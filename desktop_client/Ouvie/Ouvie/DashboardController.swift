//
//  DashboardController.swift
//  Ouvie
//
//  Created by Roman Prochazka on 04/05/2020.
//  Copyright © 2020 Roman Prochazka. All rights reserved.
//

import Cocoa

class DashboardController: NSViewController {
    
    @IBOutlet weak var tabView: NSTabView!
    @IBOutlet weak var branchTab: NSTabViewItem!
    @IBOutlet weak var commitTab: NSTabViewItem!
    @IBOutlet weak var commitBtn: NSButton!
    @IBOutlet weak var projectLabel: NSTextField!
    @IBOutlet weak var projectSelection: NSTextField!
    @IBOutlet weak var welcomeMsg: NSTextField!
    @IBOutlet weak var logoIcon: NSImageView!
    @IBOutlet weak var slogan: NSTextField!
    @IBOutlet weak var commitsLabel: NSTextField!
    @IBOutlet weak var commitSelection: NSTextField!
    
    var user: String = ""
    var email: String = ""
    var token: String = ""
    var pid: String = ""
    var projects: [String] = []
    var commits: [String] = []
    var result: String = ""
    
    let oConf: String = "oConf.txt";
    
    var saveBranchTab: NSTabViewItem = NSTabViewItem()
    var saveCommitTab: NSTabViewItem = NSTabViewItem()

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do view setup here.
        self.view.wantsLayer = true;
        let color : CGColor = CGColor(red: 0.09, green: 0.09, blue: 0.22, alpha: 1.0)
        self.view.layer?.backgroundColor = color
        
        self.saveBranchTab = branchTab
        self.saveCommitTab = commitTab
        self.tabView.removeTabViewItem(branchTab)
        self.tabView.removeTabViewItem(commitTab)
        self.commitBtn.isHidden = true;
        
        self.tabView.isHidden = true
        
    }
    
    override func viewDidAppear() {
        super.viewDidAppear()
        self.view.window?.title = "Ouvie Dashboard"
    }
    
    func onLogin(user: String, email: String, token: String) -> Void {
        self.user = user
        self.token = token
        
        self.tabView.isHidden = false
        self.logoIcon.isHidden = true
        self.slogan.isHidden = true;
        self.welcomeMsg.isHidden = true
        
        setProjects()
    }
    
    func onLogout() -> Void {
        self.user = ""
        self.token = ""
        
        self.tabView.isHidden = true
        self.logoIcon.isHidden = false
        self.slogan.isHidden = false;
        self.welcomeMsg.isHidden = false
    }
    
    @IBAction func onSelectProject(_ sender: Any) {
        let fileManager = FileManager.default;
        
        let result = selectFileDialog(files: false)
        
        if (result != "nil"){
            let ouvieConf = result + "/.ouvie";
            print(ouvieConf)
            
            if (fileManager.fileExists(atPath: ouvieConf)){
                print("Ouvie Project")
                self.commitBtn.isHidden = false;
                self.tabView.addTabViewItem(saveCommitTab)
                self.tabView.addTabViewItem(saveBranchTab)
            } else {
                print("Not an Ouvie project")
            }
        }
    }
    
    @IBAction func onCommitProject(_ sender: Any) {
        let result = selectFileDialog(files: true)
        if (result != "nil") {
            uploadFile(filePath: result, endpoint: "http://127.0.0.1:5001/api/v1/add/project")
        }
    }
    
    @IBAction func onInitProject(_ sender: Any) {
        let fileManager = FileManager.default;
        
        let result = selectFileDialog(files: false)
        if (result != "nil") {
            let dictUrl = URL(fileURLWithPath: result)
            let initOuvie = dictUrl.appendingPathComponent(".ouvie")
            
            do {
                try fileManager.createDirectory(at: initOuvie, withIntermediateDirectories: true, attributes: nil)
            } catch  {
                print("error: Project not initialized")
            }
        }
    }
    
    func setProjects() -> Void {
        let session = URLSession.shared;
        let url = URL(string: "http://127.0.0.1:5000/api/v1/retrieve/project?" + "user=" + self.user)!

        var request = URLRequest(url: url)
        
        request.setValue(self.token, forHTTPHeaderField: "Authorization")

        let task = session.dataTask(with: request, completionHandler: { data, response, error in
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
                print(json)
                if (json.code == "OV1111") {
                    DispatchQueue.main.async {
                        self.projects = json.data;
                        self.projectLabel.stringValue = json.data.joined(separator: "\n")
                    }
                }


            } catch {
                print("JSON error: \(error.localizedDescription)")
            }
        })
        task.resume()
    }
    
    @IBAction func onSelectCommit(_ sender: Any) {
        let selection = self.commitSelection.stringValue;
        
        if self.commits.contains(selection) {
            let resultFile = selectFileDialog(files: true)
            if (resultFile != "nil") {
                let url = URL(string: "http://localhost:5001/api/v1/rebuild/version?" + "user=" + self.user + "&pid=" + self.pid + "&chash=" + selection)!

                var request = URLRequest(url: url)

                request.setValue(self.token, forHTTPHeaderField: "Authorization")

                let task = URLSession.shared.downloadTask(with: request) { data, response, error in
                    if let data = data {
                        do {
                            try FileManager.default.removeItem(at: URL(fileURLWithPath: resultFile))
                            var rs = resultFile.split(separator: "/")
                            rs.removeLast()
                            let rsurl = URL(fileURLWithPath: "/" + rs.joined(separator: "/") + "/SampleVideo1.mp4")
                            try FileManager.default.copyItem(at: data, to: rsurl)
                        } catch let error {
                            print("Copy Error: \(error.localizedDescription)")
                        }
                    }
                }

                task.resume()
            }
        }
    }
    
    @IBAction func onClone(_ sender: Any) {
        let selection = self.projectSelection.stringValue;
        
        if self.projects.contains(selection) {
            result = selectFileDialog(files: false)
            if (result != "nil") {
                let url = URL(string: "http://localhost:5001/api/v1/clone/project?" + "user=" + self.user + "&pname=" + selection)!

                var request = URLRequest(url: url)
                
                request.setValue(self.token, forHTTPHeaderField: "Authorization")
                
                let task = URLSession.shared.downloadTask(with: request) { data, response, error in
                    if let data = data {
                        do {
                            var initOuvie = URL(fileURLWithPath: self.result + "/" + selection)
                            try FileManager.default.createDirectory(at: initOuvie, withIntermediateDirectories: true, attributes: nil)
                            
                            var dictUrl = URL(fileURLWithPath: self.result + "/" + selection + "/SampleVideo.mp4")
                            try FileManager.default.copyItem(at: data, to: dictUrl)
                            dictUrl = URL(fileURLWithPath: self.result + "/" + selection)
                            initOuvie = dictUrl.appendingPathComponent(".ouvie")
                            try FileManager.default.createDirectory(at: initOuvie, withIntermediateDirectories: true, attributes: nil)
                            print("done")
                            self.getPid(pname: selection)
                        } catch let error {
                            print("Copy Error: \(error.localizedDescription)")
                        }
                    }
                }

                task.resume()
            } else {
                return
            }
        } else {
            return
        }
    }
    
    func getPid(pname: String) -> Void {
        let session = URLSession.shared;
        let url = URL(string: "http://127.0.0.1:5000/api/v1/retrieve/pid?" + "user=" + self.user + "&pname=" + pname)!

        var request = URLRequest(url: url)
        
        request.setValue(self.token, forHTTPHeaderField: "Authorization")

        let task = session.dataTask(with: request, completionHandler: { data, response, error in
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
                print(json)
                if (json.code == "OV1111") {
                    self.getChash(pid: json.data.first ?? "", pname: pname)
                }


            } catch {
                print("JSON error: \(error.localizedDescription)")
            }
        })
        task.resume()
    }
    
    func getChash(pid: String, pname: String) -> Void {
        let session = URLSession.shared;
        let url = URL(string: "http://127.0.0.1:5000/api/v1/retrieve/commits?" + "user=" + self.user + "&pid=" + pid)!

        var request = URLRequest(url: url)
        
        request.setValue(self.token, forHTTPHeaderField: "Authorization")

        let task = session.dataTask(with: request, completionHandler: { data, response, error in
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
                print(json)
                if (json.code == "OV1111") {
                    DispatchQueue.main.async {
                        self.createConfFile(data: [pid, (json.data.first ?? "")], pFolderConf: self.result + "/" + pname + "/.ouvie")
                    }
                    self.getCommits(pname: pname);
                }


            } catch {
                print("JSON error: \(error.localizedDescription)")
            }
        })
        task.resume()
    }
    
    func getCommits(pname: String) {
        let session = URLSession.shared;
        let url = URL(string: "http://127.0.0.1:5000/api/v1/retrieve/commit/count?" + "user=" + self.user + "&pname=" + pname + "&branch=master")!

        var request = URLRequest(url: url)
        
        request.setValue(self.token, forHTTPHeaderField: "Authorization")

        let task = session.dataTask(with: request, completionHandler: { data, response, error in
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
                print(json)
                if (json.code == "OV1111") {
                    DispatchQueue.main.async {
                        self.commits = json.data;
                        self.commitsLabel.stringValue = json.data.joined(separator: "\n")
                    }
                }


            } catch {
                print("JSON error: \(error.localizedDescription)")
            }
        })
        task.resume()
    }
    
    func createConfFile(data : [String], pFolderConf: String) -> Void {
        self.pid = data.first!
        var confStr = "pid:" + (data.first ?? "nil")
        confStr = confStr + "\n" + "chash:" + (data.last ?? "nil")
        let confUrl = URL(fileURLWithPath: pFolderConf + "/" + self.oConf)
        print(confUrl)
        // Creates config file
        FileManager.default.createFile(atPath: pFolderConf + "/" + self.oConf, contents: nil, attributes: nil)
        
        // Writes hashes to config file
        do {
            try confStr.write(to: confUrl, atomically: false, encoding: .utf8)
        }
        catch {/* error handling here */}
    }
    
    func selectFileDialog(files: Bool) -> String {
        let dialog = NSOpenPanel();
        var filePath: String = "nil";
        
        dialog.showsResizeIndicator    = true;
        dialog.showsHiddenFiles        = false;
        dialog.allowsMultipleSelection = false;
        dialog.canChooseDirectories = !files;
        dialog.canChooseFiles = files;

        if (dialog.runModal() ==  NSApplication.ModalResponse.OK) {
            let result = dialog.url // Pathname of the file

            if (result != nil) {
                filePath = result!.path // Path to selected file
            }
        } else {
            // User clicked "Cancel"
            return "nil"
        }
        return filePath
    }
    
    func uploadFile(filePath: String, endpoint: String) -> Void {
        
        let fileName = filePath.split(separator: "/").last
        let prName = Array(filePath.split(separator: "/").suffix(2)).first!
        let fileUrl = URL(fileURLWithPath: filePath);
        let fileManager = FileManager.default
        
        var params: String = "?" + "user=" + self.user;
        params = params + "&name=" + prName;
        params = params + "&cfiles=" + (fileName ?? "nil");
        
        var pFolderConfA = filePath.split(separator: "/")
        var _ = pFolderConfA.removeLast()
        let pFolderConf = "/" + pFolderConfA.joined(separator: "/") + "/.ouvie"
        print(pFolderConf)

        if (fileManager.fileExists(atPath: pFolderConf)){
            let session = URLSession.shared
            let url = URL(string: endpoint + params)!

            var request = URLRequest(url: url)

            request.httpMethod = "POST"
            request.setValue(self.token, forHTTPHeaderField: "Authorization")


            let task = session.uploadTask(with: request, fromFile: fileUrl, completionHandler: { data, response, error in
            // Check the response
                if error != nil || data == nil {
                    print("Seems like an error! error || data nil")
                    return
                }

                guard let response = response as? HTTPURLResponse, (200...299).contains(response.statusCode) else {
                    print("Server response error!")
                    return
                }

                do {
                    let json = try JSONDecoder().decode(Responses.self, from: data! )
                    if (json.code == "OV1111") {
                        print(json.data)
                        self.createConfFile(data: json.data, pFolderConf: pFolderConf)
                    }


                } catch {
                    print("JSON error: \(error.localizedDescription)")
                }
            })
            task.resume()
        } else { print("Not an Ouvie project")}

    }
    
}
