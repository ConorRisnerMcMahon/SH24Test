describe('Test postcode search', () => {

    beforeEach(() => {
        cy.visit('http://localhost:5000')
      })

    it('Displays results for a servable postcode', () => {
      cy.contains('Search for a postcode')
      cy.get('[test-id="postcode-search-form"]')
      cy.get('#postcode').type('SE5 0NF')
      cy.get('#submit').click()
      cy.contains('SE5 0NF')
      cy.get('[test-id="is_servable"]')
      cy.get('[test-id="is_not_servable"]').should('not.exist')
    })

    it('Displays results for a not servable postcode', () => {
        cy.contains('Search for a postcode')
        cy.get('[test-id="postcode-search-form"]')
        cy.get('#postcode').type('SE55 0NF')
        cy.get('#submit').click()
        cy.contains('SE55 0NF')
        cy.get('[test-id="is_servable"]').should('not.exist')
        cy.get('[test-id="is_not_servable"]')
      })

  })
  