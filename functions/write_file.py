import os

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