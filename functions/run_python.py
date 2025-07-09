import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    absolute_working_directory = os.path.abspath(working_directory)
    joined_working_path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(joined_working_path)

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python3", file_path], timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, text=True)
        if result.stdout.strip() == "":
            return "No output produced."
        else:
            return f"STDOUT: {result.stdout}\n STDERR: {result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e.returncode}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)