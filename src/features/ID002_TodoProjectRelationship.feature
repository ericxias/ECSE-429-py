Feature: Create a Todo and Project Relationship
    As a user of the rest api todo list manager application
    I want to create a relationship between a todo task and a project
    So I can track what project my task belongs to
    
    Background:
        Given the application is running
    
    Scenario Outline: User creates a relationship between Todo and Project (Normal Flow)
        When the user creates a relationship between Todo with id "<id>" and Project with id "<pid>"
        And a Todo task with id "<id>" and a Project with id "<pid>" exists in the system and are not associated with each other
        Then the relationship between Todo with id "<id>" and Project with id "<pid>" is created successfully
        Examples:
            | id | pid |
            | 1 | 1 |
            | 1 | 2 |
            | 1 | 3 |
            | 2 | 1 |
            | 2 | 2 |
            | 2 | 3 |
            | 3 | 1 |
            | 3 | 2 |
            | 3 | 3 |
            | 4 | 1 |
            | 4 | 2 |
            | 4 | 3 |
            | 4 | 4 |
            | 10 | 10 |

    Scenario Outline: Todo and Project relationship already exists (Alternate Flow)
        When the user creates a relationship between Todo with id "<id>" and Project with id "<pid>"
        And a relationsip between Todo task with id "<id>" and a Project with id "<pid>" already exists in the system
        Then the system should return with a valid response code
        Examples:
            | id | pid |
            | 1 | 1 |
            | 1 | 2 |
            | 1 | 3 |
            | 2 | 1 |
            | 2 | 2 |
            | 2 | 3 |
            | 3 | 1 |
            | 3 | 2 |
            | 3 | 3 |
            | 4 | 1 |
            | 4 | 2 |
            | 4 | 3 |
            | 4 | 4 |
            | 10 | 10 |

    Scenario Outline: Todo does not exist (Error Flow)
        When the user creates a relationship between Todo with id "<id>" and Project with id "<pid>"
        And a Todo task with id "<id>" does not exist
        Then the system should return an error message "Could not find parent thing for relationship todos/<id>/tasksof"
        Examples:
            | id | pid |
            | 1 | 1 |
            | 1 | 2 |
            | 1 | 3 |
            | 2 | 1 |
            | 2 | 2 |
            | 2 | 3 |
            | 3 | 1 |
            | 3 | 2 |
            | 3 | 3 |
            | 4 | 1 |
            | 4 | 2 |
            | 4 | 3 |
            | 4 | 4 |
            | 10 | 10 |
