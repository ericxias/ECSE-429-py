Feature: Create a Project Instance
    As a user of the rest api todo list manager application
    I want to create a Project
    So I can manage the projects that I need to complete

    Scenario: User creates a Project (Normal Flow)
        When the user creates a Project with title "Clean Up Desk" and completed "False" and active "False" and description "tidy up deskspace"
        Then the Project is successfully created with title "Clean Up Desk", completed "false", active "false", and description "tidy up deskspace"

    Scenario: User creates a Project with empty description (Alternate Flow)
        When the user creates a Project with title "Clean Up Desk" and completed "False" and active "False"
        Then the Project is successfully created with title "Clean Up Desk", completed "false", active "false", and no description

    Scenario: User creates a Project with non boolean completed (Error Flow)
        When the user creates a Project with title "Clean Up Desk" and completed "not a boolean" and active "False" and description "tidy up deskspace"
        Then the system should return an error message "Failed Validation: completed should be BOOLEAN" and status code "400"