import os

def get_file_content(working_directory, file_path):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(file_path)

    if not absolute_file_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'