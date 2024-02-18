import io
import os
import tempfile
import pytest
from app.file_upload import upload_script

# Test that the upload function creates files in the temporary directory
def test_upload_creates_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        script_content = b'print("Hello, world!")'
        requirements_content = b"pytest==6.2.5"

        # Mock file-like objects
        script_file = io.BytesIO(script_content)
        requirements_file = io.BytesIO(requirements_content)

        # Call the upload function
        upload_script(script_file, requirements_file, temp_dir)

        # Check that the files were created
        assert os.path.isfile(os.path.join(temp_dir, "script.py"))
        assert os.path.isfile(os.path.join(temp_dir, "requirements.txt"))

# Test that the upload function handles None for requirements.txt
def test_upload_handles_none_requirements():
    with tempfile.TemporaryDirectory() as temp_dir:
        script_content = b'print("Hello, world!")'

        # Mock file-like object
        script_file = io.BytesIO(script_content)

        # Call the upload function
        upload_script(script_file, None, temp_dir)

        # Check that the script file was created and requirements.txt was not
        assert os.path.isfile(os.path.join(temp_dir, "script.py"))
        assert not os.path.isfile(os.path.join(temp_dir, "requirements.txt"))

# Test that the upload function returns correct file paths
def test_upload_returns_file_paths():
    with tempfile.TemporaryDirectory() as temp_dir:
        script_content = b'print("Hello, world!")'
        requirements_content = b"pytest==6.2.5"

        # Mock file-like objects
        script_file = io.BytesIO(script_content)
        requirements_file = io.BytesIO(requirements_content)

        # Call the upload function
        script_path, requirements_path = upload_script(script_file, requirements_file, temp_dir)

        # Check that the returned paths are correct
        assert script_path == os.path.join(temp_dir, "script.py")
        assert requirements_path == os.path.join(temp_dir, "requirements.txt")