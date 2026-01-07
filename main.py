import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

import argparse


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return True

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)

        if not function_call_result.parts:
            raise Exception(
                "Object that we return from call_function should have a non-empty .parts list"
            )
        if function_call_result.parts[0].function_response is None:
            raise Exception(
                "The .function_response property of the first item in the list of parts should be a FunctionResponse object"
            )
        if function_call_result.parts[0].function_response.response is None:
            raise Exception(
                ".response field of the FunctionResponse object should have a value"
            )

        function_responses.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    messages.append(types.Content(role="user", parts=function_responses))


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("API Not Found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        done = generate_content(client, messages, args.verbose)
        if done:
            return

    print("Maximum number of iterations have reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
