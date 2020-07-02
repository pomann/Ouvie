//
//  OuvieUITests.swift
//  OuvieUITests
//
//  Created by Roman Prochazka on 26/03/2020.
//  Copyright © 2020 Roman Prochazka. All rights reserved.
//

import XCTest

class OuvieUITests: XCTestCase {

    override func setUp() {
        // Put setup code here. This method is called before the invocation of each test method in the class.

        // In UI tests it is usually best to stop immediately when a failure occurs.
        continueAfterFailure = false

        // In UI tests it’s important to set the initial state - such as interface orientation - required for your tests before they run. The setUp method is a good place to do this.
    }

    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testLogin() {
        // UI tests must launch the application that they test.
        let app = XCUIApplication()
        app.launch()
        
        let ouvieDashboardWindow = XCUIApplication().windows["Ouvie Dashboard"]
        let usernameTextField = ouvieDashboardWindow/*@START_MENU_TOKEN@*/.textFields["Username"]/*[[".splitGroups.textFields[\"Username\"]",".textFields[\"Username\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/
        usernameTextField.click()
        usernameTextField.typeText("omo")
        let passwordTextField = ouvieDashboardWindow/*@START_MENU_TOKEN@*/.secureTextFields["Password"]/*[[".splitGroups.secureTextFields[\"Password\"]",".secureTextFields[\"Password\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/
        passwordTextField.click()
        passwordTextField.typeText("ouvie")
        ouvieDashboardWindow/*@START_MENU_TOKEN@*/.buttons["Login"]/*[[".splitGroups.buttons[\"Login\"]",".buttons[\"Login\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/.click()
        
        // Use recording to get started writing UI tests.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
    }
    
    func testClone() {
        let app = XCUIApplication()
        app.launch()
        
        
        let ouvieDashboardWindow = XCUIApplication().windows["Ouvie Dashboard"]
        let usernameTextField = ouvieDashboardWindow/*@START_MENU_TOKEN@*/.textFields["Username"]/*[[".splitGroups.textFields[\"Username\"]",".textFields[\"Username\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/
        usernameTextField.click()
        usernameTextField.typeText("omo")
        let passwordTextField = ouvieDashboardWindow/*@START_MENU_TOKEN@*/.secureTextFields["Password"]/*[[".splitGroups.secureTextFields[\"Password\"]",".secureTextFields[\"Password\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/
        passwordTextField.click()
        passwordTextField.typeText("ouvie")
        ouvieDashboardWindow/*@START_MENU_TOKEN@*/.buttons["Login"]/*[[".splitGroups.buttons[\"Login\"]",".buttons[\"Login\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/.click()
        ouvieDashboardWindow/*@START_MENU_TOKEN@*/.tabs["Clone"]/*[[".splitGroups",".tabGroups.tabs[\"Clone\"]",".tabs[\"Clone\"]"],[[[-1,2],[-1,1],[-1,0,1]],[[-1,2],[-1,1]]],[0]]@END_MENU_TOKEN@*/.click()
        
        let textField = ouvieDashboardWindow/*@START_MENU_TOKEN@*/.tabGroups/*[[".splitGroups.tabGroups",".tabGroups"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/.children(matching: .textField).element
        textField.click()
        textField.typeText("Please")
        ouvieDashboardWindow/*@START_MENU_TOKEN@*/.buttons["Clone"]/*[[".splitGroups",".tabGroups.buttons[\"Clone\"]",".buttons[\"Clone\"]"],[[[-1,2],[-1,1],[-1,0,1]],[[-1,2],[-1,1]]],[0]]@END_MENU_TOKEN@*/.click()
        
    }

    func testLaunchPerformance() {
        if #available(macOS 10.15, iOS 13.0, tvOS 13.0, *) {
            // This measures how long it takes to launch your application.
            measure(metrics: [XCTOSSignpostMetric.applicationLaunch]) {
                XCUIApplication().launch()
            }
        }
    }
}
