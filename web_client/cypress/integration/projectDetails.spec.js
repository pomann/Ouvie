/// <reference types="cypress" />

context('Project Info', () => {
  beforeEach(() => {
    cy.visit('http://localhost:4200/login')
    cy.get('#user').type("omo")
    cy.get('#pass').type('ouvie')
    cy.get('#loginBtn').click()
    cy.get(':nth-child(4) > #project-details > .linkText').click()
  })

  it('Should display Project info', () => {
    cy.get('#project-commit').should('be.visible')
  })

  it('Should display filename', () => {
    cy.get('.project-item > :nth-child(1)').should('be.visible')
    cy.get('.project-item > :nth-child(1)').should('contain', 'poo.mp4')
  })

  it('Should be on master branch', () => {
    cy.get('#branches').should('contain', 'master')
  })

  it('Should display 9 commits and 2 branches', () => {
    cy.get('#project-info > :nth-child(1)').should('contain', 'Commits: 9')
    cy.get('#project-info > :nth-child(2)').should('contain', 'Branches: 2')
  })

  it('should display 7 commits on branch master', () => {
    cy.get('#dashboard-workspace-projects-wrapper > [style="float: right;"]').should('contain', 'master: 7')
  })

  it('Should display switch branches when different branch is selected', () => {
    cy.get('#branches').select('test')
    cy.get('.project-item > :nth-child(1)').should('contain', 'pood.mp4')
    cy.get('#branches').should('contain', 'test')
  })

  it('should display 1 commit on branch test', () => {
    cy.get('#branches').select('test')
    cy.get('#dashboard-workspace-projects-wrapper > [style="float: right;"]').should('contain', 'test: 1')
  })
})
