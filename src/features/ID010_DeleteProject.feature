Feature: Delete a Project or Relationship
    As a user of the rest api todo list manager application
    I want to delete a project or relationship
    So I can keep a tidy database of relevant projects

    Scenario: User deletes a Project (Normal Flow)
        Given a Project with title "Test Project", completed "False", active "False", and description "Test Description" exists in the system
        When the user deletes the Project
        Then the Project is successfully deleted

    Scenario: User deletes a Project Category Relationship (Alternate Flow)
        Given a relationship between a Project with title "Test Project", completed "False", active "False", and description "Test Description", and a Category "ctest" already exists in the system
        When the user deletes a relationship between the Project and Category
        Then the relationship between the Project and Category is successfully deleted
    
    Scenario: User deletes a Project Todo Relationship (Alternate Flow)
        Given a relationship between a Project with title "Test Project", completed "False", active "False", and description "Test Description", and a Todo task with title "Test" and doneStatus "False" alrady exists in the system
        When the user deletes a relationship between the Project and Todo
        Then the relationship between the Project and Todo is successfully deleted

    Scenario: User deletes a Project that does not exist (Error Flow)
        Given a Project does not exist
        When the user deletes the Project
        Then the system should return an error message with id "Could not find any instances with projects/" and status code "404"