Feature: Delete a Todo or Relationship
    As a user of the rest api todo list manager application
    I want to delete a todo task or relationship
    So I can remove tasks that are no longer needed

    Background:
        Given the application is running
    
    Scenario Outline: User deletes a Todo task (Normal Flow)
        When the user deletes a Todo task with id "<id>"
        And a Todo task with id "<id>" exists in the system
        Then the Todo task with id "<id>" is deleted successfully
        Examples:
            | id |
            | 1 |
            | 2 |
            | 3 |
            | 4 |
            | 10 |

    Scenario Outline: User deletes a Todo Category relationship (Alternate Flow)
        When the user deletes a relationship between Todo with id "<id>" and Category with id "<cid>"
        And a Todo task with id "<id>" is associated with a category with id "<cid>"
        Then the relationship between Todo with id "<id>" and Category with id "<cid>" is deleted successfully
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
        
    Scenario Outline: User deletes a Todo Project relationship (Alternate Flow)
        When the user deletes a relationship between Todo with id "<id>" and Project with id "<pid>"
        And a Todo task with id "<id>" is associated with a project with id "<pid>"
        Then the relationship between Todo with id "<id>" and Project with id "<pid>" is deleted successfully
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

    Scenario Outline: Todo task does not exist (Error Flow)
        When the user deletes a Todo task with id "<id>"
        And a Todo task with id "<id>" does not exist
        Then the system should return an error message "Could not find an instance with todos/<id>"
        Examples:
            | id |
            | 1 |
            | 2 |
            | 3 |
            | 4 |
            | 10 |