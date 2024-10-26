import requests
import json
from behave import * 

# install pip-install behave
# to run -> behave -i <feature file name> 
# to run all -> behave

# ID001_TodoCategoryRelationship.feature

@given('a Todo task with title "{title}" and doneStatus "{doneStatus}" and a Category with title "{cTitle}" exists in the system')
def step_given_todo_and_category_exist(context, title, doneStatus, cTitle):
    done_status_bool = process_bool(doneStatus)
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": title, "doneStatus": done_status_bool})
    category_response = requests.post(f'http://localhost:4567/categories', json={"title": cTitle, "description": "test"})
    assert todo_response.status_code == 201
    assert category_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    print(context.todo_id)
    context.category_id = category_response.json()['id']
    print(context.category_id)

@given('a relationship between a Todo task with title "{title}" and doneStatus "{doneStatus}" and a Category with title "{cTitle}" already exists in the system')
def step_given_relationship_exists(context, title, doneStatus, cTitle):
    done_status_bool = process_bool(doneStatus)
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": title, "doneStatus": done_status_bool})
    category_response = requests.post(f'http://localhost:4567/categories', json={"title": cTitle})
    relationship_response = requests.post(f'http://localhost:4567/todos/{todo_response.json()["id"]}/categories', json={"id": category_response.json()["id"]})
    assert todo_response.status_code == 201
    assert category_response.status_code == 201
    assert relationship_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.category_id = category_response.json()['id']

@given('a Category does not exist')
def step_given_category_does_not_exist(context):
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": "test", "doneStatus": False})
    category_response = requests.post('http://localhost:4567/categories', json={"title": "test"})
    assert todo_response.status_code == 201
    assert category_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.category_id = category_response.json()['id']
    response = requests.delete(f'http://localhost:4567/categories/{context.category_id}')
    assert response.status_code == 200

@when('the user creates a relationship between the Todo and the Category')
def step_impl(context):
    body = {"id": context.category_id}
    response = requests.post(f'http://localhost:4567/todos/{context.todo_id}/categories', json=body)
    context.response = response

@then('the relationship between Todo and Category is created successfully')
def step_then_verify_relationship_created(context):
    response = context.response
    assert response.status_code == 201

@then('the system should return an error message "{error_message}" and status code "{status_code}"')
def step_then_verify_error_message(context, error_message, status_code):
    response = context.response
    assert response.status_code == int(status_code)
    assert response.json()['errorMessages'][0] == error_message


# ID002_TodoProjectRelationship.feature

@given('a Todo task with title "{title}" and doneStatus "{doneStatus}" and a project with title "{ptitle}", completed "{completed}", and active "{active}" exists in the system')
def step_given_todo_and_project_exist(context, title, doneStatus, ptitle, completed, active):
    done_status_bool = process_bool(doneStatus)
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": title, "doneStatus": done_status_bool})
    project_response = requests.post(f'http://localhost:4567/projects', json={"title": ptitle, "completed": completed_bool, "active": active_bool})
    assert todo_response.status_code == 201
    assert project_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.project_id = project_response.json()['id']

@given('a relationship between a Todo task with title "{title}" and doneStatus "{doneStatus}" and a project with title "{ptitle}", completed "{completed}", and active "{active}" already exists in the system')
def step_given_relationship_exists(context, title, doneStatus, ptitle, completed, active):
    done_status_bool = process_bool(doneStatus)
    completed_bool = process_bool(completed)
    active_bool = process_bool(active)
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": title, "doneStatus": done_status_bool})
    project_response = requests.post(f'http://localhost:4567/projects', json={"title": ptitle, "completed": completed_bool, "active": active_bool})
    relationship_response = requests.post(f'http://localhost:4567/todos/{todo_response.json()["id"]}/tasksof', json={"id": project_response.json()["id"]})
    assert todo_response.status_code == 201
    assert project_response.status_code == 201
    assert relationship_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.project_id = project_response.json()['id']

@given('a project does not exist')
def step_given_project_does_not_exist(context):
    todo_response = requests.post(f'http://localhost:4567/todos', json={"title": "test", "doneStatus": False})
    project_response = requests.post('http://localhost:4567/projects', json={"title": "test"})
    assert todo_response.status_code == 201
    assert project_response.status_code == 201
    context.todo_id = todo_response.json()['id']
    context.project_id = project_response.json()['id']
    response = requests.delete(f'http://localhost:4567/projects/{context.project_id}')
    assert response.status_code == 200

@when('the user creates a relationship between the Todo and the Project')
def step_impl(context):
    body = {"id": context.project_id}
    response = requests.post(f'http://localhost:4567/todos/{context.todo_id}/tasksof', json=body)
    context.response = response

@then('the relationship between Todo and Project is created successfully')
def step_then_verify_relationship_created(context):
    response = context.response
    assert response.status_code == 201

# ID003_CreateTodo.feature

@when('the user creates a Todo task with title "{title}" and doneStatus "{doneStatus}" and description "{description}"')
def step_when_create_todo_task(context, title, doneStatus, description):
    done_status_bool = process_bool(doneStatus)
    body = {"title": title, "doneStatus": done_status_bool, "description": description}
    response = requests.post('http://localhost:4567/todos', json=body)
    context.response = response

@when('the user creates a Todo task with title "{title}" and doneStatus "{doneStatus}"')
def step_when_create_todo_task(context, title, doneStatus):
    done_status_bool = process_bool(doneStatus)
    body = {"title": title, "doneStatus": done_status_bool}
    response = requests.post('http://localhost:4567/todos', json=body)
    context.response = response

@then('the Todo task is successfully created with title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_then_verify_todo_created(context, title, doneStatus, description):
    response = context.response
    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['doneStatus'] == doneStatus
    assert response.json()['description'] == description

@then('the Todo task is successfully created with title "{title}", doneStatus "{doneStatus}", and no description')
def step_then_verify_todo_created(context, title, doneStatus):
    response = context.response
    assert response.status_code == 201
    assert response.json()['title'] == title
    assert response.json()['doneStatus'] == doneStatus
    assert response.json()['description'] == ""

# ID004_UpdateTodo.feature



# ID005_DeleteTodo.feature

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