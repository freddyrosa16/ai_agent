import os

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = working_directory if directory is None else os.path.join(working_directory, directory)
    absolute_directory = os.path.abspath(target_dir)
    
    if not absolute_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(absolute_directory):
        return f'Error: "{absolute_directory}" is not a directory'
    
    try:
        list_result = []
        for entry in os.listdir(absolute_directory):
            entry_path = os.path.join(absolute_directory, entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            entries = f"- {entry}: file_size={size} bytes, is_dir={is_dir}"
            list_result.append(entries)
        return "\n".join(list_result)
    except Exception as e:
        print(f"Error: {e}")