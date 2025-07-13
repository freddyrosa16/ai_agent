import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
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


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    else:
        directory = os.path.join(working_directory, directory)
    if not directory.startswith(working_directory) or working_directory not in os.path.abspath(directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    result = ""
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        result += f"- {item}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}\n"
    return result