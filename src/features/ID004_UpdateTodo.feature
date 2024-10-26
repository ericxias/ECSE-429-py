Feature: Update a Todo Task Instance
    As a user of the rest api todo list manager application
    I want to update the information of a todo task
    So I can organize the tasks I need to complete

    Background:
    Given a Todo task with title "test", doneStatus "false", and description "test" exists in the system

    Scenario: User updates all information of a Todo task (Normal Flow)
        When the user updates a Todo task with new title "shred paperwork", doneStatus "True", and description "shred all the paperwork"
        Then the Todo task should have title "shred paperwork", doneStatus "true", and description "shred all the paperwork"
    
    Scenario: User updates only the title of a Todo task (Alternate Flow)
        When the user updates a Todo task with new title "shred paperwork" 
        Then the Todo task should have title "shred paperwork", doneStatus "false", and description "test"
    
    Scenario: User updates a Todo task without a Title (Error Flow)
        When the user updates a Todo task with new doneStatus "True" and description "shred all the paperwork"
        Then the system should return an error message "title : field is mandatory" and status code "400"