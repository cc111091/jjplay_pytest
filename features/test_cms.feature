Feature: CMS Page

    Scenario: Get Code
        Given Navigate to "CMS"'s "MobileVerificationCode" page
        Given Login as "river01" / "123qwe"
        Then Search and get "13405017718"'s newest validation code today
