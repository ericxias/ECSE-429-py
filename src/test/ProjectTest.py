import pytest
import requests
import json

# Run the tests
if __name__ == '__main__':
    pytest.main()


# Retrieve projects by searching by ID.
def test_get_projects_with_id():
    # Get all projects.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

    # Check if any projects exist.
    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        project_id = projects["projects"][0]["id"]
        print(project_id)
        response1 = requests.get('http://localhost:4567/projects/' + str(project_id))
        assert response1.json() == {'projects': [projects["projects"][0]]}
        assert response1.status_code == 200
    ## If not found, test error response.
    else:
        response2 = requests.get('http://localhost:4567/projects/1')
        assert response2.json() == {"errorMessages":["Could not find an instance with projects/1"]}
        response2.status_code == 404

def test_get_tasks_with_project_id():
    # Get all projects.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

    # Check if any projects exist.
    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        project_id = projects["projects"][0]["id"]

        # Check if projects have todos.
        if "tasks" in response.json()["projects"][0] and projects["projects"][0]["tasks"] != []:
            print("4")
            task_data = {"todos": []}
            # Get tasks of the first project.
            response1 = requests.get('http://localhost:4567/projects/' + str(project_id) + '/tasks')
            response2 = requests.get('http://localhost:4567/projects/' + str(project_id))

            # Get each task from the project, and check if the task data matches.
            for task in response2.json()["projects"][0]["tasks"]:
                response3 = requests.get('http://localhost:4567/todos/' + task["id"])
                if response3.status_code == 200 and response3.json()["todos"] != []:
                    task_data["todos"].append(response3.json()["todos"][0])
            
            assert response1.json() == task_data
            assert response1.status_code == 200
            
        else:
            response4 = requests.get('http://localhost:4567/projects/' + str(project_id) + '/tasks')
            assert response4.json() == {"todos":[]}
            assert response4.status_code == 200
    else:
        response1 = requests.get('http://localhost:4567/projects/1/tasks')
        assert response1.status_code == 404

def test_post_update_categories():
    # Get all projects and categories.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()
    response2 = requests.get('http://localhost:4567/categories')
    categories = response2.json()

    # Check for project existence.
    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        # Get first project ID.
        project_id = projects["projects"][0]["id"]

        # Check for category existence.
        if response2.status_code == 200 and isinstance(categories, dict) and len(categories) > 0:
            # Get first category ID.
            category_id = categories["categories"][0]["id"]
            # Create relationship between project and category.
            response1 = requests.post('http://localhost:4567/projects/' + str(project_id) + '/categories', json={"id": category_id})
            assert response1.status_code == 201

            # Verify creation of the relationship.
            response5 = requests.get('http://localhost:4567/projects/' + str(project_id))
            assert{"id": category_id} in response5.json()["projects"][0]["categories"]
        else:
            # Category does not exist.
            response6 = requests.post('http://localhost:4567/projects/' + str(project_id) + '/categories', json={"id": category_id})
            assert response6.json() == {"errorMessages":["Could not find thing matching value for id"]}
            assert response6.status_code == 404
    
    else:
        # Project does not exist.
        response3 = requests.post('http://localhost:4567/projects/' + str(project_id) + '/categories', json={"id":"1"})
        assert response3.json() == {"errorMessages":["Could not find parent thing for relationship projects/1/categories"]}
        assert response3.status_code == 404

def test_post_create_project():
    # Test creation.
    response = requests.post('http://localhost:4567/projects', json={"title":"test","completed": False,"active": False,"description":"test description"})
    assert response.status_code == 201
    project_id = response.json()["id"]

    response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
    assert response2.json() == {"projects":[{"id":project_id,"title":"test","completed":"false","active":"false","description":"test description"}]}

def test_invalid_post_create_project():
    # Test create new project with invalid inputs.
    response = requests.post('http://localhost:4567/projects', json={"id":1,"completed": False,"active": False,"description":"test description"})
    assert response.json() == {"errorMessages": ["Invalid Creation: Failed Validation: Not allowed to create with id"]}
    assert response.status_code == 400

    response2 = requests.post('http://localhost:4567/projects', json={"title":"test","completed": False,"active":"false","description":"test description"})
    assert response2.json() == {"errorMessages":["Failed Validation: active should be BOOLEAN"]}
    assert response2.status_code == 400

    response3 = requests.post('http://localhost:4567/projects', json={"title":"test","completed":"false","active": False,"description":"test description"})
    assert response3.json() == {"errorMessages":["Failed Validation: completed should be BOOLEAN"]}
    assert response3.status_code == 400

def test_post_update_project():
    # Get all projects.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        project_id = projects["projects"][0]["id"]
        response1 = requests.post('http://localhost:4567/projects/' + str(project_id), json={"title":"test2","completed": False, "active": False, "description":"test2 description"})
        assert response1.status_code == 200

        response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
        assert response1.json() == response2.json()["projects"][0]
    
    else:
        response3 = requests.post('http://localhost:4567/projects/' + str(project_id), json={"title":"test2","completed": False, "active": False, "description":"test2 description"})
        assert response3.json() == {"errorMessages":["No such project entity instance with GUID or ID 1 found"]}
        assert response3.status_code == 404
    
def test_put_update_project():
    # Get all projects.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        project_id = projects["projects"][0]["id"]
        response1 = requests.put('http://localhost:4567/projects/' + str(project_id), json={"title":"test2","completed": False, "active": False, "description":"test2 description"})
        assert response1.status_code == 200

        response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
        assert response1.json() == response2.json()["projects"][0]
    
    else:
        response3 = requests.put('http://localhost:4567/projects/1', json={"title":"test2","completed": False, "active": False, "description":"test2 description"})
        assert response3.json() == {"errorMessages":["Invalid GUID for 1 entity todo"]}
        assert response3.status_code == 404

def test_post_new_task_relationship_to_project():
    # Get all projects.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        # Get first project ID.
        project_id = projects["projects"][0]["id"]

        # Post new task relationship.
        response3 = requests.post('http://localhost:4567/projects/' + str(project_id) + '/tasks', json={"title":"task1","doneStatus": False, "description":"do this task"})
        assert response3.status_code == 201

        # Verify existence of relationship.
        response2 = requests.get('http://localhost:4567/projects/' + str(project_id) + '/tasks')
        assert response2.status_code == 200
        assert {"id": project_id} in response2.json()["todos"][0]["tasksof"] == response3.json()["tasksof"]
    else:
        # Project does not exist.
        response4 = requests.post('http://localhost:4567/projects/' + str(project_id) + '/tasks', json={"title":"task1","doneStatus": False, "description":"do this task"})
        assert response4.json() == {"errorMessages":["Could not find parent thing for relationship projects/1/tasks"]}
        assert response4.status_code == 404

def test_delete_categories():
    # Get all projects and categories.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()
    response2 = requests.get('http://localhost:4567/categories')
    categories = response2.json()

    # Check for project existence.
    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        # Get first project ID.
        project_id = projects["projects"][0]["id"]

        if "categories" in projects["projects"][0] and projects["projects"][0] != []:
            # Get category ID.
            category_id = projects["projects"][0]["categories"][0]["id"]
            response3 = requests.delete('http://localhost:4567/projects/' + str(project_id) + '/categories/' + str(category_id))
            assert response3.status_code == 200

            # Verify relationship is deleted.
            response4 = requests.get('http://localhost:4567/projects/' + str(project_id))
            if "categories" in response4.json()["projects"][0]:
                if response2.json()["projects"][0]["categories"] != []:
                    assert {"id": category_id} not in response4.json()["projects"][0]["categories"]
    else:
        # Invalid input.
        response3 = requests.delete('http://localhost:4567/projects/' + str(project_id) + '/categories/' + str(category_id))
        assert response3.status_code == 404

def test_delete_project():
    # Test delete project with id.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

     # Check if any projects exist.
    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        project_id = projects["projects"][0]["id"]
        response2 = requests.delete('http://localhost:4567/projects/' + str(project_id))
        assert response2.status_code == 200

        # Check if the project is deleted.
        response3 = requests.get('http://localhost:4567/projects/' + str(project_id))
        assert response3.json() == {"errorMessages":["Could not find an instance with projects/" + str(project_id)]}
        assert response3.status_code == 404
    
    else:
        # Test the error message when attempting to delete project with an id that does not exist.
        response2 = requests.delete('http://localhost:4567/projects/1')
        assert response2.json() == {"errorMessages":["Could not find an instance with projects/1"]}
        assert response2.status_code == 404