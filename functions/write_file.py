
import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes file in the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    file_path = os.path.join(working_directory, file_path)
    if not file_path.startswith(working_directory) or working_directory not in os.path.abspath(file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    with open(file_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
