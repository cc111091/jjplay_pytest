Feature: CMS Page

    Scenario: Get Code
        Given Navigate to "http://20.24.16.242:8002/mobileverificationcode/"
        Given Login as "river01" / "123qwe"
        Then Search and get "13405017718"'s newest validation code today
