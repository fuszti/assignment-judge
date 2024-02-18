import os
import shutil
import tempfile

def upload_script(script_file, requirements_file, temp_dir):
    # Create a new temporary directory for this upload
    upload_dir = tempfile.mkdtemp(dir=temp_dir)

    # Define file paths
    script_path = os.path.join(upload_dir, "script.py")
    requirements_path = os.path.join(upload_dir, "requirements.txt")

    # Write the script file
    with open(script_path, "wb") as f:
        f.write(script_file.read())

    # Write the requirements file if it exists
    if requirements_file:
        with open(requirements_path, "wb") as f:
            f.write(requirements_file.read())
    else:
        requirements_path = None  # No requirements file provided

    return script_path, requirements_path
