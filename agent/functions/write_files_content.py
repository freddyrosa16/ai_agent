import os
from google.genai import types

def write_file_content(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not abs_target.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'

    try:
        os.makedirs(os.path.dirname(abs_target), exist_ok=True)
        with open(abs_target, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written).'
    except Exception as err:
        return f"Error writing to file: {err}"

schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Write text content to a file within the working directory. Creates parent directories as needed, and overwrites the file if it already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to a single file within the working directory. Must not be a directory or outside the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the specified file."
            ),
        },
        required=["file_path", "content"],
    ),
)
