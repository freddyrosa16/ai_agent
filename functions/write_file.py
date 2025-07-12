import os
from google.genai import types

def write_file(working_directory, file_path, content):
    absolute_working_directory = os.path.abspath(working_directory)
    full_file_path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(full_file_path)

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_file_path):
        try:
            f = open(absolute_file_path, "x")
        except Exception as e:
            print(f"Error: {e}")
    else:
        with open(absolute_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the specified content to the file at the given path, relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path for the file to write to, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            )
        },
    )
)