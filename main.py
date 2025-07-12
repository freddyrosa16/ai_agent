import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function 


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
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt),)

    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        try:
            actual_response = function_call_result.parts[0].function_response.response
            if verbose:
                print(f"-> {actual_response}")
        except (AttributeError, IndexError) as e:
            raise Exception(f"Unexpected function call result structure: {e}")
    


if __name__ == "__main__":
    main()