Feature: Create a Todo Task Instance
    As a user of the rest api todo list manager application
    I want to create a todo task
    So I can organize the tasks I need to complete

    Background:
        Given the following Todo tasks exist in the system:
            | id | title | doneStatus | description |
            | 1 | scan paperwork | false | scan all the paperwork |
            | 2 | file paperwork | false | file all the paperwork |
    
    Scenario Outline: User creates a Todo task with (Normal Flow)
        When the user creates a Todo task with title "shred paperwork" and doneStatus "False" and description "shred all the paperwork"
        Then the Todo task is successfully updated with title "shred paperwork", doneStatus "false", and description "shred all the paperwork"

    Scenario Outline: User creates a Todo task with no description (Alternate Flow)
        When the user creates a Todo task with title "shred paperwork" and doneStatus "False" and description ""
        Then the Todo task is successfully updated with title "shred paperwork", doneStatus "false", and description ""

    Scenario Outline: User creates a Todo task with a non boolean doneStatus (Error Flow)
        When the user creates a Todo task with title "shred paperwork" and doneStatus "not a boolean" and description "shred all the paperwork"
        Then the system should return an error message "Failed Validation: doneStatus should be BOOLEAN"