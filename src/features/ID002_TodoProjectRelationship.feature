Feature: Create a Todo and Project Relationship
    As a user of the rest api todo list manager application
    I want to create a relationship between a todo task and a project
    So I can track what project my task belongs to
    
    Scenario: User creates a relationship between Todo and Category (Normal Flow)
        Given a Todo task with title "test" and doneStatus "False" and a project with title "ptest", completed "False", and active "False" exists in the system
        When the user creates a relationship between the Todo and the Project
        Then the relationship between Todo and Project is created successfully

    Scenario: Todo and Category relation already exist (Alternate Flow)
        Given a relationship between a Todo task with title "test" and doneStatus "False" and a project with title "ptest", completed "False", and active "False" already exists in the system
        When the user creates a relationship between the Todo and the Project
        Then the relationship between Todo and Project is created successfully

    Scenario: Project does not exist (Error Flow)
        Given a Project does not exist
        When the user creates a relationship between the Todo and the Project
        Then the system should return an error message "Could not find thing matching value for id" and status code "404"
