import pytest
import requests
import json

def test_initial_get_todos():
    # Test initial content in todos
    response = requests.get('http://localhost:4567/todos')
    assert response.json() == [{"todos":[{"id":"2","title":"file paperwork","doneStatus":"false","description":"","tasksof":[{"id":"1"}]},
                                         {"id":"1","title":"scan paperwork","doneStatus":"false","description":"","categories":[{"id":"1"}],"tasksof":[{"id":"1"}]}]}]
    assert response.status_code == 200

    # Test error with input in id
    response2 = requests.get('http://localhost:4567/todos/:id')
    assert response2.json() == [{"errorMessages":["Could not find an instance with todos/:id"]}]
    assert response2.status_code == 404

    # Get todo with id 1 and 2
    response3 = requests.get('http://localhost:4567/todos/1')
    assert response3.json() == [{"todos":[{"id":"1","title":"scan paperwork","doneStatus":"false","description":"","categories":[{"id":"1"}],"tasksof":[{"id":"1"}]}]}]
    assert response3.status_code == 200
    response4 = requests.get('http://localhost:4567/todos/2')
    assert response4.json() == [{"todos":[{"id":"2","title":"file paperwork","doneStatus":"false","description":"","tasksof":[{"id":"1"}]}]}]
    assert response4.status_code == 200

    # Retrieve relationship of categories of todo with id 1
    response5 = requests.get('http://localhost:4567/todos/1/categories')
    assert response5.json() == [{"categories":[{"id":"1","title":"Office","description":""}]}]
    assert response5.status_code == 200

    # Retrieve relationship categories of todo with id 2
    response6 = requests.get('http://localhost:4567/todos/2/categories')
    assert response6.json() == [{"categories":[]}]
    assert response6.status_code == 200

    # Retrieve taskof relationship of projects of todo with id 1
    response7 = requests.get('http://localhost:4567/todos/1/tasksof')
    assert response7.json() == [{"projects":[{"id":"1","title":"Office Work","completed":"false","active":"false","description":"","tasks":[{"id":"1"},{"id":"2"}]}]}]
    assert response7.status_code == 200

def test_delete_category_relationship():
    # Test delete relationship of category with todo with id 1
    response = requests.delete('http://localhost:4567/todos/1/categories/1')
    assert response.json() == []
    assert response.status_code == 200
    

    # Test delete relationship of category with todo with id 2
    response2 = requests.delete('http://localhost:4567/todos/2/categories/1')
    assert response2.json() == []
    assert response2.status_code == 200
