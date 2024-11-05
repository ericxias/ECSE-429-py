Feature: Update a Todo Task Instance
    As a user of the rest api todo list manager application
    I want to update the information and details of a Project
    So that my projects are consistently kept up to date

    Background:
    Given a Project with title "Sample Project", completed "true", active "false", and description "sample description" already exists in the system

    Scenario: User updates all Project information (Normal Flow)
        When the user updates a Project with new title "Clean Up Desk", completed "False", active "True", and description "tidy up deskspace"
        Then the Project should have title "Clean Up Desk", completed "false", active "true", and description "tidy up deskspace"

    Scenario: User only updates the title of a Project (Alternate Flow)
        When the user updates a Project with new title "Clean Up Desk"
        Then the Project should have title "Clean Up Desk", completed "true", active "false", and description "sample description"
    
    Scenario: User updates Project with non boolean completed (Error Flow)
        When the user updates a Project using PUT with new title "Clean Up Desk", completed "not a boolean", active "False", and description "tidy up deskspace"
        Then the system should return an error message "Failed Validation: completed should be BOOLEAN" and status code "400"