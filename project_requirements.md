I need a simple Gradio app where the users can upload their python code. The server would run the code on pre-defined test cases. An evaluator could write the score on the results. The results would show on a leaderboard, that the users (aka students) can watch.

Some details:
Authentication would use the simple username and password solution of the gradio with pre-defined users.
A user can do 2 things:
- upload a new solution, which is a python code.
    - The server creates a new task, that is about the run this code on the pre-defined input files.
        - The output file from this running would feed an evaluator script, that generates score overall the python script.
        - So one uploaded python script gets one score.
        - The server logs in a db which user which attempt was this python script and what is the score of it.
- See the current leaderboard

About the scoring system: the evaluator would compute one public score from a subset of all input files. And the leaderboard shows just this public score. But the final results, when the status of the server is closed shows the results based on the total score.
The leaderboard has this two state, that the superusers can change: open and closed.

The resource requirement does not allow that to run many tasks parallel, so it should handled by a queue. The infrastracture requirement is lightweight. Keep the infrastructure as simple as it possible.

The input files:
text files. It will be feed into the python scripts, that the users upload. The users may upload a requirements.txt that is used in the python env where their script will be run.
The output of their script should be json file.
And the evaluator would run get the input and output json files as parameters to calculate the score.

# Users
The users will be stored in a simple csv files, that is generated randomly with 3 columns.
username, password, role
The username and the password is generated. The role is edited by a human. This file is not allowed to commit in the git repository. But in the CD it will provided from GitHub secret.

# Sandbox environment to run the user's code
It will be resolved in a container, that the server creates. This means the server is also containerized, should use docker in docker solution.
Example code running, as a template draft:
```bash
# Pull a lightweight Python image
docker pull python:3.9-slim

# Run the user's script in a new container with resource limits
docker run --rm --memory=128m --cpus=0.5 --net=none --user=code_runner \
  -v /path/to/host/input:/input:ro \
  -v /path/to/host/output:/output \
  python:3.9-slim python /input/user_script.py > /output/results.json
```
# Test-cases list
The public and private testset, which input file lists is stored in a config.py
# Example Input File and Description in English
## Input File Example
```
4 5 3 2
0 2
0 1 10
1 2 15
2 3 10
3 0 5
0 3 20
5 0 3
10 1 2
15 2 0
```
## File Description
This input file provides an example of how to structure data for a task involving autonomous vehicles transporting items across a factory network. The first line contains four numbers representing:

4 nodes in the factory.
5 edges connecting these nodes.
3 different transportation tasks.
2 autonomous vehicles available.
The second line specifies the starting positions of the vehicles. In this case:

The first vehicle starts at node 0.
The second vehicle starts at node 2.
The next 5 lines describe the edges, indicating which nodes are connected and the time required to traverse between them. For example:

10 time units are needed to travel between node 0 and node 1.
The last 3 lines detail the transportation tasks, specifying when and from where to where each package needs to be delivered. For example:

The first package should be picked up at node 0 at time unit 5 and delivered to node 3.
## Input Data Interpretation
The structure of the file allows for efficient scheduling and route planning for the vehicles and transportation tasks. Nodes and edges represent the factory's internal topology, while the transportation tasks define the dynamics of package movement. Autonomous vehicles must optimize their routes and schedules to accomplish tasks while considering their initial positions and the distances between nodes.

# Example Output File and Description in English
## Output File Example
```json
{
  "commands": [
    {"1": "GO 0-1", "2": "GO 2-3"},
    {"1": "FORWARD", "2": "PICK UP"}
  ]
}
```
## File Description
This output JSON file contains the commands for the vehicles to execute the tasks over time units. Each element in the commands array represents the actions to be taken by the vehicles in each time unit.

In the example:

In the first time unit, both vehicles move to an edge: vehicle 1 moves towards the edge between nodes 0 and 1 (GO 0-1), while vehicle 2 moves towards the edge between nodes 2 and 3 (GO 2-3).
In the second time unit, vehicle 1 continues along the edge (FORWARD), and vehicle 2 picks up a package at its current node (PICK UP).

## Interpretation
This example demonstrates how the commands can be distributed and scheduled among vehicles over time to efficiently execute the transportation tasks. The JSON format makes the data easily interpretable and processable, allowing developers and systems to integrate algorithms and simulations smoothly. This format facilitates the visualization of vehicle movements and the package delivery process, as well as performance evaluation and optimization.

# Scoring
Each output json file contains steps. The evaluator has to check the commands list that solve the original pick up and delivery task that is in the input file or not.
- So the packages are picked up and droped at the required node.
- The packages are picked up after and only after its release time.
- That also good, if during the transport the package is dropped on a different node, but later another vehicle picked up and continue the transport.
If the script does not run, or the output json does not contain feasible solution, then the score on that test-case is infinity.
Otherwheise it is the time frames/units that the output.json contains.
If the public test-cases contains infinity solution, then the score of that solution is also infinity.
But if the leadorboar is open, and only the private board contains infinty solution it will be not show up on the leaderboard as infinity.

# Database
```
-- Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(255) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Role ENUM('student', 'evaluator', 'superuser') NOT NULL
);

-- Attempts Table
CREATE TABLE Attempts (
    AttemptID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ScriptID VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Scores Table
CREATE TABLE Scores (
    ScoreID INT PRIMARY KEY AUTO_INCREMENT,
    AttemptID INT,
    PublicScore DECIMAL(10, 2),
    TotalScore DECIMAL(10, 2),
    FOREIGN KEY (AttemptID) REFERENCES Attempts(AttemptID)
);
```

This schema assumes:

- Each user has a unique UserID.
- Passwords are stored securely as hashes.
- Each attempt is logged with a reference to the UserID and a Timestamp.
- Scores are associated with attempts, with separate fields for public and total scores.

# Queue system
```python
import queue
import threading
import subprocess
import time

# Define a simple FIFO queue
task_queue = queue.Queue()

# Worker function to process tasks
def worker():
    while True:
        # Get the next task
        task = task_queue.get()
        try:
            # Process the task using a Docker container
            subprocess.run(["docker", "run", "--rm", ...], check=True)
            # Handle the results here (e.g., update the database)
        except subprocess.CalledProcessError as e:
            # Log the error
            print(f"An error occurred: {e}")
        finally:
            # Signal that the task is done
            task_queue.task_done()

# Start the worker thread
threading.Thread(target=worker, daemon=True).start()

# Function to add a task to the queue
def add_task(script_path):
    task_queue.put(script_path)

# Example of adding a task
add_task("/path/to/user_script.py")

# Main thread continues doing other work, worker thread processes tasks in the background
```

# Deployment Plan

1. Hosting Service: Use a Platform as a Service (PaaS) like Heroku, which abstracts away much of the infrastructure management and provides easy scaling options.

2. Containerization: Use Docker to containerize the application, ensuring consistency across development, testing, and production environments.

3. Source Control: Use Git with GitHub for version control, taking advantage of its integration with various CI/CD tools.

4. CI/CD Pipeline: Set up a GitHub Actions workflow that triggers on every push to the main branch, running tests and deploying the application to Heroku.

5. Database: Choose a managed database service that integrates with the hosting service, like Heroku Postgres, to avoid manual database administration.

6. Monitoring: Utilize Heroku's built-in monitoring tools to keep track of application performance and uptime.

7. Logging: Use Heroku's log management for simplicity, or integrate a third-party service like Papertrail if more advanced features are needed.

8. Security: Ensure that all communication is over HTTPS, use Heroku's automated security patching, and follow best practices for secret management.

9. Documentation: Document the deployment process, including environment setup, deployment steps, and rollback procedures.

10. Testing: Before full-scale deployment, perform a test deployment to a staging environment on Heroku to ensure everything works as expected.

11. Backup and Recovery: Set up Heroku's automated database backups for disaster recovery.

12. Training: Train the team on the deployment process and the use of Heroku for monitoring and scaling the application.

13. Review: Periodically review the deployment strategy to ensure it continues to meet the project's needs and adjust as necessary.