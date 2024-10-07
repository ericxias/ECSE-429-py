import pytest
import requests
import json

def test_get_todos_with_id():
    # Retrieve all todos and test read the first todo if any todos exist
    response = requests.get('http://localhost:4567/todos')
    todos = response.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]
        print(todo_id)
        response1 = requests.get('http://localhost:4567/todos/' + str(todo_id))
        assert response1.json() == {'todos': [todos["todos"][0]]}
        assert response1.status_code == 200

    else:
        # If there is no todo, test the error message when attempting to get todo with id 1
        response2 = requests.get('http://localhost:4567/todos/1')
        assert response2.json() == {"errorMessages":["Could not find an instance with todos/1"]}
        assert response2.status_code == 404

#JSONDecodeError when appending categories to the category_data dictionary
def test_get_categories_with_todos_id():
    # Retrieve all todos and test read the categories of the first todo if any todos with category relationships exist
    response = requests.get('http://localhost:4567/todos')
    todos = response.json()

    # bug in the application -> if the id of the todo inputted is not in the database, the application will output the first category always instead of an error message
    # Correct behaviour:
    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]

        # Check if the first todo has any categories
        if "categories" in todos["todos"][0] and todos["todos"][0]["categories"] != []:
            # Get the id of the first category of the first todo and check that the categories of the first todo match the categories of the first category
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/categories')
            category_data = {"categories": []}
            response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
            
            # Check if the categories of the first todo match the category data retrieved
            for category in response2.json()["todos"][0]["categories"]:
                response3 = requests.get('http://localhost:4567/categories/' + category["id"])
                if response3.status_code == 200 and response3.json()["categories"] != []:
                    category_data["categories"].append(response3.json()["categories"][0])
            
            # Check if the tasksof of the first todo match the tasksof data retrieved        
            assert response3.json() == category_data
            assert response1.status_code == 200

        else:
            # If no categories exist, return an empty list
            response4 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/categories')
            assert response4.json() == {"categories": []}
            assert response4.status_code == 200
    else:
        # another bug in the application -> if no todos exist, the application will output {"categories":[]} always
        response5 = requests.get('http://localhost:4567/todos/1/categories')
        assert response5.json() == {"categories": []}
        assert response5.status_code == 200
        

#JSONDecodeError when appending tasksof to the tasksof_data dictionary
def test_get_tasksof_with_todos_id():
    # Retrieve all todos and test read the first todo if any todos exist
    response = requests.get('http://localhost:4567/todos')
    todos = response.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]

        # Check if the first todo has any tasksof relationships
        if "tasksof" in todos["todos"][0] and todos["todos"][0]["tasksof"] != []:
            # Get the id of the first tasksof of the first todo and check that the tasksof of the first todo match the tasksof of the first tasksof
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/tasksof')
            tasksof_data = {"projects": []}
            response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))

            # for each tasksof of the first todo, get the tasksof data and add it to the tasksof_data dictionary
            for tasksof in response2.json()["todos"][0]["tasksof"]:
                response3 = requests.get('http://localhost:4567/projects/' + tasksof["id"])
                if response3.status_code == 200 and response3.json()["projects"] != []:
                    tasksof_data["projects"].append(response3.json()["projects"][0])

            # Check if the tasksof of the first todo match the tasksof data retrieved        
            assert response1.json() == tasksof_data
            assert response1.status_code == 200

        else:
            # If no tasksof relationships exist, return an empty list
            response1 = requests.get('http://localhost:4567/todos/' + str(todo_id) + '/tasksof')
            assert response1.json() == {"projects":[]}
            assert response1.status_code == 200
    else:
        # When attempting to get tasksof of a todo that does not exist, assert error
        response2 = requests.get('http://localhost:4567/todos/1/tasksof')
        assert response2.status_code == 404
        

def test_post_create_todo():
    # Test create new todo
    response = requests.post('http://localhost:4567/todos', json={"title":"test","doneStatus": False,"description":""})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    # Check if the new todo is created
    response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
    
    assert response2.json() == {"todos":[{"id":todo_id,"title":"test","doneStatus":"false","description":""}]}


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
    todos = response.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]
        response1 = requests.post('http://localhost:4567/todos/' + str(todo_id), json={"title":"test","doneStatus": True,"description":""})

        # Check if the todo is updated
        response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
        assert response1.json() == response2.json()["todos"][0]
        assert response1.status_code == 200

    else:
        # If there is no todo, test the error message when attempting to update todo with id 1
        response2 = requests.post('http://localhost:4567/todos/1', json={"title":"test","doneStatus": True,"description":""})
        assert response2.json() == {"errorMessages":["No such todo entity instance with GUID or ID 1 found"]}
        assert response2.status_code == 404


def test_update_todo_with_put():
    # Test update todos with id
    response = requests.get('http://localhost:4567/todos')
    todos = response.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]
        response1 = requests.put('http://localhost:4567/todos/' + str(todo_id), json={"title":"test","doneStatus": True,"description":""})
        assert response1.status_code == 200

        # Check if the todo is updated
        response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
        assert response1.json() == response2.json()["todos"][0]

        # test the error message when attempting to update without inputting a title
        response2 = requests.put('http://localhost:4567/todos/' + str(todo_id), json={"doneStatus": True,"description":""})
        assert response2.json() == {"errorMessages":["title : field is mandatory"]}
        assert response2.status_code == 400

    else:
        # If there is no todo, test the error message when attempting to update todo with id 1
        response3 = requests.put('http://localhost:4567/todos/1', json={"title":"test","doneStatus": True,"description":""})
        assert response3.json() == {"errorMessages":["Invalid GUID for 1 entity todo"]}
        assert response3.status_code == 404

def test_creating_category_relationship():
    # Test create relationship of category with todo with id
    response = requests.get('http://localhost:4567/todos')
    response2 = requests.get('http://localhost:4567/categories')
    todos = response.json()
    categories = response2.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]

        # Check if any categories exist
        if response2.status_code == 200 and isinstance(categories, dict) and len(categories) > 0:
            # Get the id of the first category
            category_id = categories["categories"][0]["id"]
            # Create relationship of category with todo with id
            response3 = requests.post('http://localhost:4567/todos/' + str(todo_id) + '/categories', json={"id": category_id})
            assert response3.status_code == 201

            # Check if the category relationship is created
            response4 = requests.get('http://localhost:4567/todos/' + str(todo_id))
            assert {"id": category_id} in response4.json()["todos"][0]["categories"] 
        else:
            # if the category id does not exist, error message
            response5 = requests.post('http://localhost:4567/todos/' + str(todo_id) + '/categories', json={"id": 1})
            assert response5.json() == {"errorMessages":["Could not find thing matching value for id"]}
            assert response5.status_code == 404
    else:
        # if the todo id does not exist, error message
        response6 = requests.post('http://localhost:4567/todos/1/categories', json={"id": 1})
        assert response6.json() == {{"errorMessages":["Could not find parent thing for relationship todos/1/categories"]}}
        assert response6.status_code == 404

def test_creating_taskof_relationship():
     # Test create relationship of category with todo with id
    response = requests.get('http://localhost:4567/todos')
    response2 = requests.get('http://localhost:4567/projects')
    todos = response.json()
    projects = response2.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]

        # Check if any categories exist
        if response2.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
            # Get the id of the first project
            project_id = projects["projects"][0]["id"]
            # Create relationship of category with todo with id
            response3 = requests.post('http://localhost:4567/todos/' + str(todo_id) + '/tasksof', json={"id": project_id})
            assert response3.status_code == 201

            # Check if the category relationship is created
            response4 = requests.get('http://localhost:4567/todos/' + str(todo_id))
            assert {"id": project_id} in response4.json()["todos"][0]["tasksof"]

        else:
            # if the project id does not exist, error message
            response5 = requests.post('http://localhost:4567/todos/' + str(todo_id) + '/tasksof', json={"id": 1})
            assert response5.json() == {"errorMessages":["Could not find thing matching value for id"]}
            assert response5.status_code == 404

    else:
        # if the todo id does not exist, error message
        response6 = requests.post('http://localhost:4567/todos/1/tasksof', json={"id": 1})
        assert response6.json() == {{"errorMessages":["Could not find parent thing for relationship todos/1/tasksof"]}}
        assert response6.status_code == 404


def test_delete_category_relationship():
    # Test delete relationship of category with todo with id
    response = requests.get('http://localhost:4567/todos')
    response2 = requests.get('http://localhost:4567/categories')
    todos = response.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]
        
        # Check if the first todo has any categories
        if "categories" in todos["todos"][0] and todos["todos"][0]["categories"] != []:
            # Get the id of the first category of the first todo and delete the relationship
            category_id = todos["todos"][0]["categories"][0]["id"]
            response1 = requests.delete('http://localhost:4567/todos/' + str(todo_id) + '/categories/' + str(category_id))
            assert response1.status_code == 200
            
            # Check if the category relationship is deleted
            # If no more categories exist, then "categories" is not a field in the todo
            response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
            if "categories" in response2.json()["todos"][0]:
                if response2.json()["todos"][0]["categories"] != []:
                    assert {"id": category_id} not in response2.json()["todos"][0]["categories"]

    else:
        # If input is invalid, test the error message when attempting to delete category relationship
        response3 = requests.delete('http://localhost:4567/todos/' + str(todo_id) + '/categories/1')
        assert response3.json() == {"errorMessages":["Could not find any instances with todos/" + str(todo_id) + "/categories/1"]}
        assert response3.status_code == 404
    


def test_delete_taskof_relationship():
    # Test delete relationship of taskof with todo with id
    response = requests.get('http://localhost:4567/todos')
    response2 = requests.get('http://localhost:4567/projects')
    todos = response.json()

    # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo
        todo_id = todos["todos"][0]["id"]

        # Check if the first todo has any tasksof relationships
        if "tasksof" in todos["todos"][0] and todos["todos"][0]["tasksof"] != []:
            # Get the id of the first tasksof of the first todo and delete the relationship
            project_id = todos["todos"][0]["tasksof"][0]["id"]
            response1 = requests.delete('http://localhost:4567/todos/' + str(todo_id) + '/tasksof/' + str(project_id))
            assert response1.status_code == 200

            # Check if the tasksof relationship is deleted
            # If no more tasksof relationships exist, then "tasksof" is not a field in the todo
            response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
            if "tasksof" in response2.json()["todos"][0]: 
                if response2.json()["todos"][0]["tasksof"] != []:
                    assert {"id": project_id} not in response2.json()["todos"][0]["tasksof"]
            
    
    else:
        # If input is invalid, test the error message when attempting to delete taskof relationship
        response3 = requests.delete('http://localhost:4567/todos/' + str(todo_id) + '/tasksof/1')
        assert response3.json() == {"errorMessages":["Could not find any instances with todos/" + str(todo_id) + "/tasksof/1"]}
        assert response3.status_code == 404


def test_delete_todo():
    # Test delete todo with id 
    response = requests.get('http://localhost:4567/todos')
    todos = response.json()

     # Check if any todos exist
    if response.status_code == 200 and isinstance(todos, dict) and len(todos) > 0:
        # Get the id of the first todo and delete
        todo_id = todos["todos"][0]["id"]
        response1 = requests.delete('http://localhost:4567/todos/' + str(todo_id))
        assert response1.status_code == 200

        # Check if the todo is deleted
        response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
        assert response2.json() == {"errorMessages":["Could not find an instance with todos/" + str(todo_id)]}
        assert response2.status_code == 404
    
    else:
        # Test the error message when attempting to delete todo with an id that does not exist
        response3 = requests.delete('http://localhost:4567/todos/1')
        assert response3.json() == {"errorMessages":["Could not find an instance with todos/1"]}
        assert response3.status_code == 404


if __name__ == '__main__':
    pytest.main()
