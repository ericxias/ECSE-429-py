Feature: Update a Todo Task Instance
    As a user of the rest api todo list manager application
    I want to update the information of a todo task
    So I can organize the tasks I need to complete

    Background:
        Given the following Todo tasks exist in the system:
            | id | title | doneStatus | description |
            | 1 | scan paperwork | false | scan all the paperwork |
            | 2 | file paperwork | false | file all the paperwork |
        
    Scenario Outline: User updates all information of a Todo task (Normal Flow)
        When the user updates a Todo task with new title "shred paperwork" and doneStatus "True" and description "shred all the paperwork"
        Then the Todo task should have title "shred paperwork", doneStatus "true", and description "shred all the paperwork"
    
    Scenario Outline: User updates only the title of a Todo task (Alternate Flow)
        When the user updates a Todo task with new title "shred paperwork" 
        Then the Todo task should have title "shred paperwork", doneStatus "false", and description "scan all the paperwork"
    
    Scenario Outline: User updates a Todo task without a Title (Error Flow)
        When the user updates a Todo task with new doneStatus "True" and description "shred all the paperwork"
        Then the system should return an error message "title : field is mandatory"