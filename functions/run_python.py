import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path with the python file to run, relative to the working directory.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path):
    modified_file_path = os.path.join(working_directory, file_path)
    if not modified_file_path.startswith(working_directory) or working_directory not in os.path.abspath(modified_file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(modified_file_path):
        return f'Error: File "{file_path}" not found.'
    if os.path.splitext(file_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    result = subprocess.run(["python3", file_path],
                            cwd=working_directory, capture_output=True, text=True, timeout=30)
    if len(result.stdout) == 0 and len(result.stderr) == 0 and result.returncode == 0:
        return "No output produced"
    output = "STDOUT:" + result.stdout + "\n"
    output += "STDERR:" + result.stderr + "\n"
    if result.returncode != 0:
        output += f"Process exited with code {result.returncode}"
    return output