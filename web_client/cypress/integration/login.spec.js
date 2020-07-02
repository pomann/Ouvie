/// <reference types="cypress" />

context('Login', () => {
  beforeEach(() => {
    cy.visit('http://localhost:4200/login')
  })

  it('Should display Login Page', () => {
    // Check if main elements present on Login page
    cy.get('#login-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
  })

  it('Should display register form when "Sign up now" is clicked', () => {
    // Click Sign up now button and check if register page is displayed
    cy.get('p > .linkText').click()
    cy.get('#signup-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
    cy.get('#login-container > p > .linkText').click()
  })

  it('Should display an error message when incorrect details are entered', () => {
    cy.get('#user').type("omo")
    cy.get('#pass').type('12234')
    cy.get('#loginBtn').click()
    cy.get('form.ng-invalid > div').should('be.visible')
  })

  it('Should display an Dashboard when correct details are entered', () => {
    cy.get('#user').type("omo")
    cy.get('#pass').type('ouvie')
    cy.get('#loginBtn').click()
    cy.get('#username').should('be.visible')
  })
})
