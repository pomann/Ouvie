/// <reference types="cypress" />

context('Dashboard', () => {
  beforeEach(() => {
    cy.visit('http://localhost:4200/login')
    cy.get('#user').type("omo")
    cy.get('#pass').type('ouvie')
    cy.get('#loginBtn').click()
  })

  it('Should display dashboard', () => {
    cy.get('#username').should('be.visible')
  })

  it('Should toggle user menu when username is clicked', () => {
    cy.get('#username').click()
    cy.get('#user-details-wrapper').should('be.visible')
    cy.get('#username').click()
    cy.get('#user-details-wrapper').should('not.be.visible')
  })

  it('Should Display projects', () => {
    cy.get(':nth-child(4) > #project-details > .linkText').should('be.visible')
  })

  it('Should Display project invo when project name is clicked', () => {
    cy.get(':nth-child(4) > #project-details > .linkText').click()
    cy.get('#project-commit').should('be.visible')
  })

  it('Should log user out when logout is clicked', () => {
    cy.get('#username').click()
    cy.get('#logout-btn').click()
    cy.get('#username').should('not.be.visible')
    cy.get('#login-container').should('be.visible')
  })
})
