Feature: Create a Project and Todo Relationship
    As a user of the rest api todo manager application
    I want to create a relationship between a project and a task
    So I can keep track of what tasks need to be completed for a project

    Scenario: User creates a relationship between Project and Task (Normal Flow)
        Given a Project with title "Test Project", completed "False", active "False", and a Todo task with title "Test" and doneStatus "False" already exists in the system
        When the user creates a relationship between the Project and Todo
        Then the relationship between Project and Todo is successfully created

    Scenario: User creates a relationship that already exists (Alternate Flow)
        Given a relationship between a Project with title "Test Project", completed "False", active "False", and a Todo task with title "Test" and doneStatus "False" already exists in the system
        When the user creates a relationship between the Project and Todo
        Then the relationship between Project and Todo is successfully created

    Scenario: Todo does not exist (Error Flow)
        Given a Todo does not exist
        When the user creates a relationship between the Project and Todo
        Then the system should return an error message "Could not find thing matching value for id" and status code "404"