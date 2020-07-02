/// <reference types="cypress" />

context('Register', () => {
  beforeEach(() => {
    cy.visit('http://localhost:4200/register')
  })

  it('Should display Register Page', () => {
    // Check if main elements present on Login page
    cy.get('#signup-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
  })

  it('Should display login form when "Log in" is clicked', () => {
    // Click Sign up now button and check if register page is displayed
    cy.get('#login-container > p > .linkText').click()
    cy.get('#login-container').should('be.visible')
    cy.get('#banner').should('not.be.visible')
    cy.get('p > .linkText').click()
  })

  it('Should display error messages when register button is clicked and form is empty', () => {
    cy.get('#registerBtn').click()
    cy.get(':nth-child(30)').should('be.visible')
  })

  it('Should display error when username is taken', () => {
    cy.get('[formcontrolname="username"]').type('omo').blur()
    cy.get(':nth-child(30)').should('be.visible')
  })

  it('Should display an error when email is taken', () => {
    cy.get('[formcontrolname="email"]').type('ouvie@ouvie.com').blur()
    cy.get('.valid-error').should('be.visible')
  })

  it('Should display an error when emails don\'t match', () => {
    cy.get('[formcontrolname="email"]').type('ouvie1234@ouvie.com').blur()
    cy.get('[formcontrolname="confirmEmail"]').type('ouvie124@ouvie.com').blur()
    cy.get('.valid-error').should('be.visible')

  })

  it('Should display an error when passwords don\' match', () => {
    cy.get('[formcontrolname="password"]').type('ouvie1234@ouvie.com').blur()
    cy.get('[formcontrolname="confirmPassword"]').type('ouvie124@ouvie.com').blur()
    cy.get('.valid-error').should('be.visible')

  })
})
