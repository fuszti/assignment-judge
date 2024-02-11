1. Entities Layer
This layer contains the business objects of the application.
```python
class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role

class Attempt:
    def __init__(self, user_id, timestamp, script_id):
        self.user_id = user_id
        self.timestamp = timestamp
        self.script_id = script_id

class Score:
    def __init__(self, attempt_id, public_score, total_score):
        self.attempt_id = attempt_id
        self.public_score = public_score
        self.total_score = total_score
```

2. Use Cases Layer
This layer contains application-specific business rules.
```python
class UploadScriptUseCase:
    def execute(self, user, script, requirements):
        # Validate user permissions
        # Create a new task for the script
        # Queue the task for execution

class CalculateScoreUseCase:
    def execute(self, script_output, test_cases):
        # Process the script output
        # Calculate the score based on test cases

class ViewLeaderboardUseCase:
    def execute(self, state):
        # Fetch and return leaderboard data based on state (open/closed)
```

3. Interface Adapters Layer
This layer contains adapters that convert data from the format most convenient for use cases and entities to the format most convenient for some external agency such as the database or the web.
```python
class GradioInterface:
    def upload_script_endpoint(self, user, script, requirements):
        # Interface for uploading scripts through Gradio

    def leaderboard_endpoint(self, state):
        # Interface for viewing the leaderboard through Gradio

class DatabaseAdapter:
    def save_new_attempt(self, attempt):
        # Save attempt to the database

    def save_score(self, score):
        # Save score to the database
```

4. Frameworks and Drivers Layer
This layer includes tools like the database, the web framework, etc.
```python
# Gradio app setup
import gradio as gr

def upload_script(user, script, requirements):
    # Endpoint logic

def view_leaderboard(state):
    # Endpoint logic

# Define Gradio interfaces
iface = gr.Interface(
    fn=upload_script,
    inputs=["text", "file", "file"],
    outputs="text"
)

# Run the Gradio app
iface.launch()

# Database connection setup (e.g., SQLAlchemy for SQLite)
```

5. External Interfaces
- Authentication: Integrate Gradio's authentication system.
- File Upload: Gradio interface to upload Python scripts and requirements.txt.
- Task Queue: Use the provided queue system to manage task execution.
- Code Execution: Docker in Docker setup for running user scripts securely.
- Leaderboard: Gradio interface to display the leaderboard based on state.
6. Database Schema
Follow the provided schema for Users, Attempts, and Scores tables.
7. Queue Management System
Implement the provided Python queue system to manage task execution.
8. Deployment
Follow the deployment plan using Heroku, Docker, and GitHub Actions.
9. Testing and Documentation
Write unit tests for each component and document the codebase and architecture.
10. Maintenance and Iteration
Establish a maintenance plan and gather feedback for iterative improvements.

@startuml GradioAppSystemOverview

!define RECTANGLE class

package "Web Interface" {
    RECTANGLE GradioApp {
        RECTANGLE "Upload Script Interface" as UploadScript
        RECTANGLE "Leaderboard Interface" as Leaderboard
    }
}

package "Core Application" {
    RECTANGLE UseCases {
        RECTANGLE "Upload Script Use Case" as UploadScriptUseCase
        RECTANGLE "Calculate Score Use Case" as CalculateScoreUseCase
        RECTANGLE "View Leaderboard Use Case" as ViewLeaderboardUseCase
    }
    RECTANGLE "Authentication Service" as AuthService
    RECTANGLE "Task Queue Manager" as TaskQueueManager
    RECTANGLE "Code Execution Environment" as CodeExecEnv
    RECTANGLE "Evaluator Script" as EvaluatorScript
}

package "Database" {
    RECTANGLE "Database Adapter" as DBAdapter {
        RECTANGLE "Users Table"
        RECTANGLE "Attempts Table"
        RECTANGLE "Scores Table"
    }
}

package "Infrastructure" {
    RECTANGLE "Docker Container Manager" as DockerManager
    RECTANGLE "CI/CD Pipeline" as CICDPipeline
    RECTANGLE "Monitoring & Logging" as MonitoringLogging
}

GradioApp --> AuthService : authenticate
GradioApp --> UseCases : use cases

UploadScriptUseCase --> TaskQueueManager : queue task
TaskQueueManager --> CodeExecEnv : execute code
CodeExecEnv --> EvaluatorScript : process output
EvaluatorScript --> DBAdapter : update scores

ViewLeaderboardUseCase --> DBAdapter : fetch scores

DBAdapter --> Database : SQL

CICDPipeline --> DockerManager : deploy
MonitoringLogging --> DockerManager : monitor

@enduml

# Wireframe Description
Gradio App Interface Wireframe Description
1. Script Upload Page
- Script Upload Field: A file picker to upload the Python script.
- Requirements.txt Upload Field: A file picker to upload the requirements.txt file.
- Submit Button: A button to submit the script and requirements for processing.
- Upload Status: An area to show the status of the upload and any error messages.
2. Leaderboard Page
- Leaderboard Table: A table to display the leaderboard with columns for rank, username, and public score.
- Refresh Button: A button to refresh the leaderboard data.
3. Superuser Controls (visible only to superusers)
- Toggle Leaderboard State: A control to change the leaderboard from open to closed state and vice versa.
4. Navigation (for authenticated users)
- Upload Option: A menu item or button to navigate to the upload script page.
- Leaderboard Option: A menu item or button to navigate to the leaderboard page.

The navigation and superuser controls would be part of the Gradio interface and should be designed to be intuitive and user-friendly. The wireframes for these pages should focus on functionality and ease of use, ensuring that users can easily upload scripts, view the leaderboard, and for superusers, toggle the state of the leaderboard.

# Database
Database Schema Design
Users Table
- UserID: A unique identifier for each user (Primary Key, Auto Increment).
- Username: The user's chosen username (Unique, Not Null).
- PasswordHash: A hash of the user's password for security (Not Null).
- Role: The user's role in the system, which can be 'student', 'evaluator', or 'superuser' (Not Null).
Attempts Table
- AttemptID: A unique identifier for each attempt (Primary Key, Auto Increment).
- UserID: A reference to the user who made the attempt (Foreign Key).
- Timestamp: The date and time when the attempt was made (Default to Current Timestamp).
- ScriptID: A unique identifier for the script that was uploaded (Not Null).
Scores Table
- ScoreID: A unique identifier for each score entry (Primary Key, Auto Increment).
- AttemptID: A reference to the attempt this score is associated with (Foreign Key).
- PublicScore: The score based on the public test cases (Decimal, Nullable).
- TotalScore: The score based on all test cases, public and private (Decimal, Nullable).
Additional Considerations

- Indexes: Besides primary keys, consider adding indexes to frequently queried columns, such as Username in the Users table or UserID in the Attempts table.
- Constraints: Add constraints to ensure data integrity, such as NOT NULL constraints on critical fields and UNIQUE constraints where applicable.
- Normalization: Ensure the schema is normalized to reduce redundancy and improve data integrity. The provided schema appears to be normalized to at least the third normal form (3NF).
- Security: Passwords should never be stored in plain text. Ensure that the PasswordHash column is used to store a secure hash of the password, ideally with a salt.
- Scalability: Consider the expected load on the database and whether the schema supports efficient querying under that load. This might influence decisions on denormalization or the use of additional indexing.

# Authentication
Authentication Flow Description

1. User Registration (Not covered by Gradio):
- Users are pre-defined and stored in a CSV file.
- A separate script or admin interface is needed to hash passwords and populate the Users table in the database.

2. User Login:
- Gradio's authentication system prompts the user for a username and password.
- The system hashes the entered password and compares it with the PasswordHash stored in the database.
- If the credentials match, the user is authenticated and granted access based on their role.

3. Session Management:
- Upon successful login, the system generates a session token.
- The session token is sent to the client and stored in a secure, HTTP-only cookie.
- The token is used for subsequent requests to validate the user's session.

4. Role-Based Access Control (RBAC):
- The system checks the user's role to determine access levels.
- Students can upload scripts and view the leaderboard.
- Evaluators can view the leaderboard and may have additional permissions to manage test cases or view detailed scores.
- Superusers can toggle the leaderboard state and have full administrative access.

5. Logout:
- The user initiates a logout request.
- The system invalidates the session token and clears the session cookie.

6. Security Considerations:
- Use HTTPS to protect credentials and session tokens in transit.
- Implement rate limiting and account lockout mechanisms to prevent brute force attacks.
- Store session tokens securely and ensure they are invalidated upon logout or expiration.

@startuml AuthenticationFlow

actor User
participant "Gradio Interface" as Gradio
database "Users Database" as UsersDB
participant "Session Manager" as Session

User -> Gradio : Enter username and password
Gradio -> UsersDB : Retrieve PasswordHash for username
UsersDB -> Gradio : Return PasswordHash
Gradio -> Gradio : Hash entered password and compare
alt Successful Authentication
    Gradio -> Session : Create session token
    Session -> User : Set session cookie with token
else Authentication Failed
    Gradio -> User : Display authentication error
end
User -> Gradio : Request access (with session token)
Gradio -> Session : Validate session token
alt Valid Session
    Session -> Gradio : Grant access
    Gradio -> User : Provide requested resource
else Invalid Session
    Gradio -> User : Redirect to login
end

@enduml

# Task Queue System Design

1. Task Queue:
- A thread-safe queue that holds tasks to be processed.
- Tasks are added to the queue when a user uploads a script.

2. Worker Threads:
- Dedicated threads that continuously monitor the queue and process tasks.
- Each worker thread runs in a separate Docker container to isolate the execution environment.

3. Task Processing:
- When a task is processed, the worker thread executes the user-uploaded script in a secure environment.
- The output of the script is captured and stored for the evaluator script to calculate the score.

4. Error Handling:
- If a task fails to execute, the error is logged, and the task may be retried or marked as failed based on the error type.

5. Database Integration:
- After a task is processed, the result is stored in the database along with the score.
- The attempt is logged in the Attempts table, and the score is logged in the Scores table.

6. Concurrency Control:
- The number of worker threads is limited to prevent overloading the server.
- The system ensures that tasks are executed sequentially or concurrently based on resource availability.

7. Resource Limits:
- Each Docker container is configured with resource limits to prevent any script from using excessive CPU or memory.

8. Security:
- The Docker containers are configured with security in mind, ensuring that user scripts cannot access the host system or network.

@startuml TaskQueueSystem

actor User
control "Web Interface" as Web
entity "Task Queue" as Queue
control "Worker Thread" as Worker
database "Database" as DB
entity "Docker Container" as Docker

User -> Web : Upload script
Web -> Queue : Add task to queue
loop Worker Thread Loop
    Queue -> Worker : Get next task
    Worker -> Docker : Run script in container
    Docker -> Worker : Return script output
    Worker -> DB : Log attempt and score
end

@enduml

## Implementation in Python

Here's a simplified example of how you might implement the task queue system in Python:

```python
import queue
import threading
import subprocess

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

# Start the worker threads
for _ in range(NUMBER_OF_WORKERS):
    threading.Thread(target=worker, daemon=True).start()

# Function to add a task to the queue
def add_task(script_path):
    task_queue.put(script_path)

# Example of adding a task
add_task("/path/to/user_script.py")
```

In this code, NUMBER_OF_WORKERS should be set based on the server's capacity. The subprocess.run command should include the necessary Docker commands and resource limits.

# Integration of the evaluator

File Upload and Task Creation

1. File Upload Endpoint:
- Create a Gradio interface that includes file inputs for the Python script and the requirements.txt file.
- Ensure that the file inputs accept the correct file types (.py for scripts and .txt for requirements).

2. Task Creation:
- Upon file upload, validate the files and create a new task that includes the path to the uploaded files.
- Add the task to the task queue system designed previously.

3. Security Measures:
- Sanitize the filenames to prevent directory traversal attacks.
- Limit the size of the files that can be uploaded to prevent denial-of-service attacks.

4. Feedback to User:
- Provide immediate feedback to the user about the status of the upload (success or failure).
- If the upload is successful, inform the user that their script will be executed and scored.

5. Integration with the Backend:
- Store the uploaded files in a temporary, secure location on the server.
- Pass the file paths to the task queue system for processing.

Example implementation:
```python
import gradio as gr
import os
import threading
import subprocess
import queue

# Define a simple FIFO queue for tasks
task_queue = queue.Queue()

# Worker function to process tasks
def process_task(script_path, requirements_path):
    # This function would handle setting up the environment,
    # running the script in a Docker container, and processing the output.
    pass  # Replace with actual implementation

# Function to add a task to the queue
def add_task_to_queue(script_path, requirements_path):
    task_queue.put((script_path, requirements_path))
    # Start a new thread for processing the task
    threading.Thread(target=process_task, args=(script_path, requirements_path), daemon=True).start()

# Gradio interface function for file upload
def upload_script(script, requirements):
    # Save the uploaded files to a temporary directory
    script_path = os.path.join(tempfile.mkdtemp(), "script.py")
    requirements_path = os.path.join(tempfile.mkdtemp(), "requirements.txt")
    with open(script_path, "wb") as f:
        f.write(script.read())
    if requirements is not None:
        with open(requirements_path, "wb") as f:
            f.write(requirements.read())
    
    # Add the task to the queue
    add_task_to_queue(script_path, requirements_path)
    
    return "Script uploaded and queued for execution."

# Define Gradio interface
iface = gr.Interface(
    fn=upload_script,
    inputs=[
        gr.inputs.File(label="Python Script", type="file"),
        gr.inputs.File(label="Requirements File", type="file", optional=True)
    ],
    outputs="text"
)

# Run the Gradio app
iface.launch()
```

## Evaluator Script Execution Flow

1. Pre-defined Test Cases:
- Store the list of pre-defined input files and their corresponding expected output files in a configuration file or database.
- Ensure that the evaluator script has access to this configuration to know which files to process.

2. Task Processing:
- After a user script is executed, the output is stored, typically in a JSON file.
- The evaluator script is then invoked with the user script's output and the pre-defined input files.

3. Scoring:
- The evaluator script reads the user's output and compares it against the expected output for each test case.
- It calculates scores based on the correctness and efficiency of the user's output.
- Public scores are calculated using a subset of all test cases, while total scores use all test cases.

4. Database Update:
- Once the scores are calculated, the evaluator script updates the Scores table with the new scores for the corresponding attempt.

5. Error Handling:
- If the user's script fails to run or the output is not in the expected format, the evaluator script assigns an "infinity" score or a predefined penalty score.
- Any exceptions or errors during the evaluation process are logged for review.
Integration with the Task Queue System

The evaluator script is integrated into the task queue system. After a user script is executed within a Docker container, the task queue system will invoke the evaluator script with the necessary parameters.

Example code:
```python
# This function would be part of the worker that processes tasks
def process_task(script_path, requirements_path, test_cases_config):
    # Run the user script in a Docker container
    # ...

    # Assume the user script's output is stored in 'output.json'
    output_path = "/path/to/output.json"

    # Now, invoke the evaluator script for each test case
    for test_case in test_cases_config:
        input_file = test_case['input']
        expected_output_file = test_case['expected_output']
        score = evaluate_script(output_path, input_file, expected_output_file)
        
        # Update the database with the score for this test case
        # ...

def evaluate_script(user_output_path, input_file, expected_output_file):
    # Read the user's output
    with open(user_output_path, 'r') as user_output:
        user_data = json.load(user_output)
    
    # Read the expected output
    with open(expected_output_file, 'r') as expected_output:
        expected_data = json.load(expected_output)
    
    # Compare the outputs and calculate the score
    # This is a placeholder for the actual scoring logic
    score = compare_outputs(user_data, expected_data)
    
    return score

# Placeholder for the comparison logic
def compare_outputs(user_data, expected_data):
    # Implement the logic to compare the user's output with the expected output
    # and calculate the score based on the comparison results
    # ...
    return calculated_score
```

# Leaderboard Display Logic

1. Leaderboard Data Retrieval:
- Fetch the scores from the database, including both public and total scores.
- Sort the scores in descending order to rank the highest scores at the top.

2. Open State:
- In the open state, only public scores are displayed to users.
- The leaderboard should indicate that it's showing public scores and that final scores will be revealed later.

3. Closed State:
- In the closed state, both public and total scores are displayed.
- The leaderboard should clearly differentiate between public and total scores, possibly with separate columns or sections.

4. Superuser Control:
- Provide a mechanism for superusers to toggle the state of the leaderboard between open and closed.
- This could be a simple button or switch in the admin interface.

5. Leaderboard Interface:
- Design the Gradio interface to display the leaderboard.
- Ensure the interface updates in real-time or has a refresh button to load the latest scores.

Example code:
```python
# Placeholder function to fetch scores from the database
def fetch_scores(open_state):
    # Fetch scores from the database
    # If open_state is True, only fetch public scores
    # If open_state is False, fetch both public and total scores
    # Sort the scores based on the state
    # ...
    return sorted_scores

# Gradio interface function for displaying the leaderboard
def display_leaderboard(open_state):
    scores = fetch_scores(open_state)
    leaderboard_data = format_leaderboard_data(scores, open_state)
    return leaderboard_data

# Function to format the leaderboard data for display
def format_leaderboard_data(scores, open_state):
    # Format the scores into a human-readable format
    # If open_state is True, only include public scores
    # If open_state is False, include both public and total scores
    # ...
    return formatted_data

# Define Gradio interface
iface = gr.Interface(
    fn=display_leaderboard,
    inputs=gr.inputs.Checkbox(label="Open State"),
    outputs="dataframe"
)

# Run the Gradio app
iface.launch()
```

## Testing the Leaderboard

After implementing the leaderboard functionality, you should test it with various scenarios to ensure that:

- The leaderboard correctly displays public scores in the open state.
- The leaderboard correctly displays both public and total scores in the closed state.
- Superusers can successfully toggle the state of the leaderboard.
- The leaderboard interface is user-friendly and updates as expected.