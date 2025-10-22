import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_target):
        f'Error: "{directory}" is not a directory'

    try:    
        lines = []
        for filename in os.listdir(abs_target):
            path = os.path.join(abs_target, filename)
            size = os.path.getsize(path)
            is_file = os.path.isfile(path)
            lines.append(f"- {filename}: file_size={size} bytes, is_dir={is_file}")
        return "\n".join(lines)
    except Exception as err:
        return f"Error: listing files: {err}"
    
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
