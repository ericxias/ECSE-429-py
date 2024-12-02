import random
import string
import time
import requests
import psutil
import matplotlib.pyplot as plt

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_data(num_todos, num_projects):
    # populate the server with random data: we focus on todos and projects
    for _ in range(num_todos):
        requests.post('http://localhost:4567/todos', json=
                      {'title': random_string(5), 
                       "doneStatus": random.choice([True, False]), 
                       "description": random_string(15)})
    for _ in range(num_projects):
        requests.post('http://localhost:4567/projects', json=
                      {'title': random_string(5), 
                       "completed": random.choice([True, False]), 
                       "active": random.choice([True, False])})
        
def measure_time(func):
    # wrapper function to measure time -> retrieve initial time, run the function, retrieve end time, calculate the difference
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return end - start
    return wrapper

@measure_time
def test_post_create_todo():
    # Test create new todo
    response = requests.post('http://localhost:4567/todos', json={"title":"test","doneStatus": False,"description":""})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    # Check if the new todo is created
    response2 = requests.get('http://localhost:4567/todos/' + str(todo_id))
    
    assert response2.json() == {"todos":[{"id":todo_id,"title":"test","doneStatus":"false","description":""}]}

@measure_time
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

@measure_time
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

@measure_time
def test_post_create_project():
    # Test creation.
    response = requests.post('http://localhost:4567/projects', json={"title":"test","completed": False,"active": False,"description":"test description"})
    assert response.status_code == 201
    project_id = response.json()["id"]

    response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
    assert response2.json() == {"projects":[{"id":project_id,"title":"test","completed":"false","active":"false","description":"test description"}]}


@measure_time
def test_delete_project():
    # Test delete project with id.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

     # Check if any projects exist.
    if response.status_code == 200 and response.json()["projects"] != []:
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

@measure_time
def test_put_update_project():
    # Get all projects.
    response = requests.get('http://localhost:4567/projects')
    projects = response.json()

    if response.status_code == 200 and response.json()["projects"] != []:
        # Get project ID.
        project_id = projects["projects"][0]["id"]
        response1 = requests.put('http://localhost:4567/projects/' + str(project_id), json={"title":"test2","completed": False, "active": False, "description":"test2 description"})
        assert response1.status_code == 200

        response2 = requests.get('http://localhost:4567/projects/' + str(project_id))
        assert response1.json() == response2.json()["projects"][0]
    
    else:
        # Update project with invalid ID.
        response3 = requests.put('http://localhost:4567/projects/1', json={"title":"test2","completed": False, "active": False, "description":"test2 description"})
        assert response3.json() == {"errorMessages":["Invalid GUID for 1 entity todo"]}
        assert response3.status_code == 404

def performance_test(num_todos, num_projects):
    # populate objects with random data
    random_data(num_todos, num_projects)

    # measure time for each test
    todo_create_time = test_post_create_todo()
    todo_update_time = test_update_todo_with_put()
    todo_delete_time = test_delete_todo()

    project_create_time = test_post_create_project()
    project_update_time = test_put_update_project()
    project_delete_time = test_delete_project()

    return todo_create_time, todo_update_time, todo_delete_time, project_create_time, project_update_time, project_delete_time

def main():
    # number of objects in the system to test
    num_objects = [5, 10, 25, 50, 75, 100]
    todo_results = []
    project_results = []

    # run performance test for each number of objects
    for num in num_objects:
        print(f"Performance test with {num} objects")
        todo_create_time, todo_update_time, todo_delete_time, project_create_time, project_update_time, project_delete_time = performance_test(num, num)
        # store the results in arrays
        todo_results.append([num, todo_create_time, todo_update_time, todo_delete_time])
        project_results.append([num, project_create_time, project_update_time, project_delete_time])

    # Plot the results
    num, todo_create_times, todo_update_times, todo_delete_times= zip(*todo_results)
    num, project_create_times, project_update_times, project_delete_times = zip(*project_results)
    plt.figure(figsize=(10, 5))

    plt.subplot(3, 1, 1)
    plt.plot(num, todo_create_times, label='Create Time')
    plt.plot(num, todo_update_times, label='Update Time')
    plt.plot(num, todo_delete_times, label='Delete Time')
    plt.xlabel('Number of Objects')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.title('Todo Transaction Time vs Number of Objects')

    plt.subplot(3, 1, 3)
    plt.plot(num, project_create_times, label='Create Time')
    plt.plot(num, project_update_times, label='Update Time')
    plt.plot(num, project_delete_times, label='Delete Time')
    plt.xlabel('Number of Objects')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.title('Project Transaction Time vs Number of Objects')

    plt.show()

if __name__ == '__main__':
    main()





