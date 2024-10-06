import pytest
import requests
import json

def test_get_todos_with_id():
    # Test get todos with id
    response = requests.get('http://localhost:4567/todos')
    assert response.status_code == 200

def test_post_create_todo():
    # Test create new todo
    response = requests.get('http://localhost:4567/todos')
    response1 = requests.post('http://localhost:4567/todos', json={"title":"test","doneStatus": False,"description":""})
    # Retrieve the ID of the new todo
    new_todo_id = response1.json()["id"]
    # Check if the new todo is created
    assert response1.json() == [response.json(), {"todos":[{"id": new_todo_id,"title":"test","doneStatus":"false","description":""}]}]
    assert response1.status_code == 201

def test_invalid_post_todo():
    # Test create new todos with invalid inputs
    response = requests.post('http://localhost:4567/todos', json={"id":1,"title":"test","doneStatus": False,"description":""})
    assert response.json() == [{"errorMessages":["Invalid Creation: Failed Validation: Not allowed to create with id"]}]
    assert response.status_code == 400

    response2 = requests.post('http://localhost:4567/todos', json={"name": "test", "title":"test","doneStatus":"false","description":""})
    assert response2.json() == [{"errorMessages":["Could not find field: name"]}]
    assert response2.status_code == 400

    response3 = requests.post('http://localhost:4567/todos', json={"title":"test","doneStatus": "false","description":""})
    assert response3.json() == [{"errorMessages":["Failed Validation: doneStatus should be BOOLEAN"]}]
    assert response3.status_code == 400


def test_delete_category_relationship():
    # Test delete relationship of category with todo with id
    response = requests.get('http://localhost:4567/todos')
    


def test_delete_taskof_relationship():
    # Test delete relationship of taskof with todo with id
    response = requests.get('http://localhost:4567/todos')

def test_delete_todo():
    # Test delete todo with id 
    response = requests.get('http://localhost:4567/todos')


