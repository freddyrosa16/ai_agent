import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(abs_target) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as err:
        return f'Error: reading file "{file_path}": {err}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a single file within the working directory. If the content exceeds MAX_CHARS, it is truncated and a message is appended.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to a single file within the working directory. Must not be a directory and must stay within the working directory."
            ),
        },
        required=["file_path"],
    ),
)