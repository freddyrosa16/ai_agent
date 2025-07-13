from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_files_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file_content import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {"list_files": get_files_info, "get_file_contents": get_file_content, "run_python_file": run_python_file, "write_file_contents": write_file}
    function_name_string = function_call_part.name
    
    if not function_name_string in function_map:
        return types.Content(role="tool",parts=[types.Part.from_function_response(name=function_name_string,response={"error": f"Unknown function: {function_name_string}"},
        )
    ],
)
    else:
        actual_function_to_call = function_map[function_name_string]
        function_call_part.args.update({"working_directory": "./calculator"})
        function_result = actual_function_to_call(**function_call_part.args)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name_string,
            response={"result": function_result},
        )
    ],
)