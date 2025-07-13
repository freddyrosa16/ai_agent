import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if not full_path.startswith(working_directory):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f'Error: File "{file_path}" not found'
    except Exception as e:
        return f'Error reading file: {str(e)}'