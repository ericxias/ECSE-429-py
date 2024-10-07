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
        assert response1.json == {'projects': [projects["projects"][0]]}
        assert response1.status_code == 200
    ## If not found, test error response.
    else:
        response2 = requests.get('http://localhost:4567/projects/1')
        assert response2.json() == {"errorMessages":["Could not find an instance with projects/1"]}
        response2.status_code == 404

# def test_get_tasks_with_project_id():
#     # Get all projects.
#     response = requests.get('http://localhost:4567/projects')
#     projects = response.json()

#     # Check if any projects exist.
#     if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
#         project_id = projects["projects"][0]["id"]

#         # Check if projects have todos.
#         if "todos" in projects["projects"][0] and projects["projects"][0]["todos"] != []:
#             # Get the tasks of the particular project.
#             response1 = requests.get('http://localhost:4567/projects/' + str(project_id) + '/tasks')
#             task_data = {"todos": []}

#             for task in projects["projects"][0]["todos"]:
#                 response2 = requests.get('http:localhost:4567/todos' + task["id"])

def test_post_create_project():
    # Test creation.
    response = requests.post('http://localhost:4567/projects', json={"title":"test","completed": False,"active": False,"description":"test description"})
    assert response.status_code == 201
    project_id = response.json()["id"]

    response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
    assert response2.json() == {"projects":[{"id":project_id,"title":"test","completed":"false","active":"false","description":"test description"}]}

def test_invalid_create_project():
    # Test create new project with invalid inputs.
    response = requests.post('http://localhost:4567/projects', json={"id":1,"completed": False,"active": False,"description":"test description"})
    assert response.json() == {"errorMessages": ["Invalid Creation: Failed Validation: Not allowed to create with id"]}
    assert response.status_code == 400

    response2 = requests.post('http://localhost:4567/projects', json={"title":"test","completed": False,"active":"false","description":"test description"})
    assert response2.json() == {"errorMessages":["Failed Validation: doneStatus should be BOOLEAN"]}
    assert response2.status_code == 400

    response3 = requests.post('http://localhost:4567/projects', json={"title":"test","completed":"false","active": False,"description":"test description"})
    assert response3.json() == {"errorMessages":["Failed Validation: doneStatus should be BOOLEAN"]}
    assert response3.status_code == 400

def test_delete_project():
    # Test delete project with id.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

     # Check if any projects exist.
    if response.status_code == 200 and isinstance(projects, dict) and len(projects) > 0:
        project_id = projects["projects"][0]["id"]
        response1 = requests.delete('http://localhost:4567/projects/' + str(project_id))
        assert response1.status_code == 200

        # Check if the project is deleted.
        response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
        assert response2.json() == {"errorMessages":["Could not find an instance with projects/" + str(project_id)]}
        assert response2.status_code == 404
    
    else:
        # Test the error message when attempting to delete project with an id that does not exist.
        response3 = requests.delete('http://localhost:4567/projects/1')
        assert response3.json() == {"errorMessages":["Could not find an instance with projects/1"]}
        assert response3.status_code == 404