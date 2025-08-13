import os
from dotenv import load_dotenv
from google import genai
import sys 
import argparse




def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="The query string") 
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if not args.query:  # Check if query was provided
        print("Error: query string is required")
        sys.exit(1)
    load_dotenv()
    isVerbose = args.verbose 
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=sys.argv[1]
    )
    if(isVerbose):
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}.")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(f"{response.text}")
    #print("Hello from pycodeagent!")
    sys.exit(0)


if __name__ == "__main__":
    main()
