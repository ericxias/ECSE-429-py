Feature: Create a Project and Category Relationship
    As a user of the rest api todo list manager application
    I want to create a relationship between a project and category
    So I can more effectively organize my projects

    Scenario: User creates a relationship between Project and Category (Normal Flow)
        Given a Project with title "Test Project", completed "False", active "False", and a Category with title "ctest" already exists in the system
        When the user creates a relationship between the Project and the Category
        Then the relationship between the Project and Category is successfully created

    Scenario: User creates a relationship that already exists (Alternate Flow)
        Given a relationship between a Project with title "Test Project", completed "False", active "False", and a Category with title "ctest" already exists in the system
        When the user creates a relationship between the Project and the Category
        Then the relationship between the Project and Category is successfully created

    Scenario: Category does not exist (Error Flow)
        Given a Category does not exist for the Project-Category relationship
        When the user creates a relationship between the Project and the Category
        Then the system should return an error message "Could not find thing matching value for id" and status code "404"