import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()

    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    verbose = "--verbose" in sys.argv

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    generate_content(client, messages, verbose, user_prompt)

def generate_content(client, messages, verbose, user_prompt):
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_files_content, schema_run_python_file, schema_write_file,])
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
),)

    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    else:
        if response.function_calls:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        print("Response:")
        print(response.text)

if __name__ == "__main__":
    main()