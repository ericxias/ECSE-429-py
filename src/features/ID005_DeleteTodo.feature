Feature: Delete a Todo or Relationship
    As a user of the rest api todo list manager application
    I want to delete a todo task or relationship
    So I can remove tasks that are no longer needed
    
    Scenario: User deletes a Todo task (Normal Flow)
        Given a Todo task with title "test", doneStatus "false", and description "test" exists in the system
        When the user deletes the Todo task 
        Then the Todo task is successfully deleted

    Scenario: User deletes a Todo Category relationship (Alternate Flow)
        Given a relationship between a Todo task with title "test" and doneStatus "False" and a Category with title "ctest" already exists in the system
        When the user deletes a relationship between the Todo and the Category
        Then the relationship between the Todo and the Category is successfully deleted
        
    Scenario: User deletes a Todo Project relationship (Alternate Flow)
        Given a relationship between a Todo task with title "test" and doneStatus "False" and a project with title "ptest", completed "False", and active "False" already exists in the system
        When the user deletes a relationship between the Todo and the Project
        Then the relationship between the Todo and the Project is successfully deleted

    Scenario: Todo task does not exist (Error Flow)
        Given a Todo task does not exist
        When the user deletes the Todo task
        # Add the id of the Todo task to the error message
        Then the system should return an error message with id "Could not find any instances with todos/" and status code "404" 
