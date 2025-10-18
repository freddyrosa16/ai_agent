import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose = "--verbose"
    user_prompt = sys.argv
    if len(user_prompt) < 1:
        print("Error: Please enter a prompt.")

    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=user_prompt
)
    if verbose in user_prompt:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
