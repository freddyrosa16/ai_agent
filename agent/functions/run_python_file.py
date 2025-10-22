import os
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    args = args or []

    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            [sys.executable, abs_target, *args],
            timeout=30,
            capture_output=True,
            cwd=working_directory,
        )
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
    except Exception as err:
        return f"Error executing Python file: {err}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file located within the working directory, optionally with command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to a single Python file within the working directory. Must not be a directory or outside the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
        required=["file_path"],
    ),
)
