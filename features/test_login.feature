Feature: Login

    Scenario: Test return passed
        Then return passed
    
    Scenario: Test return failed
        Then return failed

    Scenario Outline: Test return Outline
        Then return "<result>"

        Examples: example outline 1
            | result |
            | passed |
            | failed |
