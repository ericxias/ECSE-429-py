import pytest
import requests
import json

""" def test_get_todos_with_id():
    # Retrieve all todos and test read the first todo if any todos exist
    response = requests.get('http://localhost:4567/todos')

    if response.status_code == 200 and response.json() != []:
        # Get the id of the first todo
        todo_id = response.json()[0]["id"]
        response1 = requests.get('http://localhost:4567/todos/' + str(todo_id))

        assert response1.json() == response.json()[0]
        assert response1.status_code == 200

    else:
        # If there is no todo, test the error message when attempting to get todo with id 1
        response2 = requests.get('http://localhost:4567/todos/1')
        assert response2.json() == [{"errorMessages":["Could not find an instance with todos/1"]}]
        assert response2.status_code == 404


def test_get_categories_with_todo_id():
    # Retrieve all todos and test read the categories of the first todo if any todos with category relationships exist
    response = requests.get('http://localhost:4567/todos')

    if response.status_code == 200 and response.json() != []:
        # Get the id of the first todo
        todo_id = response.json()[0]["id"]
        # Check if the first todo has any categories

        if response.json()[0]["categories"] != []:
            # Get the id of the first category of the first todo and check that the categories of the first todo match the categories of the first category
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/categories')
            category_data = {}
            # for each category of the first todo, get the category data and add it to the category_data dictionary

            for i in range(len(response.json()[0]["categories"]) - 1):
                response2 = requests.get('http://localhost:4567/categories/' + response.json()[0]["categories"][i+1]["id"])
                category_data += response2.json()

            # Check if the categories of the first todo match the category data retrieved        
            response3 = requests.get('http://localhost:4567/categories/' + response.json()[0]["categories"][0]["id"])
            assert category_data == response3.json()
            assert response1.status_code == 200

        else:
            # If no categories exist, return an empty list
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/categories')
            assert response1.json() == [{"categories":[]}]
            assert response1.status_code == 200


def test_get_tasksof_with_todo_id():
    # Retrieve all todos and test read the tasksof of the first todo if any todos with tasksof relationships exist
    response = requests.get('http://localhost:4567/todos')

    if response.status_code == 200 and response.json() != []:
        # Get the id of the first todo
        todo_id = response.json()[0]["id"]
        # Check if the first todo has any tasksof relationships

        if response.json()[0]["tasksof"] != []:
            # Get the id of the first tasksof of the first todo and check that the tasksof of the first todo match the tasksof of the first tasksof
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/tasksof')
            tasksof_data = {}
            # for each tasksof of the first todo, get the tasksof data and add it to the tasksof_data dictionary

            for i in range(len(response.json()[0]["tasksof"]) - 1):
                response2 = requests.get('http://localhost:4567/tasksof/' + response.json()[0]["tasksof"][i+1]["id"])
                tasksof_data += response2.json()

            # Check if the tasksof of the first todo match the tasksof data retrieved        
            response3 = requests.get('http://localhost:4567/tasksof/' + response.json()[0]["tasksof"][0]["id"])
            assert tasksof_data == response3.json()
            assert response1.status_code == 200

        else:
            # If no tasksof relationships exist, return an empty list
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/tasksof')
            assert response1.json() == [{"projects":[]}]
            assert response1.status_code == 200
 """

def test_post_create_todo():
    # Test create new todo
    response = requests.post('http://localhost:4567/todos', json={"title":"test","doneStatus": False,"description":""})
    assert response.status_code == 201
    new_todo_id = response.json()["id"]
    print(new_todo_id)

    # Check if the new todo is created
    response2 = requests.get('http://localhost:4567/todos/' + str(new_todo_id))
    
    assert response2.json() == {"todos":[{"id":new_todo_id,"title":"test","doneStatus":"false","description":""}]}


def test_invalid_post_todo():
    # Test create new todos with invalid inputs
    response = requests.post('http://localhost:4567/todos', json={"id":1,"title":"test","doneStatus": False,"description":""})
    assert response.json() == {"errorMessages": ["Invalid Creation: Failed Validation: Not allowed to create with id"]}
    assert response.status_code == 400

    response2 = requests.post('http://localhost:4567/todos', json={"name": "test", "title":"test","doneStatus":False,"description":""})
    assert response2.json() == {"errorMessages":["Could not find field: name"]}
    assert response2.status_code == 400

    response3 = requests.post('http://localhost:4567/todos', json={"title":"test","doneStatus": "false","description":""})
    assert response3.json() == {"errorMessages":["Failed Validation: doneStatus should be BOOLEAN"]}
    assert response3.status_code == 400


def test_update_todo_with_post():
    # Test update todos with id
    response = requests.get('http://localhost:4567/todos')

    if response.status_code == 200:
        todos = response.json()

        # Check if any todos exist
        if isinstance(todos, list) and len(todos) > 0:
            # Get the id of the first todo
            todo_id = todos[0]["id"]
            response1 = requests.post('http://localhost:4567/todos/' + str(todo_id), json={"title":"test","doneStatus": True,"description":""})

            # Check if the todo is updated
            assert response1.json() == {"id":todo_id,"title":"test","doneStatus":"true","description":"","tasksof":[{"id":"1"}]}
            assert response1.status_code == 200

    else:
        # If there is no todo, test the error message when attempting to update todo with id 1
        response2 = requests.post('http://localhost:4567/todos/1', json={"title":"test","doneStatus": True,"description":""})
        assert response2.json() == {"errorMessages":["No such todo entity instance with GUID or ID 1 found"]}
        assert response2.status_code == 404


def test_update_todo_with_put():
    # Test update todos with id
    response = requests.get('http://localhost:4567/todos')

    if response.status_code == 200:
        todos = response.json()

        # Check if any todos exist
        if isinstance(todos, list) and len(todos) > 0:
            # Get the id of the first todo
            todo_id = todos[0]["id"]
            response1 = requests.put('http://localhost:4567/todos/' + str(todo_id), json={"title":"test","doneStatus": True,"description":""})

            # Check if the todo is updated
            assert response1.json() == {"id":todo_id,"title":"test","doneStatus":"true","description":"","tasksof":[{"id":"1"}]}
            assert response1.status_code == 200

            # test the error message when attempting to update without inputting a title
            response2 = requests.put('http://localhost:4567/todos/' + str(todo_id), json={"doneStatus": True,"description":""})
            assert response2.json() == {"errorMessages":["title : field is mandatory"]}
            assert response2.status_code == 400

    else:
        # If there is no todo, test the error message when attempting to update todo with id 1
        response3 = requests.put('http://localhost:4567/todos/1', json={"title":"test","doneStatus": True,"description":""})
        assert response3.json() == {"errorMessages":["Invalid GUID for 1 entity todo"]}
        assert response3.status_code == 404

""" def test_creating_category_relationship():
    # Test create relationship of category with todo with id
    response = requests.get('http://localhost:4567/todos')
    response2 = requests.get('http://localhost:4567/categories')



def test_delete_category_relationship():
    # Test delete relationship of category with todo with id
    response = requests.get('http://localhost:4567/todos')
    


def test_delete_taskof_relationship():
    # Test delete relationship of taskof with todo with id
    response = requests.get('http://localhost:4567/todos')

def test_delete_todo():
    # Test delete todo with id 
    response = requests.get('http://localhost:4567/todos')
 """
# Run the tests
if __name__ == '__main__':
    pytest.main()
