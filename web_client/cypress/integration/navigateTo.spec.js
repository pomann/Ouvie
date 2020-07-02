/// <reference types="cypress" />

context('Navigate', () => {
  beforeEach(() => {
    cy.visit('http://localhost:4200/')
  })

  it('Should display Main Page', () => {
    // Check if main elements present on Main page
    cy.get('#banner').should('be.visible')
    cy.get('#menu-container').should('be.visible')
    cy.get('#advantage').should('be.visible')
    cy.get('#footer').should('be.visible')
  })

  it('Should display Login Page', () => {
    // Click Login button and check if login page is displayed
    cy.get('[routerlink="/login"]').click()
    cy.get('#login-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
  })

  it('Should display Register Page', () => {
    cy.get('#signup-btn').click()
    cy.get('#signup-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
  })

  it('Should not display Dashboard', () => {
    cy.visit('http://localhost:4200/dashboard')
    cy.get('#login-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
  })
})
