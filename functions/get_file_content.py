import os

def get_file_content(working_directory, file_path):
    absolute_working_directory = os.path.abspath(working_directory)
    full_file_path = os.path.join(working_directory, file_path)
    absolute_file_path = os.path.abspath(full_file_path)

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    try:
        with open(absolute_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            next_char = f.read(1)
            if next_char:
                return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
    except Exception as e:
        return f"Error: {e}"