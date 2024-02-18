import os
import tempfile
from typing import IO, Optional, Tuple


def upload_script(
    script_file: IO[bytes], requirements_file: Optional[IO[bytes]], temp_dir: str
) -> Tuple[str, Optional[str]]:
    """
    Uploads a script and an optional requirements file to a temporary directory.

    :param script_file: A file-like object containing the script content.
    :param requirements_file: A file-like object containing the requirements content. (optional)
    :param temp_dir: The temporary directory where the script and requirements files will be uploaded.

    :return: A tuple containing the paths of the uploaded script and requirements files.

    This function creates a new temporary directory within the specified temp_dir and writes the script file to a file
    named "script.py" within the upload directory. If a requirements_file is provided, it is also written to a file
    named "requirements.txt" within the upload directory. If no requirements_file is provided, the requirements_path
    in the returned tuple will be None.

    Example usage:
        script_file = io.BytesIO(b'print("Hello, world!")')
        requirements_file = io.BytesIO(b"pytest==6.2.5")
        temp_dir = "/path/to/temp/dir"

        script_path, requirements_path = upload_script(script_file, requirements_file, temp_dir)

        # script_path will be "/path/to/temp/dir/upload_dir/script.py"
        # requirements_path will be "/path/to/temp/dir/upload_dir/requirements.txt"
        # (if requirements_file is provided)

    Note: This function uses the tempfile module to create a new temporary directory and the os module to join file
    paths and check if files exist.
    """
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
