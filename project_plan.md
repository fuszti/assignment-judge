1. Requirements Clarification
- [x] Confirm the list of pre-defined users for authentication.
- [x] Clarify the security measures for running user-uploaded code.
- [x] Determine the format and examples of pre-defined test cases.
- [x] Define the structure of the JSON output file expected from user scripts.
- [x] Confirm the scoring algorithm details for the evaluator script.
- [x] Establish the database schema for logging attempts, scores, and user details.
- [x] Clarify the queue management system for task execution.
- [x] Determine the infrastructure and tools for deployment.
2. Design Phase
- [x] Design the code architecture with a focus on modularity and security.
- [x] Create a wireframe for the Gradio app interface.
- [x] Design the database schema for user attempts and scores.
- [x] Outline the authentication flow.
- [x] Design the task queue system.
- [x] Plan the evaluator script integration.
- [x] Design the leaderboard display logic for open and closed states.
- [x] Document the setup for the Python environment for running user scripts.
3. Environment Setup
- [x] Set up the development environment.
- [x] Set up version control with Git.
- [x] Choose a lightweight database system (e.g., SQLite).
4. Authentication
- [x] Implement the username and password authentication system.
- [x] Set up user session management.
5. File Upload and Task Creation
- [ ] Implement the file upload system for Python scripts and requirements.txt.
- [ ] Develop the task creation system that queues the uploaded scripts for execution.
6. Code Execution Environment
- [ ] Set up a secure sandbox environment to run user-uploaded Python scripts.
- [ ] Implement the logic to feed input files into the user scripts.
- [ ] Ensure the output is captured in a JSON file.
7. Evaluator Script
- [ ] Develop the evaluator script that calculates scores from the JSON output.
- [ ] Integrate the evaluator script with the task execution flow.
8. Leaderboard and Scoring
- [ ] Implement the leaderboard display functionality.
- [ ] Develop the logic to switch between open and closed states.
- [ ] Integrate the public and total scoring system.
9. Database Logging
- [ ] Implement database logging for user attempts, scores, and script metadata.
10. Queue Management
- [ ] Develop the queue management system to handle task execution sequentially.
11. Testing
- [ ] Write unit tests for each component.
- [ ] Conduct integration testing for the entire app flow.
- [ ] Perform security testing, especially for the code execution environment.
12. Deployment
- [ ] Prepare the production environment.
- [ ] Deploy the application.
- [ ] Conduct load testing and optimize performance.
13. Documentation and Training
- [ ] Document the codebase and architecture.
- [ ] Create user guides for students and evaluators.
- [ ] Train staff on managing the application and leaderboard.
14. Maintenance Plan
- [ ] Establish a maintenance and update schedule.
- [ ] Set up monitoring and alerting for system performance and security.
15. Review and Iteration
- [ ] Gather feedback from users and evaluators.
- [ ] Plan for iterative improvements based on feedback.