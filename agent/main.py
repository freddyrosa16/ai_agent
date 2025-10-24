import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_files_content import schema_write_file_content


from call_function import call_function

def content_has_text(content: types.Content) -> bool:
    if not content or not getattr(content, "parts", None):
        return False
    for p in content.parts:
        if getattr(p, "text", None):
            return True
    return False

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=api_key)
    is_verbose = "--verbose" in sys.argv
    model_name = "gemini-2.0-flash-001"

    system_prompt = """
You are a helpful AI coding agent.
You have access to the following tools:
- get_files_info
- get_file_content
- write_file_content
- run_python_file
Use them to inspect and modify the calculator project.
All file paths are relative to the working directory.
After calling get_files_info once, you must call get_file_content on the most relevant files next.
Do not produce a final answer until you've inspected at least one file with get_file_content.
"""

    args = [a for a in sys.argv[1:] if a != "--verbose"]
    if not args:
        print("Error: Please enter a prompt.")
        return

    prompt = " ".join(args)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file_content,
            schema_run_python_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    ]

    for step in range(20):
        if is_verbose:
            print(f"\n=== Step {step+1} (messages: {len(messages)}) ===\n")

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error during generate_content: {e}")
            break

        if not response.candidates:
            print("No candidates returned by the model — stopping loop.")
            break

        executed_function = False
        should_stop = False

        for candidate in response.candidates:
            if not candidate.content:
                if is_verbose:
                    print("Warning: candidate.content is None — skipping.")
                continue

            messages.append(candidate.content)

            if is_verbose:
                print(f"Candidate parts: {len(candidate.content.parts)}")
                for idx, part in enumerate(candidate.content.parts):
                    if hasattr(part, "function_call") and part.function_call:
                        print(f"  Part {idx}: function_call - {part.function_call.name}")
                    elif hasattr(part, "text") and part.text:
                        print(f"  Part {idx}: text - {part.text[:50]}...")

            for part in candidate.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    executed_function = True
                    function_call_part = part.function_call

                    print(f" - Calling function: {function_call_part.name}")
                    if is_verbose:
                        print(f"   Arguments: {function_call_part.args}")

                    function_call_result = call_function(function_call_part, verbose=is_verbose)

                    if (
                        not hasattr(function_call_result.parts[0], "function_response")
                        or not function_call_result.parts[0].function_response.response
                    ):
                        raise RuntimeError("Fatal: No valid function response found.")

                    if is_verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

                    messages.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_call_part.name,
                                    response=function_call_result.parts[0].function_response.response,
                                )
                            ],
                        )
                    )

            if not content_has_text(candidate.content) and not executed_function:
                print("Model provided no text and no function calls — stopping.")
                should_stop = True
                break

        if executed_function:
            continue
        elif response.text:
            print("Final response:")
            print(response.text)
            break
        elif should_stop:
            break
        else:
            print("No text or function calls returned — stopping.")
            break

    else:
        print("Reached max iteration limit (20).")

if __name__ == "__main__":
    main()