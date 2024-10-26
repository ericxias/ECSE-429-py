Feature: Create a Todo and Category Relationship
    As a user of the rest api todo list manager application
    I want to create a relationship between a todo task and a category
    So I can track what category my task belongs to
    
    Scenario: User creates a relationship between Todo and Category (Normal Flow)
        Given a Todo task with title "test" and doneStatus "False" and a Category with title "ctest" exists in the system
        When the user creates a relationship between the Todo and the Category
        Then the relationship between Todo and Category is created successfully

    Scenario: Todo and Category relation already exist (Alternate Flow)
        Given a relationship between a Todo task with title "test" and doneStatus "False" and a Category with title "ctest" already exists in the system
        When the user creates a relationship between the Todo and the Category
        Then the relationship between Todo and Category is created successfully

    Scenario: Category does not exist (Error Flow)
        Given a Category does not exist
        When the user creates a relationship between the Todo and the Category
        Then the system should return an error message "Could not find thing matching value for id" and status code "404"
