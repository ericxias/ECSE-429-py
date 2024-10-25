Feature: Create a Todo and Category Relationship
    As a user of the rest api todo list manager application
    I want to create a relationship between a todo task and a category
    So I can track what category my task belongs to
    
    Background:
        Given the following categories exist in the system:
            | id | title | description |
            | 1 | Office | Work related tasks |
            | 2 | Home | Personal tasks |
        Given the following Todo tasks exist in the system:
            | id | title | doneStatus | description |
            | 1 | scan paperwork | false | scan all the paperwork |
            | 2 | file paperwork | false | file all the paperwork |
    
    Scenario Outline: User creates a relationship between Todo and Category (Normal Flow)
        When the user creates a relationship between Todo with id "<id>" and Category with id "<cid>"
        And a Todo task with id "<id>" and a Category with id "<cid>" exists in the system
        Then the relationship between Todo with id "<id>" and Category with id "<cid>" is created successfully
        Examples:
            | id | cid |
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

    Scenario Outline: Todo and Category relation already exist (Alternate Flow)
        When the user creates a relationship between Todo with id "<id>" and Category with id "<cid>"
        And a relationship between a Todo task with id "<id>" and a Category with id "<cid>" already exists in the system
        Then the system should return with a valid response code
        Examples:
            | id | cid |
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
        When the user creates a relationship between Todo with id "<id>" and Category with id "<cid>"
        And a Todo task with id "<id>" does not exist
        Then the system should return an error message "Could not find parent thing for relationship todos/<id>/categories"
        Examples:
            | id | cid |
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