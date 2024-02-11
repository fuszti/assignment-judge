# Python Environment Setup for User Scripts

## Prerequisites
- Python 3.9
- Docker

## Steps

1. **Install Python 3.9**: Ensure Python 3.9 is installed on the host system.

2. **Virtual Environment**:
   - Use `python3.9 -m venv /path/to/new/virtual/environment` to create a new virtual environment.
   - Activate the virtual environment before installing any packages.

3. **Handling requirements.txt**:
   - Users must provide a `requirements.txt` file.
   - Use `pip install -r requirements.txt` within the virtual environment to install dependencies.

4. **Docker Installation**:
   - Install Docker on the host system.
   - Ensure the Docker daemon is running.

5. **Docker in Docker Configuration**:
   - If using Docker in Docker, ensure the host Docker can manage other Docker containers.

6. **Resource Limits**:
   - Set resource limits for Docker containers to prevent excessive use of CPU or memory.

7. **Security Measures**:
   - Run user scripts as a non-root user within the Docker container.
   - Disable network access for the container to isolate it from external systems.

8. **Execution Command Template**:
```bash
docker run --rm --memory=128m --cpus=0.5 --net=none --user=code_runner \
-v /path/to/host/input:/input:ro \
-v /path/to/host/output:/output \
python:3.9-slim python /input/user_script.py > /output/results.json
```

9. **Output Handling**:
   - The output from the user script will be redirected to a `results.json` file in the specified output directory.

10. **Error Handling**:
    - Capture any errors during the execution and log them for review.
    - Provide feedback to the user if their script fails to execute.

11. **Cleanup**:
    - After script execution, remove any temporary files and containers to maintain a clean environment.