import requests
import json
from behave import * 

# install pip-install behave
# to run -> behave -i <feature file name> 
# to run all -> behave

# ID001_TodoCategoryRelationship.feature

@given('a Todo task with title "{title}" and doneStatus "{doneStatus}" and a Category with title "{cTitle}" exists in the system')
def step_impl(context, title, doneStatus, cTitle):
    # Create a Todo task and a Category, store the ids in the context
    done_status_bool = process_bool(doneStatus)
    todo_body = {
        "title": title,
        "doneStatus": done_status_bool
    }
    todo_response = requests.post(f'http://localhost:4567/todos', json=todo_body)
    category_response = requests.post(f'http://localhost:4567/categories', json={"title": cTitle})
    assert todo_response.status_code == 201
    assert category_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.category_id = category_response.json()['id']

@given('a relationship between a Todo task with title "{title}" and doneStatus "{doneStatus}" and a Category with title "{cTitle}" already exists in the system')
def step_impl(context, title, doneStatus, cTitle):
    # Create a Todo task and a Category, create a relationship between them, store the ids in the context
    done_status_bool = process_bool(doneStatus)
    todo_body = {
        "title": title,
        "doneStatus": done_status_bool
    }
    todo_response = requests.post(f'http://localhost:4567/todos', json=todo_body)
    category_response = requests.post(f'http://localhost:4567/categories', json={"title": cTitle})
    relationship_response = requests.post(f'http://localhost:4567/todos/{todo_response.json()["id"]}/categories', json={"id": category_response.json()["id"]})
    assert todo_response.status_code == 201
    assert category_response.status_code == 201
    assert relationship_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.category_id = category_response.json()['id']

@given('a Category does not exist')
def step_impl(context):
    # Create a Todo task and a Category, delete the Category, store the ids in the context
    # This ensures a valid Todo task exists, but a Category with the id does not
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": "test"})
    category_response = requests.post('http://localhost:4567/categories', json={"title": "test"})
    assert todo_response.status_code == 201
    assert category_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.category_id = category_response.json()['id']
    response = requests.delete(f'http://localhost:4567/categories/{context.category_id}')
    assert response.status_code == 200

@when('the user creates a relationship between the Todo and the Category')
def step_impl(context):
    # Run the POST request to create the relationship
    response = requests.post(f'http://localhost:4567/todos/{context.todo_id}/categories', json={"id": context.category_id})
    context.response = response

@then('the relationship between Todo and Category is created successfully')
def step_impl(context):
    response = context.response
    assert response.status_code == 201

@then('the system should return an error message "{error_message}" and status code "{status_code}"')
def step_impl(context, error_message, status_code):
    # Generic, used for multiple features
    response = context.response
    assert response.status_code == int(status_code)
    assert response.json()['errorMessages'][0] == error_message


# ID002_TodoProjectRelationship.feature

@given('a Todo task with title "{title}" and doneStatus "{doneStatus}" and a project with title "{ptitle}", completed "{completed}", and active "{active}" exists in the system')
def step_impl(context, title, doneStatus, ptitle, completed, active):
    # Create a Todo task and a Project, store the ids in the context
    done_status_bool = process_bool(doneStatus)
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    todo_body = {
        "title": title,
        "doneStatus": done_status_bool
    }
    project_body = {
        "title": ptitle,
        "completed": completed_bool,
        "active": active_bool
    }
    todo_response = requests.post(f'http://localhost:4567/todos', json=todo_body)
    project_response = requests.post(f'http://localhost:4567/projects', json=project_body)
    assert todo_response.status_code == 201
    assert project_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.project_id = project_response.json()['id']

@given('a relationship between a Todo task with title "{title}" and doneStatus "{doneStatus}" and a project with title "{ptitle}", completed "{completed}", and active "{active}" already exists in the system')
def step_impl(context, title, doneStatus, ptitle, completed, active):
    # Create a Todo task and a Project, create a relationship between them, store the ids in the context
    done_status_bool = process_bool(doneStatus)
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    todo_body = {
        "title": title,
        "doneStatus": done_status_bool
    }
    project_body = {
        "title": ptitle,
        "completed": completed_bool,
        "active": active_bool
    }
    todo_response = requests.post(f'http://localhost:4567/todos', json=todo_body)
    project_response = requests.post(f'http://localhost:4567/projects', json=project_body)
    relationship_response = requests.post(f'http://localhost:4567/todos/{todo_response.json()["id"]}/tasksof', json={"id": project_response.json()["id"]})
    assert todo_response.status_code == 201
    assert project_response.status_code == 201
    assert relationship_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.project_id = project_response.json()['id']

@given('a Project does not exist')
def step_impl(context):
    # Create a Todo task and a Project, delete the Project, store the ids in the context
    # This ensures a valid Todo task exists, but a Project with the id does not
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": "test"})
    project_response = requests.post('http://localhost:4567/projects', json={"title": "test"})
    assert todo_response.status_code == 201
    assert project_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.project_id = project_response.json()['id']
    response = requests.delete(f'http://localhost:4567/projects/{context.project_id}')
    assert response.status_code == 200

@when('the user creates a relationship between the Todo and the Project')
def step_impl(context):
    # Run the POST request to create the relationship
    response = requests.post(f'http://localhost:4567/todos/{context.todo_id}/tasksof', json={"id": context.project_id})
    context.response = response

@then('the relationship between Todo and Project is created successfully')
def step_impl(context):
    response = context.response
    assert response.status_code == 201

# ID003_CreateTodo.feature

@when('the user creates a Todo task with title "{title}" and doneStatus "{doneStatus}" and description "{description}"')
def step_impl(context, title, doneStatus, description):
    # Run the POST request to create the Todo task with the given title, doneStatus, and description
    done_status_bool = process_bool(doneStatus)
    body = {
        "title": title, 
        "doneStatus": done_status_bool, 
        "description": description
        }
    response = requests.post('http://localhost:4567/todos', json=body)
    context.response = response

@when('the user creates a Todo task with title "{title}" and doneStatus "{doneStatus}"')
def step_impl(context, title, doneStatus):
    # Run the POST request to create the Todo task with the given title and doneStatus
    done_status_bool = process_bool(doneStatus)
    body = {
        "title": title, 
        "doneStatus": done_status_bool
        }
    response = requests.post('http://localhost:4567/todos', json=body)
    context.response = response

@then('the Todo task is successfully created with title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    response = context.response
    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['doneStatus'] == doneStatus
    assert response.json()['description'] == description

@then('the Todo task is successfully created with title "{title}", doneStatus "{doneStatus}", and no description')
def step_impl(context, title, doneStatus):
    response = context.response
    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['doneStatus'] == doneStatus
    assert response.json()['description'] == ""

# ID004_UpdateTodo.feature

@given('a Todo task with title "{title}", doneStatus "{doneStatus}", and description "{description}" exists in the system')
def step_impl(context, title, doneStatus, description):
    # Create a Todo task with the given title, doneStatus, and description, store the id in the context
    # This ensures a valid Todo task exists for us to update
    done_status_bool = process_bool(doneStatus)
    body = {
        "title": title,
        "doneStatus": done_status_bool,
        "description": description
    }
    response = requests.post('http://localhost:4567/todos', json=body)
    assert response.status_code == 201
    context.todo_id = response.json()['id']

@when('the user updates a Todo task with new title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    # Run the POST request to update the Todo task with the given title, doneStatus, and description
    done_status_bool = process_bool(doneStatus)
    body = {
        "title": title, 
        "doneStatus": done_status_bool, 
        "description": description
        }
    response = requests.post(f'http://localhost:4567/todos/{context.todo_id}', json=body)
    context.response = response    

@when('the user updates a Todo task with new title "{title}"')
def step_impl(context, title):
    # Run the POST request to update the Todo task with the given title
    response = requests.post(f'http://localhost:4567/todos/{context.todo_id}', json={"title": title})
    context.response = response

@when('the user updates a Todo task with new doneStatus "{doneStatus}" and description "{description}"')
def step_impl(context, doneStatus, description):
    # Run the PUT request to update the Todo task with the given doneStatus and description
    # This results in an error with PUT
    done_status_bool = process_bool(doneStatus)
    body = {
        "doneStatus": done_status_bool, 
        "description": description
        }
    response = requests.put(f'http://localhost:4567/todos/{context.todo_id}', json=body)
    context.response = response

@then('the Todo task should have title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    response = context.response
    assert response.status_code == 200
    assert response.json()['title'] == title
    assert response.json()['doneStatus'] == doneStatus
    assert response.json()['description'] == description

# ID005_DeleteTodo.feature

@given('a Todo task does not exist')
def step_impl(context):
    # Create a Todo task, delete the Todo task, store the id in the context
    # This a Todo task with the id does not exist
    response = requests.post('http://localhost:4567/todos', json={"title": "test"})
    assert response.status_code == 201
    context.todo_id = response.json()['id']
    response = requests.delete(f'http://localhost:4567/todos/{context.todo_id}')
    assert response.status_code == 200

@when('the user deletes the Todo task')
def step_impl(context):
    # Run the DELETE request to delete the Todo task
    response = requests.delete(f'http://localhost:4567/todos/{context.todo_id}')
    context.response = response

@when('the user deletes a relationship between the Todo and the Category')
def step_impl(context):
    # Run the DELETE request to delete the relationship between the Todo and the Category
    response = requests.delete(f'http://localhost:4567/todos/{context.todo_id}/categories/{context.category_id}')
    context.response = response

@when('the user deletes a relationship between the Todo and the Project')
def step_impl(context):
    # Run the DELETE request to delete the relationship between the Todo and the Project
    response = requests.delete(f'http://localhost:4567/todos/{context.todo_id}/tasksof/{context.project_id}')
    context.response = response

@then('the Todo task is successfully deleted')
def step_impl(context):
    response = context.response
    assert response.status_code == 200

@then('the relationship between the Todo and the Category is successfully deleted')
def step_impl(context):
    # Check if the relationship between the Todo and the Category is successfully deleted
    response = context.response
    assert response.status_code == 200
    get_response = requests.get('http://localhost:4567/todos/{context.todo_id}/categories')
    if 'categories' in get_response.json():
        for category in get_response.json()['categories']:
            assert category['id'] != context.category_id

@then('the relationship between the Todo and the Project is successfully deleted')
def step_impl(context):
    # Check if the relationship between the Todo and the Project is successfully deleted
    response = context.response
    assert response.status_code == 200
    get_response = requests.get('http://localhost:4567/todos/{context.todo_id}/tasksof')
    if 'tasksof' in get_response.json():
        for project in get_response.json()['tasksof']:
            assert project['id'] != context.project_id

@then('the system should return an error message with id "{error_message}" and status code "{status_code}"')
def step_impl(context, error_message, status_code):
    # Append the todo_id to the error message, check if the error message and status code match the expected values
    response = context.response
    error_message = error_message + context.todo_id
    assert response.json()['errorMessages'][0] == error_message
    assert response.status_code == int(status_code)

# ID006_CreateProject.feature

@when('the user creates a Project with title "{title}" and completed "{completed}" and active "{active}" and description "{description}"')
def step_impl(context, title, completed, active, description):
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    body = {
        "title": title,
        "completed": completed_bool,
        "active": active_bool,
        "description": description
        }
    response = requests.post('http://localhost:4567/projects', json=body)
    context.response = response

@when('the user creates a Project with title "{title}" and completed "{completed}" and active "{active}"')
def step_impl(context, title, completed, active):
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    body = {
        "title": title,
        "completed": completed_bool,
        "active": active_bool,
        }
    response = requests.post('http://localhost:4567/projects', json=body)
    context.response = response

@then('the Project is successfully created with title "{title}", completed "{completed}", active "{active}", and description "{description}"')
def step_impl(context, title, completed, active, description):
    response = context.response
    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['completed'] == completed
    assert response.json()['active'] == active
    assert response.json()['description'] == description

@then('the Project is successfully created with title "{title}", completed "{completed}", active "{active}", and no description')
def step_impl(context, title, completed, active):
    response = context.response
    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['completed'] == completed
    assert response.json()['active'] == active
    assert response.json()['description'] == ""

#ID007_UpdateProject.feature

@given('a Project with title "{title}", completed "{completed}", active "{active}", and description "{description}"')
def step_impl(context, title, completed, active, description):
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    body = {
        "title": title,
        "completed": completed_bool,
        "active": active_bool,
        "description": description
    }
    response = requests.post('http://localhost:4567/projects', json=body)
    assert response.status_code == 201
    context.project_id = response.json()['id']

@when('the user updates a Project with new title "{title}", completed "{completed}", active "{active}", and description "{description}"')
def step_impl(context, title, completed, active, description):
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    body = {
        "title": title,
        "completed": completed_bool,
        "active": active_bool,
        "description": description
    }
    response = requests.post(f'http://localhost:4567/projects/{context.project_id}', json=body)
    context.response = response

@when('the user updates a Project using PUT with new title "{title}", completed "{completed}", active "{active}", and description "{description}"')
def step_impl(context, title, completed, active, description):
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    body = {
        "title": title,
        "completed": completed_bool,
        "active": active_bool,
        "description": description
    }
    response = requests.put(f'http://localhost:4567/projects/{context.project_id}', json=body)
    context.response = response

@when('the user updates a Project with new title "{title}"')
def step_impl(context, title):
    response = requests.post(f'http://localhost:4567/projects/{context.project_id}', json={"title": title})
    context.response = response

@then('the Project should have title "{title}", completed "{completed}", active "{active}", and description "{description}"')
def step_impl(context, title, completed, active, description):
    response = context.response
    assert response.status_code == 200
    assert response.json()['title'] == title
    assert response.json()['completed'] == completed
    assert response.json()['active'] == active
    assert response.json()['description'] == description






# processing strings to boolean if the string is "true" or "false"
def process_bool(string):
    if isinstance(string, bool):
        return string
    elif isinstance(string, str):
        string_lower = string.lower()
        if string_lower == "true":
            return True
        elif string_lower == "false":
            return False
        else:
            return string