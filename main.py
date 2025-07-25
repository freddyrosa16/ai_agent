import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

if len(sys.argv) < 2:
    print("Need a prompt")
    sys.exit(1)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
user_prompt = sys.argv[1]

verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

for i in range(20):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    for candidate in response.candidates:
        messages.append(candidate.content)
    if response.function_calls is None:
        print(response.text)
        break
    for call in response.function_calls:
        result = call_function(call, verbose)
        messages.append(result)
        if (verbose):
            print(f"-> {result.parts[0].function_response.response}")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")